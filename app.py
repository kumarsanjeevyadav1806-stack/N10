import streamlit as st
import requests
import base64

# UI Setup
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# Custom CSS for ChatGPT Look + White Theme
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .stChatMessage { border-radius: 15px; border: 1px solid #f0f2f6; margin-bottom: 10px; }
    img { border-radius: 12px; margin-top: 10px; width: 100%; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")
st.caption("Now with FAST Direct Image Generation | Developed by Sanjeev")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg:
            st.image(msg["image"])

# --- CHAT INPUT & PROCESSOR ---
if prompt := st.chat_input("Ask Nexus to draw something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # UPDATED BACKEND URL (From your Railway screenshot)
    backend_url = "https://web-production-68d0e.up.railway.app/ask" 
    
    with st.chat_message("assistant"):
        with st.spinner("Nexus is thinking... 🧠🎨"):
            try:
                # Call backend and get response with Base64 image string
                response = requests.post(backend_url, json={"user_input": prompt}, timeout=150)
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("response")
                    img_b64 = data.get("image") # Base64 image string

                    st.markdown(answer)
                    new_msg = {"role": "assistant", "content": answer}

                    if img_b64:
                        # Convert Base64 back to bytes for display
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
    st.title("🛡️ Nexus Control")
    st.write("---")
    if st.button("🗑️ Clear All Memory"):
        st.session_state.messages = []
        st.rerun()
    
    st.write("---")
    st.info("**Active Modes:**\n- 🎨 Direct Image Gen\n- 🐍 Python/C++ Expert\n- 🎓 SAT/BSEB Tutor")
    
