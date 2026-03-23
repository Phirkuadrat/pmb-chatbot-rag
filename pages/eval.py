import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import time
import json
from dotenv import load_dotenv
import os
from threading import Lock

GLOBAL_RATE_LIMIT_LOCK = Lock()
LAST_REQUEST_TIME = 0
MIN_REQUEST_INTERVAL = 10  # detik

load_dotenv()

# ── Constants ─────────────────────────────────────────────────────────────────
API_URL     = "http://127.0.0.1:8000/api/v1/chat"
METRIC_NAMES = [
    "Contextual Relevancy",
    "Contextual Recall",
    "Contextual Precision",
    "Answer Correctness",
    "Citation Accuracy",
    "Faithfulness",
]
THRESHOLD = 0.5

# ── Helpers ───────────────────────────────────────────────────────────────────
def query_api(q: str):
    """Hit RAG API, return (answer, retrieval_context)."""
    try:
        r = requests.post(API_URL, json={"query": q, "session_id": "eval_run"}, timeout=60)
        if r.status_code == 200:
            data = r.json().get("data", {})
            return data.get("answer", ""), data.get("retrieval_context", [])
    except Exception as e:
        st.error(f"❌ API error: {e}")
    return "", []


def run_evaluation(df: pd.DataFrame):
    """Run DeepEval metrics for each row in df, return list of result dicts."""
    # Lazy imports – heavy, only load when actually running
    from deepeval.metrics import (
        ContextualRelevancyMetric,
        ContextualRecallMetric,
        ContextualPrecisionMetric,
        FaithfulnessMetric,
    )
    from deepeval.metrics import GEval
    from deepeval.test_case import LLMTestCase, LLMTestCaseParams
    from deepeval.models.base_model import DeepEvalBaseLLM
    from langchain_groq import ChatGroq
    from threading import Lock
    import time

    class GroqJudge(DeepEvalBaseLLM):

        def __init__(self):
            self.model = ChatGroq(
                model="llama-3.1-8b-instant",
                groq_api_key=os.getenv("GROQ_API_KEY"),
                temperature=0
            )

        def load_model(self):
            return self.model

        def _to_str(self, content):
            if isinstance(content, list):
                return "".join(
                    part.get("text", str(part)) if isinstance(part, dict) else str(part)
                    for part in content
                )
            return str(content)

        def generate(self, prompt: str) -> str:
            resp = self.model.invoke(
                prompt + "\n\nIMPORTANT: Return ONLY valid JSON."
            )
            text = self._to_str(resp.content)
            try:
                json_match = re.search(r'\{.*\}', text, re.DOTALL)
                if json_match:
                    return json_match.group(0)

                return text

            except Exception:
                return text

        async def a_generate(self, prompt: str) -> str:
            return self.generate(prompt)

        def get_model_name(self):
            return "Llama-3.1-8B-Instant (Groq)"

    judge = GroqJudge()

    metric_pairs = [
        (ContextualRelevancyMetric(threshold=THRESHOLD, model=judge),  "Contextual Relevancy"),
        (ContextualRecallMetric(threshold=THRESHOLD, model=judge),     "Contextual Recall"),
        (ContextualPrecisionMetric(threshold=THRESHOLD, model=judge),  "Contextual Precision"),
        (GEval(
            name="Answer Correctness",
            criteria="Evaluate if the actual output is correct and complete given the input and retrieved context. Reduce score if answer is wrong or incomplete.",
            evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.RETRIEVAL_CONTEXT],
            threshold=THRESHOLD,
            model=judge,
        ), "Answer Correctness"),
        (GEval(
            name="Citation Accuracy",
            criteria="Check if the citations or facts stated in the actual output are correct and directly supported by the retrieved context. Reduce score if facts are unsupported or fabricated.",
            evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.RETRIEVAL_CONTEXT],
            threshold=THRESHOLD,
            model=judge,
        ), "Citation Accuracy"),
        (FaithfulnessMetric(threshold=THRESHOLD, model=judge),         "Faithfulness"),
    ]

    results = []
    progress = st.progress(0, text="Memulai evaluasi...")

    def measure_with_retry(metric, tc, label: str, max_retries: int = 8):
        last_error = None
        for attempt in range(max_retries):
            try:
                metric.measure(tc)
                reason = getattr(metric, "reason", "Tidak ada penjelasan tambahan.")
                return round(metric.score, 3), metric.score >= THRESHOLD, reason
            except Exception as e:
                last_error = e
                err_msg = str(e)

                if "429" in err_msg or "exhausted" in err_msg.lower() or "rate_limit" in err_msg.lower():
                    wait = 120
                    st.info(f"⏳ Limit Gemini Penuh — '{label}' (Coba {attempt+1}/{max_retries}). Tidur {wait} detik...")
                elif "json" in err_msg.lower():
                    wait = 15
                    st.info(f"🔄 JSON Error — '{label}' (Coba {attempt+1}/{max_retries}). Tidur {wait} detik...")
                else:
                    wait = 20
                    st.info(f"⚠️ Error — '{label}': `{err_msg[:60]}` (Coba {attempt+1}/{max_retries}). Tidur {wait} detik...")

                time.sleep(wait)

        st.error(f"❌ Metrik **'{label}'** gagal total setelah {max_retries} percobaan.")
        return 0.0, False, "Gagal diproses karena error API konstan."

    for idx, row in df.iterrows():
        q  = str(row.get("input", ""))
        ex = str(row.get("expected_output", ""))

        progress.progress(idx / len(df), text=f"Memproses Q{idx+1}/{len(df)}: {q[:60]}...")

        answer, raw_ctx = query_api(q)
        
        # --- 5. PEMBERSIH TIPE DATA (MENCEGAH ERROR .FIND) ---
        clean_answer = "\n".join([str(a) for a in answer]) if isinstance(answer, list) else str(answer)
        
        clean_ctx = []
        if not raw_ctx:
            clean_ctx = ["No context retrieved."]
        elif isinstance(raw_ctx, list):
            for item in raw_ctx:
                if isinstance(item, dict):
                    clean_ctx.append(str(item.get("page_content", item.get("document", str(item)))))
                elif isinstance(item, list):
                    clean_ctx.append(" ".join([str(i) for i in item]))
                else:
                    clean_ctx.append(str(item))
        else:
            clean_ctx = [str(raw_ctx)]

        tc = LLMTestCase(
            input=str(q),
            actual_output=clean_answer,
            expected_output=str(ex),
            retrieval_context=clean_ctx,
        )

        row_result = {"question": q, "expected": ex, "actual": clean_answer}

        if not clean_answer.strip():
            st.warning(f"⚠️ Q{idx+1}: RAG mengembalikan jawaban kosong.")
            for _, label in metric_pairs:
                row_result[label]           = 0.0
                row_result[f"{label}_pass"] = False
                row_result[f"{label}_reason"] = "Jawaban kosong dari RAG."
            results.append(row_result)
            continue

        for m, label in metric_pairs:
            st.toast(f"⏳ Menilai {label} (Q{idx+1})...")
            score, passed, reason = measure_with_retry(m, tc, label)
            row_result[label]           = score
            row_result[f"{label}_pass"] = passed
            row_result[f"{label}_reason"] = reason
            
            # Pendinginan antar metrik
            time.sleep(30)

        results.append(row_result)
        
        # Pendinginan antar soal
        if idx < len(df) - 1:
            time.sleep(60)

    progress.progress(1.0, text="✅ Evaluasi selesai!")
    return results


