from app.utils.preprocess import preprocess, clean_text

def test_clean_text():
    text = "   Olá,   Mundo!!!   "
    result = clean_text(text)
    assert result == "olá, mundo!!!"

def test_preprocess_basic():
    text = "Os gatos estão correndo rapidamente!"
    result = preprocess(text)
    # Deve conter versões lematizadas
    assert "gato" in result
    assert "correr" in result
    # Stopwords removidas
    assert "os" not in result
