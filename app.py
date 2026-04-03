import streamlit as st
import requests
import base64

st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# Professional UI Styling
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow Mega AI 🤖⚡")
st.caption("Vision + Internet Search + Advanced Coding | By Sanjeev")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for Attachments
with st.sidebar:
    st.header("📎 Nexus Vision")
    cam_photo = st.camera_input("Take a photo of a doubt")
    uploaded_file = st.file_uploader("Upload Image/PDF", type=['png', 'jpg', 'jpeg'])
    
    st.write("---")
    if st.button("🗑️ Clear Memory"):
        st.session_state.messages = []
        st.rerun()

# Display Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Process Input
if prompt := st.chat_input("Ask anything or search the web..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Image handling (Base64 conversion)
    img_b64 = None
    target_file = cam_photo if cam_photo else uploaded_file
    if target_file:
        img_b64 = base64.b64encode(target_file.getvalue()).decode()

    backend_url = "https://web-production-68d0e.up.railway.app/ask" 
    
    with st.chat_message("assistant"):
        with st.spinner("Nexus is analyzing... 🧠🔍"):
            try:
                payload = {"user_input": prompt, "image_b64": img_b64}
                response = requests.post(backend_url, json=payload, timeout=90)
                
                if response.status_code == 200:
                    answer = response.json().get("response")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Engine busy. Try again.")
            except Exception as e:
                st.error(f"Connection Error: {e}")
                
