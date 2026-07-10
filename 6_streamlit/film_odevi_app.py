import streamlit as st
import requests

# sayfa ayarları
st.set_page_config(
    page_title="Film Yorumu Duygu Analizi",
    page_icon="🎬",
    layout="centered"
)

# Başlık ve açıklama
st.title("🎬 Film Yorumu Duygu Analizi")
st.write("Bir film yorumu yazın. Sistem yorumun pozitif, negatif veya nötr olup olmadığını analiz etsin.")
st.markdown("---")

# Örnek yorumlar
sample_comment = st.selectbox(
    "Hazır bir örnek yorum seçebilirsiniz",
    [
        "Bir yorum seçiniz",
        "Film gerçekten harikaydı, oyunculuklar çok başarılıydı ve çok etkilendim.",
        "Bu kadar sıkıcı ve anlamsız bir film uzun zamandır izlememiştim.",
        "Film ne çok iyi ne de çok kötüydü, ortalama bir yapımdı."
    ]
)

# yorum giriş alanı
if sample_comment != "Bir yorum seçiniz":
    default_text = sample_comment
else:
    default_text = ""

comment = st.text_area(
    "Film yorumunuzu yazınız",
    value=default_text,
    height=180,
    placeholder="Örneğin: Film çok güzeldi, oyuncuların performansını çok beğendim."
)

# analiz butonu
if st.button("Yorumu Analiz Et"):
    if not comment.strip():
        st.warning("Lütfen analiz etmek için bir yorum giriniz.")
    else:
        try:
            api_url = "http://127.0.0.1:8000/analyze"

            payload = {
                "comment": comment
            }

            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                result = response.json()

                if result["success"]:
                    st.success("Analiz tamamlandı.")
                    st.markdown("---")
                    st.subheader("Analiz Sonucu:")
                    
                    st.write(f"**Yorum:** {result['comment']}")
                    st.write(f"**Duygu Durumu:** {result['sentiment']}")
                    st.write(f"**Açıklama:** {result['explanation']}")
                    st.write(f"**Pozitif Kelime Skoru:** {result['positive_score']}")
                    st.write(f"**Negatif Kelime Skoru:** {result['negative_score']}")

                    if result["sentiment"] == "Pozitif":
                        st.success("Sonuç: Pozitif Yorum")
                    elif result["sentiment"] == "Negatif":
                        st.error("Sonuç: Negatif Yorum")
                    else:
                        st.info("Sonuç: Nötr Yorum")

                else:
                    st.error(result["message"])
            else:
                st.error("API tarafında bir hata oluştu.")
                st.write(response.text)

        except requests.exceptions.ConnectionError:
            st.error("FastAPI servisine bağlanılamadı. Önce backend'i çalıştırın.")

        except Exception as e:
            st.error(f"Beklenmeyen bir hata oluştu: {e}")