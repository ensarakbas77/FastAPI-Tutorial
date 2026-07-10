"""
Streamlit Nedir ? 
    - Python ile web arayüzü geliştirme freamework'ü

Yapay Zeka ve veri bilimi prolerinde neden kullanılır ?
    - ui ile hızlı bir şekilde prototip geliştirmek için
    - eğitilen bir modelin arayüzünü hızlı bir şekilde oluşturmak için
    - chabot örneği
    - model tahmini gösterme

Amaç:
    - Streamlit temel bileşenlerini öğrenmek
    - fastapi ile bir ml projesi yapmış gibi yapacağız

Temel bileşenler:
    1. sayfa ayarları
    2. başlık ve metinler
    3. sidebar örneği
    4. metiş giriş işlemleri
    5. sayısal giriş örneği
    6. seçim bileşenleri
    7. checkbox bileşenleri
    8. tarih ve saat
    9. dosya yükleme
    10. buton
    11. mesaj kutuları
    12. dataframe gösterimi
    13. sütun yapısı
    14. son bilgilendirme
"""

import streamlit as st
import pandas as pd
from datetime import date, datetime, time

# 1. sayfa ayarları
st.set_page_config(
    page_title="Streamlit Temel Bileşenler",
    page_icon=":guardsman:",
    layout="wide",
    initial_sidebar_state="expanded"
)
# çalıştırma komutu: streamlit run streamlit_temel_bilesenler.py

# 2. başlık ve metinler
st.title("Streamlit Temel Bileşenler Sayfası")
st.header("Python ile Web Uygulamlarına Giriş")
st.subheader("İlk Ders Uygulaması")
st.write("Streamlit, Python ile web arayüzü geliştirme framework'üdür. Yapay zeka ve veri bilimi projelerinde hızlı prototip geliştirmek için kullanılır.")

# 3. sidebar örneği
st.sidebar.title("Yan Menü")
st.sidebar.write("Streamlit sidebar alanıdır")
sidebar_name = st.sidebar.text_input("Adınızı Giriniz:", key="name")
sidebar_theme = st.sidebar.selectbox(
    "Sevdiğiniz alanı seçiniz:",
    ["Yapay Zeka", "NLP", "Veri Bilimi", "Görüntü İşleme"]
)
st.sidebar.success(f"Seçilen alan: {sidebar_theme}")

# 4. metin giriş işlemleri
st.header("Metin Giriş İşlemleri")
name = st.text_input("Ad Soyad Giriniz:", placeholder="Örn: Ahmet Yılmaz")
email = st.text_input("Email Adresinizi Giriniz:", placeholder="Örn: example@gmail.com")
about = st.text_area("Kendiniz Hakkında Kısa Bir Bilgi Yazınız:", placeholder="Örn: Ben bir veri bilimciyim...", height=120)

# 5. sayısal giriş örneği
st.header("Sayısal Giriş İşlemleri")
age = st.number_input("Yaşınızı Giriniz:", min_value=0, max_value=120, value=25, step=1)
experience = st.number_input("Deneyim Yılınızı Giriniz:", min_value=0, max_value=15, value=2, step=1)

# 6. seçim bileşenleri
city = st.selectbox("Şehir Seçiniz:", ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya"])
hobbies = st.multiselect("Hobilerinizi Seçiniz:", ["Spor", "Müzik", "Kitap Okuma", "Seyahat", "Yemek Yapma"])
education = st.radio("Eğitim Durumunuzu Seçiniz:", ["Lise", "Üniversite", "Yüksek Lisans", "Doktora"])

# 7. checkbox bileşenleri
st.header("Checkbox Bileşenleri")
is_student = st.checkbox("Öğrenci misiniz?")
accept_rules = st.checkbox("Kuralları kabul ediyorum")

# 8. tarih ve saat
st.header("Tarih ve Saat Seçimi")
selected_date = st.date_input("Tarih Seçiniz:", value=date.today())
selected_time = st.time_input("Saat Seçiniz:", value= time(10, 30))

# 9. dosya yükleme
st.header("Dosya Yükleme")
uploaded_file = st.file_uploader("Dosya Yükleyiniz:", type=["csv", "xlsx", "txt"])
if uploaded_file is not None:
    st.success(f"Dosya başarıyla yüklendi: {uploaded_file.name}")
    st.info(f"Dosya tipi: {uploaded_file.type}")
    st.info(f"Dosya boyutu: {uploaded_file.size} bytes")

# 10. buton
st.header("Buton Örneği")
if st.button("Gönder"):
    st.subheader("Girilen Bilgiler:")
    st.write(f"**Ad Soyad**: {name}")
    st.write(f"**Email**: {email}")

# 11. mesaj kutuları
st.header("Mesaj Kutuları")
st.info("Bu bir bilgilendirme mesajıdır.")
st.success("Bu bir başarı mesajıdır.")
st.warning("Bu bir uyarı mesajıdır.")
st.error("Bu bir hata mesajıdır.")

# 12. dataframe gösterimi
st.header("DataFrame Gösterimi")
sample_data = pd.DataFrame({
    "Ad": ["Ahmet", "Mehmet", "Ayşe", "Fatma"],
    "Yaş": [25, 30, 22, 28],
    "Şehir": ["İstanbul", "Ankara", "İzmir", "Bursa"]
})

st.dataframe(sample_data, use_container_width=True)

# 13. sütun yapısı
st.header("Sütun Yapısı")
col1, col2, col3 = st.columns(3)
with col1:
    st.write("Bu sütun 1'dir.")
    st.text_input("Sütun 1 için metin giriniz:", key="col1_input")
with col2:
    st.write("Bu sütun 2'dir.")
    st.text_input("Sütun 2 için metin giriniz:", key="col2_input")
with col3:
    st.write("Bu sütun 3'dir.")
    st.text_input("Sütun 3 için metin giriniz:", key="col3_input")
