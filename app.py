import streamlit as st
import requests

# Professional UI Setup
st.set_page_config(page_title="Nexus Flow AI", page_icon="⚡", layout="wide")

# Custom CSS for ChatGPT Look
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_headers=True)

st.title("Nexus Flow AI ⚡")
st.caption("Advanced Assistant for Coding, SAT & BSEB Preparation")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("How can Nexus help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    backend_url = "https://web-production-68d0e.up.railway.app/ask" 
    
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("Nexus is processing..."):
            try:
                response = requests.post(
                    backend_url, 
                    json={"user_input": prompt},
                    timeout=100
                )
                
                if response.status_code == 200:
                    answer = response.json().get("response")
                    response_placeholder.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Nexus Engine is busy. Please try again.")
            except Exception as e:
                st.error(f"Connection Error: {e}")

# Sidebar for Stats & Tools
with st.sidebar:
    st.title("🛡️ Nexus Control")
    st.write("---")
    if st.button("🗑️ Clear All Memory"):
        st.session_state.messages = []
        st.success("Memory Wiped!")
        st.rerun()
    
    st.write("---")
    st.info("**Active Modes:**\n- 🐍 Python/C++ Expert\n- 🎓 SAT/BSEB Tutor\n- 🎬 Video Editing Tips")
    
