"""
Fastapi ve streamlit ile görüntü üzerinden hastalık tespiti sistemi

Amaç:
    - görüntüyü streamlit ile yükleriz, fastapi servisine gider, sanki bir ai avarmış gibi hastalık teşhisi yapılır

Sistem Senaryosu:
    1. kullanıcı streamlit ekranından bir görüntü yükler
    2. streamlit bu görüntüyü fastapi endpointine gönderir
    3. fastapi gelen dosyayı alır
    4. servis tarafında ml/ai sahte bir teşhis yapar
    5. sistem hastalık var yada yok sonucunu bir olasılık ile geri döner
    6. streamlit üzerinden cevap ekrana yazdırılır

Plan/program:
    1. import libraries
    2. fastapi app başlatma
    3. test amaçlı endpoint tanımla
    4. görüntü yüklemeyi kabul eden tahmin endpointi
    5. görüntü olup olmadığını kontrol et
    6. sahte ml tahmin mantığı kur
    7. hastalık durumu ve olasılık değeri json olarak döndür
    8. uvicorn ile servisi çalıştır
"""

# import libraries
from fastapi import FastAPI, File, UploadFile, HTTPException
import random

# fastapi app başlatma
app = FastAPI(
title="Görüntü Üzerinden Sahte Hastalık Tespiti Sistemi",
    description="Bu sistem, yüklenen görüntü üzerinden sahte bir hastalık tespiti yapar.",
    version="0.0.1"
)

# test amaçlı endpoint tanımla6_streamlit/main.py
@app.get("/")
def root():
    """
    api çalışıyor mu test etmek için basit bir endpoint
    """
    return {
        "message": "API çalışıyor. Görüntü yüklemek için /predict endpointini kullanın.",
        "status": "success"
    }

# görüntü yüklemeyi kabul eden tahmin endpointi
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Bu endpoint, yüklenen görüntüyü alır ve sahte bir hastalık tespiti yapar.
    """

    # görüntü olup olmadığını kontrol et
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Yüklenen dosya bir görüntü değil.")
    
    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(status_code=400, detail="Görüntü yüklenemedi veya boş.")

    # sahte ml tahmin mantığı kur
    probability = round(random.uniform(0.4, 0.99), 2) # 0.4 ile 0.99 arasında rastgele bir olasılık değeri üret 

    # eğer olasılık 0.5'ten büyükse hastalık var, değilse yok olarak kabul et
    disease_status = "Hastalık var" if probability > 0.5 else "Hastalık yok"

    return {
        "file_name": file.filename,
        "disease_status": disease_status,
        "probability": probability
    }