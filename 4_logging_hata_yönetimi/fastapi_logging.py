"""
Amaç:
    - fastapi endpoint içersinde logging kullanmak
    - istem ve işlem bilgilerini loglamak
"""

from fastapi import FastAPI
import logging
from pydantic import BaseModel

# logging ayarları
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(asctime)s | %(message)s")

# fastapi app oluşturma
app = FastAPI()

# post isteği için veri modeli
class UserCreate(BaseModel):
    username: str
    age: int

# get endpointi tanımla
@app.get("/user/{username}")
async def get_user(username: str):
    # endpoint çağrıldığında loglama
    logging.info(f"GET /user endpointi çağrıldı. username: {username}")

    # geliştirme sırasında detaylı bilgi görmek için debug logu
    logging.debug(f"kullanıcı bilgisi hazırlanıyor. username: {username}")

    # boş veya anlamsız bir verinin kontrolü
    if len(username) < 3:
        logging.error(f"kullanıcı adı 3 karakterden az olamaz!")
        return {"error": "Kullanıcı adı 3 karakterden az olamaz!"}
    
    logging.info(f"{username} kullanıcı bilgisi başarıyla döndürüldü.")

    return {
        "username": username, 
        "message": "Kullanıcı bilgisi başarıyla geldi."
    }

# post endpointi tanımla
@app.post("/users")
async def create_user(user: UserCreate):

    # endpoint çağrısı ve gelen veri loglama
    # Aklımızda Olsun: Bir fonksiyona, endpointe geleni çıkanı kesinlikle loglayın

    logging.info(f"POST /users endpointi çağrıldı. username = {user.username}, age = {user.age}")

    # hatalı duruma örnek
    if user.age < 0:
        logging.error(f"Yaş negatif olamaz! age: {user.age}") # bu bir hata durumudur ve uygulamanın çalışmasını engeller. Devam ettirmememiz gerekir.
        return {"error": "Yaş negatif olamaz!"}
    
    # uyarrı seviyesi
    if user.age < 18:
        logging.warning(f"{user.username} kullanıcısı 18 yaşından küçük. age: {user.age}") # bu uyarı uygulamayı çökertmez ama dikkat edilmesi gereken bir durumdur.
    
    logging.info(f"{user.username} kullanıcısı başarıyla oluşturuldu.")

    return {
        "message": "kullanıcı başarıyla oluşturuldu.",
        "user": {
            "username": user.username,
            "age": user.age
        }
    }