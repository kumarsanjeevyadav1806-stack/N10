import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Ultra-Fix CSS
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .main .block-container { padding-bottom: 120px !important; max-width: 850px; }
    .stChatMessage { border-radius: 15px; background-color: #f7f7f8; margin-bottom: 12px; border: 1px solid #eee; }
    [data-testid="stBottomBlockContainer"] { background-color: white !important; border-top: 1px solid #f0f2f6; padding: 15px 5% 35px 5% !important; }
    [data-testid="column"] { width: fit-content !important; flex: unset !important; min-width: unset !important; }
    div[data-testid="stPopover"] > button { border-radius: 50% !important; width: 48px; height: 48px; background-color: #f0f4f9 !important; border: none !important; font-size: 22px; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")

# 3. Session State Management
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FIX: Input Clearing Logic ---
def handle_input():
    user_input = st.session_state.nexus_input
    if user_input:
        st.session_state.current_prompt = user_input
        st.session_state.nexus_input = "" # Input box ko turant khali karo

if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = None

# Display Chat History
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if st.button(f"📋 Copy", key=f"cp_{i}"):
                st.write(f'<script>navigator.clipboard.writeText("{msg["content"].encode("unicode_escape").decode()}");</script>', unsafe_allow_html=True)

# 4. FIXED BOTTOM UI (Plus + Search)
with st.container():
    col1, col2 = st.columns([0.15, 0.85])
    with col1:
        with st.popover("➕"):
            uploaded_file = st.file_uploader("Upload", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")
    with col2:
        # 'on_change' use kar rahe hain taaki enter dabate hi input clear ho jaye
        st.text_input("", placeholder="Ask Gemini...", key="nexus_input", on_change=handle_input, label_visibility="collapsed")

# 5. PROCESSING LOGIC
if st.session_state.current_prompt:
    prompt = st.session_state.current_prompt
    st.session_state.current_prompt = None # Reset taaki loop na bane

    img_b64 = None
    if uploaded_file and uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    # User side display
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun() # Turant rerun karo taaki user ka message screen par dikhe

# AI Response Logic (Jab messages mein last message 'user' ka ho)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_user_msg = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        with st.spinner("Analyzing... 🧠"):
            try:
                backend_url = "https://web-production-68d0e.up.railway.app/ask"
                res = requests.post(backend_url, json={"user_input": last_user_msg, "image_b64": None}, timeout=120)
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
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()
        
