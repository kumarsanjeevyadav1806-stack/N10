import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Ultra-Fix CSS (Gemini Bottom Sheet Layout)
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    
    /* Content Padding */
    .main .block-container { padding-bottom: 150px !important; }

    /* Gemini Style Bottom Sheet Simulation */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        background-color: #f0f4f9 !important;
        border: none !important;
        font-size: 22px !important;
    }

    /* Styling for the List inside Popover */
    .menu-header {
        width: 40px;
        height: 4px;
        background: #e0e0e0;
        border-radius: 10px;
        margin: 0 auto 15px auto;
    }

    /* Hide default Streamlit footer */
    footer {visibility: hidden;}
    [data-testid="stBottomBlockContainer"] {
        background-color: white !important;
        border-top: 1px solid #f0f2f6;
        padding: 10px 5% 30px 5% !important;
    }
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

# 4. THE BOTTOM SHEET (List Style Like Gemini)
with st.container():
    col1, col2 = st.columns([0.15, 0.85])
    
    with col1:
        # Gemini Style: Popover used as a Slide-up list
        with st.popover("➕"):
            st.markdown('<div class="menu-header"></div>', unsafe_allow_html=True)
            
            # List options with Icons
            choice = st.radio(
                "Choose Action",
                ["📷 Camera", "🖼️ Gallery", "📎 Files", "📁 Drive", "📓 Notebooks"],
                label_visibility="collapsed"
            )
            
            # File handling logic based on choice
            if "Camera" in choice:
                uploaded_file = st.camera_input("Take Photo", label_visibility="collapsed")
            else:
                uploaded_file = st.file_uploader("Select File", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")

    with col2:
        prompt = st.chat_input("Ask Gemini...")

# 5. BRAIN LOGIC (90B Model + Direct Solve)
if prompt:
    img_b64 = None
    if uploaded_file and hasattr(uploaded_file, 'getvalue'):
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    backend_url = "https://web-production-68d0e.up.railway.app/ask"
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        with st.spinner("Analyzing... 🧠"):
            try:
                # Instruction to backend
                payload = {"user_input": f"Directly solve: {prompt}", "image_b64": img_b64}
                res = requests.post(backend_url,
                
