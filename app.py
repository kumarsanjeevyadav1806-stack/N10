import streamlit as st
import requests
import base64

st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# Custom CSS for clean UI
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { border-radius: 15px; }
    img { border-radius: 10px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖✨")
st.caption("Now with Direct Image Generation | Developed by Sanjeev")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])

# User Input
if prompt := st.chat_input("Ask me to 'Draw a futuristic Bihar'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    backend_url = "https://web-production-68d0e.up.railway.app/ask" 
    
    with st.chat_message("assistant"):
        with st.spinner("Nexus is processing... ⚡"):
            try:
                response = requests.post(backend_url, json={"user_input": prompt}, timeout=120)
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("response")
                    img_data = data.get("image") # Base64 image string

                    st.markdown(answer)
                    
                    msg_to_store = {"role": "assistant", "content": answer}
                    
                    if img_data:
                        # Convert Base64 back to bytes for display
                        decoded_img = base64.b64decode(img_data)
                        st.image(decoded_img)
                        msg_to_store["image"] = decoded_img
                    
                    st.session_state.messages.append(msg_to_store)
                else:
                    st.error("Server is busy. Try again!")
            except Exception as e:
                st.error(f"Connection Error: {e}")

with st.sidebar:
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
        
