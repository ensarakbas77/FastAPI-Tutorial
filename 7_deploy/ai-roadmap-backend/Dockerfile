# hangi temel imajı kullanacağımızı belirtiyoruz
# python:3.11 kullanalım
FROM python:3.11-slim

# container içinde çalışma klasörünü belirle
WORKDIR /app

# requirements.txt kurulsun
COPY requirements.txt .

# gerekli paketleri kuruyoruz
RUN pip install --no-cache-dir -r requirements.txt

# projedeki diğer dosyaları container içine kopyalıyoruz
COPY . .

# container ayağa kalktığında hangi komut çalışsın onu belirtiyoruz
# fastapi uvicorn ile çalıştırılacak, 0.0.0.0 container dışından erişim için, 8000 portu kullanılacak
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]