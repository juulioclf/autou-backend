import pytest
from app.services.responder import generate_response

def test_generate_response_produtivo():
    resp = generate_response("Produtivo")
    assert "Obrigado" in resp
    assert resp.endswith("em breve.")

def test_generate_response_improdutivo():
    resp = generate_response("Improdutivo")
    assert "Agradecemos" in resp
    assert resp.endswith("reconhecimento.")

def test_generate_response_invalid_category():
    with pytest.raises(ValueError):
        generate_response("Outro")