def radar_chart(avg_scores: dict):
    """Build a Plotly radar chart matching the Confident AI dark theme."""
    labels = list(avg_scores.keys())
    values = list(avg_scores.values())
    # Close the polygon
    labels_c = labels + [labels[0]]
    values_c = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_c,
        theta=labels_c,
        fill='toself',
        fillcolor='rgba(139,92,246,0.25)',
        line=dict(color='#a78bfa', width=2),
        marker=dict(size=7, color='#e2e8f0'),
        name='Score',
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='#1a1a2e',
            radialaxis=dict(
                visible=True, range=[0, 1],
                tickfont=dict(color='#94a3b8', size=10),
                gridcolor='#2a2a4a',
                linecolor='#2a2a4a',
            ),
            angularaxis=dict(
                tickfont=dict(color='#e2e8f0', size=12),
                gridcolor='#2a2a4a',
                linecolor='#2a2a4a',
            ),
        ),
        paper_bgcolor='#1a1a2e',
        plot_bgcolor='#1a1a2e',
        showlegend=False,
        margin=dict(l=60, r=60, t=60, b=60),
        height=420,
    )
    return fig


# ── UI Layout ─────────────────────────────────────────────────────────────────
st.markdown("## 📊 Evaluasi RAG — Tenice")
st.markdown("Jalankan evaluasi DeepEval terhadap dataset pertanyaan-jawaban untuk mengukur performa chatbot.")

