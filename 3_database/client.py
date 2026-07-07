"""
Amaç:
    - fastapi ile oluşturulan endpointleri test etme
    - post isteği ile yeni kayıt ekleme ve get isteği ile kayıtları listeleme
"""

import requests

BASE_URL = "http://127.0.0.1:7002"

gonderilecek_veri = {
    "kullanici_mesaji": "Merhaba ben client", 
    "bot_cevabi": "Merhaba client ben de chatbot"
}

post_response = requests.post(f"{BASE_URL}/mesaj-ekle", json=gonderilecek_veri) # http://127.0.0.1:7002/mesaj-ekle
print("POST İsteği Durumu:", post_response.status_code)
print("POST İsteği Yanıtı:", post_response.json())

get_response = requests.get(f"{BASE_URL}/mesajlar") # http://127.0.0.1:7002/mesajlar
print("GET İsteği Durumu:", get_response.status_code)
print("GET İsteği Yanıtı:", get_response.json())


"""
POST İsteği Durumu: 200
POST İsteği Yanıtı: {'durum': 'Başarılı', 'mesaj': 'Kayıt db ye başarıyla eklendi.', 'eklenen_veri': {'kullanici_mesaji': 'Merhaba ben client', 'bot_cevabi': 'Merhaba client ben de chatbot'}}


GET İsteği Durumu: 200
GET İsteği Yanıtı: {

'durum': 'Başarılı', 'toplam_kayit_sayisi': 5, 

'kayitlar': [
{'id': 1, 'kullanici_mesaji': 'Merhaba ben Ronaldo', 'bot_cevabi': 'Merhaba! Ronaldocum nasılsın?'}, 
{'id': 3, 'kullanici_mesaji': 'Merhaba ben Messi', 'bot_cevabi': 'Merhaba! Messiciğim nasılsın?'}, 
{'id': 6, 'kullanici_mesaji': 'Merhaba', 'bot_cevabi': 'Merhaba! Size nasıl yardımcı olabilirim?'}, 
{'id': 9, 'kullanici_mesaji': 'ensar sa', 'bot_cevabi': 'as'}, 
{'id': 21, 'kullanici_mesaji': 'Merhaba ben client', 'bot_cevabi': 'Merhaba client ben de chatbot'}
]
}
"""