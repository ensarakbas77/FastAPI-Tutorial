"""
Kullanıcı tarafı simülasyon
"""

import requests

BASE_URL = "http://127.0.0.1:8000"

"""
# kullanıcı mesajı
kullanici_mesaji = input("Mesajınızı girin: ")

# veri yapısı
gonderilecek_veri = {
    "mesaj": kullanici_mesaji
}

# chat endpoint'ine istek gönderme
response = requests.post(f"{BASE_URL}/chat", json=gonderilecek_veri)

# cevabı ekrana yazdırma
print(f"status code: {response.status_code}")
print("Cevap:", response.json()["model_cevabi"])
"""

# while döngüsü ile llm chatbotu gibi yapalım

while True:
    kullanici_mesaji = input("Mesajınızı girin (çıkmak için 'q' tuşuna basın): ")
    
    if kullanici_mesaji.lower() == 'q':
        print("Chatbot simülasyonu sonlandırıldı.")
        break

    gonderilecek_veri = {
        "mesaj": kullanici_mesaji
    }

    response = requests.post(f"{BASE_URL}/chat", json=gonderilecek_veri)

    print(f"status code: {response.status_code}")
    print("Cevap:", response.json()["model_cevabi"])
