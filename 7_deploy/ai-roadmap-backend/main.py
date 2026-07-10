from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

ROADMAPS = {
    "yapay_zeka": [
        "Python Temelleri",
        "Veri Analizi",
        "Makine Öğrenmesi",
        "Model Değerlendirme",
        "Mini Projeler"
    ],
    "derin_ogrenme": [
        "Python ve NumPy",
        "Yapay Sinir Ağları",
        "CNN",
        "RNN ve LSTM",
        "Derin Öğrenme Projeleri"
    ],
    "nlp": [
        "Metin Ön İşleme",
        "Word Embedding",
        "RNN ve LSTM ile NLP",
        "Transformer",
        "RAG ve Chatbot Projeleri"
    ]
}

class RoadmapRequest(BaseModel):
    roadmap_name: str

@app.get("/")
def home():
    return {"message": "AI Roadmap API"}

@app.post("/roadmap")
def get_roadmap(data: RoadmapRequest):
    roadmap_name = data.roadmap_name.lower()
    if roadmap_name not in ROADMAPS:
        return {"error": "Geçersiz seçim"}
    return {
        "alan": roadmap_name,
        "adımlar": ROADMAPS[roadmap_name]
    }