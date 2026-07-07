"""
Amaç:
    - fastapi ile veritabanına veri yazma ve okuma
    - daha önce fonksiyonlar ile tanımlanan veritabanı işlemlerini API katmanına bağlamak
    - kullanıcıdan gelen verileri kaydetme ve kayıtlı verileri listeleme endpoint üzerinde yapalım
"""

import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

from crud import veritabani_baglantisi, tablo_olustur, mesaj_ekle, tum_mesajlari_listele, mesaj_sil

app = FastAPI()

# api ye post isteği ile gelecek olan veriyi tanımlama
class MesajModel(BaseModel):
    kullanici_mesaji: str
    bot_cevabi: str

# veritabanı oluşturma fonksiyonunu çağırıyoruz
veritabani_baglantisi()  

# tablo oluşturma fonksiyonunu çağırıyoruz
tablo_olustur()  

# FASTAPI ile veri ekleme ve silme endpointlerini tanımlama
@app.post("/mesaj-ekle")
def mesaj_ekle_endpoint(veri: MesajModel):

    # gelen veriyi veritabanına ekleme
    mesaj_ekle(veri.kullanici_mesaji, veri.bot_cevabi)

    return {
        "durum": "Başarılı",
        "mesaj": "Kayıt db ye başarıyla eklendi.",
        "eklenen_veri": {
            "kullanici_mesaji": veri.kullanici_mesaji,
            "bot_cevabi": veri.bot_cevabi
        }
    }

@app.post("/mesaj-sil")
def mesaj_sil_endpoint(mesaj_id: int):
    # gelen id ile veritabanından kaydı silme
    mesaj_sil(mesaj_id)

    return {
        "durum": "Başarılı",
        "mesaj": f"{mesaj_id} id'li kayıt db den başarıyla silindi."
    }


# get endpoint ile tüm kayıtları listeleme
@app.get("/mesajlar")
def mesajlari_listele_endpoint():
    kayitlar = tum_mesajlari_listele()
    
    sonuc = []
    for kayit in kayitlar:
        sonuc.append({
            "id": kayit[0],
            "kullanici_mesaji": kayit[1],
            "bot_cevabi": kayit[2]
        })

    return {
        "durum": "Başarılı",
        "toplam_kayit_sayisi": len(sonuc),
        "kayitlar": sonuc
    }