def explain_risk(llm, clause_text, classification):
    prompt = f"""
Explain why the following clause is risky.

ONLY explain risk if there is REAL consequence:
- financial loss
- penalty
- liability
- legal enforcement

DO NOT treat normal job responsibilities as risk.

Clause:
{clause_text}

Classification:
{classification}

Give a short 1-2 line explanation.
"""

    response = llm.invoke(prompt)
    return response

