# Logging ve Hata Yönetimi 📋🛡️

Bu doküman, `4_logging_hata_yönetimi` klasöründeki dosyalarda anlatılan konuları **sıfırdan** açıklamak için hazırlanmıştır. Amaç: "log ne demek, `print`'ten farkı ne, hata olunca program neden çökmesin?" sorularının hiç bilmeyen birinin kafasında net oturmasıdır.

> **Ön koşul:** `1_fastapi`, `2_asenkron_programlama` ve `3_database` klasörlerini bitirmiş olman iyi olur. Buradaki örnekler onların üzerine kuruludur.

---

## İçindekiler

1. [Neden Logging ve Hata Yönetimi?](#1-neden-logging-ve-hata-yönetimi)
2. [Kurulum ve Çalıştırma](#2-kurulum-ve-çalıştırma)
3. [Logging Modülü ve Log Seviyeleri](#3-logging-modülü-ve-log-seviyeleri) — `logging_modulu.py`
4. [Logları Dosyaya Yazmak](#4-logları-dosyaya-yazmak) — `dosyaya_log_yazma.py`
5. [`try / except` ile Hata Yakalama](#5-try--except-ile-hata-yakalama) — `try_except.py`
6. [FastAPI Endpoint'lerinde Logging](#6-fastapi-endpointlerinde-logging) — `fastapi_logging.py`
7. [FastAPI'de `HTTPException` ile Hata Döndürme](#7-fastapide-httpexception-ile-hata-döndürme) — `fastapi_httpexception.py`
8. [Ödev: Loglayan Hesaplama Servisi](#8-ödev-loglayan-hesaplama-servisi) — `logging_odev.py`
9. [Özet Tablo](#9-özet-tablo)

---

## 1. Neden Logging ve Hata Yönetimi?

Bir uygulama yazdın ve çalıştırdın. Peki:
- 🕵️ Kim, ne zaman, hangi isteği attı? Nasıl takip edeceksin?
- 💥 Kullanıcı hatalı bir veri gönderirse programın **çökmesin** mi istersin, yoksa nazikçe uyarı mı versin?
- 🔍 Sunucu gece 3'te hata verdiyse, sabah **neyin ters gittiğini** nereden anlayacaksın?

İşte bu iki kavram tam da bunun için var:

| Kavram | Ne işe yarar? | Kısaca |
|--------|---------------|--------|
| **Logging** | Uygulamada olan biteni **kayıt altına almak** | "Uygulamanın günlüğü / kara kutusu" |
| **Hata Yönetimi** | Hata olunca programı **çökertmeden** kontrol etmek | "Güvenlik ağı" |

> **Benzetme:** Logging, bir uçağın **kara kutusudur**. Uçak normal uçarken bile her şeyi kaydeder; bir sorun olduğunda kayıtlara bakıp "tam olarak ne oldu?" sorusunu cevaplarsın. Hata yönetimi ise **hava yastığıdır**: kaza anında hasarı en aza indirir, her şeyin paramparça olmasını engeller.

Yapay zeka servislerinde ikisi de kritiktir: model çağrıları, kullanıcı istekleri ve beklenmedik veriler sürekli loglanmalı ve güvenli şekilde ele alınmalıdır.

---

## 2. Kurulum ve Çalıştırma

### Gerekli paketler

```bash
pip install fastapi uvicorn
```

> `logging` Python ile **birlikte gelir**, ayrı kurulum gerekmez.

### Dosyaların rolleri

| Dosya | Türü | Nasıl çalıştırılır? |
|-------|------|---------------------|
| `logging_modulu.py` | Öğrenme betiği | `python logging_modulu.py` |
| `dosyaya_log_yazma.py` | Öğrenme betiği | `python dosyaya_log_yazma.py` |
| `try_except.py` | Öğrenme betiği | `python try_except.py` |
| `fastapi_logging.py` | FastAPI sunucusu | `uvicorn fastapi_logging:app --reload` |
| `fastapi_httpexception.py` | FastAPI sunucusu | `uvicorn fastapi_httpexception:app --reload` |
| `logging_odev.py` | Ödev çözümü (sunucu) | `uvicorn logging_odev:app --reload` |

---

## 3. Logging Modülü ve Log Seviyeleri

📄 İlgili dosya: [logging_modulu.py](logging_modulu.py) — `python logging_modulu.py` ile çalıştırılır.

Python'un yerleşik `logging` modülü, uygulamada olan biteni farklı **önem seviyelerinde** kaydetmeni sağlar.

### `print` yerine neden `logging`?

Yeni başlayanlar her şeyi `print` ile yazdırır. Ama `logging`'in ciddi avantajları var:

| | `print` | `logging` |
|--|---------|-----------|
| Önem seviyesi | Yok (hepsi aynı) | Var (DEBUG → CRITICAL) |
| Zaman damgası | Yok | Otomatik ekler |
| Dosyaya kaydetme | Zahmetli | Tek satır ayar |
| Kapatıp açma | Tek tek silmen gerekir | Seviye ayarıyla toplu kontrol |

> **Kural:** Geçici deneme için `print`, gerçek uygulamalarda **her zaman `logging`**.

### 5 log seviyesi

Loglar önem sırasına göre 5 seviyeye ayrılır:

| Seviye | Ne zaman kullanılır? | Örnek |
|--------|----------------------|-------|
| 🔵 **DEBUG** | Geliştirme sırasında detaylı bilgi | `Değişken yas = 15` |
| 🟢 **INFO** | Normal işleyiş bilgisi | `Kullanıcı giriş yaptı` |
| 🟡 **WARNING** | Dikkat! (ama çökme yok) | `Kullanıcı 18 yaşından küçük` |
| 🔴 **ERROR** | Bir işlem başarısız oldu | `Kullanıcı adı boş bırakıldı` |
| ⚫ **CRITICAL** | Ciddi, uygulamayı tehdit eden hata | `Yaş negatif geldi` |

**Seviye sırası:** `DEBUG → INFO → WARNING → ERROR → CRITICAL`

### Temel ayar: `basicConfig`

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,   # DEBUG ve ÜZERİ tüm seviyeleri göster
    format="%(levelname)s | %(asctime)s | %(message)s"
)
```

- **`level=logging.DEBUG`** → "DEBUG ve üstündeki her şeyi göster" demektir. Yani hepsini görürsün.
- Eğer `level=logging.WARNING` yazsaydın, **DEBUG ve INFO logları gizlenir**, sadece WARNING, ERROR, CRITICAL görünürdü. Bu, "gürültüyü" kontrol etmenin yoludur.

### `format` neyi kontrol eder?

`format` her log satırının nasıl görüneceğini belirler:

| Kod | Anlamı | Örnek çıktı |
|-----|--------|-------------|
| `%(levelname)s` | Log seviyesi | `INFO` |
| `%(asctime)s` | Zaman damgası | `2026-07-08 10:36:14` |
| `%(message)s` | Senin yazdığın mesaj | `Kullanıcı giriş yaptı` |

Örnek çıktı:
```
INFO | 2026-07-08 10:36:14,851 | Kullanıcı giriş yaptı
```

### Kullanım örneği

```python
logging.debug("Bu bir debug mesajıdır.")
logging.info("Bu bir info mesajıdır.")
logging.warning("Bu bir warning mesajıdır.")
logging.error("Bu bir error mesajıdır.")
logging.critical("Bu bir critical mesajıdır.")
```

> **Altın ipucu:** Değişkenleri loglarken `f"yas: {yas}"` gibi **etiketli** yaz. Böylece loglarda arama yaparken `yas:` diye aratıp değeri kolayca bulursun.

---

## 4. Logları Dosyaya Yazmak

📄 İlgili dosya: [dosyaya_log_yazma.py](dosyaya_log_yazma.py) — `python dosyaya_log_yazma.py` ile çalıştırılır.

Loglar ekrana yazılırsa, program kapanınca **kaybolur**. Gerçek uygulamalarda logları bir **dosyaya** yazıp kalıcı hale getiririz. Böylece sonradan geriye dönüp inceleyebiliriz.

Tek fark, `basicConfig`'e `filename` eklemek:

```python
import logging

logging.basicConfig(
    filename="uygulama.log",   # 👈 loglar bu dosyaya yazılır (ekrana değil)
    level=logging.DEBUG,
    format="%(levelname)s | %(asctime)s | %(message)s",
    encoding="utf-8"           # 👈 Türkçe karakterler (ç, ş, ı...) düzgün yazılsın
)

def log_ornekleri():
    logging.debug("debug kaydı")
    logging.info("info kaydı")
    logging.warning("warning kaydı")
    logging.error("error kaydı")
    logging.critical("critical kaydı")

if __name__ == "__main__":
    log_ornekleri()
```

### Dikkat edilmesi gerekenler

- **`filename="uygulama.log"`** → Loglar artık ekrana değil, bu dosyaya yazılır. Dosya yoksa otomatik oluşturulur, varsa **sonuna eklenir** (üzerine yazmaz).
- **`encoding="utf-8"`** → Türkçe karakterlerin bozuk görünmemesi için şart.
- **`if __name__ == "__main__":`** → [3_database'de öğrendiğimiz](../3_database/README.md#6-️-önemli-ders-if-__name__--__main__-tuzağı) koruma. Bu dosya import edilirse loglar kendiliğinden üretilmesin diye.

> **Deneme:** Betiği çalıştırdıktan sonra klasörde oluşan `uygulama.log` dosyasını aç — tüm log satırlarını orada zaman damgalarıyla göreceksin.

---

## 5. `try / except` ile Hata Yakalama

📄 İlgili dosya: [try_except.py](try_except.py) — `python try_except.py` ile çalıştırılır.

Normalde bir Python programında hata oluşursa, program **anında çöker** ve durur. `try / except` yapısı, hatayı **yakalayıp** programın çökmesini engeller.

### Temel mantık

```python
try:
    # Yapmak istediğimiz, hata verebilecek işlem
    sayi = int("abc")
except ValueError:
    # try içinde hata olursa BURASI çalışır (program çökmez)
    print("Bu metin sayıya çevrilemez.")
```

> **Benzetme:** `try`, ipte yürüyen bir cambazdır. `except` ise altındaki **güvenlik ağıdır**. Cambaz düşerse (hata olursa) yere çakılmaz (program çökmez), ağa düşer (except bloğu devreye girer).

### Farklı hata türlerini yakalamak

Her hata türünün bir adı vardır. Hangi hatayı beklediğini `except` yanına yazarsın:

| Hata türü | Ne zaman olur? | Örnek |
|-----------|----------------|-------|
| `ValueError` | Değer uygun tipte değil | `int("abc")` |
| `ZeroDivisionError` | Sıfıra bölme | `10 / 0` |
| `TypeError` | Tip uyuşmazlığı | `5 + "10"` |
| `IndexError` | Listede olmayan index | `[1,2,3][5]` |

Dosyadaki örnekler tam olarak bunları gösterir:

```python
def bolme(sayi1, sayi2):
    try:
        sonuc = sayi1 / sayi2
        print(f"✅ Sonuç: {sonuc}")
    except ZeroDivisionError:
        print("❌ HATA: Sıfıra bölme hatası.")

bolme(10, 2)   # ✅ Sonuç: 5.0
bolme(10, 0)   # ❌ HATA: Sıfıra bölme hatası. (program çökmez!)
```

### Genel hata yakalama: `Exception as e`

Hangi hatanın geleceğini bilemediğin durumlarda, **tüm hataları** yakalayan genel bir yapı kullanılır:

```python
try:
    eleman = liste[index]
except Exception as e:   # her türlü hatayı yakalar
    print(f"❌ HATA: {e}")   # e, hatanın açıklamasını tutar
```

> `Exception as e` — `e` değişkeni hatanın ne olduğunu içerir. Loglarken çok işine yarar: `logging.error(f"Hata: {e}")`.

### `finally`: Ne olursa olsun çalışır

`finally` bloğu, **hata olsa da olmasa da** her zaman çalışır. Genellikle "temizlik" işleri için kullanılır (dosya kapatma, bağlantı kapatma):

```python
def dosya_oku():
    try:
        dosya = open("olmayan_dosya.txt", "r")
        print(dosya.read())
    except Exception as e:
        print(f"❌ HATA: {e}")
    finally:
        print("Dosya işlemi sona erdi.")   # her durumda çalışır
```

| Blok | Ne zaman çalışır? |
|------|-------------------|
| `try` | Her zaman denenir |
| `except` | **Sadece** hata olursa |
| `finally` | **Her durumda** (hata olsun olmasın) |

---

## 6. FastAPI Endpoint'lerinde Logging

📄 İlgili dosya: [fastapi_logging.py](fastapi_logging.py) — `uvicorn fastapi_logging:app --reload` ile çalıştırılır.

Şimdi loglamayı gerçek bir API'ye uyguluyoruz. Amaç: her endpoint çağrıldığında **kim, ne gönderdi, ne oldu** bilgisini kaydetmek.

```python
from fastapi import FastAPI
import logging
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(asctime)s | %(message)s")

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    age: int

@app.post("/users")
async def create_user(user: UserCreate):
    # Endpoint çağrısını ve gelen veriyi logla
    logging.info(f"POST /users çağrıldı. username={user.username}, age={user.age}")

    if user.age < 0:
        logging.error(f"Yaş negatif olamaz! age: {user.age}")   # hata durumu
        return {"error": "Yaş negatif olamaz!"}

    if user.age < 18:
        logging.warning(f"{user.username} 18 yaşından küçük. age: {user.age}")   # uyarı

    logging.info(f"{user.username} başarıyla oluşturuldu.")
    return {"message": "kullanıcı başarıyla oluşturuldu.", "user": {"username": user.username, "age": user.age}}
```

### Altın kural: Gireni ve çıkanı logla

> **Aklımızda olsun:** Bir fonksiyona / endpoint'e **geleni (input) ve çıkanı (output) kesinlikle logla.** Bir sorun olduğunda "acaba hangi veri gelmişti?" sorusunu ancak böyle cevaplayabilirsin.

### Hangi durumda hangi seviye?

Bu dosya, log seviyelerinin **doğru kullanımını** güzel gösterir:

| Durum | Seviye | Neden? |
|-------|--------|--------|
| Endpoint çağrıldı | `INFO` | Normal akış bilgisi |
| Kullanıcı 18'den küçük | `WARNING` | Dikkat çekici ama çökme yok |
| Yaş negatif | `ERROR` | Geçersiz veri, işlemi durdurmalı |
| İşlem başarılı | `INFO` | Normal sonuç |

> **Deneme:** Sunucuyu çalıştır, `/docs`'tan farklı yaş değerleriyle istek at ve **terminaldeki log çıktılarının** seviyesine göre nasıl değiştiğini izle.

---

## 7. FastAPI'de `HTTPException` ile Hata Döndürme

📄 İlgili dosya: [fastapi_httpexception.py](fastapi_httpexception.py) — `uvicorn fastapi_httpexception:app --reload` ile çalıştırılır.

Önceki örnekte hatayı `return {"error": ...}` ile döndürdük. Bu çalışır ama **doğru yöntem değildir** — çünkü HTTP durum kodu hâlâ `200 OK` kalır, yani "her şey yolunda" der. Oysa hata var!

Doğru yol: **`HTTPException` fırlatmak.** Böylece hem anlamlı bir mesaj hem de doğru **durum kodu** döner.

```python
from fastapi import FastAPI, HTTPException

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    # Ürün bulunamazsa hata fırlat
    raise HTTPException(status_code=404, detail="Ürün bulunamadı")
```

### `return {"error": ...}` vs `raise HTTPException`

| | `return {"error": ...}` | `raise HTTPException(...)` |
|--|-------------------------|----------------------------|
| HTTP durum kodu | `200 OK` (yanlış!) | `404`, `400`... (doğru) |
| İstemci hatayı anlar mı? | Zor (200 gördüğü için başarılı sanır) | Kolay (kod hatayı belli eder) |
| Doğru yöntem mi? | ❌ Hayır | ✅ Evet |

### Örnekteki hata senaryoları

```python
@app.post("/products")
async def create_product(product: Product):
    # Aynı ID zaten var mı?
    for item in products:
        if item["id"] == product.id:
            raise HTTPException(status_code=400, detail="Aynı ID'ye sahip ürün zaten mevcut")

    # Fiyat geçerli mi?
    if product.price <= 0:
        raise HTTPException(status_code=400, detail="Fiyat sıfırdan büyük olmalıdır")

    products.append({"id": product.id, "name": product.name, "price": product.price})
    return {"message": "Ürün başarıyla eklendi"}
```

| Durum kodu | Anlamı | Bu dosyada |
|-----------|--------|------------|
| `400` | Bad Request (kullanıcı hatası) | Geçersiz fiyat, tekrar eden ID |
| `404` | Not Found (bulunamadı) | Olmayan ürün |

> **Not:** `HTTPException`'ı [1_fastapi'de](../1_fastapi/README.md#73-hata-yönetimi--httpexception) kısaca görmüştük. Bu klasörde onu **logging ile birlikte** kullanmayı öğreniyoruz: önce hatayı **logla**, sonra `HTTPException` ile **döndür**. (Bir sonraki bölümdeki ödev tam olarak bunu yapıyor.)

---

## 8. Ödev: Loglayan Hesaplama Servisi

📄 İlgili dosya: [logging_odev.py](logging_odev.py) — `uvicorn logging_odev:app --reload` ile çalıştırılır.

Bu ödev, **bu klasörün tüm konularını birleştirir**: dosyaya loglama + FastAPI + `HTTPException` + doğru log seviyeleri.

### Senaryo

`/calculate` endpoint'i `username` ve `number` alır, doğrulama yapar, sayıyı 2 ile çarpıp sonucu döndürür. Her adımı `app.log` dosyasına kaydeder.

```python
from fastapi import FastAPI, HTTPException
import logging

# Loglar app.log dosyasına yazılıyor
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(levelname)s | %(asctime)s | %(message)s",
    encoding="utf-8"
)

app = FastAPI(title="Merhaba FastAPI!", description="FastAPI açıklaması")

@app.get("/calculate")
async def calculate_endpoint(username: str, number: int):
    logging.info(f"/calculate çağrıldı, username={username}, number={number}")   # gireni logla

    if len(username) < 3:
        logging.error(f"Kullanıcı adı 3 harften kısa, username={username}")
        raise HTTPException(status_code=400, detail="Kullanıcı adı en az 3 karakter olmalıdır")

    if number < 0:
        logging.error(f"Sayı negatif, number={number}")
        raise HTTPException(status_code=400, detail="Sayı negatif olamaz")

    if number == 0:
        logging.warning(f"Sayı 0 girildi, number={number}")

    result = number * 2
    logging.info(f"İşlem başarılı. username={username}, result={result}")   # çıkanı logla

    return {"status": "Başarılı", "username": username, "number": number, "result": result}
```

### Kullanılan tüm kavramlar

| Konu | Kodda nerede? |
|------|---------------|
| Dosyaya loglama | `filename="app.log"` |
| Query parametreleri | `username: str, number: int` |
| Gireni loglama (INFO) | İlk `logging.info(...)` |
| Hata loglama + döndürme (ERROR + 400) | `logging.error` + `raise HTTPException` |
| Uyarı (WARNING) | `number == 0` durumu |
| Başarı loglama (INFO) | Son `logging.info(...)` |
| `title` / `description` | `FastAPI(title=..., description=...)` → Swagger'da görünür |

### Test adımları

1. Çalıştır: `uvicorn logging_odev:app --reload`
2. Tarayıcıdan: `http://127.0.0.1:8000/docs`
3. `/calculate`'i farklı değerlerle dene:
   - `username=ensar, number=10` → ✅ başarılı (result=20)
   - `username=en, number=10` → ❌ 400 (isim çok kısa)
   - `username=ensar, number=-10` → ❌ 400 (negatif sayı)
   - `username=ensar, number=0` → ⚠️ warning loglar ama çalışır (result=0)
4. Klasörde oluşan **`app.log`** dosyasını açıp log kayıtlarını incele.

### `app.log` örnek çıktısı

```
INFO    | 2026-07-08 10:36:14 | /calculate çağrıldı, username = ensar, number = 10
INFO    | 2026-07-08 10:36:14 | İşlem başarılı. username=ensar, result=20
ERROR   | 2026-07-08 10:36:25 | Kullanıcı adı 3 harften kısa gönderildi, username = en
WARNING | 2026-07-08 10:36:57 | Sayı değeri 0 girildi, number = 0
```

Gördüğün gibi, sunucu kapansa bile bu kayıtlar dosyada kalır — işte logging'in gücü budur. 🎯

---

## 9. Özet Tablo

| Kavram | Ne işe yarar? | Anahtar kod |
|--------|---------------|-------------|
| **logging** | Olan biteni kayıt altına alır | `import logging` |
| **basicConfig** | Log ayarlarını yapar | `logging.basicConfig(...)` |
| **Log seviyeleri** | Önem derecesi | `debug/info/warning/error/critical` |
| **level** | Hangi seviyeden itibaren gösterileceği | `level=logging.INFO` |
| **format** | Log satırının görünümü | `"%(levelname)s | %(asctime)s | %(message)s"` |
| **filename** | Logları dosyaya yazar | `filename="app.log"` |
| **encoding** | Türkçe karakterler için | `encoding="utf-8"` |
| **try / except** | Hatayı yakalar, çökmeyi önler | `try: ... except: ...` |
| **Exception as e** | Genel hata + açıklama | `except Exception as e:` |
| **finally** | Her durumda çalışır | `finally: ...` |
| **HTTPException** | Doğru kodla hata döndürür | `raise HTTPException(status_code=400, detail="...")` |

---

## 🧠 Kritik Hatırlatmalar

- **`print` değil `logging`** → gerçek uygulamalarda her zaman logging kullan.
- **Doğru seviye seç** → normal akış `INFO`, dikkat `WARNING`, hata `ERROR`.
- **Gireni ve çıkanı logla** → sorun çıkınca hayat kurtarır.
- **`return {"error"}` değil `raise HTTPException`** → doğru durum kodu dönsün.
- **Önce logla, sonra fırlat** → hatayı hem kaydet hem kullanıcıya bildir.
- **`encoding="utf-8"`** → dosyaya loglarken Türkçe karakterler bozulmasın.

---

## Sırada Ne Var?

Bu klasörde uygulamanı **gözlemlenebilir** ve **dayanıklı** hale getirmeyi öğrendin: logging ile ne olduğunu görüyor, hata yönetimi ile çökmeleri önlüyorsun. Bu, "çalışan kod" ile "gerçek dünyaya hazır servis" arasındaki farktır.

**Küçük tavsiye:** `logging_odev.py`'yi çalıştırıp `app.log` dosyasını açık tut. Farklı istekler attıkça dosyaya düşen satırları canlı izle — logging'in neden bu kadar değerli olduğu o an tam oturur. 💪
