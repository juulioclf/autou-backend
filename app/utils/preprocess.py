import re
import spacy

# Tenta carregar modelo em português, se não, em inglês
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        raise RuntimeError(
            "Nenhum modelo spaCy disponível. Execute:\n"
            "  python -m spacy download pt_core_news_sm\n"
            "ou\n"
            "  python -m spacy download en_core_web_sm\n"
        )

def clean_text(text: str) -> str:
    """Remove caracteres especiais e espaços extras, normalizando para lowercase."""
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text

def preprocess(text: str) -> str:
    """
    Pré-processa texto:
      - limpeza
      - tokenização
      - remoção de stopwords/pontuação
      - lematização
    Retorna string com tokens lematizados separados por espaço.
    """
    text = clean_text(text)
    doc = nlp(text)
    tokens = [
        token.lemma_ for token in doc
        if not (token.is_stop or token.is_punct or token.is_space)
    ]
    return " ".join(tokens)
