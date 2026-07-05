from fastapi import FastAPI

app = FastAPI()

# sistemden veri almak için endpoint oluşturuyoruz.
@app.get("/")
def home():
    """
    Bu bir endpointtir. Bu endpoint'e istek atıldığında sistemden veri alır ve kullanıcıya döndürür.
    Tarayıcıdan erişildiğinde basit bir mesaj döndürsün.
    """

    return {"message": "Hello FastAPI"}

# * ======================================================================================================================

# get metodumuz var, deneme endpointimiz get metodu ile çalışıyor, deneme endpointi çağrılırsa home fonksiyonu çalışır ve bir mesaj return eder.
@app.get("/deneme")
def home():
    """
    deneme
    """

    return {"message": "deneme"}

"""
Swagger Dokümantasyonu ile API Testi
    - endpoint listesini görebilmek
    - istek gönderebilmek
    - dönen cevapları incelemek    
/docs swagger arayüzü
"""
# ? ======================================================================================================================
"""
GET Endpoint ve parametre mantığı
    - get metodu sunucudan veri almak için kullanılır. Listeleme, filtreleme, arama ve görüntüleme

İki temel parametre türü vardır:
    1. Path Parametreleri: URL yolunda belirtilen parametrelerdir. 
    Örneğin, /items/{item_id} gibi bir endpointte item_id path parametresi olarak kullanılır.
    Belirli bir kaydı veya tek bir veriyi çağırmak için kullanılır. Örnek: /items/5 gibi bir endpoint çağrıldığında item_id=5 olarak alınır.

    2. Query Parametreleri: URL'de ? ile başlayan ve & ile ayrılan parametrelerdir. 
    Örneğin, /items?name=example&limit=10 gibi bir endpointte name ve limit query parametreleri olarak kullanılır.
    Arama, filtreleme ve listeleme gibi işlemler için kullanılır. 
    Örnek gibi bir endpoint çağrıldığında name=example ve limit=10 olarak alınır.
"""

# 1. basit bir get endpoint örneği, yukarıda var zaten
#@app.get("/")
#def home():
#    return {"mesaj": "get endpoint örneğine hoşgeldiniz..."}

# 2. path parametre örneği
@app.get("/urun/{urun_id}")
def urun_getir(urun_id: int):
    """
    Path parametre örneği
    - urun_id path parametresi olarak alınır ve fonksiyon içinde kullanılır.
    - Belirli bir ürünün detaylarını almak için kullanılabilir.
    """
    return {
        "mesaj": "path parametresi ile ürün bilgisi getirildi.",
        "urun_id": urun_id
    }

# 3. query parametre örneği
@app.get("/arama")
def arama_yap(kelime: str): # kelime değeri url sonunda ?kelime=.... şeklinde gönderilir.
    """
    Query parametre örneği
    - kelime query parametresi olarak alınır ve fonksiyon içinde kullanılır.
    - Arama işlemi için kullanılabilir.
    """
    return {
        "mesaj": "query parametresi ile arama yapıldı.",
        "aranan_kelime": kelime
    }


# TODO: =======================================================================================================================

"""
POST Enpointi
    - post ile sunucuya veri gönderilir. Kayıt ekleme, güncelleme ve silme işlemleri için kullanılır.

JSON Body:
    - POST isteği ile gönderilen veriler genellikle JSON formatında olur.
    - FastAPI, bu JSON verilerini otomatik olarak Python veri tiplerine dönüştürür.

Pydantic Model:
    - API ye gelen veriyi düzenli ve güvenli bir şekilde almak için Pydantic model kullanılır.
    - Hangi alanların geleceğini, bu alanların veri tiplerini ve zorunlu olup olmadığını belirleriz.
"""

from pydantic import BaseModel

# pydantic ile api input tanımla

class KullaniciBilgisi(BaseModel):
    """
    Kullanıcı bilgilerini tanımlayan Pydantic modeli
    - ad: Kullanıcının adı (str)
    - yas: Kullanıcının yaşı (int)
    - sehir: Kullanıcının yaşadığı şehir (str)
    """
    ad: str
    yas: int
    sehir: str

# post metodu sunucuya veri göndermek için kullanılır. Kullanıcı bilgilerini alıp kaydeder.
@app.post("/kullanici")
def kullanici_ekle(kullanici: KullaniciBilgisi):
    return {
        "mesaj": "Kullanıcı bilgisi başarıyla alındı.",
        "kullanici": kullanici
    }


# !========================================================================================================================

"""
Response:
    - API nin cevabı, geri döndürdüğü yapı
    - Bir istek başarılı olduğunda hangi veriyi hangi formatta döndüreceğimizi belirleriz.
    - API den dönen cevapları incelemek için kullanılır.
    - FastAPI, dönen verileri otomatik olarak JSON formatına dönüştürür.

Hata Yönetimi:
    - Kullanıcı yanlış veri gönderirse ya da sistem içersinde hata oluşursa uygun bir hata mesajı döndürmek önemlidir.
    - API de hata yönetimi, kullanıcıya anlamlı hata mesajları döndürmek için önemlidir.
    - FastAPI, HTTPException sınıfı ile hata yönetimi sağlar.
    - Hata durumunda uygun HTTP durum kodu ve mesaj döndürülür.


Status Code:
    - API nin döndürdüğü durumu gösteren HTTP durum kodlarıdır.
    - Örneğin:
        - 200: Başarılı istek
        - 201: Başarılı ve yeni kaynak oluşturuldu
        - 400: Hatalı istek
        - 404: Kaynak bulunamadı
        - 500: Sunucu hatası
"""

from fastapi import HTTPException
# from pydantic import BaseModel

# app = FastAPI()

# kullanıcıdan gelecek olan verinin yapısının tanımlanması
class UserInformation(BaseModel):
    name: str
    age: int
    city: str

# Ana endpoint
# @app.get("/")
# def ana_endpoint():
#    return {"mesaj": "Response, Hata Yönetimi ve Status Code örneklerine hoşgeldiniz..."}

@app.post("/user", status_code=201)
def create_user(user: UserInformation):
    """
    Kullanıcı oluşturma endpointi
    - Kullanıcı bilgilerini alır ve kaydeder.
    - Başarılı olduğunda 201 Created status kodu döner.
    """
    # Burada kullanıcıyı veritabanına kaydetme işlemi yapılabilir.
    return {
        "durum": "Success",
        "message": "User created successfully",
        "data": {
            "name": user.name,
            "age": user.age,
            "city": user.city
        }
    }

# hata yönetimi örneği
# burada bir ürün bulunmaz ise 404 hatası versin

@app.get("/product/{product_id}")
def get_product(product_id: int):
    if product_id != 1:  # Örnek olarak sadece product_id 1 olan ürün var
        raise HTTPException(
            status_code=404, 
            detail="Ürün bulunamadı"
        )
    return {
        "durum": "Başarılı",
        "mesaj": "Ürün bulundu",
        "veri": {
            "product_id": product_id,
            "name": "Example Product",
            "price": 99.99
        }
    }