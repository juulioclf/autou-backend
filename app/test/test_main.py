# app/test/test_main.py
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient
import app.main as main

client = TestClient(main.app)


def _make_tmp_txt(content: str) -> Path:
    with tempfile.NamedTemporaryFile("w+", suffix=".txt", delete=False, encoding="utf-8") as tmp:
        tmp.write(content)
        tmp.flush()
        return Path(tmp.name)


def _make_tmp_pdf() -> Path:
    from PyPDF2 import PdfWriter
    f = tempfile.NamedTemporaryFile("wb+", suffix=".pdf", delete=False)
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)  # página em branco
    writer.write(f)
    f.flush()
    f.close()
    return Path(f.name)


def test_process_email_txt_produtivo(monkeypatch):
    monkeypatch.setattr(main, "preprocess", lambda txt: txt)
    monkeypatch.setattr(main, "classify_email", lambda txt: "Produtivo")

    path = _make_tmp_txt("Precisamos marcar reunião sobre o projeto amanhã.")
    with open(path, "rb") as f:
        resp = client.post(
            "/process-email/",
            files={"file": ("email.txt", f, "text/plain")},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["categoria"] == "Produtivo"
    assert "Obrigado" in data["resposta"]


def test_process_email_txt_improdutivo(monkeypatch):
    monkeypatch.setattr(main, "preprocess", lambda txt: txt)
    monkeypatch.setattr(main, "classify_email", lambda txt: "Improdutivo")

    path = _make_tmp_txt("Promoção imperdível: compre um e leve dois!")
    with open(path, "rb") as f:
        resp = client.post(
            "/process-email/",
            files={"file": ("spam.txt", f, "text/plain")},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["categoria"] == "Improdutivo"
    assert "Agradecemos" in data["resposta"]


def test_process_email_pdf(monkeypatch):
    monkeypatch.setattr(main, "preprocess", lambda txt: txt)
    monkeypatch.setattr(main, "classify_email", lambda txt: "Produtivo")

    path = _make_tmp_pdf()
    with open(path, "rb") as f:
        resp = client.post(
            "/process-email/",
            files={"file": ("doc.pdf", f, "application/pdf")},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["categoria"] == "Produtivo"
    assert "resposta" in data


def test_invalid_file_format_returns_400():
    jpg_path = Path(tempfile.NamedTemporaryFile("wb+", suffix=".jpg", delete=False).name)
    with open(jpg_path, "rb") as f:
        resp = client.post(
            "/process-email/",
            files={"file": ("image.jpg", f, "image/jpeg")},
        )

    assert resp.status_code == 400
