"""
Amaç: 
    - async fonksiyonlarını başka bir .py dosyasından (client) test et
    - request kütüphanesi kullanma
    - swagger yerine python içinden test etmeyi öğreneceğiz
"""

import asyncio
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# POST isteği için input verisinin tanımlanması
class MesajModel(BaseModel):
    """
    Mesaj modelini tanımlar.
    - mesaj: Gönderilecek mesaj (str)
    """
    mesaj: str

# GET Endpointi
@app.get("/durum")
async def durum():

    await asyncio.sleep(2)

    return {
        "durum": "başarılı",
        "mesaj": "get endpointi çalıştı"  
    }

# POST Endpointi
@app.post("/mesaj")
async def mesaj_al(veri: MesajModel):

    await asyncio.sleep(2)

    return {
        "durum": "başarılı",
        "gelen_veri": veri.mesaj,
        "cevap": "post mesajı başarıyla alındı"
    } 