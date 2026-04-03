import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Gemini Hybrid CSS (Fixed Bottom Bar)
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    
    /* Content Padding */
    .main .block-container { padding-bottom: 150px; max-width: 850px; }

    /* Chat Bubbles */
    .stChatMessage { border-radius: 15px; background-color: #f7f7f8; margin-bottom: 10px; }
    
    /* Fixed Plus Icon at Bottom Left */
    div[data-testid="stPopover"] {
        position: fixed;
        bottom: 32px;
        left: 20px;
        z-index: 1001;
    }

    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 48px !important;
        height: 48px !important;
        background-color: #f0f4f9 !important;
        border: 1px solid #dfe1e5 !important;
        font-size: 22px !important;
    }

    /* Fixed Search Bar at Bottom */
    .stChatInput {
        position: fixed;
        bottom: 20px;
        padding-left: 65px !important; /* Space for Plus icon */
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")

# 3. Session State for Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. BOTTOM UI (Plus + Search)
with st.popover("➕"):
    st.markdown("### Attachments")
    uploaded_file = st.file_uploader("Photo or PDF", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"Attached: {uploaded_file.name}")

prompt = st.chat_input("Ask Nexus anything...")

# 5. PROCESSING LOGIC
if prompt:
    # Handle Image
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
        with st.spinner("Processing..."):
            try:
                payload = {"user_input": prompt, "image_b64": img_b64}
                res = requests.post(backend_url, json=payload, timeout=120)
                
                if res.status_code == 200:
                    answer = res.json().get("response")
                    
                    # ChatGPT Typing Effect
                    for word in answer.split():
                        full_res += word + " "
                        time.sleep(0.04)
                        placeholder.markdown(full_res + "▌")
                    placeholder.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                else:
                    st.error("Backend Error!")
            except Exception as e:
                st.error(f"Connection Failed: {e}")

# Sidebar
with st.sidebar:
    st.title("⚙️ Nexus Memory")
    if st.button("🗑️ Reset Permanent Chat"):
        st.session_state.messages = []
        st.rerun()
    st.info("Nexus Flow has 'God Level' Memory enabled.")
    
