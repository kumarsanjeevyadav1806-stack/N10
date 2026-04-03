import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Heavy Duty CSS (Custom Bottom Bar Fix)
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    
    /* Content Area Padding */
    .main .block-container {
        padding-bottom: 120px !important;
        max-width: 800px;
    }

    /* ChatGPT Style Messages */
    .stChatMessage { border-radius: 15px; background-color: #f7f7f8; margin-bottom: 10px; }

    /* Custom Floating Bottom Bar */
    .bottom-bar-container {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 750px;
        display: flex;
        align-items: center;
        gap: 10px;
        z-index: 9999;
        background: white;
        padding: 10px;
        border-radius: 30px;
        border: 1px solid #dfe1e5;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    /* Hide Streamlit Native Input if it exists */
    .stChatInput { display: none !important; }
    
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

# 4. CUSTOM BOTTOM UI (One Line Gemini Bar)
# Yahan humne column logic use kiya hai jo screen ke bottom par chipka rahega
with st.container():
    st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True) # Space filler
    
    # Is block ko bottom mein pin karne ke liye:
    col_plus, col_input = st.columns([0.15, 0.85])
    
    with col_plus:
        with st.popover("➕", help="Upload Photo/PDF"):
            uploaded_file = st.file_uploader("Attach", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")
    
    with col_input:
        # Humne st.text_input use kiya hai kyunki st.chat_input columns mein nahi chalta
        prompt = st.text_input("", placeholder="Ask Nexus anything... ✨", key="user_prompt", label_visibility="collapsed")

# 5. LOGIC
if prompt:
    img_b64 = None
    if uploaded_file and uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    backend_url = "https://web-production-68d0e.up.railway.app/ask"
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        with st.spinner("Analyzing... 🧠"):
            try:
                res = requests.post(backend_url, json={"user_input": prompt, "image_b64": img_b64}, timeout=120)
                if res.status_code == 200:
                    answer = res.json().get("response")
                    for word in answer.split():
                        full_res += word + " "
                        time.sleep(0.04)
                        placeholder.markdown(full_res + "▌")
                    placeholder.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                    # Clear input simulation by rerun
                    st.rerun()
                else:
                    st.error("Engine Timeout!")
            except Exception as e:
                st.error(f"Error: {e}")

# Sidebar
with st.sidebar:
    st.title("🕒 Activity")
    if st.button("🗑️ Reset All"):
        st.session_state.messages = []
        st.rerun()
        
