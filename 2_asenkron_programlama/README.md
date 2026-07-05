# Asenkron Programlama ve FastAPI ⚡

Bu doküman, `2_asenkron_programlama` klasöründeki dosyalarda anlatılan konuları **sıfırdan** açıklamak için hazırlanmıştır. Amaç: asenkron programlamayı hiç bilmeyen birinin okuduğunda "senkron ne, asenkron ne, `async`/`await` niye var?" sorularının kafasında net oturmasıdır.

> **Ön koşul:** Bu klasöre geçmeden önce `1_fastapi` klasöründeki temelleri (endpoint, GET/POST, Pydantic) öğrenmiş olman iyi olur. Buradaki örnekler onların üzerine kuruludur.

---

## İçindekiler

1. [Senkron vs Asenkron: Temel Fikir](#1-senkron-vs-asenkron-temel-fikir)
2. [Kurulum ve Çalıştırma](#2-kurulum-ve-çalıştırma)
3. [`async` ve `await` Nedir?](#3-async-ve-await-nedir) — `async_await.py`
4. [Normal Endpoint vs Async Endpoint](#4-normal-endpoint-vs-async-endpoint) — `fastapi_async.py`
5. [I/O-Bound İşlemler ve `asyncio.gather`](#5-io-bound-i̇şlemler-ve-asynciogather) — `io_bound.py`
6. [Sık Yapılan Asenkron Hatalar](#6-sık-yapılan-asenkron-hatalar) — `async_hatalari.py`
7. [Python İçinden Test Etmek: `requests`](#7-python-i̇çinden-test-etmek-requests) — `main_requests.py` + `test_requests.py`
8. [Mini Proje: Sahte Chatbot Servisi](#8-mini-proje-sahte-chatbot-servisi) — `mini_proje.py` + `mini_proje_client.py`
9. [En Sık Düşülen Tuzak: `await` Unutmak](#9-en-sık-düşülen-tuzak-await-unutmak)
10. [Özet Tablo](#10-özet-tablo)

---

## 1. Senkron vs Asenkron: Temel Fikir

### Senkron (Eş Zamanlı) Programlama

İşlemler **sırayla** çalışır. Bir işlem bitmeden bir sonrakine geçilmez.

> **Benzetme:** Tek kasiyeri olan bir markette sıradasın. Kasiyer önündeki müşteriyle işini tamamen bitirmeden sıradaki müşteriye bakmaz. Biri kartını unutup ararsa, **arkadaki herkes bekler.**

Zaman alan bir işlem (dosya okuma, API bekleme) sırasında program **hiçbir şey yapmadan bekler**. Bu boşa harcanan zamandır.

### Asenkron (Eş Zamansız) Programlama

Zaman alan bir işlem devam ederken program **başka işlere geçebilir**. Beklerken boş durmaz.

> **Benzetme:** Akıllı bir garson düşün. Bir masanın siparişini mutfağa verir; yemek pişerken **boş beklemez**, gidip başka masaların siparişini alır. Yemek hazır olunca geri döner. Tek garson, ama beklemeleri değerlendirdiği için çok daha fazla masaya bakar.

### Ne zaman avantaj sağlar?

Asenkron yapı özellikle **I/O-bound** (girdi/çıktı ağırlıklı) işlemlerde parlar:

- 📁 Dosya okuma/yazma
- 🌐 API istekleri (dış servisten cevap bekleme)
- 🗄️ Veritabanı işlemleri
- 🤖 Yapay zeka modelinden cevap bekleme (LLM çağrıları)

Bu işlemlerin ortak özelliği: programın **beklediği** (CPU'nun boş durduğu) işlemler olmasıdır. İşte asenkron yapı, bu bekleme sürelerini başka işler yaparak değerlendirir.

> **Not:** Asenkron her derde deva değildir. Yoğun **hesaplama** (CPU-bound) işlerinde — örneğin milyonlarca sayıyı toplamak — asenkron pek fayda sağlamaz, çünkü orada program beklemiyor, sürekli çalışıyordur.

---

## 2. Kurulum ve Çalıştırma

### Gerekli paketler

```bash
pip install fastapi uvicorn requests
```

| Paket | Ne işe yarar? |
|-------|---------------|
| `fastapi` | API'yi yazdığımız ana kütüphane |
| `uvicorn` | FastAPI uygulamasını çalıştıran sunucu |
| `requests` | Python içinden HTTP isteği göndermek için (test dosyalarında kullanılır) |
| `asyncio` | Python'un **yerleşik** asenkron kütüphanesi (ayrı kurulum gerekmez) |

### İki tür dosya var

Bu klasördeki dosyalar iki gruba ayrılır:

**A) Uvicorn ile çalışan FastAPI sunucuları** (`app = FastAPI()` içerenler):
```bash
uvicorn dosya_adi:app --reload
```
Örnek: `uvicorn fastapi_async:app --reload`

**B) Doğrudan Python ile çalışan betikler** (sunucu değil, script):
```bash
python dosya_adi.py
```
Örnek: `python async_await.py`

Her bölümde hangi dosyanın nasıl çalıştırılacağını ayrıca belirteceğiz.

---

## 3. `async` ve `await` Nedir?

📄 İlgili dosya: [async_await.py](async_await.py) — bu bir **script**'tir, `python async_await.py` ile çalıştırılır.

Asenkron programlamanın iki temel anahtar kelimesi vardır:

- **`async def`** → "Bu fonksiyon asenkrondur" der. Böyle bir fonksiyon çağrıldığında hemen çalışmaz; **beklenebilir (awaitable)** bir iş olur.
- **`await`** → "Bu işin bitmesini bekle, ama beklerken gerekirse başka işlere izin ver" der. Sadece `async def` fonksiyonların **içinde** kullanılabilir.

### Örnek kod

```python
import asyncio

async def gorev1():
    print("Görev 1 başladı")
    await asyncio.sleep(2)   # 2 saniyelik bir iş simülasyonu (örn. ML modeli çalışıyor)
    print("Görev 1 tamamlandı")

async def gorev2():
    print("Görev 2 başladı")
    await asyncio.sleep(1)   # 1 saniyelik bir iş
    print("Görev 2 tamamlandı")

async def main():
    # gather: birden fazla asenkron görevi AYNI ANDA başlatır
    await asyncio.gather(gorev1(), gorev2())

asyncio.run(main())   # asenkron dünyaya giriş kapısı
```

### Çıktı ve neden bu sırada?

```
Görev 1 başladı
Görev 2 başladı      ← Görev 1 beklerken Görev 2 hemen başladı!
Görev 2 tamamlandı   ← 1 saniye sonra (daha kısa olduğu için önce bitti)
Görev 1 tamamlandı   ← 2 saniye sonra
```

Dikkat et: Görev 1 henüz bitmeden Görev 2 başladı. Çünkü `gorev1` içindeki `await asyncio.sleep(2)` sırasında program "nasılsa bekliyorum" deyip `gorev2`'yi başlattı. **İki görev toplamda 3 saniye değil, sadece 2 saniyede** bitti (en uzun görevin süresi kadar).

### Önemli kavramlar

| Kavram | Açıklama |
|--------|----------|
| `async def` | Asenkron fonksiyon tanımlar |
| `await` | Bir asenkron işin bitmesini bekler (bu sırada başka işlere izin verir) |
| `asyncio.sleep(n)` | `n` saniyelik asenkron bekleme (gerçek bir bekleme işini simüle eder) |
| `asyncio.gather(...)` | Birden fazla görevi aynı anda çalıştırır |
| `asyncio.run(...)` | Asenkron programı başlatan giriş noktası (script'lerde) |

> **`gather` olmasaydı?** Eğer görevleri `await gorev1()` sonra `await gorev2()` şeklinde tek tek beklseydik, sıralı (senkron gibi) çalışır ve toplam süre **3 saniye** olurdu. `gather` sayesinde ikisini paralel yürüttük.

---

## 4. Normal Endpoint vs Async Endpoint

📄 İlgili dosya: [fastapi_async.py](fastapi_async.py) — `uvicorn fastapi_async:app --reload` ile çalıştırılır.

FastAPI'de endpoint'ler hem normal (`def`) hem asenkron (`async def`) yazılabilir.

```python
# Normal (senkron) endpoint
@app.get("/")
def home():
    return {"message": "Normal Endpoint", "type": "Senkron"}

# Asenkron endpoint
@app.get("/asenkron")
async def home_async():
    await asyncio.sleep(5)   # 5 saniyelik bir işi bekliyoruz
    return {
        "message": "Asenkron Endpoint",
        "type": "Asenkron",
        "situtaion": "5 saniye bekledim"
    }
```

### Farkı nasıl gözlemlerim?

`/asenkron` endpoint'i 5 saniye bekliyor. Asenkron yazıldığı için, **bu 5 saniye boyunca sunucu başka istekleri işlemeye devam edebilir**. Yani sen `/asenkron`'u beklerken başka bir sekmede `/` adresine gidersen, o anında cevap verir.

Eğer bu endpoint içinde asenkron `await asyncio.sleep(5)` yerine senkron bir bekleme (`time.sleep(5)`) kullansaydık, sunucu **tüm 5 saniye boyunca kilitlenir** ve başka hiçbir isteğe cevap veremezdi. (Bu tuzağı [6. bölümde](#6-sık-yapılan-asenkron-hatalar) göreceğiz.)

> **Ne zaman `async def` kullanmalıyım?** Endpoint içinde `await` gerektiren bir işlem (dış API çağrısı, veritabanı, `asyncio.sleep`) varsa `async def` kullan. Yalnızca basit, anlık işlemler yapıyorsan normal `def` de yeterlidir.

---

## 5. I/O-Bound İşlemler ve `asyncio.gather`

📄 İlgili dosya: [io_bound.py](io_bound.py) — `uvicorn io_bound:app --reload` ile çalıştırılır.

Bu dosya, gerçek bir yapay zeka senaryosunu simüle eder: **Bir PDF dosyasını işleyip vektör veritabanına kaydetmek.** (RAG sistemlerinde çok yaygın bir işlemdir.)

```python
async def pdf_isle(dosya_adi: str):
    print(f"{dosya_adi} dosyası işleniyor...")
    await asyncio.sleep(2)   # PDF okuma simülasyonu

    print(f"{dosya_adi} okundu, vektör DB'ye kaydediliyor...")
    await asyncio.sleep(2)   # embedding (vektöre çevirme) simülasyonu

    await asyncio.sleep(2)   # veritabanına yazma simülasyonu
    print(f"{dosya_adi} vektör veritabanına kaydedildi.")
```

Bu fonksiyon **3 ayrı I/O adımı** içerir (okuma, embedding, yazma) — her biri gerçekte beklenen işlerdir, bu yüzden `await` ile simüle edilmiştir.

### Tek dosya işleyen endpoint

```python
@app.post("/pdf_isle")
async def pdf_isle_endpoint(pdf_verisi: PDFVerisi):
    await pdf_isle(pdf_verisi.dosya_adi)
    return {"durum": "başarılı", "mesaj": f"{pdf_verisi.dosya_adi} işlendi."}
```

### İki dosyayı AYNI ANDA işleyen endpoint

```python
@app.get("/iki-pdf-isle")
async def iki_pdf_isle():
    await asyncio.gather(
        pdf_isle("dosya1.pdf"),
        pdf_isle("dosya2.pdf")
    )
    return {"durum": "başarılı", "mesaj": "İki dosya da işlendi."}
```

İşte asenkronun gücü burada: Her PDF işlemi 6 saniye sürüyor (2+2+2). Ama `gather` ile ikisini paralel yürüttüğümüz için **toplam 12 saniye değil, yaklaşık 6 saniyede** biterler. İki dosya birbirinin bekleme süresini "doldurur".

> **Deneme:** Sunucuyu çalıştırıp `/iki-pdf-isle` endpoint'ini çağır ve terminaldeki `print` çıktılarının sırasına dikkat et. İki dosyanın mesajlarının **iç içe geçtiğini** göreceksin — ikisi de aynı anda ilerliyor demektir.

---

## 6. Sık Yapılan Asenkron Hatalar

📄 İlgili dosya: [async_hatalari.py](async_hatalari.py) — `uvicorn async_hatalari:app --reload` ile çalıştırılır.

> **Altın kural:** Bir fonksiyonun başına `async` yazmak, onu sihirli bir şekilde hızlandırmaz. Kod gerçekten asenkron çalışsın diye, beklemeler **doğru şekilde** `await` edilmelidir.

### Hata 1: Blocking (durdurucu) kod kullanmak

```python
@app.get("/blocking-ornek")
async def blocking_ornek():
    time.sleep(5)   # ❌ YANLIŞ! Bu senkrondur, tüm sunucuyu 5 saniye kilitler.
    func1()         # ❌ Normal senkron fonksiyon
    return {"durum": "hata", "mesaj": "async yazıldı ama blocking kod içeriyor."}
```

Buradaki sorun: Endpoint `async def` ile yazılmış ama içinde `time.sleep(5)` var. `time.sleep`, **tüm programı** durduran senkron bir beklemedir. Bu 5 saniye boyunca sunucu **başka hiçbir isteğe cevap veremez**. `async` etiketi burada tamamen boşa gitmiştir.

### Hata 2 (Doğrusu): Asenkron bekleme kullanmak

```python
@app.get("/dogru-bekleme-ornek")
async def dogru_bekleme_ornek():
    await asyncio.sleep(5)   # ✅ DOĞRU! Beklerken başka işlere izin verir.
    await func2()            # ✅ func2 bir async fonksiyon, await ile çağrıldı
    return {"durum": "başarılı", "mesaj": "doğru bekleme yöntemi kullanıldı."}
```

### Karşılaştırma tablosu

| Yanlış (blocking) | Doğru (non-blocking) |
|-------------------|----------------------|
| `time.sleep(5)` | `await asyncio.sleep(5)` |
| `func1()` (senkron) | `await func2()` (asenkron) |
| Sunucu kilitlenir | Sunucu diğer isteklere bakabilir |

### Hata 3: `await`'i unutmak

```python
async def veri_hazirla():
    await asyncio.sleep(2)
    return "veri hazırlandı"

@app.get("/await-kullanimi-ornek")
async def await_kullanimi_ornek():
    veri = await veri_hazirla()   # ✅ await ile GERÇEK sonuç alınır
    return {"durum": "başarılı", "mesaj": f"veri: {veri}"}
```

Eğer buradaki `await`'i unutup `veri = veri_hazirla()` yazsaydık, `veri` değişkeni **string yerine bir "coroutine nesnesi"** olurdu. Bu, bizim `mini_proje.py`'de yakaladığımız hatanın ta kendisidir → [9. bölüm](#9-en-sık-düşülen-tuzak-await-unutmak).

---

## 7. Python İçinden Test Etmek: `requests`

📄 İlgili dosyalar: [main_requests.py](main_requests.py) (sunucu) + [test_requests.py](test_requests.py) (istemci)

Şimdiye kadar API'lerimizi tarayıcıdan (`/docs`) test ettik. Ama gerçek uygulamalarda API'ye **başka bir program** istek atar. Bunu simüle etmek için `requests` kütüphanesini kullanırız.

### Adım 1: Sunucuyu çalıştır

`main_requests.py` iki endpoint içerir (GET `/durum` ve POST `/mesaj`), her ikisi de 2 saniye bekler:

```bash
uvicorn main_requests:app --reload
```

### Adım 2: İstemci betiğini çalıştır

Sunucu **çalışırken**, **ayrı bir terminalde**:

```bash
python test_requests.py
```

`test_requests.py` içeriği:

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# GET isteği
get_response = requests.get(f"{BASE_URL}/durum")
print(f"status code: {get_response.status_code}")
print(f"get response: {get_response.json()}")

# POST isteği (json body ile)
post_data = {"mesaj": "merhaba fastapi"}
post_response = requests.post(f"{BASE_URL}/mesaj", json=post_data)
print(f"status code: {post_response.status_code}")
print(f"post response: {post_response.json()}")
```

### Beklenen çıktı

```
status code: 200
get response: {'durum': 'başarılı', 'mesaj': 'get endpointi çalıştı'}

status code: 200
post response: {'durum': 'başarılı', 'gelen_veri': 'merhaba fastapi', 'cevap': 'post mesajı başarıyla alındı'}
```

### `requests` fonksiyonları

| Fonksiyon | Ne yapar? |
|-----------|-----------|
| `requests.get(url)` | Sunucudan veri ister (GET) |
| `requests.post(url, json=veri)` | Sunucuya JSON gövde gönderir (POST) |
| `.status_code` | Dönen HTTP durum kodu (200, 404, ...) |
| `.json()` | Cevabın JSON gövdesini Python sözlüğüne çevirir |

> **Önemli:** Sunucu ile istemci **iki ayrı terminalde** çalışmalı. Önce `uvicorn ...` ile sunucuyu ayağa kaldır, sonra başka bir terminalde `python test_requests.py` çalıştır. Sunucu kapalıysa istemci "bağlantı hatası" verir.

---

## 8. Mini Proje: Sahte Chatbot Servisi

📄 İlgili dosyalar: [mini_proje.py](mini_proje.py) (sunucu) + [mini_proje_client.py](mini_proje_client.py) (istemci)

Bu proje, öğrendiğimiz her şeyi birleştiren küçük bir **chatbot** simülasyonudur.

### Senaryo

> Arka planda bir dil modeli (LLM) varmış gibi davranan bir chat servisi. Kullanıcı mesaj gönderir → sistem "düşünüyormuş" gibi bekler → uygun bir cevap üretir → mesajı kayıt altına alır.

### Sunucu tarafı (`mini_proje.py`)

```python
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class MesajIstek(BaseModel):
    mesaj: str

# Sahte "dil modeli" — cevap üretmeyi simüle eder
async def sahte_dil_modeli_cevap_uret(mesaj: str) -> str:
    await asyncio.sleep(2)   # model "düşünüyor"
    kullanici_mesaji = mesaj.lower()
    if "merhaba" in kullanici_mesaji:
        return "Merhaba! Size nasıl yardımcı olabilirim?"
    elif "hava" in kullanici_mesaji:
        return "Bugün hava durumu için elimde gerçek veri yok."
    else:
        return f"mesajınızı aldım: '{kullanici_mesaji}'"

# Mesajı "veritabanına kaydetmeyi" simüle eder
async def mesaj_kaydet(kullanici_mesaji: str, model_cevabi: str):
    await asyncio.sleep(1)
    print(f"Mesaj kaydedildi: '{kullanici_mesaji}' | Cevap: '{model_cevabi}'")

@app.post("/chat")
async def chat_yap(istek: MesajIstek):
    cevap = await sahte_dil_modeli_cevap_uret(istek.mesaj)  # ⚠️ await ŞART!
    await mesaj_kaydet(istek.mesaj, cevap)
    return {
        "durum": "başarılı",
        "kullanici_mesaji": istek.mesaj,
        "model_cevabi": cevap
    }
```

### İstemci tarafı (`mini_proje_client.py`)

Bu betik, gerçek bir kullanıcı gibi terminalden mesaj girip sürekli sohbet etmeni sağlar (bir `while` döngüsü ile):

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

while True:
    kullanici_mesaji = input("Mesajınızı girin (çıkmak için 'q'): ")
    if kullanici_mesaji.lower() == 'q':
        print("Chatbot simülasyonu sonlandırıldı.")
        break

    gonderilecek_veri = {"mesaj": kullanici_mesaji}
    response = requests.post(f"{BASE_URL}/chat", json=gonderilecek_veri)

    print(f"status code: {response.status_code}")
    print("Cevap:", response.json()["model_cevabi"])
```

### Nasıl çalıştırırım?

1. **1. terminal** — sunucuyu başlat:
   ```bash
   uvicorn mini_proje:app --reload
   ```
2. **2. terminal** — istemciyi başlat:
   ```bash
   python mini_proje_client.py
   ```
3. Mesaj yaz (örn. "merhaba"), cevabı gör. Çıkmak için `q` yaz.

### Bu projede hangi kavramlar var?

| Kavram | Kodda nerede? |
|--------|---------------|
| FastAPI + Pydantic | `app`, `class MesajIstek` |
| Async endpoint | `async def chat_yap` |
| Async yardımcı fonksiyonlar | `sahte_dil_modeli_cevap_uret`, `mesaj_kaydet` |
| Doğru `await` kullanımı | `await sahte_dil_modeli_cevap_uret(...)` |
| İstemci–sunucu ayrımı | `mini_proje_client.py` ↔ `mini_proje.py` |

---

## 9. En Sık Düşülen Tuzak: `await` Unutmak

Bu klasörde çalışırken karşılaştığımız gerçek bir hataydı — o kadar yaygın ki ayrı bir başlığı hak ediyor.

### Hatalı kod

```python
cevap = sahte_dil_modeli_cevap_uret(istek.mesaj)   # ❌ await YOK
```

### Ne olur?

`async def` bir fonksiyonu `await` olmadan çağırırsan, fonksiyon **çalışmaz**. Geriye metin yerine bir **coroutine nesnesi** döner:

```
<coroutine object sahte_dil_modeli_cevap_uret at 0x000001C5DCB7B1B0>
```

FastAPI bu coroutine'i JSON'a çevirmeye çalışır, çeviremez ve şu hatayı fırlatır:

```
TypeError: 'coroutine' object is not iterable
→ 500 Internal Server Error
```

### Doğrusu

```python
cevap = await sahte_dil_modeli_cevap_uret(istek.mesaj)   # ✅ await VAR
```

> **Hatırlatma:** `async def` bir fonksiyonu her çağırdığında, sonucuna ihtiyacın varsa **mutlaka** `await` kullan. `await` unutmak, asenkron programlamada 1 numaralı hatadır.

---

## 10. Özet Tablo

| Kavram | Ne işe yarar? | Anahtar kod |
|--------|---------------|-------------|
| **Senkron** | İşleri sırayla, bekleyerek yapar | normal `def` |
| **Asenkron** | Beklerken başka işlere geçer | `async def` |
| **`async def`** | Asenkron fonksiyon tanımlar | `async def f():` |
| **`await`** | Asenkron işin bitmesini bekler | `await f()` |
| **`asyncio.sleep(n)`** | Asenkron bekleme (I/O simülasyonu) | `await asyncio.sleep(2)` |
| **`asyncio.gather`** | Görevleri aynı anda çalıştırır | `await asyncio.gather(a(), b())` |
| **`asyncio.run`** | Asenkron programı başlatır (script) | `asyncio.run(main())` |
| **Blocking hata** | Sunucuyu kilitleyen senkron bekleme | ❌ `time.sleep(5)` |
| **`requests`** | Python'dan API'ye istek atmak | `requests.post(url, json=...)` |
| **`await` unutma** | Coroutine hatası, 500 döner | ❌ `f()` yerine ✅ `await f()` |

---

## Zihin Haritası: I/O-Bound vs CPU-Bound 🧠

Asenkronun **ne zaman** işe yaradığını bilmek, onu nasıl kullanacağını bilmek kadar önemlidir:

| | I/O-Bound (Asenkron faydalı ✅) | CPU-Bound (Asenkron faydasız ❌) |
|--|-------------------------------|----------------------------------|
| **Ne yapar?** | Bekler (dış cevap, disk, ağ) | Hesaplar (CPU sürekli meşgul) |
| **Örnek** | API çağrısı, DB sorgusu, dosya, LLM çağrısı | Görüntü işleme, büyük matris çarpımı |
| **Neden?** | Bekleme süresi başka işlere ayrılabilir | Beklenen bir şey yok, CPU zaten dolu |

Yapay zeka uygulamalarının çoğu (LLM'e istek at, cevabı bekle, veritabanına yaz) **I/O-bound**'dur. İşte bu yüzden FastAPI + asenkron programlama, yapay zeka servisleri için biçilmiş kaftandır. 🎯

---

## Sırada Ne Var?

Bu klasörde asenkron programlamanın temellerini ve FastAPI ile nasıl birleştiğini öğrendin. Artık:
- Senkron/asenkron farkını biliyorsun,
- `async`/`await`'i doğru kullanabiliyorsun,
- Sık yapılan hataları (blocking kod, `await` unutma) tanıyorsun,
- İstemci–sunucu mimarisini `requests` ile test edebiliyorsun.

**Küçük tavsiye:** `io_bound.py`'deki `/iki-pdf-isle` endpoint'ini çalıştırıp terminaldeki çıktıların nasıl iç içe geçtiğini kendi gözünle gör. Asenkronun "aynı anda ilerleme" fikri, o çıktıyı görünce tam olarak oturur. 💪