tab_run, tab_result = st.tabs(["⚙️ Jalankan Evaluasi", "📈 Hasil Evaluasi"])

# ─── TAB 1: Run ───────────────────────────────────────────────────────────────
with tab_run:
    st.markdown('<div class="eval-card">', unsafe_allow_html=True)
    st.markdown("### 1. Upload Dataset Golden")
    st.info("Format CSV wajib memiliki kolom **`input`** (pertanyaan) dan **`expected_output`** (kunci jawaban).", icon="ℹ️")

    uploaded = st.file_uploader("Pilih file CSV dataset", type=["csv"], label_visibility="collapsed")

    if uploaded:
        df_input = pd.read_csv(uploaded)
        st.success(f"✅ Dataset berhasil dimuat — **{len(df_input)} baris**")
        st.dataframe(df_input, use_container_width=True)

        st.markdown("---")
        st.markdown("### 2. Konfigurasi Metrik")

        col1, col2, col3 = st.columns(3)
        with col1:
            threshold = st.slider("Ambang Batas Skor (Threshold)", 0.0, 1.0, THRESHOLD, 0.05)
        with col2:
            st.markdown("**Metrik Retriever:**")
            st.markdown("✅ Contextual Relevancy\n\n✅ Contextual Recall\n\n✅ Contextual Precision")
        with col3:
            st.markdown("**Metrik Generator:**")
            st.markdown("✅ Answer Correctness (GEval)\n\n✅ Citation Accuracy (GEval)\n\n✅ Faithfulness")

        st.markdown("---")
        st.markdown("### 3. Eksekusi")

        col_btn, col_info = st.columns([1, 3])
        with col_btn:
            run_btn = st.button("🚀 Jalankan Evaluasi", type="primary", use_container_width=True)
        with col_info:
            st.caption("Proses ini akan memanggil API RAG dan DeepEval (Groq judge) untuk setiap baris dataset. Membutuhkan waktu beberapa menit.")

        if run_btn:
            THRESHOLD_ = threshold
            with st.spinner("Menginisialisasi metrik dan juri AI..."):
                try:
                    results = run_evaluation(df_input)
                    st.session_state["eval_results"] = results
                    st.session_state["eval_done"] = True
                    st.success("🎉 Evaluasi selesai! Lihat tab **Hasil Evaluasi**.")
                except Exception as e:
                    st.error(f"❌ Evaluasi gagal: {e}")
    else:
        st.caption("Belum ada dataset yang diunggah.")
    st.markdown('</div>', unsafe_allow_html=True)


