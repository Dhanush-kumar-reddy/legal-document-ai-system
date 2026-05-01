def validate_classification(result):
    allowed_categories = [
        "Payment", "Termination", "Liability", "Confidentiality",
        "Indemnity", "Dispute Resolution", "Obligations",
        "Warranty", "Intellectual Property", "Force Majeure"
    ]

    if result.get("category") not in allowed_categories:
        result["category"] = "Obligations"

    if not isinstance(result.get("keywords"), list):
        result["keywords"] = []

    confidence = result.get("confidence", 0.5)
    if not (0 <= confidence <= 1):
        result["confidence"] = 0.5

    if "risk_flag" not in result:
        result["risk_flag"] = False

    return result