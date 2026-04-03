import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Custom CSS (Clean White Look)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #f0f2f6; margin-bottom: 10px; }
    /* Image styling to ensure it looks good */
    img { border-radius: 12px; margin-top: 10px; width: 100%; border: 2px solid #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")
st.caption("Fast Direct Image Generation | Developed by Sanjeev")

# 3. Chat Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display Chat History (Including Images)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image_url" in msg:
            st.image(msg["image_url"], use_column_width=True)

# 5. User Input Section
if prompt := st.chat_input("Ask Nexus to draw something..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ⚠️ Check your Railway Backend URL here
    backend_url = "https://web-production-68d0e.up.railway.app/ask" 
    
    with st.chat_message("assistant"):
        with st.spinner("Nexus is processing... ⚡"):
            try:
                # Backend se response mangna
                response = requests.post(backend_url, json={"user_input": prompt}, timeout=60)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("response")
                    img_url = data.get("image_url") # Direct Link from Pollinations AI

                    # Text answer dikhana
                    st.markdown(answer)
                    
                    # Message object create karna
                    new_msg = {"role": "assistant", "content": answer}

                    # AGAR IMAGE URL HAI TOH USKO DIKHANA
                    if img_url:
                        st.image(img_url, use_column_width=True)
                        new_msg["image_url"] = img_url # Save for history
                    
                    # History mein save karna
                    st.session_state.messages.append(new_msg)
                else:
                    st.error(f"Backend Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")

# 6. Sidebar Controls
with st.sidebar:
    st.title("🛡️ Nexus Control")
    if st.button("🗑️ Clear Chat Memory"):
        st.session_state.messages = []
        st.rerun()
        
