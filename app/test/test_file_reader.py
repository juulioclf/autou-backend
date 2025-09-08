import tempfile
from pathlib import Path
from app.utils.file_reader import read_txt, read_pdf

def test_read_txt():
    with tempfile.NamedTemporaryFile("w+", suffix=".txt", delete=False, encoding="utf-8") as tmp:
        tmp.write("Olá mundo")
        tmp.flush()
        path = Path(tmp.name)

    result = read_txt(path)
    assert "Olá mundo" in result

def test_read_pdf():
    # cria PDF temporário com PyPDF2
    from PyPDF2 import PdfWriter
    tmp_pdf = tempfile.NamedTemporaryFile("wb+", suffix=".pdf", delete=False)
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)  # página em branco
    writer.write(tmp_pdf)
    tmp_pdf.flush()
    tmp_pdf.close()
    # Deve retornar string (mesmo vazia, mas sem erro)
    result = read_pdf(tmp_pdf.name)
    assert isinstance(result, str)
