# Email Classifier API

API em FastAPI para classificação automática de emails em **Produtivo** ou **Improdutivo**, com geração de resposta automática.  
Suporta entrada de texto e upload de arquivos `.txt` e `.pdf`.

---

## Pré-requisitos

- Python 3.9 ou superior
- pip atualizado
- Git instalado

---

## Frontend:
https://github.com/juulioclf/autou-frontend

## Funcionalidades

- Classificação de emails usando **Zero-Shot Classification** (`facebook/bart-large-mnli` via HuggingFace Transformers).
- Suporte a textos em português e inglês com **spaCy**.
- Upload e leitura de arquivos `.txt` e `.pdf`.
- Geração de resposta automática baseada na categoria.
- Documentação interativa com Swagger UI e ReDoc.

---

## Dependências

O projeto utiliza as seguintes bibliotecas:

```txt
spacy>=3.4
pt_core_news_sm @ https://github.com/explosion/spacy-models/releases/download/pt_core_news_sm-3.6.0/pt_core_news_sm-3.6.0-py3-none-any.whl
en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.6.0/en_core_web_sm-3.6.0-py3-none-any.whl

fastapi>=0.95
uvicorn[standard]>=0.22
openai>=1.0
python-dotenv>=1.0
PyPDF2>=3.0
python-multipart>=0.0.2

transformers>=4.40
torch>=2.0
requests>=2.31
```

## Como rodar localmente

Clone o repositório:
```txt
git clone https://github.com/juulioclf/autou-backend.git
cd autou-backend
```

Atualize o pip e instale as dependências:
```txt
python -m pip install --upgrade pip
pip install -r requirements.txt
```

(Opcional) Baixe os modelos do spaCy manualmente:
```txt
python -m spacy download pt_core_news_sm
python -m spacy download en_core_web_sm
```

Suba a API localmente com Uvicorn:
```txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
