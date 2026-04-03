import streamlit as st
import requests

st.set_page_config(page_title="Nexus Flow AI", page_icon="⚡", layout="centered")

st.title("Nexus Flow AI ⚡")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message Nexus Flow..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # FINAL URL - Ensure it ends with /ask
    backend_url = "web-production-68d0e.up.railway.app/ask" 
    
    with st.spinner("Nexus is thinking..."):
        try:
            response = requests.post(
                backend_url, 
                json={"user_input": prompt},
                timeout=90  # 90 seconds timeout
            )
            
            if response.status_code == 200:
                answer = response.json().get("response")
                with st.chat_message("assistant"):
                    st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                # Backend se aane wala specific error message dikhayega
                try:
                    error_msg = response.json().get("detail", "Server Crash (502)")
                except:
                    error_msg = "Railway is not responding. Check Deploy Logs."
                st.error(f"Backend Error: {error_msg}")
                
        except Exception as e:
            st.error(f"Critical Connection Error: {e}")

with st.sidebar:
    st.header("Nexus Control")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
