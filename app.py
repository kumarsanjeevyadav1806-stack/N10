import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Advanced CSS for Fixed Bottom Bar
st.markdown("""
    <style>
    /* White Theme */
    .stApp { background-color: white; color: black; }
    
    /* Content Padding to avoid bottom overlap */
    .main .block-container {
        padding-bottom: 150px;
        max-width: 800px;
    }

    /* Message Bubbles */
    .stChatMessage { 
        border-radius: 15px; 
        background-color: #f7f7f8; 
        margin-bottom: 10px; 
    }

    /* Fixed Bottom Container for Plus + Input */
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 10px 5% 30px 5%;
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 10px;
        border-top: 1px solid #f0f2f6;
    }

    /* Plus Button Popover Styling */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 48px !important;
        height: 48px !important;
        background-color: #f0f4f9 !important;
        border: none !important;
        font-size: 22px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Make chat input fit properly next to plus */
    .stChatInput {
        padding-bottom: 0px !important;
    }
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

# 4. THE MAGIC BOTTOM ROW (Plus + Search)
# Columns allow them to sit side-by-side at the bottom
col_plus, col_input = st.columns([0.12, 0.88])

with col_plus:
    with st.popover("➕"):
        st.markdown("### Attach File")
        uploaded_file = st.file_uploader("Photo or PDF", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")
        if uploaded_file:
            st.success(f"Attached: {uploaded_file.name}")

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
                    # Typing Effect
                    for word in answer.split():
                        full_res += word + " "
                        time.sleep(0.04)
                        placeholder.markdown(full_res + "▌")
                    placeholder.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
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
        
