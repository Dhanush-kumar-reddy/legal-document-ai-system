def summarize_document(llm, text: str) -> str:

    prompt = f"""
You are a legal contract summarization expert.

Your job is to summarize the document in a clear, structured format.

--------------------------------
OUTPUT FORMAT (STRICT)
--------------------------------

Return summary in this format:

SUMMARY:
- 3 to 5 bullet points explaining the contract

KEY OBLIGATIONS:
- What each party must do

RISKS:
- Any potential risks or penalties (if present)

IMPORTANT TERMS:
- Key conditions (notice period, payments, etc.)

--------------------------------

RULES:
- Use simple English
- Avoid legal jargon
- Be concise
- Do NOT hallucinate
- If something is missing, skip that section

--------------------------------

DOCUMENT:
{text[:4000]}

Return structured summary:
"""

    response = llm.invoke(prompt)

    return response.strip()