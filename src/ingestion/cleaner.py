import re
from src.utils.logger import get_logger

logger = get_logger()


def normalize_dots(text: str) -> str:
    # Replace sequences of dots with a placeholder
    text = re.sub(r"\.{2,}", " ", text)
    return text

def preserve_numbered_sections(text: str) -> str:
    # Ensure section numbers stay with headers
    text = re.sub(r"\n\s*(\d+)\.\s*\n", r"\n\n\1. ", text)
    return text

def fix_broken_punctuation(text: str) -> str:
    # Fix cases like "UNDER \n :"
    text = re.sub(r"\n\s*:\s*", ":", text)
    return text

def fix_broken_punctuation(text: str) -> str:
    # Fix cases like "UNDER \n :"
    text = re.sub(r"\n\s*:\s*", ":", text)
    return text

def remove_headers_footers(text: str) -> str:
    lines = text.split("\n")

    cleaned_lines = []
    for line in lines:
        # Remove page numbers like "Page 1"
        if re.match(r"^\s*Page\s+\d+", line):
            continue

        # Remove very short noisy lines
        if len(line.strip()) < 3:
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

def fix_line_breaks(text: str) -> str:
    # Join broken lines within sentences
    text = re.sub(r"\n(?=[a-z,])", " ", text)

    # Keep numbered / section structure
    text = re.sub(r"\n(?=\d+\.)", "\n\n", text)

    # Keep bullet structure (A., B., etc.)
    text = re.sub(r"\n(?=[A-Z]\.)", "\n", text)

    return text

def normalize_whitespace(text: str) -> str:
    # Replace multiple spaces with single space
    text = re.sub(r"[ \t]+", " ", text)

    # Preserve paragraph breaks
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

def remove_special_characters(text: str) -> str:
    # Keep legal symbols like ₹, $, %, etc.
    text = re.sub(r"[^\w\s₹$%.,;:()\-\/\"']", "", text)
    return text

def fix_broken_words(text: str) -> str:
    # Fix words broken by newline
    text = re.sub(r"([a-zA-Z])\n([a-zA-Z])", r"\1\2", text)
    return text

def fix_split_punctuation(text: str) -> str:
    text = re.sub(r"\n([,.;])", r"\1", text)
    return text

def enhance_section_spacing(text: str) -> str:
    # Add spacing before ALL CAPS headings
    text = re.sub(r"\n([A-Z][A-Z\s]{5,})", r"\n\n\1\n", text)
    return text

def clean_section_spacing(text: str) -> str:
    # Remove extra spaces before/after headers
    text = re.sub(r"\n\s+\n", "\n\n", text)
    return text

def fix_missing_newline_after_colon(text: str) -> str:
    # Ensure newline after section intro like "UNDER:"
    text = re.sub(r"(:)(\d+\.)", r"\1\n\n\2", text)
    return text

def clean_text(text: str) -> str:
    try:
        text = normalize_dots(text)
        text = preserve_numbered_sections(text)
        text = remove_headers_footers(text)
        text = fix_broken_words(text)       
        text = fix_line_breaks(text)
        text = fix_split_punctuation(text)      
        text = enhance_section_spacing(text)
        text = fix_broken_punctuation(text)
        text = fix_missing_newline_after_colon(text)
        text = clean_section_spacing(text)
        text = normalize_whitespace(text)
        text = remove_special_characters(text)
        
        logger.info("Text cleaning completed")
        return text

    except Exception as e:
        logger.error(f"Cleaning error: {e}")
        raise