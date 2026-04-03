import streamlit as st
import requests
import base64

# 1. Page Config
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Gemini Style CSS (White Theme + Rounded UI)
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .stChatMessage { border-radius: 20px; border: none; background-color: #f0f4f9; padding: 15px; margin-bottom: 10px; }
    
    /* Plus Menu Container Styling */
    .stPopover { width: 100%; }
    button[kind="secondary"] { 
        border-radius: 50%; 
        width: 45px; 
        height: 45px; 
        border: 1px solid #dfe1e5;
        background-color: #f8f9fa;
    }
    
    /* Bottom Sheet Simulation Styling */
    .menu-item {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 12px;
        border-radius: 10px;
        cursor: pointer;
        transition: 0.3s;
    }
    .menu-item:hover { background-color: #f1f3f4; }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")

# 3. Memory Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. GEMINI PLUS MENU (Bottom Sheet Simulation)
# Hum Popover use kar rahe hain jo click karne par Gemini menu kholega
with st.popover("➕"):
    st.markdown("### Attach")
    
    # Menu Options
    cam_file = st.camera_input("📷 Camera")
    gal_file = st.file_uploader("🖼️ Gallery / Files", type=['png', 'jpg', 'jpeg', 'pdf'])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📁 Drive"): st.info("Drive coming soon")
    with col2:
        if st.button("📓 Notebooks"): st.info("Notebooks coming soon")

# 5. CHAT INPUT
if prompt := st.chat_input("Ask Gemini..."):
    # Image handling if attached
    img_b64 = None
    target_file = cam_file if cam_file else gal_file
    if target_file:
        img_b64 = base64.b64encode(target_file.getvalue()).decode()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Backend API Call
    backend_url = "https://web-production-68d0e.up.railway.app/ask"
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                payload = {"user_input": prompt, "image_b64": img_b64}
                response = requests.post(backend_url, json=payload, timeout=90)
                if response.status_code == 200:
                    answer = response.json().get("response")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Engine busy.")
            except:
                st.error("Connection Failed")

# Sidebar
with st.sidebar:
    st.title("🕒 History")
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()
        
