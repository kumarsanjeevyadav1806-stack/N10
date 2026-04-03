import streamlit as st
import requests
import base64

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Gemini Style CSS (Plus icon side-by-side with Search Bar)
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: white; color: black; }
    
    /* Custom Chat Message Bubbles */
    .stChatMessage { 
        border-radius: 20px; 
        border: none; 
        background-color: #f0f4f9; 
        padding: 15px; 
        margin-bottom: 10px; 
    }

    /* Styling for the Plus Icon Button inside Popover */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        border: none !important;
        background-color: #f0f4f9 !important;
        font-size: 20px !important;
        margin-top: 10px;
    }
    
    /* Layout fix for Side-by-Side */
    .chat-container {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖")
st.caption("Advanced Chat with Document & Photo Support")

# 3. Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. GEMINI STYLE INPUT BAR (Plus Icon on the side)
# Hum columns ka use kar rahe hain taaki Plus aur Input side-by-side dikhen
col_icon, col_input = st.columns([0.15, 0.85])

with col_icon:
    # Camera remove kar diya gaya hai, sirf Upload options hain
    with st.popover("➕"):
        st.markdown("### Attach")
        uploaded_file = st.file_uploader("Photos / Documents", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")
        if uploaded_file:
            st.success(f"Selected: {uploaded_file.name}")

with col_input:
    prompt = st.chat_input("Ask Nexus...")

# 5. PROCESSING LOGIC
if prompt:
    # File handling (Base64 for Images)
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
                    st.error("Engine busy.")
            except:
                st.error("Connection Failed. Check Railway backend.")

# Sidebar for Reset
with st.sidebar:
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()
        
