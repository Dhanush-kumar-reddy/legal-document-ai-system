import re


def clean_entities(entity_list, entity_type=None):
    """
    Cleans extracted NER entities based on type-aware rules.

    entity_type ∈ ["PERSON", "ORG", "DATE", "MONEY", "GPE"]
    """

    cleaned = []

    # -----------------------------
    # GLOBAL BLACKLIST
    # -----------------------------
    blacklist = {
        "agreement", "annex", "clause", "section",
        "company", "employee", "party", "term",
        "bank", "donor", "contribution",
        "board", "executive", "shares",
        "notice period", "cause", "rapporti",
        "role", "band"
    }

    # -----------------------------
    # VALID ORG KEYWORDS
    # -----------------------------
    valid_org_keywords = {
        "inc", "ltd", "llc", "corp", "corporation",
        "bank", "agency", "ministry", "department",
        "authority", "university", "association"
    }

    # -----------------------------
    # DATE MONTHS
    # -----------------------------
    months = {
        "january","february","march","april","may","june",
        "july","august","september","october","november","december"
    }

    # -----------------------------
    # CLEAN LOOP
    # -----------------------------
    for e in entity_list:
        if not e:
            continue

        # -----------------------------
        # NORMALIZATION
        # -----------------------------
        e = e.strip()
        e = re.sub(r"[\"']", "", e)           # remove quotes
        e = re.sub(r"\s+", " ", e)            # normalize spaces

        # -----------------------------
        # BASIC FILTERS
        # -----------------------------
        if len(e) < 3:
            continue

        if "\n" in e or "\t" in e:
            continue

        # numeric-only
        if e.replace(" ", "").isdigit():
            continue

        # blacklist
        if any(word in e.lower() for word in blacklist):
            continue

        # remove ALL CAPS noise (VERY IMPORTANT FIX)
        if e.isupper() and len(e.split()) >= 2:
            continue

        # -----------------------------
        # TYPE-SPECIFIC RULES
        # -----------------------------

        # 👤 PERSON
        if entity_type == "PERSON":
            if len(e.split()) < 2:
                continue
            if not all(word[0].isupper() for word in e.split() if word[0].isalpha()):
                continue

        # 🏢 ORG (STRICT BUT SAFE)
        elif entity_type == "ORG":

            org_blacklist = {"board", "executive", "shares", "notice", "cause"}
            if any(word in e.lower() for word in org_blacklist):
                continue

            # remove short uppercase tokens like "CIN"
            if e.isupper() and len(e) < 5:
                continue

            # must contain meaningful org indicator
            if not any(k in e.lower() for k in valid_org_keywords):
                # allow multi-word capitalized names (fallback)
                if len(e.split()) < 2:
                    continue

        # 📅 DATE
        elif entity_type == "DATE":
            if not any(char.isdigit() for char in e) and not any(m in e.lower() for m in months):
                continue

        # 💰 MONEY
        elif entity_type == "MONEY":
            currency_tokens = ["₹", "$", "€", "INR", "USD", "EUR"]
            if not any(c in e for c in currency_tokens):
                if not any(char.isdigit() for char in e):
                    continue

        # 🌍 LOCATION (GPE)
        elif entity_type == "GPE":
            # remove noise like "D.C.", "N.W."
            if re.fullmatch(r"[A-Z]\.[A-Z]\.", e):
                continue

            if len(e.split()) == 1:
                if not e[0].isupper():
                    continue

        # -----------------------------
        # FINAL ADD
        # -----------------------------
        cleaned.append(e)

    # -----------------------------
    # DEDUP (CASE-INSENSITIVE)
    # -----------------------------
    cleaned = list(set([c.strip() for c in cleaned if c]))

    return sorted(cleaned)