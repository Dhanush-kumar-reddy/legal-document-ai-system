DOMAIN_WEIGHTS = {
    "Employment Contract": {
        "Termination": 1.0,
        "Payment": 0.7,
        "Obligations": 0.6
    },
    "Financial Document": {
        "Liability": 1.0,
        "Warranty": 0.8
    },
    "Court Judgment": {
        "Liability": 1.0
    },
    "Government Agreement": {
        "Obligations": 1.0,
        "Payment": 0.9
    }
}

HIGH_RISK_KEYWORDS = [
    "penalty", "late fee", "liability", "indemnify",
    "termination", "terminate", "damages",
    "breach", "default", "lawsuit",
    "clawback", "forfeiture", "recoupment",
    "notice period", "severance", "compensation"
]


def compute_risk(clause, domain=None):

    category = clause["category"]
    risk_flag = clause["risk_flag"]
    keywords = clause["keywords"]
    confidence = clause.get("confidence", 0.8)

    breakdown = {}

    # -----------------------------
    # BASE SCORE (more conservative)
    # -----------------------------
    CATEGORY_BASE = {
        "Termination": 0.45,
        "Indemnity": 0.55,
        "Liability": 0.55,
        "Payment": 0.45,
        "Confidentiality": 0.35,
        "Obligations": 0.25,
        "Warranty": 0.25,
        "Intellectual Property": 0.35,
        "Force Majeure": 0.2,
        "Dispute Resolution": 0.35
    }

    score = CATEGORY_BASE.get(category, 0.3)
    breakdown["base"] = score

    # -----------------------------
    # DOMAIN BOOST (reduced)
    # -----------------------------
    domain_boost = 0

    if domain == "Employment Contract":
        if category == "Termination":
            domain_boost = 0.08
        elif category == "Payment":
            domain_boost = 0.04

    elif domain == "Financial Document":
        if category == "Liability":
            domain_boost = 0.08

    elif domain == "Government Agreement":
        if category == "Obligations":
            domain_boost = 0.08

    score += domain_boost
    breakdown["domain"] = domain_boost

    # -----------------------------
    # RISK FLAG (controlled impact)
    # -----------------------------
    flag_boost = 0.22 if risk_flag else 0
    score += flag_boost
    breakdown["risk_flag"] = flag_boost

    # -----------------------------
    # KEYWORD BOOST (smarter)
    # -----------------------------
    HIGH_RISK_KEYWORDS = [
        "penalty", "late fee", "liability", "indemnify",
        "damages", "breach", "default",
        "clawback", "forfeiture", "recoupment",
        "notice period", "severance", "termination fee"
    ]

    keyword_hits = 0

    for kw in keywords:
        kw_lower = kw.lower()

        # smarter match (not exact match)
        if any(risk_word in kw_lower for risk_word in HIGH_RISK_KEYWORDS):
            keyword_hits += 1

    keyword_boost = min(keyword_hits * 0.025, 0.08)  # lower + capped
    score += keyword_boost
    breakdown["keywords"] = keyword_boost

    # -----------------------------
    # CONFIDENCE PENALTY (important)
    # -----------------------------
    confidence_penalty = -0.07 if confidence < 0.75 else 0
    score += confidence_penalty
    breakdown["confidence"] = confidence_penalty

    # -----------------------------
    # IMPORTANT: NON-RISKY CLAUSE CONTROL
    # -----------------------------
    if not risk_flag:
        score = min(score, 0.55)  # cannot become High
        breakdown["non_risk_cap"] = True
    else:
        breakdown["non_risk_cap"] = False

    # -----------------------------
    # NORMALIZE
    # -----------------------------
    score = max(0, min(score, 1.0))

    # -----------------------------
    # FINAL LEVEL (slightly stricter)
    # -----------------------------
    if score > 0.8:
        level = "High"
    elif score > 0.55:
        level = "Medium"
    else:
        level = "Low"

    return {
        "clause_id": clause["clause_id"],
        "category": category,
        "risk_score": round(score, 2),
        "risk_level": level,
        "breakdown": breakdown
    }