import os
from transformers import pipeline

# Configuração de ambiente
classifier = None

# Categorias de classificação
CATEGORIES = ["Produtivo", "Improdutivo"]

def _load_local_model():
    global classifier
    if classifier is None:
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    return classifier

def classify_email(text: str) -> str:
    """
    Classifica email em 'Produtivo' ou 'Improdutivo' usando zero-shot classification.
    """
    clf = _load_local_model()
    result = clf(text, candidate_labels=CATEGORIES)

    category = result["labels"][0]
    return category
