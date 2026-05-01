import spacy
import re
from collections import defaultdict
from src.utils.logger import get_logger

logger = get_logger()
import spacy
import os

try:
    nlp = spacy.load("en_core_web_sm")
except:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# -----------------------------
# CLEAN ENTITIES
# -----------------------------
def clean_entities(entities):
    cleaned = {}

    blacklist = set([
        "agreement", "party", "section", "clause",
        "confidential information", "services",
        "scope of services", "contract", "damages",
        "execution date", "effective date"
    ])

    for key, values in entities.items():
        temp = set()

        for val in values:
            val = val.strip()

            if len(val) < 3:
                continue

            # remove numeric junk
            if re.fullmatch(r"[\d,.\-]+", val):
                continue

            # remove blacklist
            if val.lower() in blacklist:
                continue

            # remove ALL CAPS noise (except ORG like "IBM")
            if key != "ORG" and val.isupper() and len(val) < 6:
                continue

            # normalize spacing
            val = re.sub(r"\s+", " ", val)

            temp.add(val)

        cleaned[key] = sorted(temp)

    return cleaned


# -----------------------------
# ROLE EXTRACTION
# -----------------------------
def extract_roles(text):
    roles = {}

    patterns = {
        "Employer": r'([A-Z][A-Za-z\s]+)\s*\(.*Employer',
        "Employee": r'([A-Z][A-Za-z\s]+)\s*\(.*Employee',
        "Consultant": r'([A-Z][A-Za-z\s]+)\s*\(.*Consultant',
    }

    for role, pattern in patterns.items():
        match = re.search(pattern, text[:1500])
        if match:
            roles[role] = match.group(1).strip()

    return roles


# -----------------------------
# MONEY EXTRACTION (IMPROVED)
# -----------------------------
def extract_money(text):
    pattern = r'(?:₹|\$|USD|INR)\s?\d+(?:,\d{3})*(?:\.\d+)?'
    return list(set(re.findall(pattern, text)))


# -----------------------------
# CHUNK LEVEL EXTRACTION
# -----------------------------
def extract_entities_from_chunk(text):
    doc = nlp(text)

    entities = defaultdict(set)

    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "DATE", "GPE"]:
            entities[ent.label_].add(ent.text)

    return entities


# -----------------------------
# MAIN AGGREGATION
# -----------------------------
def extract_entities(text, chunks=None):

    if not chunks:
        chunks = [text]

    final_entities = defaultdict(set)

    for chunk in chunks:
        chunk_entities = extract_entities_from_chunk(chunk)

        for key in chunk_entities:
            final_entities[key].update(chunk_entities[key])

    # MONEY (regex better than spaCy)
    money_entities = extract_money(text)
    final_entities["MONEY"].update(money_entities)

    # CLEAN
    final_entities = clean_entities(final_entities)

    # ROLES
    final_entities["ROLES"] = extract_roles(text)

    logger.info("NER extraction completed")

    return final_entities