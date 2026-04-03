import streamlit as st
import requests
import base64

st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# --- GEMINI STYLE CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: white; }
    
    /* Search Bar Styling */
    .stChatInputContainer {
        padding-bottom: 20px;
        position: relative;
    }
    
    /* Attachment Icons like Gemini */
    .gemini-icons {
        display: flex;
        gap: 15px;
        padding: 10px;
        background: #f8f9fa;
        border-radius: 20px;
        margin-bottom: -10px;
        width: fit-content;
        border: 1px solid #e5e7eb;
    }
    
    .stChatMessage { border-radius: 15px; border: 1px solid #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")
st.caption("Now with Memory & Gemini-style Attachments")

# Memory State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- GEMINI STYLE ATTACHMENT BOX ---
st.markdown('<div class="gemini-icons">📸 🖼️ 📂 🔗</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
with col2:
    cam_file = st.camera_input("Camera", label_visibility="collapsed")

# Chat Input
if prompt := st.chat_input("Ask Nexus anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Convert Image to Base64
    img_b64 = None
    target_file = cam_file if cam_file else uploaded_file
    if target_file:
        img_b64 = base64.b64encode(target_file.getvalue()).decode()

    backend_url = "https://web-production-68d0e.up.railway.app/ask" 
    
    with st.chat_message("assistant"):
        with st.spinner("Nexus is thinking... 🧠"):
            try:
                payload = {"user_input": prompt, "image_b64": img_b64}
                response = requests.post(backend_url, json=payload, timeout=90)
                
                if response.status_code == 200:
                    answer = response.json().get("response")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Server Busy!")
            except Exception as e:
                st.error(f"Error: {e}")

# Sidebar
with st.sidebar:
    if st.button("🗑️ Reset All Memory"):
        st.session_state.messages = []
        st.rerun()
        
