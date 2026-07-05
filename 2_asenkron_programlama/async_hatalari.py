"""
Asenkron Programlamada Sık Yapılan Hatalar

Asenkron programlama sadece fonksiyonun başına async yazmak değildir.
Kodun gerçekten asenkron çalışabilmesi için bekleme gerektiren işlemlerde await doğru kullanılmalıdır.

Yanlış yerde async kullanmak, blocking yani programı durduran kodlar yazmak
veya await edilmesi gereken işlemleri await etmemek asenkron yapının faydasını azaltır.

Örneğin time.sleep() kullanmak programı bloklar.
Asenkron kodlarda bunun yerine await asyncio.sleep() tercih edilmelidir.

Amaç, bir işlem beklerken programın tamamen durmasını engellemek
ve bu sırada başka işlemlerin çalışmasına izin vermektir.
"""

import time
import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "mesaj": "async hataları dersine hoş geldiniz!"
    }

def func1():
    return "deneme"

# 1. blocking kod
@app.get("/blocking-ornek")
async def blocking_ornek():
    
    # hatalı kullanım: bu yapılar senkron çalışır ve işlemi durdurur.
    time.sleep(5)  # senkron çalışır.
    func1()  # senkron çalışır.

    return {
        "durum": "hata",
        "mesaj": "bu endpoint async yazıldı ama blocking kodlar içeriyor. Bu yüzden asenkron çalışmıyor."
    }

async def func2():
    return "async deneme"

# 2. doğru bekleme yöntemi ile hatalı yöntemi karşılaştırma
@app.get("/dogru-bekleme-ornek")
async def dogru_bekleme_ornek():

    # doğru kullanım
    await asyncio.sleep(5)  # asenkron çalışır.
    await func2()  # asenkron çalışır.

    return {
        "durum": "başarılı",
        "mesaj": "bu endpoint async yazıldı ve doğru bekleme yöntemleri kullanıldı. Bu yüzden asenkron çalışıyor."
    }

async def veri_hazirla():
    await asyncio.sleep(2)
    return "veri hazırlandı"

# 3. await kullanımının neden gerekli olduğunu gösteren örnek
@app.get("/await-kullanimi-ornek")
async def await_kullanimi_ornek():

    veri = await veri_hazirla()

    return {
        "durum": "başarılı",
        "mesaj": f"await kullanımı ile veri hazırlandı: {veri}"
    }