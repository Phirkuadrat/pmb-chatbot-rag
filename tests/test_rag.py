import os
from dotenv import load_dotenv
from deepeval import evaluate
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import (
    ContextualRelevancyMetric,
    ContextualRecallMetric,
    ContextualPrecisionMetric,
    GEval
)
from deepeval.models.base_model import DeepEvalBaseLLM
from langchain_google_genai import ChatGoogleGenerativeAI
from app.services.rag_engine import PMBRagEngine

load_dotenv()

class GeminiJudge(DeepEvalBaseLLM):
    def __init__(self):
        # Gemini 1.5 Flash: andal untuk output JSON terstruktur,
        # quota besar, pool terpisah dari Groq (RAG)
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro-preview",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0,
        )

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        return self.model.invoke(prompt).content

    async def a_generate(self, prompt: str) -> str:
        res = await self.model.ainvoke(prompt)
        return res.content

    def get_model_name(self):
        return "Gemini 1.5 Flash"

llm_judge = GeminiJudge()
rag_engine = PMBRagEngine()

dataset_historis = [
    {
        "input": "Berapa total biaya masuk Informatika jalur UTBK?",
        "expected_output": "Total biaya masuk Informatika jalur UTBK adalah Rp 26.300.000.",
        "context": ["Jalur UTBK Informatika memiliki total biaya masuk Rp 26.300.000 yang mencakup DPP Rp 17.500.000 dan uang kuliah Rp 8.800.000."]
    },
    {
        "input": "Apa saja syarat kelulusan program sarjana di Itenas?",
        "expected_output": "Syarat kelulusan sarjana meliputi lulus mata kuliah kurikulum, IPK minimal 2.00, nilai B untuk Skripsi, minimal 20 SKK, EPT minimal 475, dan publikasi jurnal.",
        "context": ["Pasal 45 menetapkan syarat kelulusan sarjana: IPK min 2.00, EPT 475, SKK 20, dan publikasi ilmiah."]
    }
]


print("⏳ Menyiapkan Test Cases dengan RAG QA Agent...")
test_cases = []
for data in dataset_historis:
    result = rag_engine.ask(data["input"])
    
    test_case = LLMTestCase(
        input=data["input"],
        actual_output=result["answer"],
        retrieval_context=data["context"],
        expected_output=data["expected_output"]
    )
    test_cases.append(test_case)

print("🛠️ Membangun Metrik Evaluasi...")

relevancy = ContextualRelevancyMetric(threshold=0.7, model=llm_judge)
recall = ContextualRecallMetric(threshold=0.7, model=llm_judge)
precision = ContextualPrecisionMetric(threshold=0.7, model=llm_judge)

answer_correctness = GEval(
    name="Answer Correctness",
    criteria="Evaluate if the actual output's answer is correct and complete from the input and retrieved context.",
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.RETRIEVAL_CONTEXT],
    model=llm_judge
)

citation_accuracy = GEval(
    name="Citation Accuracy",
    criteria="Check if the citations/facts in the actual output are correct and relevant based on retrieved context.",
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.RETRIEVAL_CONTEXT],
    model=llm_judge
)

if __name__ == "__main__":
    print("\n🚀 MEMULAI EVALUASI RETRIEVER...")
    retriever_metrics = [relevancy, recall, precision]
    evaluate(test_cases, retriever_metrics)

    print("\n🚀 MEMULAI EVALUASI GENERATOR...")
    generator_metrics = [answer_correctness, citation_accuracy]
    evaluate(test_cases, generator_metrics)