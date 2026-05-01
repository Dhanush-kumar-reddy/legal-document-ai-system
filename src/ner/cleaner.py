import re

def clean_entities(entity_list, entity_type=None):

    cleaned = []

    blacklist = {
        "agreement", "annex", "clause", "section",
        "company", "employee", "party", "term",
        "bank", "donor", "contribution",
        "board", "executive", "shares",
        "notice period", "cause"
    }

    valid_org_keywords = {
        "inc", "ltd", "llc", "corp", "corporation",
        "bank", "agency", "ministry", "department",
        "authority", "university", "association"
    }

    months = {
        "january","february","march","april","may","june",
        "july","august","september","october","november","december"
    }

    for e in entity_list:
        if not e:
            continue

        e = e.strip()
        e = re.sub(r"[\"']", "", e)
        e = re.sub(r"\s+", " ", e)

        if len(e) < 3:
            continue

        if e.replace(" ", "").isdigit():
            continue

        if any(word in e.lower() for word in blacklist):
            continue

        if e.isupper() and len(e.split()) >= 2:
            continue

        # PERSON
        if entity_type == "PERSON":
            if len(e.split()) < 2:
                continue

        # ORG
        elif entity_type == "ORG":
            if not any(k in e.lower() for k in valid_org_keywords):
                if len(e.split()) < 2:
                    continue

        # DATE
        elif entity_type == "DATE":
            if not any(char.isdigit() for char in e) and not any(m in e.lower() for m in months):
                continue

        # MONEY
        elif entity_type == "MONEY":
            if not any(c in e for c in ["₹", "$", "€", "USD", "INR"]):
                continue

        cleaned.append(e)

    return sorted(list(set(cleaned)))