"""
Amaç:
    - try-except yapısını öğrenmek
"""

"""
try-except mantığı

try: yapmak istediğimiz işlemi buraya yazıyoruz.
except: eğer try bloğunda bir hata oluşursa burası çalışır.
"""

# örnek çalışma mantığı
def metni_sayiya_cevir(metin):
    """
    Kullanıcıdan bir metin alır ve bu metni sayıya çevirmeye çalışır.
    """
    try:
        sayi = int(metin)
        print(f"✅ Metin başarıyla sayıya çevrildi: {sayi}")

    except ValueError:
        print("❌ HATA: Girilen metin bir sayıya çevrilemez.")

metni_sayiya_cevir("123")  # Başarılı dönüşüm
metni_sayiya_cevir("abc")  # Hata durumu
print()

# iki sayıyı bölme
def bolme(sayi1: int, sayi2: int):
    """
    İki sayıyı böler ve sonucu döndürür.
    """
    try:
        sonuc = sayi1 / sayi2
        print(f"✅ Bölme işlemi başarılı: {sayi1} / {sayi2} = {sonuc}")

    except ZeroDivisionError:
        print("❌ HATA: Sıfıra bölme hatası.")

bolme(10, 2)  # Başarılı bölme
bolme(10, 0)  # Hata durumu
print()

# tip uyuşmazlığı
def topla(deger1, deger2):
    """
    İki değeri toplar ve sonucu döndürür.
    """
    try:
        sonuc = deger1 + deger2
        print(f"✅ Toplama işlemi başarılı: {deger1} + {deger2} = {sonuc}")

    except TypeError:
        print("❌ HATA: Tip uyuşmazlığı. Lütfen sayısal değerler girin.")

topla(5, 10)  # Başarılı toplama
topla(5, "10")  # Hata durumu
print()

# listeden eleman getir
def liste_eleman_getir(liste, index):
    """
    Verilen listeden belirtilen index'teki elemanı döndürür.
    """
    try:
        eleman = liste[index]
        print(f"✅ Eleman başarıyla getirildi: {eleman}")

    except Exception as e:  # Tüm hataları bilemeyiz o yüzden genel Exception kullanıyoruz.
        print(f"❌ HATA: {e}")

liste_eleman_getir([1, 2, 3], 1)  # Başarılı eleman getirme
liste_eleman_getir([1, 2, 3], 5)  # Hata durumu
print()

# finally
def dosya_okuma_ornegi():
    """
    Dosyayı açar ve işlemler yapar. Hata olsa bile dosya kapatılır.
    """
    try:
        dosya = open("olmayan_dosya.txt", "r", encoding="utf-8")
        icerik = dosya.read()
        print(f"✅ Dosya başarıyla açıldı ve okundu: {icerik}")
    
    except Exception as e:
        print(f"❌ HATA: {e}")
    
    finally:
        print("Dosya işlemi sona erdi.")

dosya_okuma_ornegi()