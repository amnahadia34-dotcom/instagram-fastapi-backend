import sys, os
import time
import base64
import requests
import streamlit as st

# -----------------------------------------------------
# PYTHONPATH FIX
# -----------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BASE_DIR)

from services.queue_poll import get_event


FASTAPI_URL = "http://127.0.0.1:8000"


# -----------------------------------------------------
# STREAMLIT PAGE SETUP
# -----------------------------------------------------
st.set_page_config(page_title="Instagram Auto-Reply System", layout="wide")

st.title("🤖 Instagram Auto-Reply Dashboard")


# -----------------------------------------------------
# SOUND ALERT FUNCTION
# -----------------------------------------------------
def play_sound():
    try:
        sound_file = os.path.join(CURRENT_DIR, "alert.mp3")
        with open(sound_file, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            html = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
            st.markdown(html, unsafe_allow_html=True)
    except:
        pass  # If sound file missing, ignore gracefully


# -----------------------------------------------------
# GOOGLE SHEET PREVIEW FUNCTION
# -----------------------------------------------------
def show_google_sheet():
    st.subheader("📊 Google Sheet — Current Leads")

    try:
        r = requests.get(f"{FASTAPI_URL}/leads")
        if r.status_code == 200:
            leads = r.json()
            st.dataframe(leads)
        else:
            st.error("Failed to fetch Google Sheet data.")
    except:
        st.error("Error connecting to backend.")


# -----------------------------------------------------
# SIDEBAR SETTINGS
# -----------------------------------------------------
with st.sidebar:
    st.header("⚙️ System Settings")

    ig_token = st.text_input("IG Token", type="password")
    page_id = st.text_input("Instagram Page ID")
    openai_key = st.text_input("OpenAI API Key", type="password")

    dataset_mode = st.radio("AI Reply Source", ["Use OpenAI", "Use Dataset"])

    if st.button("Save Settings"):
        payload = {
            "instagram_token": ig_token,
            "instagram_id": page_id,
            "openai_key": openai_key,
            "dataset_mode": dataset_mode
        }
        r = requests.post(f"{FASTAPI_URL}/settings/save_all", json=payload)
        if r.status_code == 200:
            st.success("Settings Saved ✔")
        else:
            st.error("Error saving settings.")

    st.markdown("---")
    show_google_sheet()  # ⭐ GOOGLE SHEET PREVIEW ADDED HERE ⭐


# -----------------------------------------------------
# DATASET UPLOAD
# -----------------------------------------------------
st.subheader("📂 Upload Dataset (Optional)")

uploaded = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

if uploaded:
    bytes_data = uploaded.read()
    encoded = base64.b64encode(bytes_data).decode()

    payload = {"filename": uploaded.name, "filedata": encoded}

    r = requests.post(f"{FASTAPI_URL}/dataset/upload", json=payload)

    if r.status_code == 200:
        st.success("Dataset processed & saved!")
    else:
        st.error("Dataset upload failed.")

st.markdown("---")


# -----------------------------------------------------
# AUTOREPLY TOGGLE
# -----------------------------------------------------
st.subheader("🤖 Auto Reply Mode")

auto_mode = st.radio("Auto Reply", ["OFF", "ON"])

if st.button("Update Auto Mode"):
    r = requests.post(f"{FASTAPI_URL}/settings/autoreply", json={"status": auto_mode})
    if r.status_code == 200:
        st.success(f"Auto Reply is now {auto_mode}")
    else:
        st.error("Error updating auto reply mode.")

st.markdown("---")


# -----------------------------------------------------
# REAL-TIME INSTAGRAM COMMENT FEED
# -----------------------------------------------------
st.subheader("🔔 Live Instagram Notifications")

event = get_event()

if event:
    play_sound()  # ⭐ SOUND ALERT TRIGGER ⭐

    st.success(
        f"""
        📩 **New Comment Received**

        👤 **User:** {event['username']}
        💬 **Comment:** {event['comment']}

        Press **Generate Reply** below to respond:
        """
    )

    if st.button("Generate Reply for Latest Comment"):
        r = requests.post(
            f"{FASTAPI_URL}/webhook/reply_now",
            json={
                "comment": event["comment"],
                "username": event["username"],
                "comment_id": event["comment_id"]
            }
        )

        if r.status_code == 200:
            st.success(f"Reply Sent ✔\n\nAI Reply: {r.json()['reply']}")
        else:
            st.error("Failed to send reply.")


# -----------------------------------------------------
# AUTO REFRESH EVERY 3 SECONDS (NO WHILE LOOP)
# -----------------------------------------------------
st.caption("Refreshing every 3 seconds…")
time.sleep(3)
st.rerun()
