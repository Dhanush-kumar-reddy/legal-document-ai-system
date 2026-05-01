import re

def split_by_sections(text: str):
    # Split on numbered sections like "1. ", "2. "
    sections = re.split(r"\n(?=\d+\.\s)", text)

    return [sec.strip() for sec in sections if sec.strip()]

def split_large_chunks(text, max_words=200, overlap=50):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + max_words
        chunk = words[start:end]
        chunks.append(" ".join(chunk))

        start += (max_words - overlap)

    return chunks

def create_chunks(text, max_words=400, overlap=80, min_words=50):
    sections = split_by_sections(text)

    final_chunks = []
    buffer = ""

    for sec in sections:
        words = (buffer + " " + sec).split()

        # If combined section is still small → keep merging
        if len(words) < max_words:
            buffer += " " + sec
        else:
            # Flush buffer
            if buffer:
                final_chunks.append(buffer.strip())
            buffer = sec

    # Add remaining buffer
    if buffer:
        final_chunks.append(buffer.strip())

    # Now split large chunks if needed
    refined_chunks = []
    for chunk in final_chunks:
        if len(chunk.split()) <= max_words:
            refined_chunks.append(chunk)
        else:
            refined_chunks.extend(split_large_chunks(chunk, max_words, overlap))

    # Remove very small chunks
    refined_chunks = [c for c in refined_chunks if len(c.split()) >= min_words]

    return refined_chunks