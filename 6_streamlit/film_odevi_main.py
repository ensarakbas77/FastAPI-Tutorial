"""
PROJE ADI:
Film Yorumundan Duygu Analizi API

PROJENİN AMACI:
Bu projede kullanıcıdan alınan bir film yorumunu analiz eden ve yorumun
pozitif, negatif veya nötr olduğunu tahmin eden bir FastAPI servisi geliştireceğiz.

PROJE AÇIKLAMASI:
Gerçek dünyada duygu analizi projelerinde doğal dil işleme (NLP) ve makine öğrenmesi
modelleri kullanılır. Bu mini projede ise sistemin genel çalışma mantığını anlamak için
daha basit bir yaklaşım kullanacağız.

Kullanıcı bir film yorumu gönderecek.
Backend tarafında bu yorum içindeki bazı pozitif ve negatif kelimeler kontrol edilecek.
Ardından sistem:
- duygu etiketi
- kısa açıklama
- pozitif ve negatif skor
şeklinde bir sonuç döndürecek.

Bu yapı sayesinde:
- FastAPI ile backend geliştirmeyi
- POST endpoint kullanmayı
- JSON veri alıp JSON veri döndürmeyi
- basit metin işleme mantığını
öğrenmiş olacağız.

SENARYO:
1. Kullanıcı Streamlit arayüzünden film yorumunu yazar.
2. Bu yorum FastAPI endpoint'ine gönderilir.
3. FastAPI yorumu analiz eder.
4. Sonuç olarak pozitif / negatif / nötr etiketi döner.
5. Açıklama ve skor bilgileri de eklenir.
6. Streamlit tarafı bu sonucu kullanıcıya gösterir.

PLAN / PROGRAM:
1. Gerekli kütüphaneleri içeriye aktaracağız.
2. FastAPI uygulamasını oluşturacağız.
3. Veri modeli için Pydantic sınıfı yazacağız.
4. Test endpoint'i oluşturacağız.
5. Yorum analizi endpoint'i yazacağız.
6. Pozitif ve negatif kelime listeleri tanımlayacağız.
7. Yorumu analiz edip sonuç üreteceğiz.
8. Sonucu JSON formatında döndüreceğiz.
"""

# 1. Gerekli kütüphaneleri içeriye aktaracağız.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

# 2. FastAPI uygulamasını oluşturacağız.
app = FastAPI(
    title="Film Yorumlarından Duygu Analizi"
)

# 3. Veri modeli için Pydantic sınıfı yazacağız.
class CommentRequest(BaseModel):
    comment: str


# 4. Test endpoint'i oluşturacağız.
@app.get("/")
def home():
    return {
        "message" : "API çalışıyor",
        "status": "Ok"
    }

positive_words = {
    "güzel", "harika", "mükemmel", "süper", "bayıldım", "etkileyici", "başarılı",
    "iyi", "keyifli", "eğlenceli", "duygusal", "kaliteli", "muhteşem", "sevdim",
    "beğendim", "şahane", "akıcı", "güçlü", "olağanüstü", "inanılmaz"
}

negative_words = {
    "kötü", "berbat", "sıkıcı", "rezalet", "saçma", "vasat", "zayıf",
    "başarısız", "beğenmedim", "nefret", "uzun", "boş", "gereksiz", "yavaş",
    "anlamsız", "uyduruk", "korkunç", "kötüydü", "sevmedim", "bıktım"
}


# yorum analiz fonksiyonu
def analyze_comment(comment: str):
    # metni küçük harfe çeviriyoruz
    comment = comment.lower()

    # noktalama işaretlerini temizliyoruz
    comment = re.sub(r"[^\wçğıöşü\s]", " ", comment)

    # metni kelimelere ayırıyoruz
    tokens = comment.split()

    # pozitif ve negatif skorları hesaplıyoruz
    positive_score = sum(1 for token in tokens if token in positive_words)
    negative_score = sum(1 for token in tokens if token in negative_words)

    total_hits = positive_score + negative_score

    if total_hits == 0:
        sentiment = "Nötr"
        explanation = "Yorum içinde belirgin pozitif veya negatif ifade bulunamadı."
        return sentiment, explanation, positive_score, negative_score

    if positive_score > negative_score:
        sentiment = "Pozitif"
        explanation = "Yorumda pozitif ifadeler daha baskın görünüyor."
    elif negative_score > positive_score:
        sentiment = "Negatif"
        explanation = "Yorumda negatif ifadeler daha baskın görünüyor."
    else:
        sentiment = "Nötr"
        explanation = "Pozitif ve negatif ifadeler dengeli görünüyor."

    return sentiment, explanation, positive_score, negative_score

# 5. Yorum analizi endpoint'i yazacağız.
@app.post("/analyze")
def analyze_sentiment(data: CommentRequest):

    comment = data.comment.strip()

    if not comment:
        return {
            "success": "False",
            "message": " Yorum alanı boş olamaz."
        }
    
    sentiment, explanation, positive_score, negative_score = analyze_comment(comment)

    return {
        "success": "True",
        "comment": comment,
        "sentiment": sentiment,
        "explanation": explanation,
        "positive_score": positive_score,
        "negative_score": negative_score
    }