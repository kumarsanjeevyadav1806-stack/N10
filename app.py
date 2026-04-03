import streamlit as st
import requests
import base64

# Page UI Setup
st.set_page_config(page_title="Nexus Flow AI", page_icon="⚡", layout="centered")

# White Theme + ChatGPT Styling
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .stChatMessage { border-radius: 15px; border: 1px solid #f0f2f6; margin-bottom: 10px; }
    img { border-radius: 12px; margin-top: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")
st.caption("Expert in Coding, SAT, BSEB & Direct Image Generation")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages & Images in Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg:
            st.image(msg["image"])

# User Interaction
if prompt := st.chat_input("How can Nexus help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Railway Backend URL
    backend_url = "https://web-production-68d0e.up.railway.app/ask" 
    
    with st.chat_message("assistant"):
        with st.spinner("Nexus is thinking... 🧠"):
            try:
                response = requests.post(backend_url, json={"user_input": prompt}, timeout=120)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("response")
                    img_b64 = data.get("image")

                    st.markdown(answer)
                    new_msg = {"role": "assistant", "content": answer}

                    if img_b64:
                        raw_image = base64.b64decode(img_b64)
                        st.image(raw_image)
                        new_msg["image"] = raw_image
                    
                    st.session_state.messages.append(new_msg)
                else:
                    st.error("Server is busy. Please try again.")
            except Exception as e:
                st.error(f"Connection Failed: {e}")

# Sidebar
with st.sidebar:
    st.title("🛡️ Nexus Settings")
    if st.button("🗑️ Clear Chat Memory"):
        st.session_state.messages = []
        st.rerun()
    st.info("**Active Features:**\n- 🎨 Direct Image Gen\n- 🐍 Coding Expert\n- 🎓 SAT/BSEB Prep")
    
