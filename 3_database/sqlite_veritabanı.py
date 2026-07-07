"""
Amaç:
    - sqlite kullanarak veritabanı oluşturma
    - python ile tablo yapısını hazırla ve ilk kaydı ekle
    - veri tabanı bağlantısı, tablo oluşturma ve veri ekleme mantığını görmüş olacağız.
"""

import sqlite3

# 1. sqlite veritabanı bağlantısı oluşturma
conn = sqlite3.connect("veritabani.db") # eğer dosya yoksa otomatik oluşturur

# sql komutları için bir cursor nesnesi oluşturma
cursor = conn.cursor()

# 2. tablo oluşturma ve kullanıcı mesajlarını tutar
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS mesajlar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kullanici_mesajlari TEXT NOT NULL,
        bot_cevabi TEXT NOT NULL
    )
    """
)

# 3. tabloya ilk kaydı ekleme
cursor.execute(
    """
    INSERT INTO mesajlar (kullanici_mesajlari, bot_cevabi) 
    VALUES (?, ?)
    """, (
        "Merhaba Nasılsın ?", "Merhaba! Size nasıl yardımcı olabilirim?"
    )
)

# yapılan değişiklikleri veri tabanına kaydetme
conn.commit()
