import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
import ollama

# Настройки
PDF_PATH = "./src/app/rags/resume.pdf"
COLLECTION_NAME = "resume_chunks"
QDRANT_URL = "http://localhost:6333"
MODEL_NAME = "mistral"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# 1. Извлекаем текст из PDF
def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text.split(". ")  # Разбиваем на предложения

# 2. Векторизация текста
model = SentenceTransformer(EMBEDDING_MODEL)
def embed_text(chunks):
    return model.encode(chunks, convert_to_numpy=True)

# 3. Сохранение в Qdrant
client = QdrantClient(QDRANT_URL)
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
)

def save_to_qdrant(chunks, vectors):
    payload = [{"text": chunk} for chunk in chunks]
    points = [
        models.PointStruct(id=i, vector=vec.tolist(), payload=payload[i])
        for i, vec in enumerate(vectors)
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)

chunks = extract_text(PDF_PATH)
vectors = embed_text(chunks)
save_to_qdrant(chunks, vectors)
print("Resume indexed in Qdrant!")

# 4. Функция поиска и ответа
def query_mistral(query):
    query_vector = model.encode([query])[0].tolist()
    search_result = client.search(
        collection_name=COLLECTION_NAME, query_vector=query_vector, limit=3
    )
    context = "\n".join([hit.payload["text"] for hit in search_result])
    prompt = f"Контекст: {context}\n\nВопрос: {query}\nОтвет:"
    response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

# 5. Тестируем запрос
query = "Какой у меня опыт работы?"
answer = query_mistral(query)
print("Ответ:", answer)
