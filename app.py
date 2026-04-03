import streamlit as st
import requests
import base64
import time

# 1. Page Config
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Advance Gemini CSS (Plus Menu & Search Bar)
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .main .block-container { padding-bottom: 120px !important; }
    
    /* Gemini Plus Button Style */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 48px !important;
        height: 48px !important;
        background-color: #f0f4f9 !important;
        border: none !important;
        font-size: 22px !important;
        transition: 0.3s ease;
    }
    
    /* Menu Item Styling */
    .menu-btn {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px;
        border-radius: 10px;
        cursor: pointer;
        font-weight: 500;
    }

    [data-testid="stBottomBlockContainer"] {
        background-color: white !important;
        border-top: 1px solid #f0f2f6;
        padding: 15px 5% 35px 5% !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")

# 3. Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            st.button(f"📋 Copy", key=f"cp_{i}")

# 4. ADVANCE PLUS MENU (Gemini Style)
with st.container():
    col1, col2 = st.columns([0.15, 0.85])
    
    with col1:
        with st.popover("➕"):
            st.markdown("### Choose Action")
            # Multiple Options like Gemini
            opt = st.radio("", ["📁 Files", "📷 Camera", "🖼️ Gallery"], label_visibility="collapsed")
            
            if opt == "📷 Camera":
                uploaded_file = st.camera_input("Take a photo")
            else:
                uploaded_file = st.file_uploader("Upload Image/PDF", type=['png', 'jpg', 'jpeg', 'pdf'])
            
            if uploaded_file:
                st.success(f"Selected: {uploaded_file.name} ✅")

    with col2:
        prompt = st.chat_input("Ask Nexus anything... ✨")

# 5. VISION & CHAT LOGIC
if prompt:
    img_b64 = None
    if uploaded_file and uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        with st.spinner("Analyzing... 🧠"):
            try:
                backend_url = "https://web-production-68d0e.up.railway.app/ask"
                res = requests.post(backend_url, json={"user_input": prompt, "image_b64": img_b64}, timeout=150)
                if res.status_code == 200:
                    answer = res.json().get("response")
                    for word in answer.split():
                        full_res += word + " "
                        time.sleep(0.03)
                        placeholder.markdown(full_res + "▌")
                    placeholder.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                    st.rerun()
                else:
                    st.error("Engine Error! Check Model.")
            except Exception as e:
                st.error(f"Error: {e}")
                
