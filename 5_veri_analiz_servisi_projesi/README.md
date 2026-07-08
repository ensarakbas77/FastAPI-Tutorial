# Veri Analiz Servisi — Ara Proje 📊🚀

Bu klasör, önceki 4 bölümde (FastAPI, Asenkron Programlama, Veritabanı, Logging & Hata Yönetimi) öğrendiğimiz her şeyi **tek bir gerçek projede** birleştiren bir **pratik / bitirme projesidir**. Amaç: parça parça öğrendiğimiz kavramların gerçek bir uygulamada nasıl birlikte çalıştığını görmek.

> **Ön koşul:** Bu proje bir **capstone (bitirme)** çalışmasıdır. `1_fastapi` → `4_logging_hata_yönetimi` klasörlerini bitirmiş olman gerekir; buradaki her parça o bilgilerin üzerine kuruludur.

---

## İçindekiler

1. [Proje Ne Yapıyor?](#1-proje-ne-yapıyor)
2. [Hangi Konuları Birleştiriyor?](#2-hangi-konuları-birleştiriyor)
3. [Kurulum ve Çalıştırma](#3-kurulum-ve-çalıştırma)
4. [🆕 Yeni Kavramlar](#4-yeni-kavramlar)
5. [Kod Mimarisi: Katman Katman](#5-kod-mimarisi-katman-katman)
6. [Endpoint'ler](#6-endpointler)
7. [İstemci ile Test](#7-i̇stemci-ile-test)
8. [Uçtan Uca Akış](#8-uçtan-uca-akış)
9. [Özet Tablo](#9-özet-tablo)

---

## 1. Proje Ne Yapıyor?

Bu servis, kullanıcının yüklediği bir **CSV dosyasını** analiz eden ve sonuçları saklayan bir veri analiz API'sidir.

**Senaryo:**
1. 📤 Kullanıcı bir CSV dosyası **yükler**.
2. 🔍 Sistem dosyayı okur, temel analizler yapar (satır/sütun sayısı, eksik değerler...).
3. 💾 Analiz sonuçlarını **veritabanına kaydeder**.
4. 📜 Kullanıcı geçmiş analizleri **listeleyebilir**.
5. 🔎 İstenirse tek bir analizin **detayına** bakabilir.

> **Gerçek hayat karşılığı:** Bu, veri bilimi platformlarının (ör. bir "veri seti yükle ve önizle" özelliği) basitleştirilmiş bir halidir. Yapay zeka projelerinde model eğitmeden önce veriyi bu şekilde analiz etmek çok yaygındır.

---

## 2. Hangi Konuları Birleştiriyor?

Bu projenin güzelliği, önceki tüm klasörlerin **aynı anda** kullanılmasıdır:

| Önceki Klasör | Bu projede nerede kullanılıyor? |
|---------------|--------------------------------|
| **1_fastapi** | Endpoint'ler, `HTTPException`, status code'lar, Pydantic mantığı |
| **2_asenkron** | `async def` endpoint'ler, `await file.read()`, `requests` ile client testi |
| **3_database** | SQLite tablo oluşturma, `INSERT`/`SELECT`, CRUD fonksiyonları |
| **4_logging** | Dosyaya loglama (`analysis_service.log`), log seviyeleri, `try/except` |

Buna ek olarak **3 yeni kavram** öğreniyoruz: dosya yükleme, `pandas` ile veri analizi ve veritabanında JSON saklama.

---

## 3. Kurulum ve Çalıştırma

### Gerekli paketler

Bu proje iki **yeni paket** gerektirir (kök `requirements.txt`'e eklenmiştir):

```bash
pip install fastapi uvicorn requests pandas python-multipart
```

| Paket | Ne işe yarar? |
|-------|---------------|
| `pandas` | CSV dosyasını okuyup analiz etmek için (veri bilimi kütüphanesi) |
| `python-multipart` | FastAPI'nin **dosya yükleme** isteklerini işleyebilmesi için (zorunlu) |

> **⚠️ Dikkat:** `python-multipart` kurulu değilse, dosya yükleme endpoint'i çalışmaz ve FastAPI başlangıçta hata verir. Dosya yükleme özelliği için bu paket şarttır.

### Çalıştırma

```bash
# 1. Sunucuyu başlat
uvicorn main:app --reload

# 2. Tarayıcıdan Swagger'a git
http://127.0.0.1:8000/docs
```

### Klasördeki dosyalar

| Dosya | Nedir? |
|-------|--------|
| `main.py` | Ana uygulama (API + analiz + veritabanı) |
| `client.py` | Python'dan test eden istemci betiği |
| `sample_data.csv` | Test için örnek veri dosyası |
| `analysis_results.db` | Analiz sonuçlarının saklandığı SQLite veritabanı (otomatik oluşur) |
| `analysis_service.log` | Log kayıtları (otomatik oluşur) |

---

## 4. 🆕 Yeni Kavramlar

### 4.1 Dosya Yükleme — `UploadFile` ve `File`

Şimdiye kadar hep JSON verisi aldık. Bu projede ilk kez **dosya** alıyoruz:

```python
from fastapi import UploadFile, File

@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    file_bytes = await file.read()   # dosya içeriğini oku
```

| Parça | Anlamı |
|-------|--------|
| `UploadFile` | Yüklenen dosyayı temsil eden FastAPI tipi |
| `File(...)` | "Bu parametre bir dosya olmalı" der. `...` = zorunlu |
| `await file.read()` | Dosyanın **ham içeriğini** (bytes) okur — asenkron olduğu için `await` |
| `file.filename` | Yüklenen dosyanın adı (ör. `sample_data.csv`) |

> Dosya içeriği **bytes** (ham baytlar) olarak gelir, metin değil. Bu yüzden pandas'a verirken `BytesIO` ile sarmalarız.

### 4.2 `pandas` ile CSV Analizi

`pandas`, veriyi tablo (DataFrame) olarak işleyen güçlü bir kütüphanedir:

```python
import pandas as pd
from io import BytesIO

dataframe = pd.read_csv(BytesIO(file_bytes))   # bytes → DataFrame

row_count = len(dataframe)                                          # satır sayısı
column_count = len(dataframe.columns)                              # sütun sayısı
column_names = list(dataframe.columns)                            # sütun isimleri
numeric_column_count = len(dataframe.select_dtypes(include=['number']).columns)  # sayısal sütunlar
missing_values = int(dataframe.isnull().sum().sum())              # eksik (boş) hücre sayısı
```

| Kod | Ne yapar? |
|-----|-----------|
| `pd.read_csv(...)` | CSV'yi bir tabloya (DataFrame) dönüştürür |
| `BytesIO(file_bytes)` | Ham baytları, pandas'ın dosya gibi okuyabileceği hale getirir |
| `len(dataframe)` | Kaç satır (kayıt) var |
| `.select_dtypes(include=['number'])` | Sadece sayısal sütunları seçer (ör. `age`, `salary`) |
| `.isnull().sum().sum()` | Tablodaki toplam **boş hücre** sayısı |

> **Örnek:** `sample_data.csv` dosyasında `Can` satırının `age` değeri boş. `missing_values` bu yüzden `1` döner.

### 4.3 Veritabanında Liste Saklama — `json.dumps` / `json.loads`

SQLite'ın "liste" diye bir veri tipi yoktur. Peki `column_names` gibi bir **listeyi** (`["name", "age", "city"]`) nasıl saklarız? Onu bir **JSON metnine** çevirerek:

```python
import json

# KAYDEDERKEN: liste → JSON metni
json.dumps(["name", "age", "city"], ensure_ascii=False)
# Sonuç: '["name", "age", "city"]'  (artık TEXT olarak saklanabilir)

# OKURKEN: JSON metni → liste
json.loads('["name", "age", "city"]')
# Sonuç: ["name", "age", "city"]  (tekrar Python listesi)
```

| Fonksiyon | Yön | Ne yapar? |
|-----------|-----|-----------|
| `json.dumps(liste)` | Python → metin | Listeyi kaydedilebilir JSON metnine çevirir |
| `json.loads(metin)` | metin → Python | JSON metnini tekrar listeye çevirir |
| `ensure_ascii=False` | — | Türkçe karakterlerin (`ş`, `ı`...) bozulmadan saklanması için |

---

## 5. Kod Mimarisi: Katman Katman

`main.py` düzenli bir plana göre yazılmıştır. Bu, gerçek projelerin nasıl organize edildiğini gösteren güzel bir örnektir:

```
1. Kütüphaneler          →  import ...
2. Logging kurulumu      →  logging.basicConfig(filename='analysis_service.log', ...)
3. FastAPI app           →  app = FastAPI(title="Veri Analiz Servisi")
4. Veritabanı kurulumu   →  init_db()  (tabloyu oluşturur)
5. Yardımcı fonksiyonlar →  analiz + veritabanı işlemleri
6-8. Endpoint'ler        →  API katmanı
```

### İki tür yardımcı fonksiyon

**A) Analiz fonksiyonu** (veriyi işler):
- `analyze_csv_file(file_bytes, filename)` → CSV'yi analiz edip sonuç sözlüğü döner.

**B) Veritabanı fonksiyonları** (CRUD):
- `save_analysis_result(result)` → sonucu kaydeder, yeni kaydın `id`'sini döner.
- `get_all_analysis_history()` → tüm kayıtları özet olarak listeler.
- `get_analysis_by_id(id)` → tek bir kaydın tüm detayını getirir.

> **Neden fonksiyonlara böldük?** Endpoint'ler sadece "trafik polisi" gibi davranır (isteği al, doğru fonksiyona yönlendir, cevabı dön). Asıl işi ayrı fonksiyonlar yapar. Bu **ayrım (separation of concerns)**, kodu okunabilir ve test edilebilir kılar.

### Her yerde `try/except` + logging

Dikkat et: her fonksiyon `try/except` ile sarılı ve her hata **loglanıyor**:

```python
try:
    # işlem
except Exception as e:
    logging.error(f"... hata oluştu: {e}")
    raise HTTPException(status_code=500, detail="...")
```

Bu, [4_logging'de öğrendiğimiz](../4_logging_hata_yönetimi/README.md) "önce logla, sonra HTTPException fırlat" prensibinin gerçek uygulamasıdır.

---

## 6. Endpoint'ler

| Metot | Yol | Ne yapar? |
|-------|-----|-----------|
| `POST` | `/upload_csv/` | CSV yükler, analiz eder, kaydeder |
| `GET` | `/analysis-history/` | Tüm analiz geçmişini listeler |
| `GET` | `/analysis/{analysis_id}/` | Tek bir analizin detayını getirir |

### POST `/upload_csv/` — Yükleme ve doğrulama zinciri

Bu endpoint çok katmanlı **doğrulama** yapar (savunmacı programlama):

```python
@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    logging.info(f"/upload_csv/ çağrıldı: filename = {file.filename}")

    # 1. Uzantı .csv mi?
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Geçersiz dosya uzantısı.")

    file_bytes = await file.read()

    # 2. Dosya boş mu?
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Boş dosya yüklendi.")

    # 3. Analiz et → 4. Kaydet
    analysis_result = analyze_csv_file(file_bytes, file.filename)
    analysis_id = save_analysis_result(analysis_result)

    return {"message": "CSV başarıyla yüklendi ve analiz edildi.", "analysis_id": analysis_id}
```

> **Neden bu kadar kontrol?** Kullanıcı her zaman doğru veri göndermez — yanlış uzantı, boş dosya, bozuk CSV... Her birini **önceden** yakalayıp anlamlı hata döndürmek, sağlam bir servisin işaretidir.

### GET endpoint'lerinde iki farklı seviye

- `get_all_analysis_history()` → **özet** bilgi döner (id, filename, satır/sütun sayısı, tarih). Liste görünümü için hafif.
- `get_analysis_by_id(id)` → **tam detay** döner (sütun isimleri, eksik değerler dahil). `column_names` burada `json.loads` ile tekrar listeye çevrilir.

> Bu ayrım gerçek API'lerde standarttır: liste endpoint'i az veri (hızlı), detay endpoint'i çok veri döner.

---

## 7. İstemci ile Test

📄 İlgili dosya: [client.py](client.py) — `python client.py` ile çalıştırılır.

Sunucu **çalışırken**, ayrı bir terminalde `client.py` üç endpoint'i sırayla test eder:

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_upload_csv(file_path):
    with open(file_path, 'rb') as f:                       # dosyayı ikili (binary) modda aç
        files = {'file': (file_path, f, 'text/csv')}       # dosya yükleme formatı
        response = requests.post(f"{BASE_URL}/upload_csv", files=files)
        print("Upload CSV Response:", response.json())

# Tüm sistemi test et
test_upload_csv("sample_data.csv")   # 1. CSV yükle
test_analysis_history()              # 2. Geçmişi listele
test_analysis_details(1)             # 3. ID=1 detayını getir
```

### Dosya yüklemede `json=` değil `files=`

Dikkat et: önceki projelerde `requests.post(url, json=veri)` kullanmıştık. Dosya yüklerken ise **`files=`** parametresi kullanılır:

```python
files = {'file': (dosya_adi, dosya_nesnesi, 'text/csv')}
requests.post(url, files=files)
```

Bu, HTTP'de "multipart/form-data" denen özel bir gönderim biçimidir — dosyalar bu şekilde taşınır. (`python-multipart` paketi tam da bunu çözmek için gerekliydi.)

### Test adımları

1. **1. terminal:** `uvicorn main:app --reload`
2. **2. terminal:** `python client.py`
3. Çıktıda üç işlemin (yükle → listele → detay) cevaplarını gör.

---

## 8. Uçtan Uca Akış

Bir CSV yüklendiğinde sistemin içinde olan bitenler:

```
📤 Kullanıcı CSV yükler
        │
        ▼
🚦 upload_csv endpoint         →  logla, uzantı & boşluk kontrolü
        │
        ▼
🔍 analyze_csv_file (pandas)   →  satır/sütun/eksik değer analizi
        │
        ▼
💾 save_analysis_result        →  sonucu SQLite'a kaydet (liste → JSON)
        │
        ▼
📨 { "analysis_id": 1 } döner   →  her adım analysis_service.log'a yazıldı
```

Sonra kullanıcı:
```
📜 GET /analysis-history/   →  tüm kayıtların özeti
🔎 GET /analysis/1/         →  1 numaralı kaydın tam detayı (JSON → liste)
```

---

## 9. Özet Tablo

| Kavram | Ne işe yarar? | Anahtar kod |
|--------|---------------|-------------|
| **UploadFile / File** | Dosya yükleme almak | `file: UploadFile = File(...)` |
| **await file.read()** | Dosya içeriğini okumak | `file_bytes = await file.read()` |
| **pandas** | CSV okuma & analiz | `pd.read_csv(BytesIO(file_bytes))` |
| **BytesIO** | Baytları dosya gibi okutmak | `BytesIO(file_bytes)` |
| **isnull().sum()** | Eksik değer sayısı | `df.isnull().sum().sum()` |
| **json.dumps** | Liste → saklanabilir metin | `json.dumps(liste, ensure_ascii=False)` |
| **json.loads** | Metin → liste | `json.loads(metin)` |
| **cursor.lastrowid** | Yeni kaydın id'si | `analysis_id = cursor.lastrowid` |
| **files=** (requests) | Dosya gönderme | `requests.post(url, files=files)` |
| **python-multipart** | Dosya yüklemeyi mümkün kılar | (paket, kurulum şart) |

---

## 🧠 Bu Projeden Çıkarılacak Dersler

- **Katmanlı yapı** → endpoint'ler ince, iş mantığı ayrı fonksiyonlarda. Kod okunabilir olur.
- **Savunmacı programlama** → her girdiyi doğrula (uzantı, boşluk, geçerlilik).
- **Her yerde logging** → sorun çıktığında `analysis_service.log` sana ne olduğunu anlatır.
- **Doğru hata kodları** → `400` kullanıcı hatası, `404` bulunamadı, `500` sunucu hatası.
- **Parçaları birleştirmek** → FastAPI + async + DB + logging bir arada gerçek bir servis oluşturur.

---

## Tebrikler! 🎉

Bu ara projeyi anladıysan, artık **gerçek bir web servisinin** tüm temel parçalarını bir araya getirebiliyorsun: veri al, işle, sakla, sun ve her adımı logla. Bu, yapay zeka uygulamalarını web servisi haline getirmenin tam da temelidir.

**Küçük tavsiye:** `sample_data.csv`'yi değiştirip (yeni sütunlar ekle, bazı hücreleri boş bırak) tekrar yükle. Analiz sonuçlarının (`missing_values`, `numeric_column_count`) nasıl değiştiğini gözlemle — sistemin gerçekten çalıştığını böyle hissedersin. 💪
