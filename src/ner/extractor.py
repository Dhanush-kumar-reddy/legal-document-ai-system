import spacy
import re
from src.ner.cleaner import clean_entities

# -----------------------------
# LOAD MODEL (SAFE FOR CLOUD)
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
def extract_money(text):
    pattern = r'[\$₹€£]\s?\d+(?:,\d{3})*(?:\.\d+)?'
    return re.findall(pattern, text)

# -----------------------------
# MAIN FUNCTION
# -----------------------------
def extract_entities(text: str):

    doc = nlp(text[:5000])

    entities = {
        "PERSON": set(),
        "ORG": set(),
        "DATE": set(),
        "MONEY": set(),
        "GPE": set()
    }

    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].add(ent.text)

    # Add money
    entities["MONEY"].update(extract_money(text))

    # Clean
    for key in entities:
        entities[key] = clean_entities(list(entities[key]), key)

    return entities