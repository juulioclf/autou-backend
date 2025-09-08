import os
from transformers import pipeline

# Configuração de ambiente
CLASSIFIER_MODE = os.getenv("CLASSIFIER_MODE", "local")  # "local" ou "api"
HF_MODEL = os.getenv("HF_MODEL", "facebook/bart-large-mnli")  # zero-shot model
classifier = None

# Categorias de classificação
CATEGORIES = ["Produtivo", "Improdutivo"]

def _load_local_model():
    global classifier
    if classifier is None:
        classifier = pipeline("zero-shot-classification", model=HF_MODEL)
    return classifier

def classify_email(text: str) -> str:
    """
    Classifica email em 'Produtivo' ou 'Improdutivo' usando zero-shot classification.
    """
    clf = _load_local_model()
    result = clf(text, candidate_labels=CATEGORIES)

    category = result["labels"][0]
    return category
