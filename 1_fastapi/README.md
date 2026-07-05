# FastAPI'ye Giriş 🚀

Bu doküman, `1_fastapi` klasöründeki [main.py](main.py) ve [example_project.py](example_project.py) dosyalarında anlatılan konuları **sıfırdan** anlatmak için hazırlanmıştır. Amaç: FastAPI'yi hiç bilmeyen birinin okuduğunda kafasında her şeyin oturmasıdır.

---

## İçindekiler

1. [API Nedir? Neden FastAPI?](#1-api-nedir-neden-fastapi)
2. [Kurulum ve Çalıştırma](#2-kurulum-ve-çalıştırma)
3. [İlk Uygulama: FastAPI Nesnesi ve Endpoint](#3-i̇lk-uygulama-fastapi-nesnesi-ve-endpoint)
4. [Swagger Dokümantasyonu (/docs)](#4-swagger-dokümantasyonu-docs)
5. [GET Endpoint ve Parametreler](#5-get-endpoint-ve-parametreler)
6. [POST Endpoint, JSON Body ve Pydantic](#6-post-endpoint-json-body-ve-pydantic)
7. [Response, Hata Yönetimi ve Status Code](#7-response-hata-yönetimi-ve-status-code)
8. [Uçtan Uca Örnek Proje: Hava Durumu Servisi](#8-uçtan-uca-örnek-proje-hava-durumu-servisi)
9. [Özet Tablo](#9-özet-tablo)

---

## 1. API Nedir? Neden FastAPI?

**API (Application Programming Interface)**, iki yazılımın birbiriyle konuşmasını sağlayan bir arayüzdür. Bir restoranı düşün:

- **Sen (Müşteri)** → İstek gönderen taraf (tarayıcı, mobil uygulama, başka bir program)
- **Garson (API)** → İsteğini mutfağa iletir, cevabı sana getirir
- **Mutfak (Sunucu)** → İşi yapan, veriyi hazırlayan taraf

Sen mutfağa girmeden, sadece garsona "bana şunu getir" dersin. API tam olarak bu garsondur.

**FastAPI**, Python ile hızlı ve modern **web API'leri** yazmak için kullanılan bir kütüphanedir. Öne çıkan özellikleri:

- ⚡ **Hızlı**: En hızlı Python framework'lerinden biridir.
- 🧠 **Kolay**: Python'un type hint (tip ipuçları) özelliğini kullanarak kod yazmayı basitleştirir.
- 📄 **Otomatik dokümantasyon**: Sen hiçbir şey yapmadan, API'nin kullanım kılavuzunu (Swagger) otomatik oluşturur.
- ✅ **Otomatik veri doğrulama**: Gelen verinin doğru tipte olup olmadığını senin yerine kontrol eder.

---

## 2. Kurulum ve Çalıştırma

### Gerekli paketler

Proje kök dizinindeki `requirements.txt` dosyası şunları içerir:

```
fastapi      # API'yi yazdığımız ana kütüphane
uvicorn      # Uygulamayı çalıştıran sunucu (server)
```

Kurmak için terminalde:

```bash
pip install fastapi uvicorn
```

> **Not:** `uvicorn`, yazdığımız FastAPI uygulamasını internet üzerinden erişilebilir hale getiren **ASGI sunucusudur**. FastAPI kodu yazar, uvicorn onu "ayağa kaldırır".

### Uygulamayı başlatma

`1_fastapi` klasöründeyken terminalde:

```bash
uvicorn main:app --reload
```

Bu komutu parçalayalım:

| Parça | Anlamı |
|-------|--------|
| `uvicorn` | Sunucuyu başlatan program |
| `main` | Çalıştırılacak dosyanın adı (`main.py`) — `.py` uzantısı yazılmaz |
| `app` | `main.py` içindeki FastAPI nesnesinin değişken adı (`app = FastAPI()`) |
| `--reload` | Kodda değişiklik yaptığında sunucuyu otomatik yeniden başlatır (geliştirme için ideal) |

Çalıştıktan sonra tarayıcıda şu adrese git: **http://127.0.0.1:8000**

> `example_project.py` dosyasını çalıştırmak için: `uvicorn example_project:app --reload`

---

## 3. İlk Uygulama: FastAPI Nesnesi ve Endpoint

Her FastAPI uygulaması bir **uygulama nesnesi** oluşturmakla başlar:

```python
from fastapi import FastAPI

app = FastAPI()   # Uygulamamızın "beyni". Tüm endpoint'leri buna bağlarız.
```

### Endpoint nedir?

**Endpoint (uç nokta)**, API'nin belirli bir URL adresinde dinleme yapan noktasıdır. Bir istek geldiğinde çalışacak fonksiyonu tanımlarız.

```python
@app.get("/")
def home():
    return {"message": "Hello FastAPI"}
```

Bu kodu satır satır okuyalım:

- `@app.get("/")` → Bu bir **decorator** (süsleyici). "Birisi `/` adresine **GET** isteği atarsa, aşağıdaki fonksiyonu çalıştır" demektir.
- `def home():` → İstek geldiğinde çalışacak fonksiyon.
- `return {"message": "Hello FastAPI"}` → FastAPI, Python sözlüğünü (`dict`) otomatik olarak **JSON**'a çevirip kullanıcıya döndürür.

> **JSON nedir?** Web dünyasında veri alışverişinin standart dilidir. Python'daki sözlüğe (`dict`) çok benzer: `{"anahtar": "değer"}`. API'ler genellikle JSON konuşur.

Tarayıcıda `http://127.0.0.1:8000/` adresine gidince şunu görürsün:

```json
{"message": "Hello FastAPI"}
```

Başka bir endpoint eklemek, yeni bir fonksiyon + decorator eklemek kadar kolaydır:

```python
@app.get("/deneme")
def deneme():
    return {"message": "deneme"}
```

Artık `http://127.0.0.1:8000/deneme` adresi de çalışıyor.

---

## 4. Swagger Dokümantasyonu (/docs)

FastAPI'nin en sevilen özelliği: **otomatik oluşturulan interaktif dokümantasyon**.

Uygulaman çalışırken şu adrese git: **http://127.0.0.1:8000/docs**

Karşına **Swagger UI** denen bir arayüz çıkar. Bu arayüzde:

- 📋 Tüm endpoint'lerinin listesini **görebilirsin**
- 🖱️ Tarayıcıdan **istek gönderebilirsin** ("Try it out" butonu ile)
- 📨 Dönen cevapları **inceleyebilirsin**

Yani Postman gibi bir araç kurmadan, API'ni doğrudan tarayıcıdan test edebilirsin. Üstelik bu kılavuz kodun değiştikçe **otomatik güncellenir** — sen elle bir şey yazmazsın.

> **İpucu:** `http://127.0.0.1:8000/redoc` adresinde alternatif bir dokümantasyon arayüzü daha vardır.

---

## 5. GET Endpoint ve Parametreler

**GET metodu**, sunucudan **veri almak** için kullanılır: listeleme, filtreleme, arama, görüntüleme gibi işlemler. (GET isteği sunucudaki veriyi değiştirmez, sadece okur.)

Parametre, endpoint'e dışarıdan gönderdiğimiz ek bilgidir. İki temel türü vardır:

### 5.1 Path (Yol) Parametresi

URL'in **yolunun içine** yazılan parametredir. Genellikle **tek ve belirli bir kaydı** çağırmak için kullanılır.

```python
@app.get("/urun/{urun_id}")
def urun_getir(urun_id: int):
    return {
        "mesaj": "path parametresi ile ürün bilgisi getirildi.",
        "urun_id": urun_id
    }
```

- `{urun_id}` → URL'deki süslü parantez, buranın değişken olduğunu belirtir.
- `urun_id: int` → **Tip ipucu (type hint).** "Bu parametre bir tam sayı olmalı" demektir. FastAPI bunu otomatik kontrol eder.

**Deneme:** `http://127.0.0.1:8000/urun/5` → `urun_id` değeri `5` olarak alınır.

> Eğer `http://127.0.0.1:8000/urun/elma` yazarsan, `elma` bir sayı olmadığı için FastAPI **otomatik hata** döndürür. Bu doğrulamayı sen yazmazsın — tip ipucu sayesinde bedava gelir.

### 5.2 Query (Sorgu) Parametresi

URL'in sonunda `?` ile başlayan, birden fazlaysa `&` ile ayrılan parametrelerdir. Genellikle **arama, filtreleme, listeleme** için kullanılır.

```python
@app.get("/arama")
def arama_yap(kelime: str):
    return {
        "mesaj": "query parametresi ile arama yapıldı.",
        "aranan_kelime": kelime
    }
```

**Deneme:** `http://127.0.0.1:8000/arama?kelime=telefon` → `kelime` değeri `telefon` olur.

Birden fazla query parametresi örneği:
```
/urunler?kategori=elektronik&limit=10
                └ kategori=elektronik   └ limit=10
```

### Path vs Query — Farkı ne?

| | Path Parametresi | Query Parametresi |
|--|------------------|-------------------|
| **Görünüm** | `/urun/5` | `/arama?kelime=telefon` |
| **Amaç** | Belirli tek bir kaydı getirmek | Arama / filtreleme / listeleme |
| **Zorunluluk** | Genellikle zorunlu | Genellikle opsiyonel olabilir |

---

## 6. POST Endpoint, JSON Body ve Pydantic

**POST metodu**, sunucuya **veri göndermek** için kullanılır: kayıt ekleme gibi işlemler. GET'ten farkı, veriyi URL'de değil **isteğin gövdesinde (body)** taşımasıdır.

### JSON Body nedir?

POST isteğiyle gönderdiğimiz veri genellikle **JSON** formatındadır ve isteğin "gövdesinde" gizlidir (URL'de görünmez). Örneğin bir kullanıcı kaydı:

```json
{
    "ad": "Ahmet",
    "yas": 25,
    "sehir": "İstanbul"
}
```

### Pydantic Model — Gelen veriyi güvene almak

Gelen verinin **hangi alanları içermesi gerektiğini, tiplerini ve zorunlu olup olmadığını** tanımlamak için **Pydantic modeli** kullanırız. `BaseModel`'den miras alan bir sınıf yazarız:

```python
from pydantic import BaseModel

class KullaniciBilgisi(BaseModel):
    ad: str      # metin (zorunlu)
    yas: int     # tam sayı (zorunlu)
    sehir: str   # metin (zorunlu)
```

Bu model şunu söyler: "Bana gelen veride `ad` ve `sehir` metin, `yas` ise tam sayı olmalı. Biri eksikse veya yanlış tipteyse **kabul etme**."

Sonra bu modeli endpoint'te parametre olarak kullanırız:

```python
@app.post("/kullanici")
def kullanici_ekle(kullanici: KullaniciBilgisi):
    return {
        "mesaj": "Kullanıcı bilgisi başarıyla alındı.",
        "kullanici": kullanici
    }
```

FastAPI burada senin yerine şunları yapar:
1. Gelen JSON'u okur.
2. `KullaniciBilgisi` modeline uygun mu diye **doğrular**.
3. Uygunsa, otomatik olarak bir Python nesnesine çevirip `kullanici` parametresine verir.
4. Uygun değilse (örneğin `yas` yerine metin gelmişse), **otomatik hata mesajı** döndürür.

> **Pydantic'in gücü:** Bu doğrulamaların hiçbirini elle yazmazsın. Sadece modeli tanımlarsın, gerisini FastAPI + Pydantic halleder.

---

## 7. Response, Hata Yönetimi ve Status Code

### 7.1 Response (Cevap)

**Response**, API'nin kullanıcıya geri döndürdüğü veridir. Fonksiyondan ne `return` edersen, FastAPI onu JSON'a çevirip gönderir. Cevabın yapısını istediğin gibi tasarlayabilirsin:

```python
@app.post("/user", status_code=201)
def create_user(user: UserInformation):
    return {
        "durum": "Success",
        "message": "User created successfully",
        "data": {
            "name": user.name,
            "age": user.age,
            "city": user.city
        }
    }
```

### 7.2 Status Code (Durum Kodu)

Her HTTP cevabı, işin nasıl sonuçlandığını gösteren bir **sayısal kod** taşır. En sık kullanılanlar:

| Kod | Anlamı | Ne zaman? |
|-----|--------|-----------|
| **200** | OK | İstek başarılı |
| **201** | Created | Başarılı **ve** yeni bir kayıt oluşturuldu |
| **400** | Bad Request | İstek hatalı (kullanıcı yanlış veri gönderdi) |
| **404** | Not Found | İstenen kaynak bulunamadı |
| **500** | Internal Server Error | Sunucuda beklenmeyen bir hata oldu |

> **Kaba bir hatırlatma:** `2xx` → başarı, `4xx` → kullanıcı hatası, `5xx` → sunucu hatası.

Bir endpoint'in varsayılan status kodunu decorator'da belirleyebilirsin. Örneğin kayıt oluşturan bir endpoint için `201` uygundur:

```python
@app.post("/user", status_code=201)
```

### 7.3 Hata Yönetimi — `HTTPException`

Kullanıcı yanlış bir şey isterse ona **anlamlı bir hata** döndürmek gerekir. FastAPI bunun için `HTTPException` sınıfını sunar:

```python
from fastapi import HTTPException

@app.get("/product/{product_id}")
def get_product(product_id: int):
    if product_id != 1:   # Diyelim ki sadece 1 numaralı ürün var
        raise HTTPException(
            status_code=404,
            detail="Ürün bulunamadı"
        )
    return {
        "durum": "Başarılı",
        "mesaj": "Ürün bulundu",
        "veri": {"product_id": product_id, "name": "Example Product", "price": 99.99}
    }
```

- `raise HTTPException(...)` → İstenen koşul sağlanmazsa, akışı durdurup bir hata fırlatır.
- `status_code=404` → Kullanıcıya "bulunamadı" durum kodu gider.
- `detail="Ürün bulunamadı"` → Açıklayıcı hata mesajı.

**Deneme:** `http://127.0.0.1:8000/product/1` → başarılı; `http://127.0.0.1:8000/product/2` → 404 hatası.

---

## 8. Uçtan Uca Örnek Proje: Hava Durumu Servisi

[example_project.py](example_project.py) dosyası, yukarıda öğrendiğimiz **tüm parçaları birleştiren** küçük bir projedir.

### Senaryo

> Elimizde basit bir "yapay zeka" modeli olduğunu düşünelim. Kullanıcı son 3 günün sıcaklık değerlerini gönderir; sistem ortalamayı hesaplar ve havanın durumu hakkında basit bir yorum döndürür.

**Gönderilen veri (input):**
```json
{ "gun1": 20, "gun2": 24, "gun3": 22 }
```

**Dönen cevap (output):**
```json
{
    "durum": "basarili",
    "ortalama_sicaklik": 22,
    "tahmin": "Hava dengeli görünüyor."
}
```

### Kod ve içerdiği kavramlar

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# 1) Pydantic modeli — gelen verinin yapısı
class TemperatureData(BaseModel):
    gun1: float
    gun2: float
    gun3: float

# 2) GET endpoint — karşılama mesajı
@app.get("/")
def home():
    return {
        "mesaj": "Hava durumu tahmin servisine hoşgeldiniz.",
        "aciklama": "Lütfen son 3 güne ait sıcaklık değerlerini gönderin."
    }

# 3) POST endpoint — asıl iş burada yapılır
@app.post("/hava-tahmin", status_code=status.HTTP_201_CREATED)
def hava_tahmin(data: TemperatureData):
    # 4) Hata kontrolü — mantıksız sıcaklıkları reddet
    for sicaklik in [data.gun1, data.gun2, data.gun3]:
        if sicaklik < -50 or sicaklik > 60:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sıcaklık değerleri -50 ile 60 arasında olmalıdır."
            )

    # 5) İş mantığı — ortalama ve yorum
    ortalama = (data.gun1 + data.gun2 + data.gun3) / 3

    if ortalama < 10:
        tahmin = "Hava soğuk görünüyor."
    elif ortalama < 25:
        tahmin = "Hava dengeli görünüyor."
    else:
        tahmin = "Hava sıcak görünüyor."

    # 6) Response — yapılandırılmış cevap
    return {
        "durum": "basarili",
        "girilen_veriler": {"gun1": data.gun1, "gun2": data.gun2, "gun3": data.gun3},
        "ortalama_sicaklik": ortalama,
        "tahmin": tahmin
    }
```

### Bu projede hangi kavramları görüyoruz?

| Öğrendiğimiz konu | Kodda nerede? |
|-------------------|---------------|
| FastAPI nesnesi | `app = FastAPI()` |
| GET endpoint | `@app.get("/")` |
| POST endpoint | `@app.post("/hava-tahmin")` |
| JSON body + Pydantic | `class TemperatureData` + `data: TemperatureData` |
| Hata yönetimi | `raise HTTPException(...)` |
| Status code | `status.HTTP_201_CREATED`, `status.HTTP_400_BAD_REQUEST` |
| Response yapısı | Fonksiyonun `return` ettiği sözlük |

> **Dikkat:** Burada `status.HTTP_201_CREATED` gibi sabitler kullanılmış. Bu, doğrudan `201` yazmakla aynıdır; ama kodu okuyanın kodun anlamını (`CREATED`) daha net görmesini sağlar.

### Nasıl test ederim?

1. `uvicorn example_project:app --reload` ile çalıştır.
2. `http://127.0.0.1:8000/docs` adresine git.
3. `/hava-tahmin` endpoint'ini aç → **"Try it out"** → örnek veriyi gir → **"Execute"**.
4. Aşağıda dönen cevabı ve status kodunu incele.

---

## 9. Özet Tablo

| Kavram | Ne işe yarar? | Anahtar kod |
|--------|---------------|-------------|
| **FastAPI nesnesi** | Uygulamanın temeli | `app = FastAPI()` |
| **GET** | Sunucudan veri **almak** | `@app.get("/yol")` |
| **POST** | Sunucuya veri **göndermek** | `@app.post("/yol")` |
| **Path parametresi** | Tek bir kaydı getirmek | `/urun/{urun_id}` |
| **Query parametresi** | Arama / filtreleme | `/arama?kelime=...` |
| **Pydantic model** | Gelen veriyi doğrulamak | `class X(BaseModel)` |
| **HTTPException** | Anlamlı hata döndürmek | `raise HTTPException(...)` |
| **Status code** | İşin sonucunu bildiren kod | `status_code=201` |
| **Swagger** | Otomatik API kılavuzu | `/docs` adresi |

---

## Sırada Ne Var? 🎯

Bu klasörde FastAPI'nin temellerini öğrendin. Bir sonraki adım olarak `2_asenkron_programlama` klasöründe, uygulamaların **birden fazla işi aynı anda** nasıl yürüttüğünü inceleyebilirsin (async/await mantığı).

**Küçük tavsiye:** Bir konuyu gerçekten öğrenmenin en iyi yolu, kodu kendin yazıp `/docs` üzerinden denemektir. Her endpoint'i çalıştır, farklı değerler gönder, hata mesajlarını görmek için bilerek yanlış veri gir. 💪
