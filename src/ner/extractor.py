import spacy
import re
from src.ner.cleaner import clean_entities

# -----------------------------
# LOAD MODEL SAFELY (Cloud Fix)
# -----------------------------
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except:
        from spacy.cli import download
        download("en_core_web_sm")
        return spacy.load("en_core_web_sm")

nlp = load_spacy_model()


# -----------------------------
# MONEY REGEX
# -----------------------------
def extract_money_regex(text):
    pattern = r'[\$₹€£]\s?\d+(?:,\d{3})*(?:\.\d+)?'
    return re.findall(pattern, text)


# -----------------------------
# MAIN ENTITY EXTRACTION
# -----------------------------
def extract_entities(text: str):

    doc = nlp(text[:5000])  # performance limit

    entities = {
        "PERSON": set(),
        "ORG": set(),
        "DATE": set(),
        "MONEY": set(),
        "GPE": set()
    }

    # -----------------------------
    # SPACY EXTRACTION
    # -----------------------------
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].add(ent.text)

    # -----------------------------
    # ADD MONEY (ONLY ONCE)
    # -----------------------------
    money_regex = extract_money_regex(text)
    entities["MONEY"].update(money_regex)

    # -----------------------------
    # CLEAN (AFTER FULL EXTRACTION)
    # -----------------------------
    entities = {k: list(v) for k, v in entities.items()}

    entities["PERSON"] = clean_entities(entities["PERSON"], "PERSON")
    entities["ORG"] = clean_entities(entities["ORG"], "ORG")
    entities["DATE"] = clean_entities(entities["DATE"], "DATE")
    entities["MONEY"] = clean_entities(entities["MONEY"], "MONEY")
    entities["GPE"] = clean_entities(entities["GPE"], "GPE")

    return entities