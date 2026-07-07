"""
CRUD: create, read, update, delete işlemleri
"""

import sqlite3

# veritabanına bağlanmak için fonksiyon
def veritabani_baglantisi():
    return sqlite3.connect("veritabani.db")

# tablo oluşturmak için fonksiyon
def tablo_olustur():
    conn = veritabani_baglantisi()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS mesajlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_mesajlari TEXT NOT NULL,
            bot_cevabi TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

# CREATE: yeni kayıt ekleme
def mesaj_ekle(kullanici_mesaji, bot_cevabi):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO mesajlar (kullanici_mesajlari, bot_cevabi) 
        VALUES (?, ?)
        """, (kullanici_mesaji, bot_cevabi)
    )
    conn.commit()
    conn.close()

# READ: tüm kayıtları listeleme
def tum_mesajlari_listele():
    conn = veritabani_baglantisi()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mesajlar")
    mesajlar = cursor.fetchall()
    conn.close()
    return mesajlar

# UPDATE: kayıt güncelleme
def mesaj_guncelle(id, yeni_kullanici_mesaji, yeni_bot_cevabi):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE mesajlar 
        SET kullanici_mesajlari = ?, bot_cevabi = ? 
        WHERE id = ?
        """, (yeni_kullanici_mesaji, yeni_bot_cevabi, id)
    )
    conn.commit()
    conn.close()


# DELETE: kayıt silme
def mesaj_sil(id):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mesajlar WHERE id = ?", (id,))
    conn.commit()
    conn.close()


# fonksiyonları çağır ve test et
# Bu blok yalnızca dosya DOĞRUDAN çalıştırıldığında (python crud.py) çalışır.
# Başka bir dosya (örn. fastapi_crud.py) crud'u import ettiğinde ÇALIŞMAZ.
if __name__ == "__main__":
    tablo_olustur()

    # create
    mesaj_ekle("Merhaba ben Messi", "Merhaba! Messiciğim nasılsın?")

    # read
    for mesaj in tum_mesajlari_listele():
        print(mesaj)

    # update
    mesaj_guncelle(1, "Merhaba ben Ronaldo", "Merhaba! Ronaldocum nasılsın?")

    # delete
    mesaj_sil(5)
