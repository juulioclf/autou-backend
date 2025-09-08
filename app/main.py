from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import tempfile

from app.utils.file_reader import read_txt, read_pdf
from app.utils.preprocess import preprocess
from app.services.classifier import classify_email
from app.services.responder import generate_response

app = FastAPI(
    title="Email Classifier API",
    description="Classificação de emails em Produtivo/Improdutivo + resposta automática",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailText(BaseModel):
    content: str

@app.post("/classify")
async def classify_email_text(payload: EmailText):
    try:
        if not payload.content.strip():
            raise HTTPException(status_code=400, detail="Texto vazio.")
        
        preprocessed = preprocess(payload.content)
        category = classify_email(preprocessed)
        response = generate_response(category)

        return {
            "category": category,
            "reply": response,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-email/")
async def process_email(file: UploadFile = File(...)):
    try:
        suffix = Path(file.filename).suffix.lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = Path(tmp.name)

        if suffix == ".txt":
            raw_text = read_txt(tmp_path)
        elif suffix == ".pdf":
            raw_text = read_pdf(tmp_path)
        else:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado. Use .txt ou .pdf")

        preprocessed = preprocess(raw_text)
        category = classify_email(preprocessed)
        response = generate_response(category)

        return {
            "arquivo": file.filename,
            "categoria": category,
            "resposta": response,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
