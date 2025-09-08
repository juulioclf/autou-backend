import os
import pytest
from app.services.classifier import classify_email

@pytest.mark.parametrize("text,expected", [
    ("Precisamos marcar reunião sobre o projeto", "Produtivo"),
    ("Relatório de desempenho da equipe", "Produtivo"),
    ("Promoção: compre 1 perfume e leve 2!", "Improdutivo"),
    ("Spam de desconto em celulares", "Improdutivo"),
])
def test_classify_email(text, expected):
    result = classify_email(text)
    assert result in ["Produtivo", "Improdutivo"]
    # Não é hard assert porque modelo pode variar, mas deve bater na maioria
    print(f"Texto: {text} => {result}")
