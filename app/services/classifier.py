import os
import requests
from transformers import pipeline

# Lê configuração de ambiente
CLASSIFIER_MODE = os.getenv("CLASSIFIER_MODE", "local")  # "local" ou "api"
HF_MODEL = os.getenv("HF_MODEL", "distilbert-base-uncased-finetuned-sst-2-english")
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HF_TOKEN = os.getenv("HF_TOKEN")  # só precisa se usar modo "api"

classifier = None

def _load_local_model():
    """Carrega pipeline Hugging Face localmente."""
    global classifier
    if classifier is None:
        classifier = pipeline("text-classification", model=HF_MODEL)
    return classifier

def classify_email(text: str) -> str:
    """
    Classifica email em 'Produtivo' ou 'Improdutivo'.
    Usa Hugging Face local (default) ou Inference API.
    """
    if CLASSIFIER_MODE == "api":
        if not HF_TOKEN:
            raise RuntimeError("HF_TOKEN não definido para modo API")

        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        response = requests.post(HF_API_URL, headers=headers, json={"inputs": text})
        response.raise_for_status()
        result = response.json()[0][0]  # top resultado
        label = result["label"]

    else:
        clf = _load_local_model()
        result = clf(text)[0]
        label = result["label"]

    # Mapeamento simples de saída para Produtivo/Improdutivo
    if "POSITIVE" in label.upper():
        return "Produtivo"
    else:
        return "Improdutivo"
