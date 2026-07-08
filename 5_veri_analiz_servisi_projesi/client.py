"""
9. request ile client testi yapmak
"""

import requests

BASE_URL = "http://127.0.0.1:8000"

def test_upload_csv(file_path: str):
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'text/csv')}
            response = requests.post(f"{BASE_URL}/upload_csv", files=files)
            print("Upload CSV Response:", response.json())

    except Exception as e:
        print(f"CSV yükleme testi sırasında bir hata oluştu: {e}")

def test_analysis_history():
    try:
        response = requests.get(f"{BASE_URL}/analysis-history")
        print("Analysis History Response:", response.json())
    except Exception as e:
        print(f"Analiz geçmişi testi sırasında bir hata oluştu: {e}")

def test_analysis_details(analysis_id: int):
    try:
        response = requests.get(f"{BASE_URL}/analysis/{analysis_id}")
        print(f"Analysis Details for ID {analysis_id} Response:", response.json())
    except Exception as e:
        print(f"Analiz detayları testi sırasında bir hata oluştu: {e}")

# 10. tüm sistemi test et
test_upload_csv("sample_data.csv")  # CSV dosyasını yükle
print("*"*50)
test_analysis_history()  # Analiz geçmişini al
print("*"*50)
test_analysis_details(1)  # ID'si 1 olan analiz detaylarını al
