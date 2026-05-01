from src.ingestion.parser import extract_text_from_pdf
from src.ingestion.cleaner import clean_text
from src.processing.chunking import create_chunks
from src.llm.client import LLMClient
from src.llm.classifier import classify_clause
from src.risk.risk_engine import compute_risk
from src.risk.contract_analyzer import analyze_contract
from src.llm.explainer import explain_risk

file_path = "data/samples/legal-document-1.pdf"

text = extract_text_from_pdf(file_path)
cleaned = clean_text(text)
chunks = create_chunks(cleaned)

llm = LLMClient()

all_risks = []
explanations = []

for i, chunk in enumerate(chunks[:5]):
    result = classify_clause(llm, chunk, f"c{i}")
    risk = compute_risk(result)

    all_risks.append(risk)

    # 👉 ADD THIS HERE
    if risk["risk_level"] == "High":
        explanation = explain_risk(llm, chunk, result)

        explanations.append({
            "clause_id": result["clause_id"],
            "explanation": explanation
        })

summary = analyze_contract(all_risks)

print("\n--- CONTRACT SUMMARY ---\n")
print(summary)

print("\n--- HIGH RISK EXPLANATIONS ---\n")
print(explanations)