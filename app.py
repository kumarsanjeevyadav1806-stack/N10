import streamlit as st
import requests

# UI Setup
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #f0f2f6; }
    img { border-radius: 12px; margin-top: 10px; width: 100%; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")
st.caption("Fast Direct Image Generation | Developed by Sanjeev")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image_url" in msg:
            st.image(msg["image_url"])

# Input Section
if prompt := st.chat_input("Ask Nexus to draw something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ⚠️ Verify this URL from your Railway Dashboard
    backend_url = "https://web-production-68d0e.up.railway.app/ask" 
    
    with st.chat_message("assistant"):
        with st.spinner("Nexus is processing... ⚡"):
            try:
                response = requests.post(backend_url, json={"user_input": prompt}, timeout=60)
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("response")
                    img_url = data.get("image_url") # Direct link from backend

                    st.markdown(answer)
                    new_msg = {"role": "assistant", "content": answer}

                    if img_url:
                        # Streamlit will download and show the image directly from the URL
                        st.image(img_url)
                        new_msg["image_url"] = img_url
                    
                    st.session_state.messages.append(new_msg)
                else:
                    st.error(f"Backend Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")

with st.sidebar:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
        
