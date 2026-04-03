import streamlit as st
import requests

# Page UI Settings
st.set_page_config(page_title="Nexus Flow AI", page_icon="⚡", layout="centered")

st.title("Nexus Flow AI ⚡")
st.markdown("---")

# Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Logic
if prompt := st.chat_input("Message Nexus Flow..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # LIVE RAILWAY URL (Apna Railway URL yahan confirm karein)
    backend_url = "https://n10-production.up.railway.app/ask" 
    
    with st.spinner("Nexus is thinking..."):
        try:
            response = requests.post(
                backend_url, 
                json={"user_input": prompt},
                timeout=60
            )
            
            if response.status_code == 200:
                answer = response.json().get("response")
                with st.chat_message("assistant"):
                    st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                error_detail = response.json().get("detail", "Backend Error")
                st.error(f"Nexus Error: {error_detail}")
                
        except Exception as e:
            st.error(f"Connection Failed: {e}")

# Sidebar for Controls
with st.sidebar:
    st.header("Settings")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.write("Target: Railway Cloud")
  
