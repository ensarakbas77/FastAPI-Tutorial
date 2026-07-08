"""
Amaç:
    - python logging modülünü tanımak
    - temel log seviyelerini öğrenmek
"""

import logging

#! temel logging ayarları

"""
Log seviyeleri:
    - DEBUG: Detaylı bilgi, genellikle tanılama amacıyla kullanılır.
    - INFO: Genel bilgi mesajları, uygulamanın normal işleyişi hakkında bilgi verir.
    - WARNING: Uyarı mesajları, potansiyel bir sorun veya dikkat edilmesi gereken durumları belirtir.
    - ERROR: Hata mesajları, bir işlevin başarısız olduğunu veya bir hatanın meydana geldiğini belirtir.
    - CRITICAL: Kritik hata mesajları, ciddi bir sorunu veya uygulamanın çalışmasını engelleyen bir durumu belirtir.

seviye sırası: DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL
"""

logging.basicConfig(
    level=logging.DEBUG, # debug ve üzerindeki tüm seviyeleri görebileceğiz, seviye sırası yukarıda yani warning yaparsak debug ve info loglarını göremeyiz.
    format="%(levelname)s | %(asctime)s | %(message)s",
)

# Log seviyeleri görme
def log_seviyeleri_gorme():

    # debug
    logging.debug("Bu bir debug mesajıdır.")

    # info
    logging.info("Bu bir info mesajıdır.")

    # warning
    logging.warning("Bu bir warning mesajıdır.")

    # error
    logging.error("Bu bir error mesajıdır.")

    # critical
    logging.critical("Bu bir critical mesajıdır.")

log_seviyeleri_gorme()

#! print ve logging arasındaki fark
print("Kullanıcı sisteme giriş yaptı.")
logging.info("Kullanıcı sisteme giriş yaptı.")


#? örnek senaryo ile log üretme
# işlem başlarken bilgi logu
kullanici_adi = "ea"
logging.info(f"Kullanıcı işleme başladı: kullanici_adi: {kullanici_adi}")

# geliştirme sırasında değişkenleri görmek için
yas = 15
logging.debug(f"Kullanıcı yaşı, yas: {yas}") # yas değişkenini kolayca bulmak için yas: {yas} şeklinde yazdık

# error
kullanici_adi = ""
if not kullanici_adi:
    logging.error("Kullanıcı adı boş bırakıldı.")

# warning
if yas < 18:
    logging.warning("Kullanıcı 18 yaşından küçük.")

# critical
yas = -5
if yas < 0:
    logging.critical("yaş bilgisi negatif geldi.")