"""
Proje:
    - sanki elimizde basit bir yapay zeka modeli varmış gibi düşünelim
    - yapay zeka modeli: kullanıcı son 3 güne ait hava durumu değerlerini sisteme gönderir, sistem de ortalama sıcaklı hesaplar ve return eder.

Kullanılacak Yapılar:
    1. fastapi uygulama nesnesi oluştur
    2. get endpointi tanımla
    3. post endpointi tanımla
    4. json body ile veri alma
    5. pydantic model kullanma
    6. response yapısı oluşturma
    7. hata kontrolü yapma
    8. status code kullanma

Senaryo:
    1. kullanıcı son 3 günün sıcaklık değerlerini gönderecek
    2. sistem bu değerlerin ortalamasını alır
    3. ortalama değere göre basit yorum döndürülür

Örnek veri:
    - gelen veri:
        {
            "gun1": 20,
            "gun2": 24,
            "gun3": 22,
        } 
    - dönen cevap:
        {
            "durum": "basarili",
            "ortalama_sicaklik": 22
            "tahmin": "hava dengeli görünüyor"
        }

"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class TemperatureData(BaseModel):
    gun1: float
    gun2: float
    gun3: float

# ana karşılama endpointi
@app.get("/")
def home():
    """
    Ana sayfa endpointi
    Proje hakkında bilgi döndürür.
    """
    return {
        "mesaj" : "Hava durumu tahmin servisine hoşgeldiniz.",
        "aciklama": "Lütfen son 3 güne ait sıcaklık değerlerini gönderin."
    }

# post endpointi ile son 3 günün hava durumu tahmin verisini alıyoruz
@app.post("/hava-tahmin", status_code = status.HTTP_201_CREATED)
def hava_tahmin(data: TemperatureData):
    """
    Kullanıcıdan gelen son 3 günün sıcaklık değerlerini alır ve ortalama sıcaklığı hesaplar.
    """

    for sicaklik in [data.gun1, data.gun2, data.gun3]:
        if sicaklik < -50 or sicaklik > 60:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sıcaklık değerleri -50 ile 60 arasında olmalıdır."
            ) 
    
    ortalama = (data.gun1 + data.gun2 + data.gun3) / 3

    if ortalama < 10:
        tahmin = "Hava soğuk görünüyor."
    elif ortalama < 25:
        tahmin = "Hava dengeli görünüyor."
    else:
        tahmin = "Hava sıcak görünüyor."

    return {
        "durum": "basarili",
        "girilen_veriler" : {
            "gun1": data.gun1,
            "gun2": data.gun2,
            "gun3": data.gun3
        },
        "ortalama_sicaklik": ortalama,
        "tahmin": tahmin
    }