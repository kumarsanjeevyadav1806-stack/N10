import streamlit as st
import requests
import base64

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Gemini Style CSS (Fixed Bottom Input + Floating Plus)
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: white; color: black; }
    
    /* Chat messages padding to avoid being hidden by the bottom bar */
    .main .block-container {
        padding-bottom: 150px;
    }

    /* Custom Chat Message Bubbles */
    .stChatMessage { 
        border-radius: 20px; 
        border: none; 
        background-color: #f0f4f9; 
        padding: 15px; 
        margin-bottom: 10px; 
    }

    /* Floating Plus Icon Button Styling */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        border: none !important;
        background-color: #f0f4f9 !important;
        font-size: 24px !important;
        position: fixed;
        bottom: 30px;
        left: 20px;
        z-index: 1000;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Ensuring the Search Input stays at the very bottom */
    .stChatInput {
        position: fixed;
        bottom: 20px;
        z-index: 999;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖")
st.caption("Advanced Chat | Fixed Bottom Search Bar")

# 3. Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. FIXED BOTTOM UI
# Plus Icon (Left Side Floating)
with st.popover("➕"):
    st.markdown("### Attach File")
    uploaded_file = st.file_uploader("Upload Photos or PDFs", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"Selected: {uploaded_file.name}")

# Search Bar (Fixed Bottom by Streamlit Default + CSS Adjustment)
prompt = st.chat_input("Ask Nexus anything...")

# 5. PROCESSING LOGIC
if prompt:
    # Image handling (Base64 for Vision)
    img_b64 = None
    if uploaded_file and uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    # Append User Message
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
                    st.error("Engine busy. Please wait.")
            except:
                st.error("Connection Failed. Make sure Railway is running.")

# Sidebar
with st.sidebar:
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()
        
