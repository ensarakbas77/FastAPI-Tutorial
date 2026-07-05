"""
Amaç: 
    - Sanki arka planda dil modeli varmış gibi çalışan bir chatbot servisi geliştireceğiz.
    - kullanıcıdan gelen mesaj alınır, mesaj işliyormuş gibi bekleme simülasyonu yapılır, uygun bir cevap üretilir, gelen mesaj kayıt altına alınır
"""

import asyncio
from fastapi import FastAPI
from pydantic import BaseModel

# 1. fastapi uygulamasını ve veri modelini oluşturma
app = FastAPI()

class MesajIstek(BaseModel):
    mesaj: str

# sanki bir dil modeli gibi cevap üreten bir asenkron fonksiyon
async def sahte_dil_modeli_cevap_uret(mesaj: str) -> str:
    await asyncio.sleep(2)  # 2 saniye bekleme simülasyonu
    
    # basit cevap modeli, llm varmış gibi yapmak
    kullanici_mesaji = mesaj.lower()
    if "merhaba" in kullanici_mesaji:
        return "Merhaba! Size nasıl yardımcı olabilirim?"
    elif "hava" in kullanici_mesaji:
        return "Bugün hava durumunu değerlendirmek için elimde gerçek veri yok."
    else:
        return f"mesajınızı aldım: '{kullanici_mesaji}'"
    
# mesaj ve cevabı sanki veritabanına kaydediyormuş gibi simüle eden asenkron fonksiyon
async def mesaj_kaydet(kullanici_mesaji: str, model_cevabi: str):

    await asyncio.sleep(1)  # 1 saniye bekleme simülasyonu

    # normalde burada veri tabanına insert işlemi yapılmalı

    print(f"Mesaj kaydedildi: '{kullanici_mesaji}' | Cevap kaydedildi: '{model_cevabi}'")
    print("Kayıt işlemi tamamlandı.")

# 2. chat endpoint'i oluşturma
@app.post("/chat")
async def chat_yap(istek: MesajIstek):

    cevap = await sahte_dil_modeli_cevap_uret(istek.mesaj)  # llm cevap üretir
    await mesaj_kaydet(istek.mesaj, cevap)    # mesaj ve cevabı kaydeder

    return {
        "durum": "başarılı",
        "kullanici_mesaji": istek.mesaj,
        "model_cevabi": cevap
    }

