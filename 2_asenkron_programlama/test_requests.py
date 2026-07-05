"""
Amaç:
    - request kütüphanesi ile get ve post istekleri gönder
"""

from urllib import request

import requests

BASE_URL = "http://127.0.0.1:8000"  # fastapi servisimizi temel adresi

# get isteği gönderme
get_response = requests.get(f"{BASE_URL}/durum")  # http://127.0.0.1:8000/durum
print(f"status code: {get_response.status_code}")
print(f"get response: {get_response.json()}")

# post isteği gönderme
post_data = {
    "mesaj": "merhaba fastapi"
}

post_response = requests.post(f"{BASE_URL}/mesaj", json=post_data)  # http://127.0.0.1:8000/mesaj
print(f"status code: {post_response.status_code}")
print(f"post response: {post_response.json()}")


"""
status code: 200
get response: {'durum': 'başarılı', 'mesaj': 'get endpointi çalıştı'}

status code: 200
post response: {'durum': 'başarılı', 'gelen_veri': 'merhaba fastapi', 'cevap': 'post mesajı başarıyla alındı'}
"""