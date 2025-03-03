from fastapi import FastAPI, UploadFile, File, Form
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
import ollama
import numpy as np
import shutil
import os

# Настройки
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "resume_chunks"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
MODEL_NAME = "mistral"
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Инициализация
app = FastAPI()
client = QdrantClient(QDRANT_URL)
model = SentenceTransformer(EMBEDDING_MODEL)

# Создание коллекции в Qdrant
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
)

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text.split(". ")  # Разбиваем на предложения

def embed_text(chunks):
    return model.encode(chunks, convert_to_numpy=True)

def save_to_qdrant(chunks, vectors):
    payload = [{"text": chunk} for chunk in chunks]
    points = [
        models.PointStruct(id=i, vector=vec.tolist(), payload=payload[i])
        for i, vec in enumerate(vectors)
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    chunks = extract_text(file_path)
    vectors = embed_text(chunks)
    save_to_qdrant(chunks, vectors)
    
    return {"message": "Resume indexed successfully!"}

@app.get("/query")
async def query_resume(query: str):
    query_vector = model.encode([query])[0].tolist()
    search_result = client.search(
        collection_name=COLLECTION_NAME, query_vector=query_vector, limit=3
    )
    context = "\n".join([hit.payload["text"] for hit in search_result])
    prompt = f"Контекст: {context}\n\nВопрос: {query}\nОтвет:"
    response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
    return {"answer": response["message"]["content"]}
