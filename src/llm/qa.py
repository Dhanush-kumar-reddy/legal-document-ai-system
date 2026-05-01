def answer_question(llm, query, context_chunks):

    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a legal assistant.

Answer the user's question using ONLY the provided context.

--------------------------------
CONTEXT:
{context}

--------------------------------
QUESTION:
{query}

--------------------------------
RULES:
- Be precise
- Do not hallucinate
- If answer not found, say:
  "Not found in document"

--------------------------------

Answer:
"""

    response = llm.invoke(prompt)

    return response.strip()