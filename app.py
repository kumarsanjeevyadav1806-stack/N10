import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Refined CSS (Fixes Visibility Problem)
st.markdown("""
    <style>
    /* Global White Theme */
    .stApp { background-color: white; color: black; }
    
    /* Padding for Chat History */
    .main .block-container {
        padding-bottom: 100px;
        max-width: 800px;
    }

    /* ChatGPT Style Messages */
    .stChatMessage { 
        border-radius: 15px; 
        background-color: #f7f7f8; 
        margin-bottom: 10px; 
    }

    /* Plus Button Popover Styling */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        background-color: #f0f4f9 !important;
        border: 1px solid #dfe1e5 !important;
        font-size: 20px !important;
    }

    /* Fixed Layout for Bottom Bar */
    .bottom-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 10px 20px;
        z-index: 1000;
        border-top: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")

# 3. Session State for History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. FIXED BOTTOM UI (Plus + Search Bar Side-by-Side)
# We use a container to keep them together at the bottom
with st.container():
    col_icon, col_input = st.columns([0.15, 0.85])
    
    with col_icon:
        with st.popover("➕"):
            st.markdown("### Attachments")
            uploaded_file = st.file_uploader("Photo/PDF", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")
    
    with col_input:
        prompt = st.chat_input("Ask Nexus anything...")

# 5. LOGIC
if prompt:
    img_b64 = None
    if uploaded_file and uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Backend URL (Ensure this matches your Railway)
    backend_url = "https://web-production-68d0e.up.railway.app/ask"
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        with st.spinner("Analyzing..."):
            try:
                payload = {"user_input": prompt, "image_b64": img_b64}
                res = requests.post(backend_url, json=payload, timeout=120)
                
                if res.status_code == 200:
                    answer = res.json().get("response")
                    for word in answer.split():
                        full_res += word + " "
                        time.sleep(0.04)
                        placeholder.markdown(full_res + "▌")
                    placeholder.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                else:
                    st.error("Server is busy. Check Railway logs.")
            except Exception as e:
                st.error(f"Error: {e}")

# Sidebar
with st.sidebar:
    st.title("🕒 Recent Activity")
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()
        
