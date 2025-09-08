from pathlib import Path
from typing import Union
import PyPDF2

def read_txt(file_path: Union[str, Path]) -> str:
    """Lê conteúdo de arquivo .txt"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(file_path: Union[str, Path]) -> str:
    """Extrai texto de arquivo .pdf"""
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text
