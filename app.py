import streamlit as st
import requests
import base64
import time
import PyPDF2

st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# --- CSS ---
st.markdown("""
<style>
.stApp { background-color: white; color: black; }
.main .block-container { padding-bottom: 120px; max-width: 800px; }
.stChatMessage { border-radius: 15px; background-color: #f7f7f8; padding: 20px; margin-bottom: 15px; }
.stChatInput { position: fixed; bottom: 20px; padding-left: 70px !important; }
div[data-testid="stPopover"] { position: fixed; bottom: 32px; left: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")
st.caption("PRO Mode Enabled 🚀")

# --- Session Memory ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- File Upload ---
with st.popover("➕"):
    uploaded_file = st.file_uploader("Upload", type=['png','jpg','jpeg','pdf'])

# --- Input ---
prompt = st.chat_input("Ask anything...")

if prompt:
    img_b64 = None
    pdf_text = None

    # Image
    if uploaded_file and uploaded_file.type in ['image/png','image/jpeg','image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    # PDF
    if uploaded_file and uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text()

    # Save user msg
    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # --- API CALL ---
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full = ""

        payload = {
            "user_input": prompt,
            "messages": st.session_state.messages,
            "image_b64": img_b64,
            "pdf_text": pdf_text
        }

        try:
            res = requests.post("http://localhost:8000/ask", json=payload)

            answer = res.json()["response"]

            # typing effect
            for word in answer.split():
                full += word + " "
                time.sleep(0.03)
                placeholder.markdown(full + "▌")

            placeholder.markdown(full)

            st.session_state.messages.append({"role":"assistant","content":full})

        except:
            st.error("Backend not running!")

# Sidebar
with st.sidebar:
    if st.button("🗑️ Clear"):
        st.session_state.messages = []
        st.rerun()
