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

| # | Konu | İçerik | Doküman |
|---|------|--------|---------|
| 1 | **FastAPI'ye Giriş** | Endpoint, GET/POST, path & query parametreleri, Pydantic, hata yönetimi, status code, Swagger | [📖 1_fastapi/README.md](1_fastapi/README.md) |
| 2 | **Asenkron Programlama** | Senkron vs asenkron, `async`/`await`, `asyncio.gather`, I/O-bound işlemler, sık yapılan hatalar, `requests` ile test, mini chatbot projesi | [📖 2_asenkron_programlama/README.md](2_asenkron_programlama/README.md) |

> Her klasörün README'si o konuyu benzetmeler, örnek kodlar ve "nasıl çalıştırırım?" adımlarıyla tek tek anlatır.

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

Her klasörü bitirdikten sonra kodları kendin çalıştırıp `/docs` üzerinden denemeni tavsiye ederim — öğrenmenin en iyi yolu deneyerek görmektir. 💪
