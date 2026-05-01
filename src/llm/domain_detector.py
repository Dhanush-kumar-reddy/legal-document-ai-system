def detect_domain(llm, text):

    prompt = f"""
Classify the document into ONE of these domains:

[Employment Contract, Financial Document, Court Judgment, Government Agreement, General Contract]

Document:
{text[:1500]}

Return ONLY the domain name.
"""

    response = llm.invoke(prompt)
    return response.strip()