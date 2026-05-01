import spacy
from src.ner.cleaner import clean_entities
import re

# Load model once (important for performance)
nlp = spacy.load("en_core_web_sm")

def extract_money_regex(text):
    pattern = r'[\$₹€]\s?\d+(?:,\d{3})*(?:\.\d+)?'
    return re.findall(pattern, text)

def extract_entities(text: str):
    doc = nlp(text[:5000])  # limit for performance

    # Step 1: Initialize entity storage
    entities = {
        "PERSON": set(),
        "ORG": set(),
        "DATE": set(),
        "MONEY": set(),
        "GPE": set()
    }

    # Step 2: Extract entities
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].add(ent.text)

    # -----------------------------
    # EXTRA MONEY DETECTION (regex)
    # -----------------------------
    money_patterns = re.findall(r'[\€\₹\$\£]\s?\d+[,\d]*', text)

    for m in money_patterns:
        entities["MONEY"].add(m)

    # Step 3: Convert sets → lists
    entities = {k: list(v) for k, v in entities.items()}

    entities["PERSON"] = clean_entities(entities["PERSON"], "PERSON")
    entities["ORG"] = clean_entities(entities["ORG"], "ORG")
    entities["DATE"] = clean_entities(entities["DATE"], "DATE")
    entities["MONEY"] = clean_entities(entities["MONEY"], "MONEY")
    entities["GPE"] = clean_entities(entities["GPE"], "GPE")

        # Add regex-based money extraction
    money_regex = extract_money_regex(text)
    entities["MONEY"] = list(set(list(entities["MONEY"]) + money_regex))
    
    return entities