def analyze_contract(all_risks):
    total_score = 0

    high = []
    medium = []
    low = []

    for r in all_risks:
        score = r["risk_score"]
        total_score += score

        if score > 0.75:
            high.append(r["clause_id"])
        elif score > 0.5:
            medium.append(r["clause_id"])
        else:
            low.append(r["clause_id"])

    avg_score = total_score / len(all_risks)

    if avg_score > 0.75:
        level = "High"
    elif avg_score > 0.5:
        level = "Medium"
    else:
        level = "Low"

    return {
        "overall_risk_score": round(avg_score, 2),
        "overall_risk_level": level,
        "high_risk_clauses": high,
        "medium_risk_clauses": medium,
        "low_risk_clauses": low
    }