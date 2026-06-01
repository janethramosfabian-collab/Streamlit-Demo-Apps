import pdfplumber
from typing import Optional

def extract_text_from_pdf(file) -> str:
    """Extrae texto de un archivo PDF usando pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error al extraer texto del PDF: {e}")
        return ""
    return text.strip()
