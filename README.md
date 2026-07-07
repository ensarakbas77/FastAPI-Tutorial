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

<br>

### 🚀 1 · FastAPI'ye Giriş

> API'nin temelleri: ilk endpoint'ten veri doğrulamaya.

`Endpoint` &nbsp;·&nbsp; `GET / POST` &nbsp;·&nbsp; `Path & Query parametreleri` &nbsp;·&nbsp; `Pydantic` &nbsp;·&nbsp; `Hata yönetimi` &nbsp;·&nbsp; `Status Code` &nbsp;·&nbsp; `Swagger`

**📖 [Dokümanı aç →](1_fastapi/README.md)**

<br>

### ⚡ 2 · Asenkron Programlama

> Sunucuyu kilitlemeden, aynı anda birden fazla işi yürütmek.

`Senkron vs Asenkron` &nbsp;·&nbsp; `async / await` &nbsp;·&nbsp; `asyncio.gather` &nbsp;·&nbsp; `I/O-bound işlemler` &nbsp;·&nbsp; `requests ile test` &nbsp;·&nbsp; `Mini chatbot projesi`

**📖 [Dokümanı aç →](2_asenkron_programlama/README.md)**

<br>

### 🗄️ 3 · Veritabanı (Database)

> Verileri kalıcı olarak saklamak ve API'ye bağlamak.

`SQLite` &nbsp;·&nbsp; `SQL` &nbsp;·&nbsp; `CRUD` &nbsp;·&nbsp; `DB → FastAPI` &nbsp;·&nbsp; `PUT / DELETE metotları` &nbsp;·&nbsp; `SQL Injection koruması` &nbsp;·&nbsp; `Çalışan kayıt ödevi`

**📖 [Dokümanı aç →](3_database/README.md)**

---

## 🛠️ Kurulum

Depoyu klonladıktan sonra gerekli paketleri kurmak için:

```bash
pip install -r requirements.txt
```

`requirements.txt` içeriği:

| Paket | Ne işe yarar? |
|-------|---------------|
| `fastapi` | API'leri yazdığımız ana kütüphane |
| `uvicorn` | FastAPI uygulamasını çalıştıran sunucu |
| `asyncio` | Python'un yerleşik asenkron kütüphanesi |

> **Not:** `2_asenkron_programlama` klasöründeki bazı istemci betikleri `requests` kütüphanesini kullanır. Gerekirse: `pip install requests`

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
3. **[3_database](3_database/README.md)** — En son verileri kalıcı olarak saklamayı öğren (SQLite + CRUD) ve API'ni bir veritabanına bağla.

Her klasörü bitirdikten sonra kodları kendin çalıştırıp `/docs` üzerinden denemeni tavsiye ederim — öğrenmenin en iyi yolu deneyerek görmektir. 💪
