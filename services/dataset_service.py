# services/dataset_service.py

import base64
import os
from PyPDF2 import PdfReader
import docx
from core.settings import settings_data


DATASET_FILE = "dataset_cache.txt"


def save_dataset_text(text: str):
    """Save extracted text into a cache file."""
    clean = text.encode("utf-8", "ignore").decode()
    with open(DATASET_FILE, "w", encoding="utf-8") as f:
        f.write(clean)
    settings_data["dataset_exists"] = True


def get_dataset_text():
    """Load dataset text from cache."""
    if not os.path.exists(DATASET_FILE):
        return None
    with open(DATASET_FILE, "r", encoding="utf-8") as f:
        return f.read()


def extract_pdf(pdf_bytes: bytes) -> str:
    """Extract text from PDF."""
    try:
        reader = PdfReader(pdf_bytes)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        return full_text
    except Exception as e:
        return f"PDF extract error: {str(e)}"


def extract_docx(doc_bytes: bytes) -> str:
    """Extract text from DOCX."""
    try:
        temp = "temp_docx.docx"
        with open(temp, "wb") as f:
            f.write(doc_bytes)

        doc = docx.Document(temp)
        text = "\n".join([p.text for p in doc.paragraphs])

        os.remove(temp)
        return text

    except Exception as e:
        return f"DOCX extract error: {str(e)}"


def process_dataset(filename: str, encoded_data: str):
    """Extract & save dataset depending on file type."""
    raw = base64.b64decode(encoded_data)

    if filename.endswith(".pdf"):
        text = extract_pdf(raw)

    elif filename.endswith(".docx"):
        text = extract_docx(raw)

    else:
        return {"error": "Invalid file format"}

    save_dataset_text(text)
    return {"status": "ok", "length": len(text)}
