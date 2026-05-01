import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd

from src.llm.summarizer import summarize_document
from src.ner.extractor import extract_entities
from src.ingestion.parser import extract_text_from_pdf
from src.ingestion.cleaner import clean_text
from src.processing.chunking import create_chunks
from src.llm.client import LLMClient
from src.llm.classifier import classify_clause
from src.risk.risk_engine import compute_risk
from src.llm.explainer import explain_risk
from src.llm.domain_detector import detect_domain
from src.rag.rag_engine import RAGEngine, answer_question


# -----------------------------
# SESSION INIT
# -----------------------------
if "processed" not in st.session_state:
    st.session_state.processed = False


# -----------------------------
# UTILS
# -----------------------------
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")


# -----------------------------
# UI CONFIG
# -----------------------------
st.set_page_config(page_title="Legal AI Analyzer", layout="wide")
st.title("📄 AI Legal Contract Analyzer")

uploaded_file = st.file_uploader("Upload Contract (PDF)", type=["pdf"])


# =====================================================
# 🚀 PROCESS BUTTON (RUN ONLY ONCE)
# =====================================================
if uploaded_file and st.button("🚀 Analyze Document"):

    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Analyzing document..."):

        text = extract_text_from_pdf("temp.pdf")

        if not text or not text.strip():
            st.error("❌ No text extracted.")
            st.stop()

        llm = LLMClient()

        domain = detect_domain(llm, text)
        summary = summarize_document(llm, text)
        entities = extract_entities(text)

        chunks = create_chunks(text)
        chunks_cleaned = [clean_text(c) for c in chunks]

        rag = RAGEngine()
        rag.build_index(chunks)

        results = []
        explanations = []

        for i in range(min(len(chunks_cleaned), 10)):
            clause_id = f"c{i}"

            result = classify_clause(llm, chunks_cleaned[i], clause_id, domain)
            risk = compute_risk(result, domain)

            results.append({
                "clause_id": clause_id,
                "domain": domain,
                "category": result["category"],
                "risk_level": risk["risk_level"],
                "risk_score": risk["risk_score"],
                "confidence": result["confidence"]
            })

            if risk["risk_level"] in ["High", "Medium"]:
                explanation = explain_risk(llm, chunks_cleaned[i], result)

                explanations.append({
                    "clause_id": clause_id,
                    "text": chunks[i][:300],
                    "explanation": explanation,
                    "breakdown": risk["breakdown"],
                    "risk": risk
                })

        df = pd.DataFrame(results)

        overall_score = round(df["risk_score"].mean(), 2)

        if overall_score > 0.75:
            overall_level = "High"
        elif overall_score > 0.5:
            overall_level = "Medium"
        else:
            overall_level = "Low"

        # STORE
        st.session_state.summary = summary
        st.session_state.entities = entities
        st.session_state.df = df
        st.session_state.explanations = explanations
        st.session_state.rag = rag
        st.session_state.domain = domain
        st.session_state.overall_score = overall_score
        st.session_state.overall_level = overall_level
        st.session_state.processed = True


# =====================================================
# 📊 DISPLAY
# =====================================================
if st.session_state.processed:

    llm = LLMClient()

    summary = st.session_state.summary
    entities = st.session_state.entities
    df = st.session_state.df
    explanations = st.session_state.explanations
    rag = st.session_state.rag
    domain = st.session_state.domain
    overall_score = st.session_state.overall_score
    overall_level = st.session_state.overall_level

    # DOMAIN
    st.success(f"📌 Detected Domain: {domain}")

    # SUMMARY
    with st.expander("🧾 Contract Summary", expanded=True):
        st.markdown(summary)

    # NER
    with st.expander("🔍 Key Entities"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("**👤 People**")
            st.write(entities.get("PERSON", []) or "—")

            st.write("**🏢 Organizations**")
            st.write(entities.get("ORG", []) or "—")

        with col2:
            st.write("**📅 Dates**")
            st.write(entities.get("DATE", []) or "—")

            st.write("**💰 Money**")
            st.write(entities.get("MONEY", []) or "—")

        with col3:
            st.write("**🌍 Locations**")
            st.write(entities.get("GPE", []) or "—")

    # RISK SUMMARY
    st.subheader("📊 Contract Risk Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Risk", overall_level)
    col2.metric("Risk Score", overall_score)
    col3.metric("Clauses", len(df))

    if overall_level == "High":
        st.error("⚠️ High Risk Contract")
    elif overall_level == "Medium":
        st.warning("⚠️ Medium Risk Contract")
    else:
        st.success("✅ Low Risk Contract")

    # =====================================================
    # 📊 INSIGHTS (NO matplotlib)
    # =====================================================
    st.subheader("📊 Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Risk Distribution")
        risk_counts = df["risk_level"].value_counts()
        st.bar_chart(risk_counts)

    with col2:
        st.write("### Clause Categories")
        cat_counts = df["category"].value_counts()
        st.bar_chart(cat_counts)

    # FILTERS
    st.subheader("🔍 Filter Clauses")

    col1, col2 = st.columns(2)

    risk_filter = col1.selectbox("Risk Level", ["All", "High", "Medium", "Low"])
    category_filter = col2.selectbox(
        "Category", ["All"] + sorted(df["category"].unique())
    )

    filtered_df = df.copy()

    if risk_filter != "All":
        filtered_df = filtered_df[filtered_df["risk_level"] == risk_filter]

    if category_filter != "All":
        filtered_df = filtered_df[filtered_df["category"] == category_filter]

    with st.expander("📋 Clause Analysis", expanded=True):
        st.dataframe(filtered_df, use_container_width=True)

    # DOWNLOAD
    st.download_button(
        "📥 Download CSV",
        convert_df_to_csv(filtered_df),
        "report.csv"
    )

    # RISKY CLAUSES
    st.subheader("⚠️ Risky Clauses")

    if not explanations:
        st.success("✅ No risky clauses found.")
    else:
        for exp in explanations:
            with st.expander(f"{exp['clause_id']} ({exp['risk']['risk_level']})"):

                st.markdown(f"```text\n{exp['text']}\n```")

                st.write("**Why Risky:**")
                st.write(exp["explanation"])

                b = exp["breakdown"]

                st.markdown(f"""
- Base: {b['base']}
- Risk Flag: {b['risk_flag']}
- Keywords: {b['keywords']}
- Domain: {b['domain']}
- Confidence: {b['confidence']}
                """)

                st.success(f"{exp['risk']['risk_score']}")

    # =====================================================
    # 💬 RAG Q&A
    # =====================================================
    st.subheader("💬 Ask Questions")

    question = st.text_input("Ask something about the document")

    if question:
        with st.spinner("Thinking..."):
            answer, source, sources = answer_question(llm, rag, question)

        st.write("**Answer:**")
        st.write(answer)

        st.write("**📌 Exact Source:**")
        st.info(source)

        st.write("**📌 Sources:**")
        for s in sources:
            st.markdown(f"- {s[:200]}...")