# ─── TAB 2: Results ───────────────────────────────────────────────────────────
with tab_result:
    if not st.session_state.get("eval_done"):
        st.info("Belum ada hasil. Jalankan evaluasi terlebih dahulu di tab **Jalankan Evaluasi**.", icon="ℹ️")
    else:
        results = st.session_state["eval_results"]
        df_res = pd.DataFrame(results)

        score_cols = METRIC_NAMES[:-1] + ["Answer Correctness", "Faithfulness"]
        # Normalize column names that may differ (GEval uses custom name)
        available_metrics = [c for c in score_cols if c in df_res.columns]

        avg_scores = {m: round(df_res[m].mean(), 3) for m in available_metrics}

        # ── Overview section ──────────────────────────────────────────────────
        st.markdown('<div class="eval-card">', unsafe_allow_html=True)
        st.markdown("### Metric Scores Overview")
        st.caption("Rata-rata skor untuk semua metrik pada test run ini")

        col_radar, col_summary = st.columns([3, 2])

        with col_radar:
            fig = radar_chart(avg_scores)
            st.plotly_chart(fig, use_container_width=True)

        with col_summary:
            st.markdown("#### Rata-rata Skor per Metrik")
            for metric, score in avg_scores.items():
                passed = score >= THRESHOLD
                color = "#4ade80" if passed else "#f87171"
                icon  = "✅" if passed else "❌"
                bar_pct = int(score * 100)
                st.markdown(f"""
                <div style="margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                        <span style="color:#e2e8f0;font-size:13px;">{icon} {metric}</span>
                        <span style="color:{color};font-weight:700;font-size:14px;">{score:.3f}</span>
                    </div>
                    <div style="background:#2a2a4a;border-radius:4px;height:6px;">
                        <div style="background:{color};width:{bar_pct}%;height:6px;border-radius:4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            overall = sum(avg_scores.values()) / len(avg_scores)
            ov_color = "#4ade80" if overall >= THRESHOLD else "#f87171"
            st.markdown(f"""
            <div style="margin-top:16px;padding:12px;background:#0d0d1a;border-radius:8px;border:1px solid #3a3a6a;text-align:center;">
                <div style="color:#94a3b8;font-size:12px;margin-bottom:4px;">OVERALL SCORE</div>
                <div style="color:{ov_color};font-size:28px;font-weight:700;">{overall:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Test Cases Table ──────────────────────────────────────────────────
        st.markdown('<div class="eval-card">', unsafe_allow_html=True)
        st.markdown("### Test Cases")
        st.caption(f"Detail hasil per pertanyaan — {len(results)} test case")

        for i, r in enumerate(results):
            with st.expander(f"**Q{i+1}:** {r['question'][:80]}..."):
                col_q, col_a = st.columns(2)
                with col_q:
                    st.markdown("**Pertanyaan:**")
                    st.write(r["question"])
                    st.markdown("**Expected Output:**")
                    st.write(r["expected"])
                with col_a:
                    st.markdown("**Actual Output:**")
                    st.write(r["actual"])

                st.markdown("**Hasil Metrik:**")
                cols = st.columns(len(available_metrics))
                for j, m in enumerate(available_metrics):
                    score = r.get(m, 0.0)
                    passed = r.get(f"{m}_pass", False)
                    tag = "PASS" if passed else "FAIL"
                    clr = "#4ade80" if passed else "#f87171"
                    bg  = "#1a3a2a" if passed else "#3a1a1a"
                    cols[j].markdown(f"""
                    <div style="background:{bg};border:1px solid {clr};border-radius:8px;padding:10px;text-align:center;">
                        <div style="color:#94a3b8;font-size:11px;margin-bottom:4px;">{m.split()[0]}<br>{"".join(m.split()[1:])}</div>
                        <div style="color:{clr};font-size:20px;font-weight:700;">{score:.2f}</div>
                        <div style="color:{clr};font-size:11px;">{tag}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Tampilkan Alasan LLM
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("🔍 Lihat Alasan Juri AI (DeepEval Reasoning)"):
                    for m in available_metrics:
                        reason = r.get(f"{m}_reason", "Tidak ada alasan spesifik")
                        passed = r.get(f"{m}_pass", False)
                        icon = "✅" if passed else "❌"
                        st.markdown(f"**{icon} {m}**: {reason}")

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Download ──────────────────────────────────────────────────────────
        st.markdown('<div class="eval-card">', unsafe_allow_html=True)
        st.markdown("### Ekspor Hasil")
        csv_out = df_res.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download CSV Hasil Evaluasi",
            data=csv_out,
            file_name=f"eval_results_{int(time.time())}.csv",
            mime="text/csv",
        )
        st.markdown('</div>', unsafe_allow_html=True)
