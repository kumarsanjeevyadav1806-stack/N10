import streamlit as st
import requests

st.set_page_config(page_title="Nexus Flow AI", page_icon="⚡")
st.title("Nexus Flow AI ⚡")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message Nexus Flow..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # FIXED URL: Added https:// at the start
    backend_url = "https://web-production-68d0e.up.railway.app/ask" 
    
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
                st.error(f"Backend Error: {response.text}")
                
        except Exception as e:
            st.error(f"Connection Failed: {e}")

with st.sidebar:
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
        
