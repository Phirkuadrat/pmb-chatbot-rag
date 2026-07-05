import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import time
import os
import sqlite3
import signal
import threading
from threading import Lock

# --- PATCH SIGNAL MENCEGAH ERROR MAIN THREAD DI STREAMLIT ---
original_signal = signal.signal
def patched_signal(signum, handler):
    if threading.current_thread() is threading.main_thread():
        return original_signal(signum, handler)
    return None
signal.signal = patched_signal

# --- KONEKSI DATABASE SQLITE ---
DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "eval_history.db")

def init_db():
    """Membuat folder data dan tabel SQLite jika belum ada."""
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Tabel master run evaluasi
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eval_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_timestamp TEXT NOT NULL,
        num_questions INTEGER NOT NULL,
        avg_faithfulness REAL,
        avg_answer_relevance REAL,
        avg_context_precision REAL,
        avg_context_recall REAL,
        avg_context_relevancy REAL,
        overall_score REAL
    )
    """)
    
    # 2. Tabel detail hasil per pertanyaan
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eval_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id INTEGER NOT NULL,
        question TEXT,
        expected_output TEXT,
        actual_output TEXT,
        faithfulness REAL,
        answer_relevance REAL,
        context_precision REAL,
        context_recall REAL,
        context_relevancy REAL,
        error_log TEXT,
        FOREIGN KEY (run_id) REFERENCES eval_runs (id) ON DELETE CASCADE
    )
    """)
    try:
        cursor.execute("ALTER TABLE eval_details ADD COLUMN error_log TEXT")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

init_db()

# --- CONSTANTS ---
_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api/v1")
API_URL = f"{_BASE}/chat"

# --- HELPER FUNCTIONS ---
def query_chatbot(q: str, session_id: str):
    """Memanggil Chatbot API secara independen menggunakan Session ID unik."""
    try:
        import requests
        # Timeout 120s karena model Qwen3-32b butuh waktu lebih lama
        r = requests.post(API_URL, json={"query": q, "session_id": session_id}, timeout=120)
        if r.status_code == 200:
            data = r.json().get("data", {})
            return data.get("answer", ""), data.get("retrieval_context", []), "OK"
        else:
            return "", [], f"HTTP {r.status_code}: {r.text[:100]}"
    except requests.exceptions.Timeout:
        return "", [], "API Timeout (>120s)"
    except Exception as e:
        st.warning(f"⚠️ API Chatbot Error: {e}")
        return "", [], f"Error: {str(e)[:100]}"

def save_run_to_db(run_timestamp, dataset_rows, scores_by_metric):
    """Menyimpan ringkasan run dan detail penilaian ke database SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    num_qs = len(dataset_rows)
    if num_qs == 0:
        conn.close()
        return None
        
    # Hitung rata-rata
    avg_f = sum(scores_by_metric["faithfulness"]) / num_qs
    avg_ar = sum(scores_by_metric["answer_relevancy"]) / num_qs
    avg_cr = sum(scores_by_metric["context_recall"]) / num_qs
    avg_cp = sum(scores_by_metric["context_precision"]) / num_qs
    avg_co = sum(scores_by_metric["llm_context_precision_without_reference"]) / num_qs
    overall = (avg_f + avg_ar + avg_cr + avg_cp + avg_co) / 5.0
    
    cursor.execute("""
    INSERT INTO eval_runs (
        run_timestamp, num_questions, avg_faithfulness, avg_answer_relevance, 
        avg_context_precision, avg_context_recall, avg_context_relevancy, overall_score
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (run_timestamp, num_qs, avg_f, avg_ar, avg_cp, avg_cr, avg_co, overall))
    
    run_id = cursor.lastrowid
    
    for i, row in enumerate(dataset_rows):
        cursor.execute("""
        INSERT INTO eval_details (
            run_id, question, expected_output, actual_output, 
            faithfulness, answer_relevance, context_precision, context_recall, context_relevancy, error_log
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            run_id,
            row["user_input"],
            row["reference"],
            row["response"],
            scores_by_metric["faithfulness"][i],
            scores_by_metric["answer_relevancy"][i],
            scores_by_metric["context_precision"][i],
            scores_by_metric["context_recall"][i],
            scores_by_metric["llm_context_precision_without_reference"][i],
            row.get("error_log", "")
        ))
        
    conn.commit()
    conn.close()
    return run_id

def get_runs_from_db():
    """Mengambil semua run yang ada di SQLite untuk dropdown."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM eval_runs ORDER BY id DESC", conn)
    conn.close()
    return df

