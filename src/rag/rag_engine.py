from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import faiss
import numpy as np


class RAGEngine:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.chunks = []
        self.bm25 = None
        self.tokenized_chunks = None

    # -----------------------------
    # BUILD INDEX
    # -----------------------------
    def build_index(self, chunks):

        self.chunks = chunks

        # -------- FAISS --------
        embeddings = self.model.encode(
            chunks,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

        # -------- BM25 --------
        self.tokenized_chunks = [c.lower().split() for c in chunks]
        self.bm25 = BM25Okapi(self.tokenized_chunks)

    # -----------------------------
    # HYBRID RETRIEVE
    # -----------------------------
    def retrieve(self, query, k=3):

        # -------------------------
        # FAISS (semantic)
        # -------------------------
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        faiss_scores, faiss_idx = self.index.search(query_embedding, len(self.chunks))

        faiss_scores = faiss_scores[0]
        faiss_idx = faiss_idx[0]

        # Normalize FAISS scores (0–1)
        faiss_norm = (faiss_scores - faiss_scores.min()) / (
            faiss_scores.max() - faiss_scores.min() + 1e-6
        )

        # -------------------------
        # BM25 (keyword)
        # -------------------------
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)

        bm25_scores = np.array(bm25_scores)

        # Normalize BM25
        bm25_norm = (bm25_scores - bm25_scores.min()) / (
            bm25_scores.max() - bm25_scores.min() + 1e-6
        )

        # -------------------------
        # COMBINE
        # -------------------------
        combined_scores = {}

        for i in range(len(self.chunks)):

            semantic_score = faiss_norm[list(faiss_idx).index(i)] if i in faiss_idx else 0
            keyword_score = bm25_norm[i]

            combined_scores[i] = 0.6 * semantic_score + 0.4 * keyword_score

        # -------------------------
        # SORT
        # -------------------------
        top_indices = sorted(
            combined_scores,
            key=combined_scores.get,
            reverse=True
        )[:k]

        return [self.chunks[i] for i in top_indices]

# =====================================================
# QA FUNCTION
# =====================================================
def answer_question(llm, rag, question):

    docs = rag.retrieve(question, k=3)

    context = "\n\n".join(docs)

    prompt = f"""
Answer strictly using context.
Also return the exact supporting sentence.

Format:
ANSWER: ...
SOURCE: ...

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    # simple parsing
    if "SOURCE:" in response:
        answer_part, source_part = response.split("SOURCE:")
        answer = answer_part.replace("ANSWER:", "").strip()
        source = source_part.strip()
    else:
        answer = response
        source = docs[0]

    return answer, source, docs