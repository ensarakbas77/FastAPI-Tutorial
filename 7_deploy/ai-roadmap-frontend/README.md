# AI Roadmap — Frontend (Streamlit + Docker) 🎨🐳

Bu doküman, `ai-roadmap-frontend` klasörünü anlatır: Streamlit ile yazılmış arayüzün **canlıdaki backend'e** nasıl bağlandığını, Docker ile nasıl paketlendiğini ve Streamlit Cloud'a nasıl deploy edildiğini.

> 🌐 **Canlı Arayüz:** [https://fastapi-tutorial-hykudcuxfuacdr3ceycaj8.streamlit.app/](https://fastapi-tutorial-hykudcuxfuacdr3ceycaj8.streamlit.app/)
> ⚙️ **Bağlandığı Backend:** [https://fastapi-tutorial-dhqf.onrender.com](https://fastapi-tutorial-dhqf.onrender.com)
>
> ⚠️ **Not:** Bu adresler **geçicidir**. Ücretsiz planlarda servisler uykuya geçebilir (ilk açılış 30–60 sn sürebilir) ve adresler ileride değişebilir/kapanabilir.

---

## İçindekiler

1. [Bu Arayüz Ne Yapıyor?](#1-bu-arayüz-ne-yapıyor)
2. [Mimari: İki Ayrı Servis, İki Ayrı Bulut](#2-mimari-i̇ki-ayrı-servis-i̇ki-ayrı-bulut)
3. [Kodun Açıklaması](#3-kodun-açıklaması) — `app.py`
4. [Frontend–Backend Sözleşmesi](#4-frontendbackend-sözleşmesi)
5. [Dockerfile: Backend'den Farkları](#5-dockerfile-backendden-farkları)
6. [Docker Compose Dosyası](#6-docker-compose-dosyası)
7. [Çalıştırma Yolları](#7-çalıştırma-yolları)
8. [Streamlit Cloud ile Deploy](#8-streamlit-cloud-ile-deploy)
9. [Özet Tablo](#9-özet-tablo)

---

## 1. Bu Arayüz Ne Yapıyor?

Kullanıcı bir alan seçer (`yapay_zeka`, `derin_ogrenme`, `nlp`), butona basar; arayüz **canlıdaki FastAPI servisine** istek atar ve dönen yol haritasını numaralı liste olarak gösterir.

```
👤 Kullanıcı alan seçer
        │
        ▼
🎨 Streamlit (Streamlit Cloud'da)
        │  requests.post(...)
        ▼
⚙️ FastAPI (Render'da)
        │  JSON cevap
        ▼
🎨 Streamlit sonucu ekrana basar
```

---

## 2. Mimari: İki Ayrı Servis, İki Ayrı Bulut

Bu projenin en öğretici yanı budur: **frontend ve backend tamamen bağımsız yaşar.**

| | Frontend | Backend |
|--|----------|---------|
| **Teknoloji** | Streamlit | FastAPI |
| **Barındırma** | Streamlit Cloud | Render |
| **Adres** | `...streamlit.app` | `...onrender.com` |
| **Görevi** | Göstermek, girdi almak | Hesaplamak, veri döndürmek |
| **Çalıştırma** | `streamlit run app.py` | `uvicorn main:app` |

> **Neden ayrı?** Böylece birini değiştirmek diğerini etkilemez. Backend'i yeniden yazsan (mesela veritabanı eklesen) arayüz aynı kalır. Arayüzü baştan tasarlasan backend'e dokunmazsın. Bu ayrım, modern web geliştirmenin temelidir.

> **Bağ nedir?** Aralarındaki tek bağ, **HTTP isteği** ve üzerinde anlaştıkları **JSON biçimidir**. Bu anlaşmaya *API sözleşmesi* denir (bkz. [4. bölüm](#4-frontendbackend-sözleşmesi)).

---

## 3. Kodun Açıklaması

📄 [app.py](app.py)

```python
import streamlit as st
import requests

# Canlıdaki backend'in adresi
BACKEND_URL = "https://fastapi-tutorial-dhqf.onrender.com/roadmap"

st.set_page_config(page_title="AI Roadmap", page_icon="🤖", layout="centered")
st.title("AI Yol Haritası Uygulaması")
st.write("Bir alan seçin, ai size hazır yol haritasını sunacaktır.")

# Kullanıcı seçimi
secim = st.selectbox("Alan Seçin", ["yapay_zeka", "derin_ogrenme", "nlp"])

if st.button("Yol Haritasını Getir"):
    try:
        # Backend'e POST isteği at
        response = requests.post(BACKEND_URL, json={"roadmap_name": secim}, timeout=50)
        data = response.json()

        if "error" in data:
            st.error(data["error"])
        else:
            st.success(f"Alan: {data['alan']}")
            st.subheader("Yol Haritası")
            for i, adim in enumerate(data["adımlar"], start=1):
                st.write(f"{i}. {adim}")

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
```

### Dikkat çeken noktalar

**`BACKEND_URL` artık `localhost` değil!**

`6_streamlit` klasöründe `http://localhost:8000` yazıyorduk — çünkü backend kendi bilgisayarımızdaydı. Şimdi backend **internette** olduğu için gerçek bir adres kullanıyoruz. Kod mantığı **hiç değişmedi**, sadece adres değişti.

**`timeout=50` neden bu kadar uzun?**

Render'ın ücretsiz planında servis uykuya geçer. Uyuyan bir servise ilk istek geldiğinde uyanması **30–60 saniye** sürer. Normal bir `timeout=5` kullansaydık, arayüz "zaman aşımı" hatası verirdi. Bu uzun süre, uyanmayı beklemek içindir. 😴

**`enumerate(data["adımlar"], start=1)`**

Listeyi 1'den başlayarak numaralandırır: `1. Metin Ön İşleme`, `2. Word Embedding`... (`start=1` olmasaydı 0'dan başlardı.)

**`try/except` ile hata yakalama**

Backend kapalıysa, adres yanlışsa veya internet yoksa uygulama **çökmez** — kullanıcıya kırmızı bir hata mesajı gösterir.

---

## 4. Frontend–Backend Sözleşmesi

İki servisin anlaşması gereken **4 şey** vardır. Biri bile uyuşmazsa sistem çalışmaz:

| # | Konu | Bu projede |
|---|------|------------|
| 1 | **HTTP metodu** | `POST` |
| 2 | **URL** | `.../roadmap` |
| 3 | **İstek gövdesi (body)** | `{"roadmap_name": "nlp"}` |
| 4 | **Cevap anahtarları** | `{"alan": ..., "adımlar": [...]}` |

Frontend ve backend kodunu yan yana koyalım:

```python
# 🎨 FRONTEND (app.py)
requests.post(BACKEND_URL, json={"roadmap_name": secim})
data["alan"], data["adımlar"]

# ⚙️ BACKEND (main.py)
@app.post("/roadmap")
def get_roadmap(data: RoadmapRequest):     # RoadmapRequest.roadmap_name
    return {"alan": ..., "adımlar": [...]}
```

Gördüğün gibi dört madde de birebir örtüşüyor. ✅

### 💡 Gerçek bir hata hikâyesi

Bu projenin ilk sürümünde frontend şöyleydi:

```python
requests.get(f"{BACKEND_URL}/{secim}", json={"secim": secim})   # ❌
data["roadmap"]                                                  # ❌
```

Sonuç: **404 Not Found**. Çünkü dördü de yanlıştı:
- `GET` gönderiyordu, backend `POST` bekliyordu.
- `/roadmap/nlp` adresine gidiyordu, öyle bir yol yoktu.
- Body anahtarı `secim`'di, backend `roadmap_name` bekliyordu.
- Cevaptan `roadmap` okuyordu, backend `adımlar` döndürüyordu.

> **Ders:** Frontend hatalarının çoğu, arayüzün "yanlış" olmasından değil, **sözleşmeye uymamasından** kaynaklanır. Bir şey çalışmıyorsa önce backend'in Swagger sayfasını (`/docs`) aç ve gerçekte ne beklediğine bak.

---

## 5. Dockerfile: Backend'den Farkları

📄 [Dockerfile](Dockerfile)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
```

> **Docker kavramlarının (imaj, katman, `RUN` vs `CMD`, layer cache) ayrıntılı anlatımı backend README'sindedir:** [../ai-roadmap-backend/README.md](../ai-roadmap-backend/README.md#3-docker-nedir-neden-gerekli)

İlk 6 satır backend ile **birebir aynı**. Tek fark son satırda:

| | Backend | Frontend |
|--|---------|----------|
| **Başlatma komutu** | `uvicorn main:app` | `streamlit run app.py` |
| **Adres bayrağı** | `--host 0.0.0.0` | `--server.address=0.0.0.0` |
| **Port bayrağı** | `--port 8000` | `--server.port=8501` |
| **Varsayılan port** | `8000` | `8501` |

### Neden farklı bayraklar?

Çünkü bunlar **farklı programlar**. `uvicorn` kendi bayrak isimlerini kullanır (`--host`), `streamlit` kendininkini (`--server.address`). İşlevleri aynıdır ama yazımları farklıdır.

### `0.0.0.0` yine kritik

Backend'de olduğu gibi burada da `--server.address=0.0.0.0` şarttır. Streamlit varsayılan olarak sadece `localhost`'u dinler; konteyner içinde bu, dış dünyadan erişilemez demektir.

📄 [requirements.txt](requirements.txt) sadece iki paket içerir:
```
streamlit
requests
```

> Backend'inki `fastapi, uvicorn, pydantic` idi. Her servis **yalnızca kendi ihtiyacını** kurar. İmajlar küçük ve bağımsız kalır.

---

## 6. Docker Compose Dosyası

📄 [docker-compose.yml](docker-compose.yml)

```yaml
version: '3.9'

services:
  frontend:
    build:
      context: .              # Dockerfile'ı bu klasörde ara
      dockerfile: Dockerfile
    container_name: ai-roadmap-frontend
    ports:
      - "8501:8501"           # bilgisayarın_portu : konteyner_portu
```

**Docker Compose**, birden fazla konteyneri tek bir dosyadan yönetmeni sağlar. Tek servis için de kullanılabilir — uzun `docker run` komutlarını ezberlemek yerine `docker compose up` yazarsın.

| Anahtar | Anlamı |
|---------|--------|
| `services` | Çalıştırılacak konteynerler |
| `build.context` | Build klasörü (`.` = burası) |
| `container_name` | Konteynerin görünen adı |
| `ports` | Port eşleme: `dış:iç` |

> **Compose'un ayrıntılı anlatımı** (orkestra şefi benzetmesi, port eşleme, komutlar) backend README'sinde: [7. bölüm](../ai-roadmap-backend/README.md#7-docker-compose-nedir)

### 🎯 Egzersiz: Backend'i de compose'a ekle

Şu an compose sadece frontend'i tanımlıyor. Compose'un asıl gücü çok servisli sistemlerde ortaya çıkar. İkisini birden çalıştırmak istersen:

```yaml
services:
  backend:
    build:
      context: ../ai-roadmap-backend
    ports:
      - "8000:8000"

  frontend:
    build:
      context: .
    ports:
      - "8501:8501"
    depends_on:
      - backend        # önce backend başlasın
```

Sonra tek komut: `docker compose up` → **iki servis birden ayağa kalkar.** 🚀

> Bu durumda `app.py`'deki `BACKEND_URL`'i `http://backend:8000/roadmap` yapman gerekir. Compose, servisleri kendi ağına koyar ve **servis adıyla** birbirlerine erişebilirler — `localhost` değil, `backend`!

---

## 7. Çalıştırma Yolları

### Yöntem 1: Doğrudan (en basit)

```bash
pip install -r requirements.txt
streamlit run app.py
```
Tarayıcı otomatik açılır: `http://localhost:8501`

> Bu şekilde çalıştırdığında bile **canlıdaki Render backend'ine** bağlanır (çünkü `BACKEND_URL` internet adresi). Yani backend'i yerelde çalıştırmana gerek yok.

### Yöntem 2: Docker ile

```bash
docker build -t ai-roadmap-frontend .
docker run -p 8501:8501 ai-roadmap-frontend
```

### Yöntem 3: Docker Compose ile (en kolay)

```bash
docker compose up
```

Durdurmak için: `docker compose down`

---

## 8. Streamlit Cloud ile Deploy

Backend'i **Render**'a koymuştuk. Frontend için **Streamlit Cloud** kullanıyoruz — Streamlit uygulamaları için ücretsiz ve özel olarak tasarlanmış bir platform.

### Adımlar

1. Kodu **GitHub'a** pushla.
2. [share.streamlit.io](https://share.streamlit.io) adresine git, GitHub ile giriş yap.
3. **New app** de ve ayarları gir:

| Ayar | Değer |
|------|-------|
| **Repository** | GitHub repon |
| **Branch** | `main` |
| **Main file path** | `7_deploy/ai-roadmap-frontend/app.py` |

4. **Deploy** de. Streamlit Cloud, `requirements.txt`'i bulur, paketleri kurar ve uygulamayı yayına alır.

> **🔑 Main file path neden kritik?** Repomuzda bir sürü klasör var (`1_fastapi`, `2_asenkron...`). Bu ayar, Streamlit'e **tam olarak hangi dosyayı çalıştıracağını** söyler. Diğer klasörler deploy'u etkilemez.

> **Not:** Streamlit Cloud, Dockerfile'ı **kullanmaz** — kendi ortamını kurar ve `requirements.txt`'e bakar. Dockerfile burada yerel geliştirme ve öğrenme amaçlıdır (ya da Streamlit'i Render/başka bir yerde çalıştırmak istersen işine yarar).

### Canlı adres

🌐 **[https://fastapi-tutorial-hykudcuxfuacdr3ceycaj8.streamlit.app/](https://fastapi-tutorial-hykudcuxfuacdr3ceycaj8.streamlit.app/)**

> ⚠️ **URL geçicidir.** Ücretsiz planlarda:
> - Uygulama bir süre kullanılmazsa **uykuya geçer**; ilk açılışta "waking up" ekranı görürsün.
> - Backend (Render) de uyuyorsa ilk "Yol Haritasını Getir" tıklaması **30–60 saniye** sürebilir. Bozuk değil, uyanıyor! 😴
> - Uygulama silinir veya yeniden oluşturulursa **adres değişir**.

### İki servisi de canlıya alınca dikkat

Frontend'in `BACKEND_URL`'i **canlı** backend'i göstermelidir:

```python
BACKEND_URL = "https://fastapi-tutorial-dhqf.onrender.com/roadmap"   # ✅ canlı
# BACKEND_URL = "http://localhost:8000/roadmap"                      # ❌ Streamlit Cloud'da çalışmaz
```

> Streamlit Cloud'daki uygulama, Google'ın sunucularında çalışır. Oradaki `localhost`, **senin bilgisayarın değil, o sunucunun kendisidir** — ve orada bir backend yoktur. Bu yüzden gerçek bir internet adresi şarttır.

---

## 9. Özet Tablo

| Kavram | Ne işe yarar? | Anahtar |
|--------|---------------|---------|
| **Streamlit çalıştırma** | Arayüzü başlatır | `streamlit run app.py` |
| **BACKEND_URL** | Backend'in adresi | Canlıda gerçek URL, asla `localhost` |
| **requests.post** | Backend'e istek atar | `json={"roadmap_name": secim}` |
| **timeout=50** | Uyuyan servisi beklemek | Render free plan uyanma süresi |
| **API sözleşmesi** | Metot + URL + body + cevap | Dördü de uyuşmalı |
| **Dockerfile (frontend)** | Arayüzü paketler | `CMD ["streamlit", "run", ...]` |
| **`--server.address=0.0.0.0`** | Konteyneri dışa açar | Streamlit'in `--host` karşılığı |
| **`--server.port=8501`** | Streamlit varsayılan portu | Backend `8000`, frontend `8501` |
| **docker compose up** | Servisleri tek komutla başlatır | `docker-compose.yml` |
| **Streamlit Cloud** | Ücretsiz Streamlit barındırma | `Main file path` ayarı |

---

## 🧠 Kritik Hatırlatmalar

- **Canlıda `localhost` kullanma** → backend'in gerçek internet adresini yaz.
- **`--server.address=0.0.0.0`** → Docker'da arayüze dışarıdan erişilebilsin.
- **Sözleşmeye uy** → metot, URL, body anahtarı, cevap anahtarı; dördü de eşleşmeli.
- **`timeout` cömert olsun** → ücretsiz servisler uyanmak için zaman ister.
- **Her servisin kendi `requirements.txt`'i** → imajlar küçük ve bağımsız kalır.
- **Streamlit Cloud Dockerfile'ı okumaz** → `requirements.txt` ve `Main file path` ile çalışır.

---

## İlgili Dokümanlar

- ⚙️ **Backend README** (Docker'ın derinlemesine anlatımı) → [../ai-roadmap-backend/README.md](../ai-roadmap-backend/README.md)
- 📚 **Ana sayfa** → [../../README.md](../../README.md)

---

## Tebrikler! 🎉

Bu noktada **uçtan uca bir yapay zeka ürünü** yayınladın: kullanıcının tarayıcıdan girdiği arayüz bir bulutta, veriyi işleyen servis başka bir bulutta, ikisi HTTP üzerinden konuşuyor. Bu, gerçek dünyadaki uygulamaların tam olarak çalışma şeklidir.

**Küçük tavsiye:** Canlı arayüzü telefonundan aç ve arkadaşına linki gönder. Yazdığın kodun, senin bilgisayarın kapalıyken bile dünyanın herhangi bir yerinden çalıştığını görmek — işte deployment'ın büyüsü budur. 🌍💪