def get_run_details_from_db(run_id):
    """Mengambil rincian evaluasi per pertanyaan dari SQLite berdasarkan run_id."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM eval_details WHERE run_id = {run_id}", conn)
    conn.close()
    return df

# --- CORE EVALUATION LOGIC ---
def execute_eval_pipeline(df: pd.DataFrame):
    """Jalankan evaluasi menggunakan RAGAS dengan LLM juri via OpenRouter."""
    from datasets import Dataset
    from ragas import evaluate
    from ragas.metrics import (
        faithfulness,
        answer_relevancy,
        context_recall,
        context_precision,
        LLMContextPrecisionWithoutReference
    )
    from ragas.run_config import RunConfig
    from app.core.config import settings
    
    # --- STEP 1: Inisialisasi model LLM evaluator ---
    or_key = settings.openrouter_eval_api_key or settings.openrouter_api_key
    
    if or_key:
        try:
            import re as _re
            from langchain_openai import ChatOpenAI
            from langchain_huggingface import HuggingFaceEmbeddings

            class CleanJSONLLM(ChatOpenAI):
                @staticmethod
                def _strip_md(text: str) -> str:
                    """Hapus markdown code block dari respons LLM agar JSON bisa di-parse."""
                    if not isinstance(text, str):
                        return text
                    text = text.strip()
                    m = _re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
                    return m.group(1).strip() if m else text
                def _clean_result(self, result):
                    """Bersihkan semua GenerationChunk dalam LLMResult."""
                    for gen_list in result.generations:
                        for g in gen_list:
                            if hasattr(g, 'message') and isinstance(getattr(g.message, 'content', None), str):
                                g.message.content = self._strip_md(g.message.content)
                            try:
                                if isinstance(getattr(g, 'text', None), str):
                                    object.__setattr__(g, 'text', self._strip_md(g.text))
                            except Exception:
                                pass
                    return result
                def _generate(self, messages, stop=None, run_manager=None, **kwargs):
                    return self._clean_result(
                        super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)
                    )
                async def _agenerate(self, messages, stop=None, run_manager=None, **kwargs):
                    return self._clean_result(
                        await super()._agenerate(messages, stop=stop, run_manager=run_manager, **kwargs)
                    )

            llm = CleanJSONLLM(
                api_key=or_key,
                base_url="https://openrouter.ai/api/v1",
                model=settings.eval_llm_model_name,
                temperature=0,
                max_tokens=1200
            )
            embeddings = HuggingFaceEmbeddings(
                model_name="paraphrase-multilingual-MiniLM-L12-v2"
            )
        except Exception as e:
            st.error(f"❌ Gagal memuat model Evaluator: {e}")
            return None
    elif settings.gemini_api_key:
        from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=settings.gemini_api_key,
                temperature=0,
                max_tokens=2000
            )
            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001",
                google_api_key=settings.gemini_api_key
            )
        except Exception as e:
            st.error(f"❌ Gagal memuat model Evaluator (Gemini): {e}")
            return None
    else:
        st.error("🔑 Kunci API tidak ditemukan di file .env.")
        return None
        
    # --- STEP 2: Setup semua metrik Ragas ---
    context_relevancy_metric = LLMContextPrecisionWithoutReference()
    all_metrics = [faithfulness, answer_relevancy, context_recall, context_precision, context_relevancy_metric]
    
    for m in all_metrics:
        m.llm = llm
        if hasattr(m, "embeddings"):
            m.embeddings = embeddings
            
    # --- STEP 3: Kumpulkan jawaban chatbot ---
    dataset_rows = []
    progress_bar = st.progress(0, text="Mengumpulkan respon chatbot...")
    
    for idx, row in df.iterrows():
        q = str(row.get("input", ""))
        ref = str(row.get("reference", row.get("expected_output", "")))
        
        pct = (idx * 0.35) / len(df)
        progress_bar.progress(pct, text=f"Chatbot menjawab Q{idx+1}/{len(df)}: '{q[:40]}...'")
        
        session_id = f"eval_{int(time.time())}_{idx}"
        answer, raw_ctx, error_msg = query_chatbot(q, session_id)
        
        clean_answer = "\n".join([str(a) for a in answer]) if isinstance(answer, list) else str(answer)
        
        row_error_log = error_msg
        if not clean_answer.strip() and error_msg == "OK":
            row_error_log = "Empty answer from LLM"
        if not raw_ctx and error_msg == "OK":
            row_error_log = "No context retrieved by agent" if row_error_log == "OK" else f"{row_error_log} | No context retrieved"
            
        n_ctx = len(raw_ctx) if isinstance(raw_ctx, list) else (1 if raw_ctx else 0)
        st.caption(f"📄 Q{idx+1} — {n_ctx} chunk konteks ditarik | Status: {row_error_log}")
        
        def _ctx_to_readable(item) -> str:
            import json as _json
            if isinstance(item, dict):
                raw = item.get("page_content", item.get("document", None))
                if raw:
                    return _ctx_to_readable(raw)
                item = _json.dumps(item, ensure_ascii=False)
            if not isinstance(item, str):
                return str(item)
            stripped = item.strip()
            if stripped.startswith("{") or stripped.startswith("["):
                try:
                    parsed = _json.loads(stripped)
                    if isinstance(parsed, dict):
                        lines = []
                        def _flat(d, prefix=""):
                            for k, v in d.items():
                                full_key = (f"{prefix} - {k}") if prefix else k
                                if isinstance(v, dict):
                                    _flat(v, full_key)
                                elif isinstance(v, list):
                                    for li in v:
                                        if isinstance(li, dict):
                                            _flat(li, full_key)
                                        elif li is not None:
                                            lines.append(f"{full_key}: {li}")
                                elif v is not None:
                                    lines.append(f"{full_key}: {v}")
                        _flat(parsed)
                        return "\n".join(lines) if lines else item
                except Exception:
                    pass
            return item
        
        clean_ctx = []
        if not raw_ctx:
            clean_ctx = ["No context retrieved."]
        elif isinstance(raw_ctx, list):
            for item in raw_ctx:
                clean_ctx.append(_ctx_to_readable(item))
        else:
            clean_ctx = [_ctx_to_readable(raw_ctx)]
            
        dataset_rows.append({
            "user_input": q,
            "response": clean_answer,
            "retrieved_contexts": clean_ctx,
            "reference": ref,
            "error_log": row_error_log
        })
        time.sleep(1) 
        
    progress_bar.progress(0.35, text="Chatbot selesai menjawab. Menyiapkan dataset Ragas...")
    
    # --- STEP 4: Buat Ragas Dataset ---
    ragas_dataset = Dataset.from_dict({
        "user_input":        [r["user_input"] for r in dataset_rows],
        "response":          [r["response"] for r in dataset_rows],
        "retrieved_contexts":[r["retrieved_contexts"] for r in dataset_rows],
        "reference":         [r["reference"] for r in dataset_rows],
        "question":          [r["user_input"] for r in dataset_rows],
        "answer":            [r["response"] for r in dataset_rows],
        "contexts":          [r["retrieved_contexts"] for r in dataset_rows],
        "ground_truth":      [r["reference"] for r in dataset_rows],
    })
    
    # --- STEP 5: Jalankan evaluasi semua metrik sekaligus ---
    import math
    scores_by_metric = {k: [0.0] * len(dataset_rows) for k in
                        ["faithfulness", "answer_relevancy", "context_precision", "context_recall", "llm_context_precision_without_reference"]}
    
    try:
        import nest_asyncio
        nest_asyncio.apply()
        
        progress_bar.progress(0.50, text="⚙️ Juri AI sedang menilai semua metrik...")
        
        run_config = RunConfig(max_workers=4, max_retries=10, max_wait=60)
        
        res_eval = evaluate(
            ragas_dataset,
            metrics=all_metrics,
            llm=llm,
            embeddings=embeddings,
            run_config=run_config,
            show_progress=False,
            raise_exceptions=False
        )
        
        progress_bar.progress(0.85, text="✅ Evaluasi selesai! Mengekstrak skor...")
        
        df_res = res_eval.to_pandas()
        st.toast(f"Kolom hasil Ragas: {list(df_res.columns)}", icon="🔍")
        
        def safe_col(col):
            if col not in df_res.columns:
                return [0.0] * len(dataset_rows)
            return [0.0 if (v is None or (isinstance(v, float) and math.isnan(v))) else float(v)
                    for v in df_res[col].tolist()]
        
        scores_by_metric["faithfulness"]                          = safe_col("faithfulness")
        scores_by_metric["answer_relevancy"]                      = safe_col("answer_relevancy")
        scores_by_metric["context_precision"]                     = safe_col("context_precision")
        scores_by_metric["context_recall"]                        = safe_col("context_recall")
        scores_by_metric["llm_context_precision_without_reference"] = safe_col("llm_context_precision_without_reference")
    except Exception as e:
        err_msg = str(e)
        if "RESOURCE_EXHAUSTED" in err_msg or "429" in err_msg:
            st.error("🚨 **Limit kuota API tercapai.** Coba lagi dalam beberapa menit.")
        else:
            st.error("⚠️ Error saat evaluasi RAGAS:")
            with st.expander("Detail Error"):
                st.code(err_msg)
                
    progress_bar.progress(0.95, text="Menyimpan data evaluasi ke SQLite...")
    
    run_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    run_id = save_run_to_db(run_timestamp, dataset_rows, scores_by_metric)
    
    progress_bar.progress(1.0, text="✅ Evaluasi berhasil diselesaikan dan disimpan!")
    return run_id

# --- CHART UTILITIES ---
def draw_trend_line_chart():
    """Membuat grafik tren histori evaluasi menggunakan Plotly."""
    df_runs = get_runs_from_db()
    if df_runs.empty:
        st.info("Belum ada data histori. Silakan jalankan evaluasi pertama Anda di tab pertama.")
        return
        
    # Urutkan secara kronologis (dari run pertama ke terakhir)
    df_runs = df_runs.iloc[::-1].reset_index(drop=True)
    
    fig = go.Figure()
    # Line utama untuk Overall Score
    fig.add_trace(go.Scatter(
        x=df_runs["run_timestamp"],
        y=df_runs["overall_score"],
        mode='lines+markers',
        name='Overall Score',
        line=dict(color='#8b5cf6', width=4),
        marker=dict(size=8, color='#a78bfa')
    ))
    
    # Tambahkan line pendukung untuk masing-masing metrik
    metrics_conf = {
        "avg_faithfulness": ("Faithfulness", "#10b981"),
        "avg_answer_relevance": ("Answer Relevance", "#3b82f6"),
        "avg_context_precision": ("Context Precision", "#f59e0b"),
        "avg_context_recall": ("Context Recall", "#ec4899"),
        "avg_context_relevancy": ("Context Relevancy", "#14b8a6")
    }
    
    for key, (label, color) in metrics_conf.items():
        if key in df_runs.columns:
            fig.add_trace(go.Scatter(
                x=df_runs["run_timestamp"],
                y=df_runs[key],
                mode='lines+markers',
                name=label,
                line=dict(color=color, width=1.5, dash='dash'),
                marker=dict(size=4)
            ))
            
    fig.update_layout(
        xaxis=dict(
            title="Tanggal & Waktu Run",
            gridcolor='#1e1e38',
            tickfont=dict(color='#94a3b8')
        ),
        yaxis=dict(
            title="Skor Rata-rata",
            range=[0, 1.05],
            gridcolor='#1e1e38',
            tickfont=dict(color='#94a3b8')
        ),
        paper_bgcolor='#0f0f23',
        plot_bgcolor='#0f0f23',
        legend=dict(font=dict(color='#e2e8f0')),
        margin=dict(l=40, r=40, t=20, b=40),
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

def draw_radar_chart(row_run):
    """Membuat Radar Chart komparatif untuk 5 metrik run tertentu."""
    labels = ["Faithfulness", "Answer Relevance", "Context Precision", "Context Recall", "Context Relevancy"]
    values = [
        row_run["avg_faithfulness"],
        row_run["avg_answer_relevance"],
        row_run["avg_context_precision"],
        row_run["avg_context_recall"],
        row_run["avg_context_relevancy"]
    ]
    # Tutup poligon
    labels_c = labels + [labels[0]]
    values_c = values + [values[0]]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_c,
        theta=labels_c,
        fill='toself',
        fillcolor='rgba(139,92,246,0.2)',
        line=dict(color='#a78bfa', width=2.5),
        marker=dict(size=6, color='#e2e8f0'),
        name='Skor'
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='#161633',
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickfont=dict(color='#94a3b8', size=9),
                gridcolor='#2d2d5a',
                linecolor='#2d2d5a'
            ),
            angularaxis=dict(
                tickfont=dict(color='#e2e8f0', size=11),
                gridcolor='#2d2d5a',
                linecolor='#2d2d5a'
            )
        ),
        paper_bgcolor='#0f0f23',
        plot_bgcolor='#0f0f23',
        showlegend=False,
        margin=dict(l=60, r=60, t=40, b=40),
        height=380
    )
    return fig

# --- STYLING CUSTOM CSS ---
st.markdown("""
<style>
    .eval-container {
        background-color: #0f0f23;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #1f1f3e;
        margin-bottom: 24px;
    }
    .metric-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 13px;
        text-align: center;
        margin: 4px 0;
    }
    .badge-pass {
        background-color: rgba(74, 222, 128, 0.15);
        color: #4ade80;
        border: 1px solid #4ade80;
    }
    .badge-fail {
        background-color: rgba(248, 113, 113, 0.15);
        color: #f87171;
        border: 1px solid #f87171;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER APP ---
st.markdown("## 📊 Evaluasi Performa RAGAS — Tenice")
st.markdown("Uji performa chatbot PMB Itenas menggunakan framework ilmiah **RAGAS** dan judge model **Gemini 1.5 Flash**.")

tab_run, tab_history, tab_detail = st.tabs(["⚙️ Jalankan Evaluasi", "📈 Histori & Tren Performa", "📂 Detail Run Sebelumnya"])

# ─── TAB 1: JALANKAN EVALUASI ───
with tab_run:
    st.markdown('<div class="eval-container">', unsafe_allow_html=True)
    st.markdown("### 1. Unggah Golden Dataset")
    st.info("Format CSV wajib memiliki kolom **`input`** (pertanyaan) dan **`reference`** (kunci jawaban FAQ).", icon="📝")
    
    uploaded_file = st.file_uploader("Unggah Dataset Evaluasi (CSV)", type=["csv"], label_visibility="collapsed")
    
    if uploaded_file:
        df_input = pd.read_csv(uploaded_file)
        
        # Validasi struktur kolom
        has_input = "input" in df_input.columns
        has_ref = "reference" in df_input.columns or "expected_output" in df_input.columns
        
        if not (has_input and has_ref):
            st.error("❌ File CSV harus memiliki kolom 'input' dan 'reference' (atau 'expected_output').")
        else:
            if "reference" not in df_input.columns and "expected_output" in df_input.columns:
                df_input = df_input.rename(columns={"expected_output": "reference"})
                
            st.success(f"✅ Golden Dataset berhasil dimuat: **{len(df_input)} baris soal**")
            st.dataframe(df_input, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 2. Konfigurasi Evaluasi")
            
            col_t, col_desc = st.columns([1, 2])
            with col_t:
                threshold_slider = st.slider("Ambang Batas Kelulusan (Threshold)", 0.0, 1.0, 0.60, 0.05)
            with col_desc:
                st.markdown("**Metrik yang Dievaluasi:**")
                st.markdown("- **Retrieval (3 metrik):** *Context Precision, Context Recall, Context Relevancy*")
                st.markdown("- **Generation (2 metrik):** *Faithfulness, Answer Relevance*")
                
            st.markdown("---")
            st.markdown("### 3. Jalankan Pengujian")
            
            btn_run = st.button("🚀 Mulai Evaluasi RAGAS", type="primary", use_container_width=True)
            
            if btn_run:
                with st.spinner("Menghubungi API Chatbot dan menginisialisasi juri Ragas..."):
                    run_id = execute_eval_pipeline(df_input)
                    if run_id:
                        st.success(f"🎉 Evaluasi selesai! ID Run: #{run_id}. Silakan periksa tab **Histori & Tren** atau **Detail Run**.")
                        # Reset state agar Streamlit memperbarui dropdown histori
                        st.rerun()
    else:
        st.caption("Unggah berkas dataset CSV Anda untuk memulai proses evaluasi.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ─── TAB 2: HISTORI & TREN PERFORMA ───
with tab_history:
    st.markdown('<div class="eval-container">', unsafe_allow_html=True)
    st.markdown("### Tren Rata-rata Skor Evaluasi")
    st.caption("Perkembangan kualitas jawaban dan akurasi retrieval dari pengujian ke pengujian.")
    draw_trend_line_chart()
    st.markdown('</div>', unsafe_allow_html=True)

# ─── TAB 3: DETAIL RUN SEBELUMNYA ───
with tab_detail:
    st.markdown('<div class="eval-container">', unsafe_allow_html=True)
    st.markdown("### Detail Evaluasi per Run")
    
    df_runs = get_runs_from_db()
    
    if df_runs.empty:
        st.info("Belum ada run evaluasi yang disimpan.")
    else:
        # Buat dropdown label run
        run_options = []
        for _, r in df_runs.iterrows():
            run_options.append(f"Run #{r['id']} - {r['run_timestamp']} ({r['num_questions']} Soal, Skor: {r['overall_score']:.3f})")
            
        selected_run_str = st.selectbox("Pilih Run Evaluasi:", run_options)
        selected_run_id = int(selected_run_str.split(" ")[1].replace("#", ""))
        
        # Ambil record run terpilih
        row_run = df_runs[df_runs["id"] == selected_run_id].iloc[0]
        
        st.markdown("---")
        
        # Kolom Ringkasan & Radar Chart
        col_radar, col_metrics = st.columns([3, 2])
        
        with col_radar:
            fig_radar = draw_radar_chart(row_run)
            st.plotly_chart(fig_radar, use_container_width=True)
            
        with col_metrics:
            st.markdown("#### Rata-rata Skor per Metrik")
            
            metrics_avg = {
                "Faithfulness (Bebas Halusinasi)": row_run["avg_faithfulness"],
                "Answer Relevance (Kesesuaian Jawaban)": row_run["avg_answer_relevance"],
                "Context Precision (Ketepatan Konteks)": row_run["avg_context_precision"],
                "Context Recall (Kelengkapan Konteks)": row_run["avg_context_recall"],
                "Context Relevancy (Relevansi Konteks)": row_run["avg_context_relevancy"]
            }
            
            for metric_label, score in metrics_avg.items():
                is_passed = score >= threshold_slider if 'threshold_slider' in locals() else score >= 0.60
                badge_class = "badge-pass" if is_passed else "badge-fail"
                status_icon = "✅" if is_passed else "❌"
                bar_width = int(score * 100)
                
                st.markdown(f"""
                <div style="margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:13px; color:#e2e8f0;">{status_icon} {metric_label}</span>
                        <span class="metric-badge {badge_class}">{score:.3f}</span>
                    </div>
                    <div style="background:#202046; border-radius:4px; height:6px; margin-top:4px;">
                        <div style="background-color:{'#4ade80' if is_passed else '#f87171'}; width:{bar_width}%; height:6px; border-radius:4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            # Overall Card
            ov_score = row_run["overall_score"]
            is_ov_passed = ov_score >= (threshold_slider if 'threshold_slider' in locals() else 0.60)
            ov_color = "#4ade80" if is_ov_passed else "#f87171"
            st.markdown(f"""
            <div style="margin-top:20px; padding:16px; background:#161633; border-radius:8px; border:1px solid #2d2d5a; text-align:center;">
                <div style="color:#94a3b8; font-size:12px; font-weight:600; letter-spacing:1px; margin-bottom:4px;">SKOR KESELURUHAN (OVERALL SCORE)</div>
                <div style="color:{ov_color}; font-size:32px; font-weight:800;">{ov_score:.3f}</div>
                <div style="color:{ov_color}; font-size:11px; margin-top:2px;">{"PASS (MEMENUHI SYARAT)" if is_ov_passed else "FAIL (DI BAWAH AMBANG BATAS)"}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.markdown("### Detail Test Case per Pertanyaan")
        
        # Ambil data rinci dari SQLite
        df_details = get_run_details_from_db(selected_run_id)
        
        for idx_d, rd in df_details.iterrows():
            q_text = rd["question"]
            title_q = f"Q{idx_d+1}: {q_text[:75]}..." if len(q_text) > 75 else f"Q{idx_d+1}: {q_text}"
            
            # Tentukan apakah baris ini lolos threshold secara rata-rata
            row_avg = (rd["faithfulness"] + rd["answer_relevance"] + rd["context_precision"] + rd["context_recall"] + rd["context_relevancy"]) / 5.0
            row_passed = row_avg >= (threshold_slider if 'threshold_slider' in locals() else 0.60)
            status_text = "🟢 PASS" if row_passed else "🔴 FAIL"
            
            with st.expander(f"{status_text} | {title_q}"):
                col_q, col_a = st.columns(2)
                with col_q:
                    st.markdown("**Pertanyaan Pengguna:**")
                    st.info(rd["question"])
                    st.markdown("**Expected Output (Jawaban FAQ):**")
                    st.success(rd["expected_output"])
                with col_a:
                    st.markdown("**Actual Output (Jawaban Chatbot):**")
                    st.warning(rd["actual_output"] if rd["actual_output"].strip() else "[Jawaban chatbot kosong]")
                    
                err_log = rd.get("error_log", "")
                if err_log and err_log != "OK":
                    st.error(f"**Sistem Log / Error:** {err_log}")
                    
                st.markdown("<br>**Hasil Metrik Evaluasi RAGAS:**", unsafe_allow_html=True)
                cols_m = st.columns(5)
                
                m_list_det = [
                    ("Faithfulness", rd["faithfulness"]),
                    ("Answer Relevance", rd["answer_relevance"]),
                    ("Context Precision", rd["context_precision"]),
                    ("Context Recall", rd["context_recall"]),
                    ("Context Relevancy", rd["context_relevancy"])
                ]
                
                for k, (m_name, m_score) in enumerate(m_list_det):
                    m_passed = m_score >= (threshold_slider if 'threshold_slider' in locals() else 0.60)
                    clr = "#4ade80" if m_passed else "#f87171"
                    bg_color = "rgba(74, 222, 128, 0.08)" if m_passed else "rgba(248, 113, 113, 0.08)"
                    cols_m[k].markdown(f"""
                    <div style="background:{bg_color}; border:1px solid {clr}; border-radius:6px; padding:10px; text-align:center; height:100px; display:flex; flex-direction:column; justify-content:center;">
                        <div style="color:#94a3b8; font-size:11px; margin-bottom:2px; line-height:1.2;">{m_name}</div>
                        <div style="color:{clr}; font-size:20px; font-weight:700;">{m_score:.2f}</div>
                        <div style="color:{clr}; font-size:10px; font-weight:600; margin-top:2px;">{"PASS" if m_passed else "FAIL"}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
        # Button untuk mengunduh hasil ekspor CSV untuk run ini
        st.markdown("<br>", unsafe_allow_html=True)
        csv_data = df_details.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Unduh CSV Hasil Run ini",
            data=csv_data,
            file_name=f"ragas_run_{selected_run_id}_{int(time.time())}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    st.markdown('</div>', unsafe_allow_html=True)
