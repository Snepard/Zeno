import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path: str, max_chars: int = 50000) -> str:
    """Extracts raw text from a PDF securely, chunking appropriately for Long-form video."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n\n"
        doc.close()
        return text[:max_chars]
    except Exception as e:
        logger.error(f"Failed to extract PDF: {e}")
        return ""
