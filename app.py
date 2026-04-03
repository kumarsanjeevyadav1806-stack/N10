import streamlit as st
import requests
import base64

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Gemini Style CSS (Fixed Bottom Row)
st.markdown("""
    <style>
    /* White Background */
    .stApp { background-color: white; color: black; }
    
    /* Padding for Chat area */
    .main .block-container {
        padding-bottom: 120px;
    }

    /* Message Bubbles */
    .stChatMessage { 
        border-radius: 20px; 
        border: none; 
        background-color: #f0f4f9; 
        padding: 15px; 
        margin-bottom: 10px; 
    }

    /* Fixed Bottom Container for Plus and Input */
    .bottom-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        padding: 20px;
        z-index: 1000;
        border-top: 1px solid #f0f2f6;
    }
    
    /* Styling Plus Popover inside the bar */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        background-color: #f0f4f9 !important;
        border: none !important;
        font-size: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖")

# 3. Memory & Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. GEMINI STYLE BOTTOM BAR (Plus + Search)
# Columns use kar rahe hain taaki Plus icon search ke sath dikhe
col_plus, col_search = st.columns([0.15, 0.85])

with col_plus:
    with st.popover("➕"):
        st.markdown("**Upload File**")
        uploaded_file = st.file_uploader("Select Photo or PDF", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")

with col_search:
    prompt = st.chat_input("Ask Nexus anything...")

# 5. PROCESSING LOGIC
if prompt:
    img_b64 = None
    if uploaded_file and uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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
                    st.error("Backend Error")
            except:
                st.error("Connection Failed")

# Sidebar
with st.sidebar:
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()
        
