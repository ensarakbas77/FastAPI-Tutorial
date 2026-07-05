"""
Senkron ve Asenkron Programlama

Senkron programlamada işlemler sırayla çalışır.
Bir işlem tamamlanmadan sonraki işleme geçilmez.

Örnek:
Bir dosya okunurken program bekler. Dosya okuma işlemi bitince diğer işlemler çalışır.

Asenkron programlamada ise zaman alan bir işlem devam ederken program başka işlemleri çalıştırabilir.
Bu sayede program beklemek zorunda kalmaz ve daha verimli çalışır.

Örnek:
Bir API isteği gönderildiğinde cevap beklenirken program başka görevleri yapmaya devam edebilir.

Asenkron yapı özellikle dosya okuma, API istekleri, veritabanı işlemleri ve web sunucuları gibi
I/O ağırlıklı işlemlerde avantaj sağlar.
"""

# FastAPI'de async def ile endpoint asenkron hale getirilir.
# await ise API isteği, veritabanı sorgusu gibi bekleme gerektiren işlemlerde kullanılır.
# Böylece istek beklenirken sunucu başka istekleri işlemeye devam edebilir.
# pip install asyncio

import asyncio

# asenkron fonksiyon tanımlama
# async def: bu fonksiyonun asenkron olduğunu belirtir.
async def gorev1():
    print("Görev 1 başladı")

    # burada sanki bir makine öğrenmesi modeli varmış
    # bu model 2 saniye çalışıyor olsun
    await asyncio.sleep(2)  # 2 saniye bekle
    print("Görev 1 tamamlandı")

async def gorev2():
    print("Görev 2 başladı")
    await asyncio.sleep(1)  # 1 saniye bekle
    print("Görev 2 tamamlandı")

# asenkron işlemleri çalıştır
async def main():
    # asyncio.gather ile birden fazla asenkron fonksiyonu aynı anda çalıştırabiliriz.
    await asyncio.gather(gorev1(), gorev2())

    #! aşağıdaki gibi yaparsak senkron olur:
    # gorev1()
    # gorev2()

# asyncio.run ile asenkron işlemleri başlatırız.
asyncio.run(main())

"""
Çıktı: 
    Görev 1 başladı
    Görev 2 başladı
    Görev 2 tamamlandı
    Görev 1 tamamlandı
"""
