import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Advanced CSS (Fixed Bottom Bar & ChatGPT Styling)
st.markdown("""
    <style>
    /* Global Background */
    .stApp { background-color: white; color: black; }
    
    /* Main Content Padding to avoid overlap with bottom bar */
    .main .block-container {
        padding-bottom: 120px;
        max-width: 800px;
    }

    /* ChatGPT Style Chat Bubbles */
    .stChatMessage { 
        border-radius: 15px; 
        border: none; 
        background-color: #f7f7f8; 
        padding: 20px; 
        margin-bottom: 15px;
        line-height: 1.6;
    }
    
    /* Plus Icon Container Fixed at Bottom */
    div[data-testid="stPopover"] {
        position: fixed;
        bottom: 32px;
        left: 20px;
        z-index: 1001;
    }

    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 48px !important;
        height: 48px !important;
        background-color: #f0f4f9 !important;
        border: 1px solid #dfe1e5 !important;
        font-size: 22px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* Fixed Bottom Search Bar Adjustment */
    .stChatInput {
        position: fixed;
        bottom: 20px;
        padding-left: 70px !important; /* Space for Plus icon */
        z-index: 1000;
    }

    /* Code Block Styling like ChatGPT */
    code {
        background-color: #2d2d2d !important;
        color: #f8f8f2 !important;
        padding: 2px 5px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")
st.caption("Advanced Brain: Llama 3.3 70B | Developed by Sanjeev")

# 3. Memory & Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. BOTTOM UI (Plus Icon & Search Bar)

# Plus Icon (Left Side)
with st.popover("➕"):
    st.markdown("### Attachments")
    uploaded_file = st.file_uploader("Upload Image or PDF", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"Attached: {uploaded_file.name}")

# Search Input (Niche Fixed)
prompt = st.chat_input("Ask Nexus anything...")

# 5. LOGIC & CHATGPT FEATURES
if prompt:
    # 1. Image handling
    img_b64 = None
    if uploaded_file and uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    # 2. Append User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Call Backend
    backend_url = "https://web-production-68d0e.up.railway.app/ask"
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty() # For Typing Effect
        full_response = ""
        
        with st.spinner("Thinking..."):
            try:
                payload = {"user_input": prompt, "image_b64": img_b64}
                response = requests.post(backend_url, json=payload, timeout=90)
                
                if response.status_code == 200:
                    answer = response.json().get("response")
                    
                    # ChatGPT "Typing Effect" simulation
                    for chunk in answer.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error("Engine Error! Try again.")
            except:
                st.error("Connection Failed. Backend is sleeping?")

# Sidebar
with st.sidebar:
    st.header("⚙️ Nexus Settings")
    if st.button("🗑️ Clear All Chats"):
        st.session_state.messages = []
        st.rerun()
    st.info("Nexus is now in **Advanced Mode**. It can analyze images and remember context.")
    
