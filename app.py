import streamlit as st
import requests
import time

st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #f0f2f6; margin-bottom: 10px; }
    img { border-radius: 12px; margin-top: 10px; width: 100%; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")
st.caption("Advanced AI Assistant | Developed by Sanjeev")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image_url" in msg:
            st.image(msg["image_url"])

# Chat Input
if prompt := st.chat_input("Ask Nexus to draw something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    backend_url = "https://web-production-68d0e.up.railway.app/ask" 
    
    with st.chat_message("assistant"):
        with st.spinner("Nexus is generating... 🎨"):
            try:
                response = requests.post(backend_url, json={"user_input": prompt}, timeout=60)
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("response")
                    img_url = data.get("image_url")

                    st.markdown(answer)
                    
                    if img_url:
                        # 🛠️ FIX: Give it a tiny moment to stabilize
                        time.sleep(1) 
                        st.image(img_url)
                        st.session_state.messages.append({"role": "assistant", "content": answer, "image_url": img_url})
                    else:
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Server Busy!")
            except Exception as e:
                st.error(f"Connection Failed: {e}")

with st.sidebar:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
        
