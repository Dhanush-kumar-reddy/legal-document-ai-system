from src.ingestion.parser import extract_text_from_pdf
from src.ingestion.cleaner import clean_text
from src.processing.chunking import create_chunks

file_path = "data/samples/legal-document-5.pdf"

text = extract_text_from_pdf("temp.pdf")

cleaned = clean_text(text)

chunks_cleaned = create_chunks(cleaned)
chunks_original = create_chunks(text)

print(f"Total chunks: {len(chunks_cleaned)}\n")

for i, chunk in enumerate(chunks_cleaned[:5]):
    print(f"\n--- Chunk {i} ---\n")
    print(chunk[:300])