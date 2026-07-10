# AI Roadmap — Backend (FastAPI + Docker) 🐳⚙️

Bu doküman, `ai-roadmap-backend` klasörünü ve onun üzerinden **Docker** ile **deployment (canlıya alma)** konularını **sıfırdan** anlatır. Amaç: "Docker nedir, Dockerfile'daki her satır ne işe yarar, uygulamamı internete nasıl açarım?" sorularının hiç bilmeyen birinin kafasında net oturmasıdır.

> 🌐 **Canlı Servis:** [https://fastapi-tutorial-dhqf.onrender.com](https://fastapi-tutorial-dhqf.onrender.com)
> 📖 **Swagger:** [https://fastapi-tutorial-dhqf.onrender.com/docs](https://fastapi-tutorial-dhqf.onrender.com/docs)
>
> ⚠️ **Not:** Bu adresler **geçicidir**. Ücretsiz Render planında kullanılmadığı zaman servis uykuya geçer (ilk istek 30–60 saniye sürebilir) ve adres ileride kapanabilir/değişebilir.

---

## İçindekiler

1. [Bu Servis Ne Yapıyor?](#1-bu-servis-ne-yapıyor)
2. [Kodun Açıklaması](#2-kodun-açıklaması) — `main.py`
3. [Docker Nedir? Neden Gerekli?](#3-docker-nedir-neden-gerekli)
4. [Docker Temel Kavramları](#4-docker-temel-kavramları)
5. [Dockerfile: Satır Satır Açıklama](#5-dockerfile-satır-satır-açıklama)
6. [`.dockerignore` Nedir?](#6-dockerignore-nedir)
7. [Docker Compose Nedir?](#7-docker-compose-nedir)
8. [Yerelde Docker ile Çalıştırma](#8-yerelde-docker-ile-çalıştırma)
9. [Render ile Canlıya Alma (Deploy)](#9-render-ile-canlıya-alma-deploy)
10. [Özet Tablo](#10-özet-tablo)

---

## 1. Bu Servis Ne Yapıyor?

Basit bir **AI yol haritası API'si**. Kullanıcı bir alan adı gönderir (`yapay_zeka`, `derin_ogrenme`, `nlp`), servis o alana ait öğrenme adımlarını döndürür.

### Endpoint'ler

| Metot | Yol | Ne yapar? |
|-------|-----|-----------|
| `GET` | `/` | Servisin ayakta olduğunu doğrular |
| `POST` | `/roadmap` | Seçilen alanın yol haritasını döndürür |

### Örnek istek/cevap

**İstek** (`POST /roadmap`):
```json
{ "roadmap_name": "nlp" }
```

**Cevap:**
```json
{
  "alan": "nlp",
  "adımlar": [
    "Metin Ön İşleme",
    "Word Embedding",
    "RNN ve LSTM ile NLP",
    "Transformer",
    "RAG ve Chatbot Projeleri"
  ]
}
```

---

## 2. Kodun Açıklaması

📄 [main.py](main.py)

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Veriyi bir sözlükte tutuyoruz (veritabanı yerine — basit tutmak için)
ROADMAPS = {
    "yapay_zeka": ["Python Temelleri", "Veri Analizi", ...],
    "derin_ogrenme": ["Python ve NumPy", "Yapay Sinir Ağları", ...],
    "nlp": ["Metin Ön İşleme", "Word Embedding", ...]
}

# Gelen isteğin yapısı (Pydantic doğrulaması)
class RoadmapRequest(BaseModel):
    roadmap_name: str

@app.get("/")
def home():
    return {"message": "AI Roadmap API"}

@app.post("/roadmap")
def get_roadmap(data: RoadmapRequest):
    roadmap_name = data.roadmap_name.lower()   # "NLP" de "nlp" de çalışsın
    if roadmap_name not in ROADMAPS:
        return {"error": "Geçersiz seçim"}
    return {"alan": roadmap_name, "adımlar": ROADMAPS[roadmap_name]}
```

Burada yeni bir şey yok — `1_fastapi`'de öğrendiğimiz her şey: `FastAPI` nesnesi, Pydantic modeli, GET/POST endpoint'leri.

> **Bu bölümün asıl konusu kod değil, o kodu dünyaya nasıl açtığımızdır.** Şimdi Docker'a geçiyoruz.

---

## 3. Docker Nedir? Neden Gerekli?

### Klasik problem: "Ama benim bilgisayarımda çalışıyordu!" 😩

Bir uygulama yazdın, senin bilgisayarında mükemmel çalışıyor. Arkadaşına gönderdin, çalışmadı. Neden?

- Onda Python 3.9 var, sende 3.11.
- Sende `fastapi` kurulu, onda değil.
- Sen Windows'tasın, sunucu Linux.

Her ortam farklıdır ve bu farklar uygulamayı bozar.

### Docker'ın çözümü: Konteyner

**Docker**, uygulamanı **ihtiyaç duyduğu her şeyle birlikte** (Python sürümü, kütüphaneler, ayarlar) tek bir paket haline getirir. Bu pakete **konteyner (container)** denir. Konteyner nereye gönderilirse gönderilsin **aynı şekilde** çalışır.

> **Benzetme:** Docker, bir **nakliye konteyneridir** 🚢. İçine ne koyduğun önemli değil — gemi, tır, tren, hepsi aynı standart kutuyu taşır. Limanın konteynerin içindekiyle ilgilenmesi gerekmez. Docker da aynısını yazılım için yapar: uygulaman, bağımlılıkları ve işletim sistemi ayarları tek bir standart kutuya girer. O kutu senin dizüstünde de, Render'ın sunucusunda da tıpatıp aynı davranır.

### Sanal makineden farkı ne?

| | Sanal Makine (VM) | Docker Konteyneri |
|--|-------------------|-------------------|
| İçinde ne var? | **Tam bir işletim sistemi** | Sadece uygulama + bağımlılıkları |
| Boyut | Gigabaytlar | Megabaytlar |
| Açılış süresi | Dakikalar | Saniyeler |

Konteyner, ana makinenin işletim sistemi çekirdeğini **paylaşır** — bu yüzden çok daha hafif ve hızlıdır.

---

## 4. Docker Temel Kavramları

Docker'da üç temel kavram vardır. Sırayla ilerlerler:

```
📄 Dockerfile   →   📦 Image (İmaj)   →   🚢 Container (Konteyner)
   (tarif)            (dondurulmuş paket)     (çalışan uygulama)
```

| Kavram | Nedir? | Benzetme |
|--------|--------|----------|
| **Dockerfile** | Paketin nasıl kurulacağını anlatan **tarif dosyası** | Yemek tarifi 📝 |
| **Image (İmaj)** | Tariften üretilen, çalıştırılmaya hazır **dondurulmuş paket** | Dondurulmuş hazır yemek 🧊 |
| **Container** | İmajın **çalışan** hali | Isıtılıp servis edilen yemek 🍽️ |

> Aynı tariften (Dockerfile) sınırsız sayıda hazır yemek (image) üretebilirsin; aynı hazır yemekten sınırsız porsiyon (container) çalıştırabilirsin.

### Temel komutlar

| Komut | Ne yapar? |
|-------|-----------|
| `docker build -t isim .` | Dockerfile'dan **imaj üretir** |
| `docker run -p 8000:8000 isim` | İmajdan **konteyner çalıştırır** |
| `docker ps` | Çalışan konteynerleri listeler |
| `docker stop <id>` | Konteyneri durdurur |
| `docker images` | İmajları listeler |

---

## 5. Dockerfile: Satır Satır Açıklama

📄 [Dockerfile](Dockerfile)

Şimdi bu projenin Dockerfile'ını **her satırını açıklayarak** inceleyelim:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5.1 `FROM python:3.11-slim`

> **Temel imajı belirler.** "Sıfırdan başlamıyorum, içinde Python 3.11 kurulu hazır bir kutudan başlıyorum" demektir.

- `python:3.11` → Docker Hub'daki resmi Python imajı.
- `-slim` → Gereksiz araçlar çıkarılmış, **küçültülmüş** sürüm. İmajın boyutu ~1GB yerine ~150MB olur. Daha hızlı indirilir, daha hızlı deploy olur.

### 5.2 `WORKDIR /app`

> **Konteyner içindeki çalışma klasörünü belirler.**

Bundan sonraki tüm komutlar `/app` klasöründe çalışır. `cd /app` yapmak gibidir, ama kalıcıdır. Klasör yoksa otomatik oluşturulur.

### 5.3 `COPY requirements.txt .`

> **Sadece `requirements.txt` dosyasını** konteynerin içine (`.` yani `/app`) kopyalar.

**🧠 Neden önce sadece bu dosya? Neden tüm proje değil?**

Bu, Docker'ın **katman önbelleği (layer cache)** özelliğinden faydalanan zekice bir numaradır:

- Docker her satırı bir **katman** olarak saklar. Bir satır değişmediyse, o katmanı **yeniden çalıştırmaz**, önbellekten alır.
- Paket kurulumu (`pip install`) yavaş bir işlemdir (dakikalar sürebilir).
- Eğer önce tüm projeyi kopyalasaydık, `main.py`'de tek bir harf değiştirdiğinde Docker "dosyalar değişti" der ve **tüm paketleri baştan kurar**. 😫
- Ama sadece `requirements.txt`'i kopyalayıp paketleri kurarsak: `main.py` değiştiğinde `requirements.txt` **değişmemiştir**, Docker paket kurulum katmanını önbellekten alır ve **saniyeler içinde** yeni imaj üretir. 🚀

> Bu, Dockerfile yazmanın en önemli optimizasyon kuralıdır: **az değişen şeyleri üste, çok değişen şeyleri alta yaz.**

### 5.4 `RUN pip install --no-cache-dir -r requirements.txt`

> **İmaj üretilirken** (build sırasında) çalışır ve paketleri kurar.

- `RUN` → Build zamanında çalışan komut.
- `--no-cache-dir` → pip'in indirdiği paketleri önbellekte tutmasını engeller. İmaj boyutunu küçültür (konteyner içinde o önbelleğe zaten ihtiyacımız yok).

Bu projede kurulan paketler ([requirements.txt](requirements.txt)):
```
fastapi
uvicorn
pydantic
```

> **Dikkat:** Bu, kök dizindeki şişkin `requirements.txt`'ten (pandas, streamlit içeren) farklıdır. Backend'in sadece bu 3 pakete ihtiyacı var — imaj küçük kalır.

### 5.5 `COPY . .`

> **Projenin geri kalan tüm dosyalarını** konteynere kopyalar.

İlk `.` = senin bilgisayarındaki mevcut klasör. İkinci `.` = konteyner içindeki `/app`.
(`.dockerignore`'da listelenen dosyalar **hariç** — bkz. bir sonraki bölüm.)

### 5.6 `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`

> **Konteyner ayağa kalktığında çalışacak komut.**

`RUN` ile farkını iyi anla:

| | `RUN` | `CMD` |
|--|-------|-------|
| Ne zaman çalışır? | İmaj **üretilirken** (build) | Konteyner **başlatılırken** (run) |
| Kaç kez? | Her satır bir kez | Dockerfile'da sadece bir tane olur |
| Örnek | `pip install ...` | `uvicorn main:app ...` |

**`--host 0.0.0.0` neden kritik?**

Bu, deployment'ta en sık yapılan hatadır:

- `127.0.0.1` (localhost) → "sadece **bu makinenin içinden** bağlanılabilir" demektir. Konteyner içinde bunu kullanırsan, dış dünya (Render, tarayıcın) uygulamana **erişemez**.
- `0.0.0.0` → "**her ağ arayüzünden** bağlantı kabul et" demektir. Konteynerin kapısını dışarıya açar.

> **Benzetme:** `127.0.0.1` odanın içinde bağırmaktır — sadece sen duyarsın. `0.0.0.0` pencereyi açıp bağırmaktır — dışarıdakiler de duyar. Konteynerde her zaman pencereyi açmalısın.

---

## 6. `.dockerignore` Nedir?

📄 [.dockerignore](.dockerignore)

`COPY . .` komutu "her şeyi kopyala" der. Ama bazı şeyleri **kopyalamak istemeyiz**. `.dockerignore`, tıpkı `.gitignore` gibi, hariç tutulacakları listeler:

```
__pycache__
*.pyc
.git
venv
.venv
```

| Hariç tutulan | Neden? |
|---------------|--------|
| `__pycache__`, `*.pyc` | Python'un derlenmiş ara dosyaları — gereksiz, konteyner kendi üretir |
| `.git` | Tüm proje geçmişi — devasa boyut, konteynerde işe yaramaz |
| `venv`, `.venv` | Senin bilgisayarındaki sanal ortam — konteynerin kendi ortamı var, çakışır |

**Faydaları:** Daha küçük imaj, daha hızlı build, daha güvenli (gizli dosyalar sızmaz).

---

## 7. Docker Compose Nedir?

Şu ana kadar **tek bir konteyner** çalıştırdık. Peki gerçek bir uygulamada birden fazla parça varsa?

Bu projede iki parça var:
- 🎨 **Frontend** (Streamlit) → 8501 portu
- ⚙️ **Backend** (FastAPI) → 8000 portu

Bunları tek tek elle başlatmak zahmetlidir:

```bash
# Elle yapmak (yorucu 😩)
docker build -t backend ./ai-roadmap-backend
docker run -p 8000:8000 backend
# ...sonra başka terminalde...
docker build -t frontend ./ai-roadmap-frontend
docker run -p 8501:8501 frontend
```

### Compose'un çözümü

**Docker Compose**, birden fazla konteyneri **tek bir YAML dosyasında** tanımlayıp **tek komutla** yönetmeni sağlar.

> **Benzetme:** Dockerfile bir **müzisyenin nota kağıdıdır** 🎻. Docker Compose ise **orkestra şefidir** 🎼 — hangi müzisyen ne zaman, nasıl çalacak, hepsini bir arada yönetir.

### Bu projedeki compose dosyası

📄 `../ai-roadmap-frontend/docker-compose.yml`

```yaml
version: '3.9'

services:
  frontend:
    build:
      context: .           # Dockerfile'ı bu klasörde ara
      dockerfile: Dockerfile
    container_name: ai-roadmap-frontend
    ports:
      - "8501:8501"
```

| Anahtar | Ne yapar? |
|---------|-----------|
| `version` | Compose dosya biçiminin sürümü |
| `services` | Çalıştırılacak konteynerlerin listesi |
| `frontend` | Servisin adı (istediğin ismi verebilirsin) |
| `build.context` | Build'in yapılacağı klasör (`.` = bulunduğun klasör) |
| `build.dockerfile` | Kullanılacak Dockerfile'ın adı |
| `container_name` | Çalışan konteynerin görünen adı |
| `ports: "8501:8501"` | **Port eşleme** → `bilgisayarın_portu : konteyner_portu` |

### Port eşlemeyi anlamak: `"8501:8501"`

```
   8501            :            8501
   ↑                            ↑
Senin bilgisayarın        Konteynerin içi
(tarayıcıdan gireceğin)   (uygulamanın dinlediği)
```

Konteyner izole bir kutudur — içindeki 8501 portuna dışarıdan doğrudan erişilemez. Bu satır, "bilgisayarımın 8501 portuna gelen her şeyi konteynerin 8501 portuna yönlendir" der. **Kutunun duvarına açılan bir kapıdır.**

> İki taraf farklı da olabilir: `"3000:8501"` yazsaydın, tarayıcıdan `localhost:3000`'e girer ama konteyner içinde uygulama yine 8501'de çalışırdı.

### Compose komutları

| Komut | Ne yapar? |
|-------|-----------|
| `docker compose up` | Tüm servisleri build edip başlatır |
| `docker compose up -d` | Aynısı, ama arka planda (detached) |
| `docker compose down` | Tüm servisleri durdurur ve siler |
| `docker compose logs` | Servislerin loglarını gösterir |

> **Not:** Bu projede compose dosyası sadece frontend servisini tanımlıyor. İstersen backend'i de aynı dosyaya ikinci bir servis olarak ekleyebilirsin — Compose'un asıl gücü orada ortaya çıkar.

---

## 8. Yerelde Docker ile Çalıştırma

### Yöntem 1: Docker olmadan (klasik)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Tarayıcı: `http://127.0.0.1:8000/docs`

### Yöntem 2: Docker ile

```bash
# 1. İmajı üret (bu klasördeyken)
docker build -t ai-roadmap-backend .

# 2. Konteyneri çalıştır
docker run -p 8000:8000 ai-roadmap-backend
```
Tarayıcı: `http://127.0.0.1:8000/docs`

| Komut parçası | Anlamı |
|---------------|--------|
| `-t ai-roadmap-backend` | İmaja bir isim (tag) ver |
| `.` (sondaki nokta) | Dockerfile'ı bu klasörde ara |
| `-p 8000:8000` | Port eşleme (bilgisayar:konteyner) |

---

## 9. Render ile Canlıya Alma (Deploy)

**Deployment (canlıya alma)**, uygulamanı senin bilgisayarından çıkarıp internetteki bir sunucuda çalıştırmaktır. Böylece herkes erişebilir.

**Render**, GitHub reponu bağlayıp otomatik deploy eden bir bulut platformudur.

### Adımlar

1. Kodu **GitHub'a** pushla.
2. Render'da **New → Web Service** de, reponu seç.
3. Ayarları yap:

| Ayar | Değer |
|------|-------|
| **Root Directory** | `7_deploy/ai-roadmap-backend` |
| **Runtime** | `Docker` |
| **Instance Type** | `Free` |

4. **Deploy** de. Render Dockerfile'ı bulur, imajı üretir, konteyneri çalıştırır.

> **🔑 Root Directory neden kritik?** Repomuzda `1_fastapi`, `2_asenkron...` gibi bir sürü klasör var. Bu ayar sayesinde Render **sadece** backend klasörüne bakar. Diğer klasörler deploy'u etkilemez.

### Canlı adres

🌐 **[https://fastapi-tutorial-dhqf.onrender.com](https://fastapi-tutorial-dhqf.onrender.com)**

Swagger dokümantasyonu: **[/docs](https://fastapi-tutorial-dhqf.onrender.com/docs)**

> ⚠️ **URL geçicidir.** Bu ücretsiz bir Render servisidir:
> - 15 dakika istek gelmezse servis **uykuya geçer**. Sonraki ilk istek servisi uyandırır ve **30–60 saniye** sürebilir. Sabırlı ol, bozuk değil! 😴
> - Servis silinir veya yeniden oluşturulursa **adres değişir**.
> - Bu yüzden bu adresi kalıcı bir yere gömme; frontend'de değişken olarak tut.

### ⚠️ Deploy'da en sık iki hata

**1. `--host 127.0.0.1` kullanmak**
Konteyner dışına açılmaz, Render erişemez. Her zaman `0.0.0.0` kullan. ✅ (Bizim Dockerfile'ımızda doğru.)

**2. Sabit port kullanmak**
Render, servisine bir `PORT` ortam değişkeni atar ve uygulamanın **o porta** bağlanmasını bekler. Bizim Dockerfile'ımız `8000`'e sabitlenmiş:

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Render bunu şu an algılayıp çalıştırıyor, ama garantili yöntem `$PORT` kullanmaktır:

```dockerfile
# Daha güvenli sürüm
ENV PORT=8000
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
```

> **Neden köşeli parantezler kalktı?** `CMD ["...", "..."]` biçimi **exec form**'dur ve ortam değişkenlerini **genişletmez** — `$PORT` harfiyen `"$PORT"` metni olarak geçer. Parantezsiz **shell form** ise bir kabuk başlatır ve `$PORT` gerçek değerine dönüşür.

---

## 10. Özet Tablo

| Kavram | Ne işe yarar? | Anahtar |
|--------|---------------|---------|
| **Docker** | Uygulamayı bağımlılıklarıyla paketler | "Bende çalışıyordu" sorununu çözer |
| **Dockerfile** | İmajın tarifi | `FROM`, `RUN`, `COPY`, `CMD` |
| **Image** | Dondurulmuş, çalıştırılabilir paket | `docker build -t isim .` |
| **Container** | İmajın çalışan hali | `docker run -p 8000:8000 isim` |
| **FROM** | Temel imaj | `FROM python:3.11-slim` |
| **WORKDIR** | Konteyner içi çalışma klasörü | `WORKDIR /app` |
| **COPY** | Dosya kopyalar | `COPY . .` |
| **RUN** | Build sırasında çalışır | `RUN pip install ...` |
| **CMD** | Konteyner başlarken çalışır | `CMD ["uvicorn", ...]` |
| **Layer cache** | Değişmeyen katmanları tekrar kullanır | Önce `requirements.txt` kopyala |
| **.dockerignore** | Kopyalanmayacak dosyalar | `__pycache__`, `.git`, `.venv` |
| **Docker Compose** | Çok konteynerli sistemi tek dosyadan yönetir | `docker compose up` |
| **Port eşleme** | Dış dünyayı konteynere bağlar | `"8501:8501"` |
| **`0.0.0.0`** | Konteyneri dışarı açar | `--host 0.0.0.0` |
| **Render** | Bulutta otomatik deploy | `Root Directory` ayarı |

---

## 🧠 Kritik Hatırlatmalar

- **`--host 0.0.0.0`** → konteynerde asla `127.0.0.1` kullanma, dışarıdan erişilemez.
- **Önce `requirements.txt`, sonra `COPY . .`** → layer cache sayesinde build'ler saniyeler sürer.
- **`-slim` imaj kullan** → boyut 1GB yerine ~150MB olur.
- **`.dockerignore` yaz** → `.git` ve `.venv` konteynere sızmasın.
- **Render'da `Root Directory`** → monorepo'da (çok klasörlü repo) doğru klasörü göster.
- **`$PORT` kullan** → platformun atadığı porta bağlan, sabitleme.

---

## İlgili Dokümanlar

- 🎨 **Frontend README** → [../ai-roadmap-frontend/README.md](../ai-roadmap-frontend/README.md)
- 📚 **Ana sayfa** → [../../README.md](../../README.md)

---

## Tebrikler! 🎉

Artık bir uygulamayı **sadece yazmakla kalmıyor**, onu paketleyip (Docker) dünyaya açabiliyorsun (Render). Bu, "kod yazan biri" ile "ürün çıkaran biri" arasındaki farktır.

**Küçük tavsiye:** `main.py`'de bir kelimeyi değiştir ve `docker build` komutunu tekrar çalıştır. Docker'ın `pip install` adımını **atlayıp** önbellekten aldığını (`CACHED` yazısı) göreceksin. Layer cache'in gücünü o an anlarsın. 💪
