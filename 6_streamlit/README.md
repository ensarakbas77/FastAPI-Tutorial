# Streamlit ile Arayüz Geliştirme 🎨🖥️

Bu doküman, `6_streamlit` klasöründeki dosyalarda anlatılan konuları **sıfırdan** açıklamak için hazırlanmıştır. Amaç: "Streamlit nedir, FastAPI'den farkı ne, ikisi birlikte nasıl çalışır?" sorularının hiç bilmeyen birinin kafasında net oturmasıdır.

> **Ön koşul:** `1_fastapi` → `5_veri_analiz_servisi_projesi` klasörlerini bitirmiş olman gerekir. Burada ilk kez **arayüz (frontend)** yazıp onu daha önce öğrendiğimiz FastAPI servislerine bağlayacağız.

---

## İçindekiler

1. [Streamlit Nedir?](#1-streamlit-nedir)
2. [Frontend vs Backend: En Önemli Kavram](#2-frontend-vs-backend-en-önemli-kavram)
3. [Kurulum ve Çalıştırma](#3-kurulum-ve-çalıştırma)
4. [Streamlit Nasıl Çalışır? (Rerun Mantığı)](#4-streamlit-nasıl-çalışır-rerun-mantığı)
5. [Temel Bileşenler](#5-temel-bileşenler) — `streamlit_temel_bilesenler.py`
6. [Proje 1: Görüntüden Hastalık Tespiti](#6-proje-1-görüntüden-hastalık-tespiti) — `main.py` + `app.py`
7. [Proje 2 (Ödev): Film Yorumu Duygu Analizi](#7-proje-2-ödev-film-yorumu-duygu-analizi) — `film_odevi_main.py` + `film_odevi_app.py`
8. [İki Projenin Karşılaştırması](#8-i̇ki-projenin-karşılaştırması)
9. [Özet Tablo](#9-özet-tablo)

---

## 1. Streamlit Nedir?

**Streamlit**, Python ile **web arayüzü (kullanıcı ekranı)** geliştirmeni sağlayan bir framework'tür. HTML, CSS veya JavaScript bilmene gerek yoktur — sadece Python yazarsın, Streamlit onu bir web sayfasına çevirir.

### Neden yapay zeka ve veri bilimi projelerinde kullanılır?

- ⚡ **Hızlı prototip** — bir modeli birkaç satırla arayüze bağlarsın.
- 🤖 **Model tahmini gösterme** — eğittiğin modelin çıktısını görsel olarak sunarsın.
- 💬 **Chatbot arayüzleri** — LLM uygulamaları için ideal.
- 📊 **Veri görselleştirme** — tabloları, grafikleri kolayca gösterirsin.

> **Benzetme:** FastAPI **mutfaktır** (yemeği pişirir, kimse görmez). Streamlit ise **restoranın salonudur** (müşterinin gördüğü, oturduğu, sipariş verdiği yer). İkisi birlikte tam bir restoran eder.

---

## 2. Frontend vs Backend: En Önemli Kavram

Bu klasörün **anahtarı** bu ayrımı anlamaktır:

| | **Backend** (Arka uç) | **Frontend** (Ön uç) |
|--|----------------------|----------------------|
| **Araç** | FastAPI | Streamlit |
| **Görevi** | Veriyi işler, hesaplar, saklar | Kullanıcıya gösterir, girdi alır |
| **Kullanıcı görür mü?** | ❌ Hayır (perde arkası) | ✅ Evet (ekran) |
| **Çalıştırma** | `uvicorn main:app --reload` | `streamlit run app.py` |
| **Adres** | `http://127.0.0.1:8000` | `http://localhost:8501` |

### Nasıl haberleşirler?

Streamlit, FastAPI'ye tıpkı önceki bölümlerdeki `client.py` gibi **`requests` ile HTTP isteği atar**:

```
👤 Kullanıcı  →  🎨 Streamlit (arayüz)  →  requests.post()  →  ⚙️ FastAPI (backend)
                                                                      │
👤 Kullanıcı  ←  🎨 Streamlit (sonucu gösterir)  ←   JSON cevap  ←────┘
```

> **Kritik nokta:** Bu iki program **ayrı ayrı çalışır**. İki farklı terminal açman gerekir. Backend kapalıyken Streamlit'te "Tahmin Et"e basarsan bağlantı hatası alırsın.

---

## 3. Kurulum ve Çalıştırma

### Gerekli paketler

```bash
pip install streamlit fastapi uvicorn requests pandas pillow
```

| Paket | Ne işe yarar? |
|-------|---------------|
| `streamlit` | Arayüzü oluşturur |
| `pillow` (`PIL`) | Görüntü açma/gösterme (`app.py`'de kullanılıyor) |

> `pillow`, Streamlit ile birlikte otomatik kurulur; ayrıca kurmana genelde gerek kalmaz.

### ⚠️ Streamlit farklı bir komutla çalışır

Şimdiye kadar hep `uvicorn` kullandık. Streamlit dosyaları **farklı** bir komutla çalışır:

```bash
streamlit run dosya_adi.py
```

Komut çalışınca tarayıcı otomatik açılır: **http://localhost:8501**

### Klasördeki dosyalar

| Dosya | Türü | Nasıl çalıştırılır? |
|-------|------|---------------------|
| `streamlit_temel_bilesenler.py` | Streamlit (öğrenme) | `streamlit run streamlit_temel_bilesenler.py` |
| `main.py` | FastAPI backend (Proje 1) | `uvicorn main:app --reload` |
| `app.py` | Streamlit frontend (Proje 1) | `streamlit run app.py` |
| `film_odevi_main.py` | FastAPI backend (Proje 2) | `uvicorn film_odevi_main:app --reload` |
| `film_odevi_app.py` | Streamlit frontend (Proje 2) | `streamlit run film_odevi_app.py` |

> **Unutma:** Projelerde **iki terminal** gerekir — biri backend (`uvicorn`), biri frontend (`streamlit`).

---

## 4. Streamlit Nasıl Çalışır? (Rerun Mantığı)

Streamlit'in en şaşırtıcı ama en önemli özelliği şudur:

> **Kullanıcı bir şeye her dokunduğunda (butona basma, metin yazma, seçim yapma), Streamlit tüm betiği baştan sona YENİDEN çalıştırır.**

Yani `app.py` dosyan yukarıdan aşağıya tekrar tekrar okunur. Bu yüzden Streamlit kodu, normal bir Python betiği gibi **düz ve sırayla** yazılır — karmaşık olay dinleyicileri (event listener) yoktur.

```python
if st.button("Gönder"):      # butona basılınca betik yeniden çalışır
    st.write("Merhaba!")     # ve bu satır artık True olur
```

Bu model sayesinde arayüz yazmak çok basitleşir: sadece "ekranda ne olsun?" diye düşünürsün, Streamlit gerisini halleder.

---

## 5. Temel Bileşenler

📄 İlgili dosya: [streamlit_temel_bilesenler.py](streamlit_temel_bilesenler.py) — `streamlit run streamlit_temel_bilesenler.py`

Bu dosya, Streamlit'in tüm temel yapı taşlarını tek sayfada gösterir.

### 5.1 Sayfa ayarları

Her Streamlit uygulamasının ilk satırı sayfa yapılandırmasıdır:

```python
st.set_page_config(
    page_title="Streamlit Temel Bileşenler",   # tarayıcı sekmesinde görünen isim
    page_icon=":guardsman:",                    # sekme ikonu (emoji de olur: "🩺")
    layout="wide",                              # "wide" (geniş) veya "centered" (ortalı)
    initial_sidebar_state="expanded"            # yan menü açık başlasın
)
```

> **Kural:** `set_page_config` **ilk Streamlit komutu** olmalıdır, yoksa hata alırsın.

### 5.2 Başlık ve metinler

| Kod | Ne yapar? |
|-----|-----------|
| `st.title("...")` | En büyük başlık |
| `st.header("...")` | Orta başlık |
| `st.subheader("...")` | Küçük başlık |
| `st.write("...")` | Genel amaçlı yazdırma (metin, tablo, sayı — her şeyi anlar) |
| `st.markdown("---")` | Yatay ayraç çizgisi |

> `st.write()` Streamlit'in İsviçre çakısıdır: içine ne verirsen (metin, DataFrame, sözlük) uygun şekilde gösterir.

### 5.3 Girdi bileşenleri

Kullanıcıdan veri almanın yolları. **Her biri girilen değeri döndürür**, onu bir değişkene atarsın:

| Bileşen | Ne için? | Örnek |
|---------|----------|-------|
| `st.text_input()` | Tek satır metin | `name = st.text_input("Ad:")` |
| `st.text_area()` | Çok satır metin | `about = st.text_area("Hakkında:", height=120)` |
| `st.number_input()` | Sayı (min/max/step ile) | `age = st.number_input("Yaş:", min_value=0, max_value=120)` |
| `st.selectbox()` | Listeden **tek** seçim | `city = st.selectbox("Şehir:", ["İstanbul", "Ankara"])` |
| `st.multiselect()` | Listeden **çoklu** seçim | `hobbies = st.multiselect("Hobiler:", [...])` |
| `st.radio()` | Tek seçim (hepsi görünür) | `education = st.radio("Eğitim:", [...])` |
| `st.checkbox()` | Evet/Hayır kutucuğu | `is_student = st.checkbox("Öğrenci misiniz?")` |
| `st.date_input()` | Tarih seçici | `st.date_input("Tarih:", value=date.today())` |
| `st.time_input()` | Saat seçici | `st.time_input("Saat:", value=time(10, 30))` |
| `st.file_uploader()` | Dosya yükleme | `st.file_uploader("Dosya:", type=["csv", "png"])` |
| `st.button()` | Buton (basılınca `True` döner) | `if st.button("Gönder"):` |

### 5.4 Yan menü (sidebar)

Herhangi bir bileşenin başına `sidebar` eklersen, o bileşen sol menüde görünür:

```python
st.sidebar.title("Yan Menü")
sidebar_name = st.sidebar.text_input("Adınızı Giriniz:", key="name")
```

### 5.5 Mesaj kutuları

Kullanıcıya renkli geri bildirim vermenin 4 yolu:

| Kod | Renk | Ne zaman? |
|-----|------|-----------|
| `st.info("...")` | 🔵 Mavi | Bilgilendirme |
| `st.success("...")` | 🟢 Yeşil | Başarılı işlem |
| `st.warning("...")` | 🟡 Sarı | Uyarı |
| `st.error("...")` | 🔴 Kırmızı | Hata |

> Bu dördü, [4_logging'de öğrendiğimiz](../4_logging_hata_yönetimi/README.md#3-logging-modülü-ve-log-seviyeleri) log seviyelerine benzer — ama bu sefer **kullanıcı görür**, terminal değil.

### 5.6 Veri gösterimi ve düzen

```python
# DataFrame göster (pandas tablosu)
st.dataframe(sample_data, use_container_width=True)

# Sayfayı 3 sütuna böl
col1, col2, col3 = st.columns(3)
with col1:
    st.write("Bu sütun 1'dir.")
with col2:
    st.write("Bu sütun 2'dir.")
```

> **`key` parametresi:** Aynı türden birden fazla bileşen varsa (örn. üç `text_input`), her birine benzersiz bir `key="col1_input"` vermelisin. Yoksa Streamlit onları karıştırır ve hata verir.

---

## 6. Proje 1: Görüntüden Hastalık Tespiti

📄 İlgili dosyalar: [main.py](main.py) (backend) + [app.py](app.py) (frontend)

İlk **tam yığın (full-stack)** projemiz! Kullanıcı bir görüntü yükler, sahte bir "yapay zeka modeli" hastalık teşhisi yapar.

### Senaryo

1. Kullanıcı Streamlit ekranından bir görüntü yükler.
2. Streamlit bu görüntüyü FastAPI endpoint'ine gönderir.
3. FastAPI dosyayı alır, görüntü olup olmadığını doğrular.
4. Sahte bir ML tahmini yapar (rastgele olasılık üretir).
5. "Hastalık var/yok" sonucunu olasılıkla birlikte döndürür.
6. Streamlit sonucu ekrana yazdırır.

### Backend — `main.py`

```python
from fastapi import FastAPI, File, UploadFile, HTTPException
import random

app = FastAPI(title="Görüntü Üzerinden Sahte Hastalık Tespiti Sistemi", version="0.0.1")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 1. Yüklenen şey gerçekten görüntü mü?
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Yüklenen dosya bir görüntü değil.")

    image_bytes = await file.read()

    # 2. Boş mu?
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Görüntü yüklenemedi veya boş.")

    # 3. Sahte ML tahmini
    probability = round(random.uniform(0.4, 0.99), 2)
    disease_status = "Hastalık var" if probability > 0.5 else "Hastalık yok"

    return {"file_name": file.filename, "disease_status": disease_status, "probability": probability}
```

**🆕 Yeni kavram: `content_type` ile dosya tipi doğrulama**

`5_veri_analiz_servisi`'nde uzantıya bakmıştık (`.endswith('.csv')`). Burada daha sağlam bir yöntem var:

```python
file.content_type.startswith("image/")   # "image/png", "image/jpeg" → hepsi geçer
```

`content_type` (MIME tipi), tarayıcının dosyanın **gerçek türünü** bildirdiği alandır. Uzantı değiştirilebilir ama içerik tipi daha güvenilirdir.

> **"Sahte model" neden?** Gerçek bir yapay zeka modeli yüklemek yerine `random` ile taklit ediyoruz. Böylece odağımız **sistem mimarisinde** kalıyor: arayüz → API → sonuç. Gerçek bir model eklemek istersen, sadece `random.uniform(...)` satırını `model.predict(image)` ile değiştirirsin — **sistemin geri kalanı aynı kalır.** İşte bu yüzden mimariyi öğrenmek modelden daha önemlidir.

### Frontend — `app.py`

```python
import streamlit as st
import requests
import PIL.Image as Image

st.set_page_config(page_title="...", page_icon="🩺", layout="centered")
st.title("Görüntü Üzerinden Sahte Hastalık Tespiti Sistemi")

uploaded_file = st.file_uploader("Bir görüntü yükleyin", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)              # görüntüyü aç
    st.image(image, caption="Yüklenen Görüntü")    # ekranda göster

    if st.button("Tahmin Et"):
        try:
            uploaded_file.seek(0)   # ⚠️ dosya okuma imlecini başa al!

            api_url = "http://localhost:8000/predict"
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            response = requests.post(api_url, files=files)

            if response.status_code == 200:
                result = response.json()
                st.success(f"Sonuç: {result['disease_status']} (Olasılık: {result['probability']})")
                if result['disease_status'] == "Hastalık var":
                    st.warning("Dikkat: Görüntüde hastalık tespit edildi.")
                else:
                    st.info("Görüntüde hastalık tespit edilmedi.")
            else:
                st.error(f"API hatası: {response.status_code}")

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
else:
    st.info("Lütfen bir görüntü yükleyin.")
```

### ⚠️ En kritik detay: `uploaded_file.seek(0)`

Bu tek satır, yeni başlayanların saatlerce takıldığı bir tuzağı çözer.

**Sorun:** `Image.open(uploaded_file)` satırı dosyayı **sonuna kadar okur**. Okuma imleci (cursor) artık dosyanın sonundadır. Sonra aynı dosyayı API'ye göndermeye çalışırsan, imleç sonda olduğu için **boş veri** gönderilir!

**Çözüm:** `uploaded_file.seek(0)` → "imleci başa sar" demektir. Böylece dosya baştan okunur.

> **Benzetme:** Bir kaseti sonuna kadar izledin. Arkadaşına vermeden önce **başa sarman** gerekir, yoksa o sadece jeneriği görür. `seek(0)` tam olarak bu geri sarma işlemidir.

### Çalıştırma (iki terminal)

```bash
# 1. Terminal — backend
uvicorn main:app --reload

# 2. Terminal — frontend
streamlit run app.py
```

---

## 7. Proje 2 (Ödev): Film Yorumu Duygu Analizi

📄 İlgili dosyalar: [film_odevi_main.py](film_odevi_main.py) (backend) + [film_odevi_app.py](film_odevi_app.py) (frontend)

Bu ödevde, bir film yorumunun **pozitif / negatif / nötr** olduğunu tahmin eden bir servis yazıyoruz. Gerçek dünyada bu iş NLP modelleriyle yapılır; burada mantığı anlamak için **basit kelime sayma** yöntemini kullanıyoruz.

### Backend — `film_odevi_main.py`

Kelime listeleriyle basit bir duygu analizi:

```python
positive_words = {"güzel", "harika", "mükemmel", "süper", "bayıldım", ...}
negative_words = {"kötü", "berbat", "sıkıcı", "rezalet", "saçma", ...}

def analyze_comment(comment: str):
    comment = comment.lower()                              # 1. küçük harfe çevir
    comment = re.sub(r"[^\wçğıöşü\s]", " ", comment)       # 2. noktalama temizle
    tokens = comment.split()                               # 3. kelimelere ayır

    # 4. eşleşen kelimeleri say
    positive_score = sum(1 for token in tokens if token in positive_words)
    negative_score = sum(1 for token in tokens if token in negative_words)

    # 5. karşılaştır ve karar ver
    if positive_score + negative_score == 0:
        return "Nötr", "Belirgin ifade bulunamadı.", positive_score, negative_score
    if positive_score > negative_score:
        return "Pozitif", "Pozitif ifadeler baskın.", positive_score, negative_score
    elif negative_score > positive_score:
        return "Negatif", "Negatif ifadeler baskın.", positive_score, negative_score
    else:
        return "Nötr", "Dengeli görünüyor.", positive_score, negative_score
```

**🆕 Metin ön işleme (NLP'nin temel adımları):**

| Adım | Kod | Neden? |
|------|-----|--------|
| Küçük harfe çevirme | `.lower()` | "Harika" ile "harika" aynı sayılsın |
| Noktalama temizleme | `re.sub(r"[^\wçğıöşü\s]", " ", ...)` | "güzel!" → "güzel" olsun (yoksa eşleşmez) |
| Tokenizasyon | `.split()` | Metni tek tek kelimelere ayır |

> **Türkçe detayı:** Düzenli ifadedeki `çğıöşü` karakterlerine dikkat et. `\w` bazı ortamlarda Türkçe harfleri kapsamayabilir; bu yüzden açıkça eklenmişler. Yoksa "güzel" kelimesi "g zel" diye bölünürdü.

Endpoint ise Pydantic ile JSON alır:

```python
class CommentRequest(BaseModel):
    comment: str

@app.post("/analyze")
def analyze_sentiment(data: CommentRequest):
    comment = data.comment.strip()
    if not comment:
        return {"success": "False", "message": "Yorum alanı boş olamaz."}

    sentiment, explanation, positive_score, negative_score = analyze_comment(comment)
    return {"success": "True", "comment": comment, "sentiment": sentiment, ...}
```

### Frontend — `film_odevi_app.py`

```python
if st.button("Yorumu Analiz Et"):
    if not comment.strip():
        st.warning("Lütfen analiz etmek için bir yorum giriniz.")
    else:
        try:
            api_url = "http://127.0.0.1:8000/analyze"
            payload = {"comment": comment}
            response = requests.post(api_url, json=payload)   # 👈 json= (dosya değil!)

            if response.status_code == 200:
                result = response.json()
                st.write(f"**Duygu Durumu:** {result['sentiment']}")

                if result["sentiment"] == "Pozitif":
                    st.success("Sonuç: Pozitif Yorum")
                elif result["sentiment"] == "Negatif":
                    st.error("Sonuç: Negatif Yorum")
                else:
                    st.info("Sonuç: Nötr Yorum")

        except requests.exceptions.ConnectionError:
            st.error("FastAPI servisine bağlanılamadı. Önce backend'i çalıştırın.")
        except Exception as e:
            st.error(f"Beklenmeyen bir hata oluştu: {e}")
```

### 🌟 Bu dosyadaki güzel detaylar

1. **`json=` vs `files=`** — Bu projede JSON gönderiliyor (`json=payload`), Proje 1'de ise dosya (`files=files`). İçeriğe göre doğru parametreyi seçmek önemli.

2. **Özel hata yakalama** — `requests.exceptions.ConnectionError` ayrı yakalanmış. Backend kapalıysa kullanıcıya net bir mesaj gösteriliyor: *"Önce backend'i çalıştırın."* Bu, kullanıcı dostu hata yönetiminin güzel bir örneğidir.

3. **Örnek yorum seçici** — `st.selectbox` ile hazır yorumlar sunulmuş, seçilen yorum `text_area`'nın varsayılan değeri oluyor. Kullanıcının denemesini kolaylaştıran hoş bir dokunuş.

### Çalıştırma (iki terminal)

```bash
# 1. Terminal — backend
uvicorn film_odevi_main:app --reload

# 2. Terminal — frontend
streamlit run film_odevi_app.py
```

---

## 8. İki Projenin Karşılaştırması

| | **Proje 1** (Hastalık Tespiti) | **Proje 2** (Duygu Analizi) |
|--|-------------------------------|------------------------------|
| Gönderilen veri | Görüntü (dosya) | Metin (JSON) |
| `requests` parametresi | `files=files` | `json=payload` |
| Backend girdisi | `UploadFile = File(...)` | Pydantic `BaseModel` |
| "Model" | `random` ile sahte tahmin | Kelime listesi eşleştirme |
| Kritik detay | `uploaded_file.seek(0)` | Metin ön işleme (`lower`, `re.sub`) |
| Hata yönetimi | Genel `Exception` | `ConnectionError` özel yakalama |

> **Ortak nokta:** İkisi de aynı mimariyi kullanır → **Streamlit (arayüz) ↔ requests ↔ FastAPI (backend)**. Değişen sadece taşınan verinin türüdür. Bu deseni anladıysan, herhangi bir yapay zeka modelini arayüze bağlayabilirsin.

---

## 9. Özet Tablo

| Kavram | Ne işe yarar? | Anahtar kod |
|--------|---------------|-------------|
| **Streamlit çalıştırma** | Arayüzü başlatır | `streamlit run app.py` |
| **set_page_config** | Sayfa ayarları (ilk komut!) | `st.set_page_config(...)` |
| **Başlıklar** | Metin hiyerarşisi | `st.title / header / subheader` |
| **st.write** | Her şeyi yazdırır | `st.write(veri)` |
| **Girdi bileşenleri** | Kullanıcıdan veri alır | `st.text_input`, `st.selectbox`... |
| **st.button** | Basılınca `True` döner | `if st.button("Gönder"):` |
| **st.file_uploader** | Dosya yükletir | `st.file_uploader("...", type=["png"])` |
| **Mesaj kutuları** | Renkli geri bildirim | `st.info / success / warning / error` |
| **st.columns** | Sayfayı sütunlara böler | `col1, col2 = st.columns(2)` |
| **sidebar** | Yan menü | `st.sidebar.text_input(...)` |
| **key** | Bileşenleri ayırt eder | `st.text_input("...", key="col1")` |
| **seek(0)** | Dosya imlecini başa alır | `uploaded_file.seek(0)` |
| **content_type** | Dosya tipi doğrulama | `file.content_type.startswith("image/")` |
| **Rerun mantığı** | Her etkileşimde betik baştan çalışır | (Streamlit'in çalışma modeli) |

---

## 🧠 Kritik Hatırlatmalar

- **İki terminal gerekir** → biri `uvicorn` (backend), biri `streamlit` (frontend).
- **`set_page_config` ilk olmalı** → başka bir `st.` komutundan sonra çağırırsan hata verir.
- **`seek(0)` unutma** → dosyayı hem gösterip hem gönderiyorsan imleci başa sar.
- **`files=` vs `json=`** → dosya gönderiyorsan `files`, JSON gönderiyorsan `json`.
- **`ConnectionError` yakala** → backend kapalıysa kullanıcı ne yapacağını bilsin.
- **Aynı tür bileşenlere `key` ver** → yoksa Streamlit karıştırır.

> **Küçük not:** `app.py`'deki `use_column_width=True` parametresi Streamlit'in yeni sürümlerinde kullanımdan kaldırıldı. Uyarı görürsen `use_container_width=True` olarak değiştirebilirsin — ikisi de aynı işi yapar.

---

## Sırada Ne Var?

Artık **tam yığın (full-stack)** bir yapay zeka uygulaması yazabiliyorsun: kullanıcının gördüğü arayüz (Streamlit) + arkada çalışan servis (FastAPI). Bu, bir yapay zeka modelini gerçek insanların kullanabileceği bir ürüne dönüştürmenin tam formülüdür.

**Küçük tavsiye:** `main.py`'deki sahte tahmin satırını (`random.uniform(...)`) gerçek bir modelle değiştirmeyi hayal et. Göreceksin ki **başka hiçbir şeyi değiştirmene gerek yok** — arayüz, istek, cevap, hepsi aynı kalır. İşte iyi mimarinin gücü budur. 💪
