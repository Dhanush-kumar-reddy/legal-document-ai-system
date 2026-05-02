import json
from tqdm import tqdm

from src.llm.client import LLMClient
from src.llm.classifier import classify_clause
from src.risk.risk_engine import compute_risk
from src.rag.rag_engine import RAGEngine, answer_question
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

def load_data(path="data/eval/eval_data.json"):
    with open(path, "r") as f:
        return json.load(f)


def evaluate():
    data = load_data()
    llm = LLMClient()

    # Build RAG corpus
    corpus = [d["text"] for d in data]
    rag = RAGEngine()
    rag.build_index(corpus)

    total = len(data)

    correct_category = 0
    correct_risk = 0
    correct_qa = 0
    total_qa = 0

    for i, item in enumerate(tqdm(data)):
        text = item["text"]

        # -------------------
        # Classification
        # -------------------
        result = classify_clause(llm, text, f"c{i}", "general")

        if result["category"] == item["expected_category"]:
            correct_category += 1

        # -------------------
        # Risk
        # -------------------
        risk = compute_risk(result, "general")

        if risk["risk_level"] == item["expected_risk"]:
            correct_risk += 1

        # -------------------
        # QA (RAG)
        # -------------------
        for q in item.get("questions", []):
            total_qa += 1

            pred_answer, _, _ = answer_question(llm, rag, q["q"])

            if q["expected_answer"].lower() in pred_answer.lower():
                correct_qa += 1

    # -------------------
    # Results
    # -------------------
    print("\n===== EVALUATION RESULTS =====")

    print(f"Classification Accuracy: {correct_category}/{total} = {correct_category/total:.2f}")
    print(f"Risk Accuracy: {correct_risk}/{total} = {correct_risk/total:.2f}")

    if total_qa > 0:
        print(f"RAG QA Accuracy: {correct_qa}/{total_qa} = {correct_qa/total_qa:.2f}")


if __name__ == "__main__":
    evaluate()