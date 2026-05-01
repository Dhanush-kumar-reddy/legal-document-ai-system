from src.ingestion.parser import extract_text_from_pdf
from src.ingestion.cleaner import clean_text

file_path = "data/samples/legal-document-1.pdf"

raw_text = extract_text_from_pdf(file_path)
cleaned_text = clean_text(raw_text)

print("\n--- RAW TEXT ---\n")
print(raw_text[:2000])
print(raw_text[2000:3000])

print("\n--- CLEANED TEXT ---\n")
print(cleaned_text[:2000])

print("\n--- SAMPLE MIDDLE ---\n")
print(cleaned_text[2000:3000])

