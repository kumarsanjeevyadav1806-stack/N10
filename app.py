import streamlit as st
import requests
import base64

st.set_page_config(page_title="Nexus Flow AI", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #f0f2f6; }
    img { border-radius: 12px; margin-top: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI ⚡")
st.caption("Direct Chat & Image Gen | Created by Sanjeev")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg:
            st.image(msg["image"])

if prompt := st.chat_input("Ask me to draw anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    backend_url = "https://web-production-68d0e.up.railway.app/ask" 
    
    with st.chat_message("assistant"):
        with st.spinner("Nexus is processing..."):
            try:
                response = requests.post(backend_url, json={"user_input": prompt}, timeout=120)
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("response")
                    img_b64 = data.get("image")

                    st.markdown(answer)
                    new_msg = {"role": "assistant", "content": answer}

                    if img_b64:
                        raw_img = base64.b64decode(img_b64)
                        st.image(raw_img)
                        new_msg["image"] = raw_img
                    
                    st.session_state.messages.append(new_msg)
                else:
                    st.error("Server Busy!")
            except Exception as e:
                st.error(f"Error: {e}")
                
