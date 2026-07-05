"""
- fastapi ile io bound işlemleri simülasyonu:
- io bound: dosya okuma, dış api bekleme, veritabanı yazma veya ağ üzerinden veri gönderme
- Örneğimiz: pdf dosyasını işleyip vektör veritabanına kaydediyormuşuz gibi yapacağız.
"""

from fastapi import FastAPI
import asyncio
from pydantic import BaseModel

app = FastAPI()

# pdf bilgisini temsil eden veri modeli
class PDFVerisi(BaseModel):
    dosya_adi: str

# 1. fastapi ile async endpoint
async def pdf_isle(dosya_adi: str):
    print(f"{dosya_adi} dosyası işleniyor...")

    # pdf okuma
    await asyncio.sleep(2) 

    print(f"{dosya_adi} dosyası okundu, vektör veritabanına kaydediliyor...")

    # embedding hazırlama süreci
    await asyncio.sleep(2)

    print(f"{dosya_adi} dosyası vektör veritabanına kayıt başladı.")

    # vektör veritabanına kaydetme
    await asyncio.sleep(2)

    print(f"{dosya_adi} dosyası vektör veritabanına kaydedildi.")

# endpoint
@app.post("/pdf_isle")
async def pdf_isle_endpoint(pdf_verisi: PDFVerisi):

    await pdf_isle(pdf_verisi.dosya_adi)
    return {
        "durum": "başarılı",
        "mesaj": f"{pdf_verisi.dosya_adi} dosyası başarıyla işlendi ve vektör veritabanına kaydedildi."
    }

# aynı anda birden fazla isteğin gelebileceğini simüle etmek için birden fazla endpoint çağrısı yapabiliriz.

@app.get("/iki-pdf-isle")
async def iki_pdf_isle():

    await asyncio.gather(
        pdf_isle("dosya1.pdf"),
        pdf_isle("dosya2.pdf")
    )

    return {
        "durum": "başarılı",
        "mesaj": "dosya1.pdf ve dosya2.pdf dosyaları başarıyla işlendi ve vektör veritabanına kaydedildi."
    }