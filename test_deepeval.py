import os
import json
import pandas as pd
import pytest
from deepeval.metrics import (
    ContextualRelevancyMetric,
    ContextualRecallMetric,
    ContextualPrecisionMetric,
    AnswerRelevancyMetric,
    FaithfulnessMetric
)
from deepeval.test_case import LLMTestCase
from deepeval.models.base_model import DeepEvalBaseLLM
from langchain_groq import ChatGroq
from deepeval import evaluate
import requests

class CustomGroqLLM(DeepEvalBaseLLM):
    """Custom LLM Wrapper agar DeepEval menggunakan Groq (Gratis) bukan OpenAI (Berbayar)"""
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        self.model = ChatGroq(model_name=model_name, temperature=0.0)
        self.model_name = model_name

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        # Mengembalikan plain text string dari AIMessage LangChain
        return chat_model.invoke(prompt).content

    async def a_generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        res = await chat_model.ainvoke(prompt)
        return res.content

    def get_model_name(self):
        return self.model_name

# Inisialisasi Juri AI (Gunakan Llama 3 70B yang canggih sebagai rater)
groq_evaluator = CustomGroqLLM()

# Konfigurasi target API
API_URL = "http://127.0.0.1:8000/api/v1/chat"

def get_rag_response(query: str):
    """Fungsi pembantu untuk menembak API dan mendapatkan konteks aktual"""
    try:
        response = requests.post(
            API_URL, 
            json={"query": query, "session_id": "eval_bot_session"},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json().get("data", {})
            answer = data.get("answer", "")
            
            # Ambil teks chunk asli dari API (bukan lagi metadata)
            retrieval_context = data.get("retrieval_context", [])
            
            if not retrieval_context:
                retrieval_context = ["No context retrieved."]
                
            return answer, retrieval_context
            
    except Exception as e:
        print(f"Failed to reach API: {e}")
    return "", ["Failed to retrieve context"]


def run_evaluation_batch(csv_path: str):
    """Menjalankan evaluasi berbaris untuk skripsi"""
    print(f"Membaca dataset dari {csv_path}...")
    df = pd.read_csv(csv_path)
    
    test_cases = []
    
    for idx, row in df.iterrows():
        input_query = row.get("input", "")
        expected_output = row.get("expected_output", "")
        
        print(f"Memproses Q{idx+1}: {input_query}")
        actual_output, retrieval_context = get_rag_response(input_query)
        
        # Buat objek LLMTestCase standard DeepEval
        test_case = LLMTestCase(
            input=input_query,
            actual_output=actual_output,
            expected_output=expected_output,
            retrieval_context=retrieval_context
        )
        test_cases.append(test_case)
        

    # 1. Metrik untuk kualitas Retrieval (Mata Sistem)
    contextual_precision = ContextualPrecisionMetric(threshold=0.5, model=groq_evaluator)
    contextual_recall = ContextualRecallMetric(threshold=0.5, model=groq_evaluator)
    contextual_relevancy = ContextualRelevancyMetric(threshold=0.5, model=groq_evaluator)

    # 2. Metrik untuk Kualitas Generator (Otak Sistem - Agent)
    answer_relevancy = AnswerRelevancyMetric(threshold=0.5, model=groq_evaluator)
    faithfulness = FaithfulnessMetric(threshold=0.5, model=groq_evaluator)

    metrics = [
        contextual_precision,
        contextual_recall,
        contextual_relevancy,
        answer_relevancy,
        faithfulness
    ]

    print(f"\\nMemulai Evaluasi DeepEval untuk {len(test_cases)} kasus... Ini mungkin akan memakan waktu.")
    
    # Jalankan evaluasi
    # Secara otomatis DeepEval menggunakan LLM (via OpenAI atau default Groq) sebagai Juri.
    results = evaluate(test_cases, metrics)
    return results

if __name__ == "__main__":
    # Tes jalankan script jika dieksekusi via terminal
    dataset_file = "dataset_evaluasi.csv"
    if os.path.exists(dataset_file):
        run_evaluation_batch(dataset_file)
    else:
        print(f"File {dataset_file} tidak ditemukan.")
