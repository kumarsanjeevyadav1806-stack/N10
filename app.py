import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Ultra-Advanced CSS (Perfect Gemini Bottom Bar)
st.markdown("""
    <style>
    /* Global White Theme */
    .stApp { background-color: white; color: black; }
    
    /* Content Padding to avoid bottom overlap */
    .main .block-container {
        padding-bottom: 150px !important;
        max-width: 850px;
    }

    /* Message Bubbles - ChatGPT Style */
    .stChatMessage { 
        border-radius: 18px; 
        background-color: #f7f7f8; 
        margin-bottom: 12px;
        border: 1px solid #f0f0f0;
    }

    /* Fixed Bottom Container for Plus + Input */
    /* This ensures it sticks like Gemini */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 20px;
        z-index: 1000;
        padding-left: 70px !important; /* Space for Plus icon on the left */
    }

    /* Plus Button Popover - Gemini Style Positioning */
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
        border: none !important;
        font-size: 22px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Clean Hide for Streamlit default footer */
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")

# 3. Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. BOTTOM UI (Plus + Search Bar Side-by-Side)
# Plus icon is fixed via CSS at bottom-left
with st.popover("➕"):
    st.markdown("### Attach File 📂")
    uploaded_file = st.file_uploader("Photo or PDF", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"Attached: {uploaded_file.name} ✅")

# Search Input (Niche Fixed via CSS)
prompt = st.chat_input("Ask Nexus anything... ✨")

# 5. LOGIC (With ChatGPT-style Emojis)
if prompt:
    img_b64 = None
    if uploaded_file and uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    # User message
    st.session_state.messages.append({"role": "user", "content": f"👤 {prompt}"})
    with st.chat_message("user"):
        st.markdown(f"👤 {prompt}")

    backend_url = "https://web-production-68d0e.up.railway.app/ask"
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        with st.spinner("Analyzing... 🧠"):
            try:
                # Adding emoji context to system prompt in payload
                payload = {"user_input": prompt, "image_b64": img_b64}
                res = requests.post(backend_url, json=payload, timeout=120)
                
                if res.status_code == 200:
                    answer = res.json().get("response")
                    
                    # ChatGPT Typing Effect ✍️
                    for word in answer.split():
                        full_res += word + " "
                        time.sleep(0.04)
                        placeholder.markdown(full_res + "▌")
                    placeholder.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                else:
                    st.error("Engine Busy! 🛑")
            except Exception as e:
                st.error(f"Error: {e} ⚠️")

# Sidebar
with st.sidebar:
    st.title("🕒 Recent Activity")
    st.write("---")
    if st.button("🗑️ Clear All Chats"):
        st.session_state.messages = []
        st.rerun()
    st.info("Nexus is in **Pro Mode** ⚡\nMemory & Search are active.")
    
