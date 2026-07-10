import streamlit as st
import requests

BACKEND_URL = "https://fastapi-tutorial-dhqf.onrender.com/roadmap"

st.set_page_config(
    page_title="AI Roadmap",
    page_icon="🤖",
    layout="centered",
)
st.title("AI Yol Haritası Uygulaması")
st.write("Bir alan seçin, ai size hazır yol haritasını sunacaktır.")

secim = st.selectbox(
    "Alan Seçin",
    ["yapay_zeka", "derin_ogrenme", "nlp"]
)

if st.button("Yol Haritasını Getir"):
    try:
        response = requests.post(BACKEND_URL, json={"roadmap_name": secim}, timeout=50)
        data = response.json()
        if "error" in data:
            st.error(data["error"])
        else:
            st.success(f"Alan: {data['alan']}")
            st.subheader("Yol Haritası")
            for i, adim in enumerate(data["adımlar"], start=1):
                st.write(f"{i}. {adim}")

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
            