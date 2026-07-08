"""
TALİMATLAR:
1. fastapi, HTTPException ve logging kütüphanelerini projeye ekleyiniz.
2. app.log isimli harici bir log dosyasına yazacak şekilde logging ayarını yapınız.
3. Bir FastAPI uygulaması oluşturunuz.
4. /calculate isimli bir GET endpointi tanımlayınız.
5. Bu endpoint içinde username ve number isminde iki parametre alınız.
6. Endpoint çağrıldığında gelen username ve number bilgisini log dosyasına kaydediniz.
7. Eğer username 3 karakterden kısa ise hata logu yazınız ve HTTPException ile 400 hatası döndürünüz.
8. Eğer number negatif ise hata logu yazınız ve HTTPException ile 400 hatası döndürünüz.
9. Eğer number değeri 0 ise warning seviyesinde log yazınız.
10. number değerini 2 ile çarpıp result isminde bir sonuç üretiniz.
11. İşlem başarılıysa info seviyesinde başarılı işlem logu yazınız.
12. Sonuç olarak username, number ve result bilgilerini JSON formatında döndürünüz.
13. Endpointi Swagger üzerinden test ediniz.
14. app.log dosyasını açarak log kayıtlarının oluştuğunu kontrol ediniz.
"""

# 1. fastapi, HTTPException ve logging kütüphanelerini projeye ekleyiniz.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

# 2. app.log isimli harici bir log dosyasına yazacak şekilde logging ayarını yapınız.
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(levelname)s | %(asctime)s | %(message)s",
    encoding="utf-8"
)

# 3. Bir FastAPI uygulaması oluşturunuz.
app = FastAPI(
    title="Merhaba FastAPI!", 
    description="FastAPI açıklaması"
)


# 4. /calculate isimli bir GET endpointi tanımlayınız.
# 5. Bu endpoint içinde username ve number isminde iki parametre alınız.
@app.get("/calculate")
async def calculate_endpoint(username: str, number: int):

    # 6. Endpoint çağrıldığında gelen username ve number bilgisini log dosyasına kaydediniz.
    logging.info(f"/calculate endpointi çağrıldı, username = {username}, number = {number}")

    # 7. Eğer username 3 karakterden kısa ise hata logu yazınız ve HTTPException ile 400 hatası döndürünüz.
    if len(username) < 3:
        logging.error(f"Kullanıcı adı 3 harften kısa gönderildi, username = {username}")
        raise HTTPException(status_code=400, detail="Kullanıcı adı en az 3 karakter olmalıdır")
    
    # 8. Eğer number negatif ise hata logu yazınız ve HTTPException ile 400 hatası döndürünüz.
    if number < 0:
        logging.error(f"Sayı negatif girildi, number = {number}")
        raise HTTPException(
            status_code=400,
            detail="Sayı negatif olamaz"
        )
    
    # 9. Eğer number değeri 0 ise warning seviyesinde log yazınız.
    if number == 0:
        logging.warning(f"Sayı değeri 0 girildi, number = {number}")

    # 10. number değerini 2 ile çarpıp result isminde bir sonuç üretiniz.
    result = number * 2

    # 11. İşlem başarılıysa info seviyesinde başarılı işlem logu yazınız.
    logging.info(f"İşlem başarılı. username={username}, result={result}")

    # 12. Sonuç olarak username, number ve result bilgilerini JSON formatında döndürünüz.
    return {
        "status": "Başarılı",
        "username": username,
        "number": number,
        "result": result  
    }

# 13. Endpointi Swagger üzerinden test ediniz. --> uvicorn logging_odev:app --reload --port 7001 --> http://127.0.0.1:7001/docs
# 14. app.log dosyasını açarak log kayıtlarının oluştuğunu kontrol ediniz.

"""
app.log

INFO | 2026-07-08 10:36:14,851 | /calculate endpointi çağrıldı, username = ensar, number = 10
INFO | 2026-07-08 10:36:14,851 | İşlem başarılı. username=ensar, result=20
INFO | 2026-07-08 10:36:25,984 | /calculate endpointi çağrıldı, username = en, number = 10
ERROR | 2026-07-08 10:36:25,985 | Kullanıcı adı 3 harften kısa gönderildi, username = en
INFO | 2026-07-08 10:36:34,944 | /calculate endpointi çağrıldı, username = ensar, number = -10
ERROR | 2026-07-08 10:36:34,944 | Sayı negatif girildi, number = -10
INFO | 2026-07-08 10:36:57,589 | /calculate endpointi çağrıldı, username = ensar, number = 0
WARNING | 2026-07-08 10:36:57,589 | Sayı değeri 0 girildi, number = 0
INFO | 2026-07-08 10:36:57,589 | İşlem başarılı. username=ensar, result=0
"""