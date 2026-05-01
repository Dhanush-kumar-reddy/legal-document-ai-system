import spacy
from loguru import logger

nlp = spacy.load("en_core_web_sm")

doc = nlp("Apple signed a contract with Microsoft on January 1, 2024 for $5000.")

for ent in doc.ents:
    logger.info(f"{ent.text} - {ent.label_}")