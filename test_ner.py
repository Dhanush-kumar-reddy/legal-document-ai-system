from src.ingestion.parser import extract_text_from_pdf
from src.ingestion.cleaner import clean_text
from src.processing.chunking import create_chunks
from src.nlp.ner import aggregate_entities

file_path = "data/samples/legal-document-4.pdf"

text = extract_text_from_pdf(file_path)
cleaned = clean_text(text)
chunks = create_chunks(cleaned)

entities = aggregate_entities(chunks, cleaned)

print("\n--- ENTITIES ---\n")
for key, values in entities.items():
    print(f"{key}: {values}")