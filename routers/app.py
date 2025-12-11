import streamlit as st
import requests

FASTAPI_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Instagram Comment Auto Reply", layout="centered")

st.markdown("""
<h1 style='text-align:center;'>Instagram Comment Auto Reply</h1>
""", unsafe_allow_html=True)

# Instagram Access Token
token = st.text_input("Instagram Access Token", type="password")

# Incoming comment
comment_text = st.text_area("Incoming Instagram Comment")

if st.button("Generate Reply"):
    if not token or not comment_text:
        st.error("Please enter both Access Token and Comment.")
    else:
        payload = {
            "token": token,
            "comment": comment_text
        }

        response = requests.post(f"{FASTAPI_URL}/webhook/manual", json=payload)

        if response.status_code == 200:
            reply = response.json().get("reply", "")
            st.subheader("Generated Reply:")
            st.success(reply)
        else:
            st.error("Backend error. Check logs.")
