import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Ultra-Fix CSS (Plus and Search in One Row at Bottom)
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    
    /* Content Padding */
    .main .block-container {
        padding-bottom: 120px !important;
        max-width: 800px;
    }

    /* Message Bubbles */
    .stChatMessage { border-radius: 15px; background-color: #f7f7f8; margin-bottom: 10px; }

    /* THE FIX: Pinning the Bottom Bar and forcing Side-by-Side */
    [data-testid="stBottomBlockContainer"] {
        background-color: white !important;
        border-top: 1px solid #eee;
        padding: 10px 5% 30px 5% !important;
    }

    /* Force columns to stay side-by-side on mobile */
    [data-testid="column"] {
        width: fit-content !important;
        flex: unset !important;
        min-width: unset !important;
    }
    
    /* Plus Button Styling */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        background-color: #f0f4f9 !important;
        border: none !important;
        font-size: 20px !important;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")

# 3. Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if st.button(f"📋 Copy", key=f"cp_{i}"):
                st.write(f'<script>navigator.clipboard.writeText("{msg["content"].encode("unicode_escape").decode()}");</script>', unsafe_allow_html=True)

# 4. FIXED BOTTOM UI (Plus + Search Together)
# Humne columns ke width ko pixels mein fix kiya hai taaki mobile par stack na ho
with st.container():
    col1, col2 = st.columns([0.15, 0.85])
    
    with col1:
        with st.popover("➕"):
            st.markdown("### Attach 📂")
            uploaded_file = st.file_uploader("Upload", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")
    
    with col2:
        prompt = st.text_input("", placeholder="Ask Nexus anything... ✨", key="nexus_input", label_visibility="collapsed")

# 5. LOGIC
if prompt:
    img_b64 = None
    if uploaded_file and uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    backend_url = "https://web-production-68d0e.up.railway.app/ask"
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        with st.spinner("Analyzing... 🧠"):
            try:
                res = requests.post(backend_url, json={"user_input": f"Direct solve: {prompt}", "image_b64": img_b64}, timeout=120)
                if res.status_code == 200:
                    answer = res.json().get("response")
                    for word in answer.split():
                        full_res += word + " "
                        time.sleep(0.04)
                        placeholder.markdown(full_res + "▌")
                    placeholder.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                    st.rerun()
                else:
                    st.error("Engine Busy!")
            except Exception as e:
                st.error(f"Error: {e}")

# Sidebar
with st.sidebar:
    st.title("🕒 Activity")
    if st.button("🗑️ Reset All"):
        st.session_state.messages = []
        st.rerun()
