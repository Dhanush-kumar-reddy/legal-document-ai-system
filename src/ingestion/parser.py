import fitz  # PyMuPDF
from src.utils.logger import get_logger
logger = get_logger()

def extract_text_from_pdf(file_path: str) -> str:
    try:
        doc = fitz.open(file_path)
        text = ""

        for page_num, page in enumerate(doc):
            page_text = page.get_text("text")

            if not page_text.strip():
                logger.warning(f"Empty page detected: {page_num}")

            text += page_text + "\n"

        logger.info("PDF text extraction completed")
        return text

    except Exception as e:
        logger.error(f"Error parsing PDF: {e}")
        raise