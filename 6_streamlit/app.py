"""
Stramlit
"""

import streamlit as st
import requests
import PIL.Image as Image

# sayfa ayarları
st.set_page_config(
    page_title="Görüntü Üzerinden Sahte Hastalık Tespiti Sistemi",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="auto"
)

# başlık ve açıklamalar
st.title("Görüntü Üzerinden Sahte Hastalık Tespiti Sistemi")
st.write("Görüntü yükle ve hastalık teşhisi sonucunu gör.")
st.markdown("---")

# dosya yükleme
uploaded_file = st.file_uploader("Bir görüntü yükleyin", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:

    image = Image.open(uploaded_file)
    st.image(image, caption="Yüklenen Görüntü", use_column_width=True)

    # tahmin butonu
    if st.button("Tahmin Et"):
        try:
            uploaded_file.seek(0)  # Dosya konumunu başa al

            api_url = "http://localhost:8000/predict"  # FastAPI endpoint URL

            files = {
                "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
            }

            response = requests.post(api_url, files=files)

            if response.status_code == 200:
                result = response.json()
                st.success(f"Sonuç: {result['file_name']} - {result['disease_status']} (Olasılık: {result['probability']})")

                if result['disease_status'] == "Hastalık var":
                    st.warning("Dikkat: Görüntüde hastalık tespit edildi.")
                else:
                    st.info("Görüntüde hastalık tespit edilmedi.")

            else:
                st.error(f"API hatası: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

else:
    st.info("Lütfen bir görüntü yükleyin.")