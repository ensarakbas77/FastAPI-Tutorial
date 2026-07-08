# Yapay Zeka için Web Uygulamaları 🤖🌐

Bu repo, **yapay zeka uygulamalarını web servisleri haline getirmek** için gereken temel becerileri sıfırdan öğrenmek amacıyla hazırlanmış bir çalışma / ders deposudur. Her klasör bir konuyu ele alır ve içinde o konuyu **hiç bilmeyen birinin bile anlayabileceği** ayrıntılı bir `README.md` bulunur.

---

## 🎯 Amaç

Modern yapay zeka projeleri (LLM tabanlı chatbotlar, RAG sistemleri, model API'leri) genellikle bir **web servisi** olarak sunulur. Kullanıcı bir istek gönderir, arka plandaki model çalışır ve cevap döner. Bu deponun amacı, o web katmanını inşa etmek için gereken araçları adım adım öğretmektir:

- 🚀 **FastAPI** ile API (endpoint) yazmak
- ⚡ **Asenkron programlama** ile model beklerken sunucuyu kilitlememek
- 🔗 İstemci–sunucu mimarisini kurmak ve test etmek

Öğrenme, basitten karmaşığa doğru **numaralı klasörler** halinde ilerler.

---

## 📚 Konular / Klasörler

Her klasörün kendi ayrıntılı README'si vardır; konuyu benzetmeler, örnek kodlar ve "nasıl çalıştırırım?" adımlarıyla tek tek anlatır.

<div align="center">

| # | 📂 Konu | 🎯 Ne Öğreniyorsun? | 📖 Doküman |
|:---:|:---|:---|:---:|
| **1** | 🚀 **FastAPI'ye Giriş** | API'nin temelleri: ilk endpoint'ten veri doğrulamaya | **[Aç →](1_fastapi/README.md)** |
| **2** | ⚡ **Asenkron Programlama** | Sunucuyu kilitlemeden aynı anda birden fazla iş yürütmek | **[Aç →](2_asenkron_programlama/README.md)** |
| **3** | 🗄️ **Veritabanı (Database)** | Verileri kalıcı olarak saklamak ve API'ye bağlamak | **[Aç →](3_database/README.md)** |
| **4** | 📋 **Logging & Hata Yönetimi** | Olan biteni kaydetmek ve hataları çökmeden yönetmek | **[Aç →](4_logging_hata_yönetimi/README.md)** |
| **5** | 🎯 **Veri Analiz Servisi** `ara proje` | 1–4 konularını tek serviste birleştiren pratik proje | **[Aç →](5_veri_analiz_servisi_projesi/README.md)** |

</div>

<details>
<summary><b>🔎 Her konuda tam olarak neler var? (genişletmek için tıkla)</b></summary>

<br>

**🚀 1 · FastAPI'ye Giriş**
`Endpoint` · `GET / POST` · `Path & Query parametreleri` · `Pydantic` · `Hata yönetimi` · `Status Code` · `Swagger`

**⚡ 2 · Asenkron Programlama**
`Senkron vs Asenkron` · `async / await` · `asyncio.gather` · `I/O-bound işlemler` · `requests ile test` · `Mini chatbot projesi`

**🗄️ 3 · Veritabanı (Database)**
`SQLite` · `SQL` · `CRUD` · `DB → FastAPI` · `PUT / DELETE metotları` · `SQL Injection koruması` · `Çalışan kayıt ödevi`

**📋 4 · Logging & Hata Yönetimi**
`logging modülü` · `Log seviyeleri` · `Dosyaya loglama` · `try / except / finally` · `HTTPException` · `Loglayan servis ödevi`

**🎯 5 · Veri Analiz Servisi (Ara Proje)**
`Dosya yükleme (UploadFile)` · `pandas ile CSV analizi` · `DB'de JSON saklama` · `Katmanlı mimari` · `1–4 konularının birleşimi`

</details>

---

## 🛠️ Kurulum

Depoyu klonladıktan sonra gerekli paketleri kurmak için:

```bash
pip install -r requirements.txt
```

`requirements.txt` içeriği:

| 📦 Paket | 🔧 Ne işe yarar? |
|:---|:---|
| `fastapi` | API'leri (endpoint'leri) yazdığımız ana kütüphane |
| `uvicorn` | FastAPI uygulamasını çalıştıran sunucu (ASGI server) |
| `asyncio` | Asenkron programlama için (`async` / `await`) |
| `requests` | Python içinden API'ye istek atıp test etmek için (istemci betikleri) |
| `pandas` | CSV/veri analizi için (5. proje) |
| `python-multipart` | FastAPI'de dosya yükleme için (5. proje) |

---

## ▶️ Bir Örneği Çalıştırma

Klasördeki FastAPI sunucularını genel olarak şu komutla başlatırsın:

```bash
uvicorn dosya_adi:app --reload
```

Örneğin `1_fastapi` klasöründeyken:

```bash
uvicorn main:app --reload
```

Ardından tarayıcıdan:
- **http://127.0.0.1:8000** → uygulamanın ana sayfası
- **http://127.0.0.1:8000/docs** → otomatik Swagger dokümantasyonu (API'yi buradan test edebilirsin)

> Her konunun ayrıntılı çalıştırma adımları ilgili klasörün README'sinde yer alır.

---

## 🗺️ Önerilen Öğrenme Sırası

1. **[1_fastapi](1_fastapi/README.md)** — Önce API'nin temellerini öğren (endpoint, istek/cevap, veri doğrulama).
2. **[2_asenkron_programlama](2_asenkron_programlama/README.md)** — Sonra bu API'leri asenkron hale getirerek performanslı ve ölçeklenebilir yap.
3. **[3_database](3_database/README.md)** — Verileri kalıcı olarak saklamayı öğren (SQLite + CRUD) ve API'ni bir veritabanına bağla.
4. **[4_logging_hata_yönetimi](4_logging_hata_yönetimi/README.md)** — Uygulamanı gözlemlenebilir ve dayanıklı yap: logging ile takip et, hataları çökmeden yönet.
5. **[5_veri_analiz_servisi_projesi](5_veri_analiz_servisi_projesi/README.md)** 🎯 — Öğrendiğin 1–4 konularını tek bir gerçek serviste birleştir (ara proje).

Her klasörü bitirdikten sonra kodları kendin çalıştırıp `/docs` üzerinden denemeni tavsiye ederim — öğrenmenin en iyi yolu deneyerek görmektir. 💪
