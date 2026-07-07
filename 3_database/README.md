# Veritabanı (Database) ve FastAPI 🗄️

Bu doküman, `3_database` klasöründeki dosyalarda anlatılan konuları **sıfırdan** açıklamak için hazırlanmıştır. Amaç: veritabanını hiç bilmeyen birinin okuduğunda "veritabanı ne, SQL ne, CRUD ne, API'ye nasıl bağlanır?" sorularının kafasında net oturmasıdır.

> **Ön koşul:** `1_fastapi` (endpoint, GET/POST, Pydantic) ve `2_asenkron_programlama` (istemci–sunucu, `requests`) klasörlerini bitirmiş olman iyi olur. Buradaki örnekler onların üzerine kuruludur.

---

## İçindekiler

1. [Veritabanı Nedir? Neden Gerekli?](#1-veritabanı-nedir-neden-gerekli)
2. [SQLite ve Temel Kavramlar](#2-sqlite-ve-temel-kavramlar)
3. [Kurulum ve Çalıştırma](#3-kurulum-ve-çalıştırma)
4. [İlk Adım: Veritabanı ve Tablo Oluşturma](#4-i̇lk-adım-veritabanı-ve-tablo-oluşturma) — `sqlite_veritabanı.py`
5. [CRUD İşlemleri](#5-crud-i̇şlemleri) — `crud.py`
6. [⚠️ Önemli Ders: `if __name__ == "__main__"` Tuzağı](#6-️-önemli-ders-if-__name__--__main__-tuzağı)
7. [Veritabanını FastAPI'ye Bağlamak](#7-veritabanını-fastapiye-bağlamak) — `fastapi_crud.py`
8. [Python İstemcisi ile Test](#8-python-i̇stemcisi-ile-test) — `client.py`
9. [Ödev: Şirket Çalışan Kayıt Sistemi](#9-ödev-şirket-çalışan-kayıt-sistemi) — `database_odev.py`
10. [Özet Tablo](#10-özet-tablo)

---

## 1. Veritabanı Nedir? Neden Gerekli?

Şimdiye kadar yazdığımız API'lerde gelen veriler **kalıcı değildi**. Sunucu kapanınca her şey silinirdi. Gerçek uygulamalarda ise verinin **kalıcı olarak saklanması** gerekir: kullanıcı mesajları, chatbot cevapları, kayıtlar...

**Veritabanı (database)**, verileri düzenli, kalıcı ve tekrar erişilebilir şekilde saklayan sistemdir.

> **Benzetme:** Veritabanı, dev bir **Excel dosyası** gibidir. İçinde **tablolar** (sayfalar) vardır, her tablonun **sütunları** (isim, yaş...) ve **satırları** (her bir kayıt) olur. Programın kapansa bile bu dosya diskte kalır, veriler kaybolmaz.

Yapay zeka uygulamalarında veritabanı şart, çünkü:
- 💬 Sohbet geçmişini saklamak (chatbot hafızası)
- 👤 Kullanıcı bilgilerini tutmak
- 📊 Model çıktılarını / logları kaydetmek gerekir.

---

## 2. SQLite ve Temel Kavramlar

**SQLite**, kurulum gerektirmeyen, **tek bir dosyada** çalışan basit bir veritabanıdır. Python'un içinde **yerleşik** gelir (`sqlite3` modülü) — ayrı bir sunucu kurmana gerek yoktur. Öğrenmek ve küçük projeler için idealdir.

> Verilerin `veritabani.db` gibi tek bir dosyada tutulur. Bu dosyayı kopyalarsan, tüm veritabanını taşımış olursun.

### SQL Nedir?

**SQL (Structured Query Language)**, veritabanıyla konuşma dilidir. Veritabanına "şunu ekle", "şunları getir" gibi komutları SQL ile veririz. En temel 4 komut:

| SQL Komutu | Ne yapar? | CRUD karşılığı |
|-----------|-----------|----------------|
| `INSERT` | Yeni kayıt ekler | **C**reate (Oluştur) |
| `SELECT` | Kayıtları okur/getirir | **R**ead (Oku) |
| `UPDATE` | Var olan kaydı günceller | **U**pdate (Güncelle) |
| `DELETE` | Kayıt siler | **D**elete (Sil) |

Bu dört işlemin baş harfleri **CRUD** kelimesini oluşturur. Neredeyse tüm veri uygulamaları bu 4 işlemin etrafında döner.

### Bağlantı (connection) ve İmleç (cursor)

SQLite ile çalışırken iki temel nesne kullanırız:

- **`connection` (bağlantı)** → Veritabanı dosyasıyla kurulan köprü. `sqlite3.connect("dosya.db")` ile açılır.
- **`cursor` (imleç)** → SQL komutlarını çalıştıran ve sonuçları getiren "kalem". `connection.cursor()` ile oluşturulur.

Tipik akış her zaman şöyledir:

```python
conn = sqlite3.connect("veritabani.db")   # 1. Bağlan
cursor = conn.cursor()                     # 2. İmleç oluştur
cursor.execute("SQL komutu...")            # 3. Komutu çalıştır
conn.commit()                              # 4. Değişiklikleri KAYDET (yazma işlemlerinde)
conn.close()                               # 5. Bağlantıyı kapat
```

> **`commit()` neden önemli?** `INSERT`, `UPDATE`, `DELETE` gibi **değiştiren** işlemlerden sonra `commit()` çağırmazsan, değişiklikler diske **kalıcı olarak yazılmaz**. Sadece okuma (`SELECT`) yapıyorsan `commit`'e gerek yoktur.

---

## 3. Kurulum ve Çalıştırma

### Gerekli paketler

```bash
pip install fastapi uvicorn requests
```

> `sqlite3` Python ile **birlikte gelir**, ayrı kurulum gerekmez.

### Dosyaların rolleri

| Dosya | Türü | Nasıl çalıştırılır? |
|-------|------|---------------------|
| `sqlite_veritabanı.py` | Öğrenme betiği | `python sqlite_veritabanı.py` |
| `crud.py` | CRUD fonksiyonları + test | `python crud.py` |
| `fastapi_crud.py` | FastAPI sunucusu | `uvicorn fastapi_crud:app --reload` |
| `client.py` | İstemci (test) betiği | `python client.py` |
| `database_odev.py` | Ödev çözümü (sunucu) | `uvicorn database_odev:app --reload` |

---

## 4. İlk Adım: Veritabanı ve Tablo Oluşturma

📄 İlgili dosya: [sqlite_veritabanı.py](sqlite_veritabanı.py) — `python sqlite_veritabanı.py` ile çalıştırılır.

Bu dosya, en temel adımı gösterir: bir veritabanı dosyası ve tablo oluşturup ilk kaydı eklemek.

```python
import sqlite3

# 1. Bağlantı — dosya yoksa otomatik oluşturulur
conn = sqlite3.connect("veritabani.db")
cursor = conn.cursor()

# 2. Tablo oluşturma
cursor.execute("""
    CREATE TABLE IF NOT EXISTS mesajlar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kullanici_mesajlari TEXT NOT NULL,
        bot_cevabi TEXT NOT NULL
    )
""")

# 3. İlk kaydı ekleme
cursor.execute("""
    INSERT INTO mesajlar (kullanici_mesajlari, bot_cevabi)
    VALUES (?, ?)
""", ("Merhaba Nasılsın ?", "Merhaba! Size nasıl yardımcı olabilirim?"))

conn.commit()   # değişiklikleri kaydet
```

### Tablo tanımını anlamak

```sql
CREATE TABLE IF NOT EXISTS mesajlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Her kayda otomatik, benzersiz numara
    kullanici_mesajlari TEXT NOT NULL,      -- Metin, boş olamaz
    bot_cevabi TEXT NOT NULL                -- Metin, boş olamaz
)
```

| Parça | Anlamı |
|-------|--------|
| `IF NOT EXISTS` | Tablo zaten varsa hata verme, atla |
| `INTEGER`, `TEXT` | Sütunun veri tipi (sayı / metin) |
| `PRIMARY KEY` | Bu sütun her kaydı benzersiz tanımlar (kimlik) |
| `AUTOINCREMENT` | Her yeni kayıtta `id`'yi otomatik 1 artır |
| `NOT NULL` | Bu alan boş bırakılamaz (zorunlu) |

### `?` işaretleri neden var? (Çok önemli güvenlik konusu)

Dikkat et: değerleri SQL'in içine doğrudan yazmadık. `?` yer tutucularını kullanıp değerleri ayrı bir demet (tuple) olarak verdik:

```python
cursor.execute("INSERT ... VALUES (?, ?)", ("değer1", "değer2"))
```

Bu yöntem **SQL Injection** denen güvenlik açığını önler. Kullanıcıdan gelen veriyi doğrudan SQL metnine eklersen, kötü niyetli biri veritabanını ele geçirebilir. `?` kullanımı bunu engeller — **her zaman böyle yazmalısın.**

---

## 5. CRUD İşlemleri

📄 İlgili dosya: [crud.py](crud.py) — `python crud.py` ile çalıştırılır.

Bu dosya, her veritabanı işlemini **ayrı bir fonksiyon** haline getirir. Böylece hem kod düzenli olur hem de bu fonksiyonları sonra FastAPI'den çağırabiliriz.

### Ortak yardımcı: bağlantı fonksiyonu

```python
def veritabani_baglantisi():
    return sqlite3.connect("veritabani.db")
```

Her fonksiyon bu yardımcıyı çağırarak bağlantıyı tek bir yerden yönetir (kod tekrarını önler).

### C — Create (Ekleme)

```python
def mesaj_ekle(kullanici_mesaji, bot_cevabi):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mesajlar (kullanici_mesajlari, bot_cevabi)
        VALUES (?, ?)
    """, (kullanici_mesaji, bot_cevabi))
    conn.commit()
    conn.close()
```

### R — Read (Listeleme)

```python
def tum_mesajlari_listele():
    conn = veritabani_baglantisi()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mesajlar")
    mesajlar = cursor.fetchall()   # tüm satırları liste olarak getir
    conn.close()
    return mesajlar
```

> `fetchall()` sonuçları **demetlerden oluşan bir liste** olarak döndürür: `[(1, "merhaba", "selam"), (2, ...)]`. Her demetin sırası tablo sütunlarının sırasıdır: `kayit[0]=id`, `kayit[1]=kullanici_mesaji`, `kayit[2]=bot_cevabi`.

### U — Update (Güncelleme)

```python
def mesaj_guncelle(id, yeni_kullanici_mesaji, yeni_bot_cevabi):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE mesajlar
        SET kullanici_mesajlari = ?, bot_cevabi = ?
        WHERE id = ?
    """, (yeni_kullanici_mesaji, yeni_bot_cevabi, id))
    conn.commit()
    conn.close()
```

> **`WHERE` çok kritik!** `UPDATE` ve `DELETE` işlemlerinde `WHERE id = ?` yazmayı unutursan, **tablodaki BÜTÜN kayıtlar** güncellenir/silinir. Hangi kaydı hedeflediğini her zaman `WHERE` ile belirt.

### D — Delete (Silme)

```python
def mesaj_sil(id):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mesajlar WHERE id = ?", (id,))
    conn.commit()
    conn.close()
```

> **Küçük ayrıntı:** Tek elemanlı demet yazarken virgül şart: `(id,)`. `(id)` yazarsan Python bunu demet değil, normal parantez sayar.

---

## 6. ⚠️ Önemli Ders: `if __name__ == "__main__"` Tuzağı

Bu klasörde çalışırken **gerçek bir hatayla** karşılaştık ve çözdük — çok öğretici olduğu için ayrı bir başlık hak ediyor.

### Sorun neydi?

`crud.py`'nin en altında test kodları vardı:

```python
tablo_olustur()
mesaj_ekle("Merhaba ben Messi", "Merhaba! Messiciğim nasılsın?")
# ... update, delete
```

`fastapi_crud.py` dosyası `crud`'u import edince (`from crud import ...`), bu test kodları **her import'ta çalışıyordu**. `uvicorn --reload` her değişiklikte yeniden yüklediği için de "Messi" kaydı **sürekli tekrar tekrar** ekleniyordu.

### Neden oluyor?

Python bir dosyayı `import` ettiğinde, o dosyanın **modül seviyesindeki tüm satırları** baştan sona çalışır — sadece fonksiyon tanımları değil, "çıplak" duran çağrılar da.

### Çözüm

Test kodlarını `if __name__ == "__main__":` bloğuna aldık:

```python
if __name__ == "__main__":
    tablo_olustur()
    mesaj_ekle("Merhaba ben Messi", "Merhaba! Messiciğim nasılsın?")
    # ...
```

### `__name__` nasıl çalışır?

| Dosya nasıl çalışıyor? | `__name__` değeri | Blok çalışır mı? |
|------------------------|-------------------|------------------|
| `python crud.py` (doğrudan) | `"__main__"` | ✅ Evet |
| `from crud import ...` (import) | `"crud"` | ❌ Hayır |

> **Altın kural:** Bir dosyada hem **başka yerden import edilecek fonksiyonlar** hem de **test kodları** varsa, test kodlarını **her zaman** `if __name__ == "__main__":` altına koy. Böylece import edildiğinde sessiz kalır, doğrudan çalıştırıldığında test eder.

---

## 7. Veritabanını FastAPI'ye Bağlamak

📄 İlgili dosya: [fastapi_crud.py](fastapi_crud.py) — `uvicorn fastapi_crud:app --reload` ile çalıştırılır.

Burada, `crud.py`'de yazdığımız fonksiyonları **API endpoint'lerine** bağlarız. Yani kullanıcı bir HTTP isteği attığında, arka planda bizim CRUD fonksiyonlarımız çalışıp veritabanına dokunur.

### Fonksiyonları içeri aktarma

```python
from crud import veritabani_baglantisi, tablo_olustur, mesaj_ekle, tum_mesajlari_listele, mesaj_sil
```

> Aynı işi iki kez yazmıyoruz — `crud.py`'deki hazır fonksiyonları tekrar kullanıyoruz. Bu, **kod tekrarını önlemenin** (DRY prensibi) güzel bir örneğidir.

### Ekleme endpoint'i (POST)

```python
class MesajModel(BaseModel):
    kullanici_mesaji: str
    bot_cevabi: str

@app.post("/mesaj-ekle")
def mesaj_ekle_endpoint(veri: MesajModel):
    mesaj_ekle(veri.kullanici_mesaji, veri.bot_cevabi)   # crud fonksiyonunu çağır
    return {
        "durum": "Başarılı",
        "mesaj": "Kayıt db ye başarıyla eklendi.",
        "eklenen_veri": {"kullanici_mesaji": veri.kullanici_mesaji, "bot_cevabi": veri.bot_cevabi}
    }
```

Akış şöyle: **Kullanıcı JSON gönderir → Pydantic doğrular → CRUD fonksiyonu veritabanına yazar → cevap döner.**

### Listeleme endpoint'i (GET)

```python
@app.get("/mesajlar")
def mesajlari_listele_endpoint():
    kayitlar = tum_mesajlari_listele()   # ham demet listesi

    sonuc = []
    for kayit in kayitlar:
        sonuc.append({
            "id": kayit[0],
            "kullanici_mesaji": kayit[1],
            "bot_cevabi": kayit[2]
        })
    return {"durum": "Başarılı", "toplam_kayit_sayisi": len(sonuc), "kayitlar": sonuc}
```

> **Neden bu dönüşüm?** Veritabanı bize veriyi demet olarak verir: `(1, "merhaba", "selam")`. Ama JSON cevabında anlamlı isimler (`id`, `kullanici_mesaji`...) olması daha kullanışlıdır. Bu döngü, ham demetleri okunabilir sözlüklere çevirir.

### Silme endpoint'i (POST)

```python
@app.post("/mesaj-sil")
def mesaj_sil_endpoint(mesaj_id: int):
    mesaj_sil(mesaj_id)
    return {"durum": "Başarılı", "mesaj": f"{mesaj_id} id'li kayıt silindi."}
```

---

## 8. Python İstemcisi ile Test

📄 İlgili dosya: [client.py](client.py) — `python client.py` ile çalıştırılır.

Swagger (`/docs`) yerine, API'yi **başka bir Python programından** test ederiz.

```python
import requests

BASE_URL = "http://127.0.0.1:7002"

# POST — yeni kayıt ekle
gonderilecek_veri = {"kullanici_mesaji": "Merhaba ben client", "bot_cevabi": "Merhaba client ben de chatbot"}
post_response = requests.post(f"{BASE_URL}/mesaj-ekle", json=gonderilecek_veri)
print("POST Durumu:", post_response.status_code)
print("POST Yanıtı:", post_response.json())

# GET — tüm kayıtları listele
get_response = requests.get(f"{BASE_URL}/mesajlar")
print("GET Durumu:", get_response.status_code)
print("GET Yanıtı:", get_response.json())
```

### ⚠️ Port uyumuna dikkat!

`client.py` içinde `BASE_URL = "http://127.0.0.1:7002"` yazıyor — yani **7002** portu. O halde sunucuyu da aynı portta başlatmalısın:

```bash
uvicorn fastapi_crud:app --reload --port 7002
```

Sunucu farklı bir portta çalışıyorsa (örn. varsayılan 8000), istemci bağlanamaz ve **bağlantı hatası** alırsın. İstemci ile sunucunun portu **aynı** olmalı.

### Test adımları

1. **1. terminal** — sunucuyu başlat: `uvicorn fastapi_crud:app --reload --port 7002`
2. **2. terminal** — istemciyi çalıştır: `python client.py`
3. Çıktıda POST ve GET cevaplarını gör.

---

## 9. Ödev: Şirket Çalışan Kayıt Sistemi

📄 İlgili dosya: [database_odev.py](database_odev.py) — `uvicorn database_odev:app --reload` ile çalıştırılır.

Bu dosya, öğrendiğimiz her şeyi tek başına uygulayan bir **alıştırma çözümüdür** ve sıfırdan yazılmıştır. Senaryo: küçük bir şirket için çalışan kayıt sistemi. Ödev sadece ekleme + listeleme istese de, çözümde **tam CRUD** (ekle, listele, güncelle, sil) uygulanmış.

### Ne değişti? (Öncekiyle karşılaştırma)

| | `fastapi_crud.py` | `database_odev.py` |
|--|-------------------|--------------------|
| İsimlendirme | Türkçe | İngilizce |
| Veritabanı dosyası | `veritabani.db` | `company.db` |
| Tablo | `mesajlar` | `employees` |
| Alanlar | `kullanici_mesajlari`, `bot_cevabi` | `name`, `department`, `age` |
| CRUD + API | Ayrı dosyalarda | **Hepsi tek dosyada** |
| HTTP metotları | GET, POST | GET, POST, **PUT, DELETE** |

Bu ödevde CRUD fonksiyonları ve endpoint'ler **aynı dosyada** toplanmış — küçük projeler için pratik bir yaklaşım.

### Yapı

```python
# Pydantic model — gelen çalışan verisi
class EmployeeModel(BaseModel):
    name: str
    department: str
    age: int

# CRUD fonksiyonları
def database_connection(): ...          # bağlantı
def create_table(): ...                 # tablo oluştur
def add_employee(name, department, age): ...   # C
def get_all_employee(): ...             # R
def update_employee(id, name, department, age): ...   # U
def delete_employee(id): ...            # D

# Endpoint'ler
@app.post("/add-employee")             # yeni çalışan ekle
@app.get("/employees")                 # tüm çalışanları listele
@app.put("/update-employee/{id}")      # çalışanı güncelle
@app.delete("/delete-employee/{id}")   # çalışanı sil
```

### 🆕 Yeni kavram: Doğru HTTP metotları (PUT & DELETE)

Şimdiye kadar hep GET (oku) ve POST (gönder) kullandık. Bu çözümde ilk kez **PUT** ve **DELETE** metotlarını görüyoruz. HTTP'de her CRUD işleminin **kendi doğru metodu** vardır:

| İşlem | Doğru HTTP metodu | Bu dosyadaki endpoint |
|-------|-------------------|------------------------|
| Create (ekle) | `POST` | `POST /add-employee` |
| Read (oku) | `GET` | `GET /employees` |
| Update (güncelle) | `PUT` | `PUT /update-employee/{id}` |
| Delete (sil) | `DELETE` | `DELETE /delete-employee/{id}` |

> **Neden önemli?** `fastapi_crud.py`'de silme işlemini `POST /mesaj-sil` ile yapmıştık — çalışır ama teknik olarak doğru değil. Bir kaydı silen bir endpoint'in `DELETE`, güncelleyen bir endpoint'in `PUT` metodu kullanması **REST API standardıdır**. Bu, API'ni okuyan başka geliştiricilerin niyetini metoda bakarak anlamasını sağlar. FastAPI bunları `@app.put(...)` ve `@app.delete(...)` ile tanımlamanı sağlar.

Ayrıca dikkat et: güncelleme ve silme endpoint'leri **path parametresi** kullanıyor (`/update-employee/{id}`). Hangi çalışanı hedeflediğimizi URL'in içinde `{id}` ile belirtiyoruz — bu, [1_fastapi'de öğrendiğimiz path parametresinin](../1_fastapi/README.md#51-path-yol-parametresi) gerçek bir kullanımıdır.

### Test (Swagger ile)

1. Çalıştır: `uvicorn database_odev:app --reload`
2. Tarayıcıdan: `http://127.0.0.1:8000/docs`
3. `POST /add-employee` ile birkaç çalışan ekle.
4. `GET /employees` ile hepsini listele.
5. `PUT /update-employee/{id}` ile bir çalışanı güncelle (id'yi listeden al).
6. `DELETE /delete-employee/{id}` ile bir çalışanı sil.

> **Not:** Bu dosyadaki `create_table()` çağrısı (satır 185) modül seviyesinde ama sorun yaratmaz — çünkü `database_odev.py` başka bir yerden import **edilmiyor**, doğrudan uvicorn ile çalıştırılıyor. `CREATE TABLE IF NOT EXISTS` sayesinde tablo zaten varsa yeniden oluşturulmaz. (Yine de ileride bu dosyayı bir yerden import edeceksen, o çağrıyı [Bölüm 6'daki](#6-️-önemli-ders-if-__name__--__main__-tuzağı) gibi korumaya almayı unutma.)

---

## 10. Özet Tablo

| Kavram | Ne işe yarar? | Anahtar kod |
|--------|---------------|-------------|
| **SQLite** | Dosya tabanlı basit veritabanı | `sqlite3.connect("db.db")` |
| **connection** | Veritabanı köprüsü | `conn = sqlite3.connect(...)` |
| **cursor** | SQL komutlarını çalıştırır | `cursor = conn.cursor()` |
| **CREATE TABLE** | Tablo oluşturur | `CREATE TABLE IF NOT EXISTS ...` |
| **INSERT** (Create) | Kayıt ekler | `INSERT INTO ... VALUES (?, ?)` |
| **SELECT** (Read) | Kayıt okur | `SELECT * FROM ...` + `fetchall()` |
| **UPDATE** | Kayıt günceller | `UPDATE ... SET ... WHERE id = ?` |
| **DELETE** | Kayıt siler | `DELETE FROM ... WHERE id = ?` |
| **commit()** | Değişiklikleri kalıcı yazar | `conn.commit()` |
| **`?` yer tutucu** | SQL Injection'ı önler | `execute(sql, (deger,))` |
| **`__name__` koruması** | Import'ta test kodunu susturur | `if __name__ == "__main__":` |
| **PUT metodu** | Kayıt güncelleyen endpoint | `@app.put("/update/{id}")` |
| **DELETE metodu** | Kayıt silen endpoint | `@app.delete("/delete/{id}")` |

---

## 🧠 Kritik Hatırlatmalar

- **`commit()` unutma** → yazma işlemi diske işlenmez.
- **`WHERE` unutma** → tüm tablo etkilenir (UPDATE/DELETE'te felaket).
- **`?` kullan** → asla değeri doğrudan SQL metnine ekleme (güvenlik).
- **`if __name__ == "__main__"`** → import edilecek dosyalarda test kodunu koru.
- **Port uyumu** → istemci ve sunucu aynı portta olmalı.

---

## Sırada Ne Var?

Bu klasörde verinin **kalıcı olarak** nasıl saklandığını öğrendin: SQLite ile CRUD işlemleri ve bunları FastAPI'ye bağlama. Artık verileri kaybetmeyen, gerçek uygulamalar yazabilirsin.

**Küçük tavsiye:** `database_odev.py`'yi baştan, README'ye bakmadan kendin yazmayı dene. CRUD mantığını gerçekten oturtmanın en iyi yolu, boş bir dosyadan başlayıp tablo → fonksiyon → endpoint zincirini kendi elinle kurmaktır. 💪
