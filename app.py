import streamlit as st
import requests
import base64
import time

# 1. Page Config
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Super Advanced CSS (Plus Icon on Right Side Overlay)
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    
    /* Chat Area Padding */
    .main .block-container {
        padding-bottom: 120px !important;
    }

    /* Message Styling */
    .stChatMessage { border-radius: 15px; background-color: #f7f7f8; margin-bottom: 10px; }

    /* Gemini Style Search Bar Fix */
    /* Hum chat input ke right side mein jagah bana rahe hain */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 20px;
        z-index: 1000;
        padding-right: 70px !important; 
    }

    /* Plus Icon Fixed at Bottom RIGHT */
    div[data-testid="stPopover"] {
        position: fixed;
        bottom: 30px;
        right: 30px; /* Right side positioning */
        z-index: 1001;
    }

    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        background-color: #f0f4f9 !important;
        border: 1px solid #dfe1e5 !important;
        font-size: 24px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }
    
    /* Copy Button */
    .stButton > button { border-radius: 10px; height: 30px; font-size: 12px; }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")

# 3. Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if st.button(f"📋 Copy", key=f"cp_{i}"):
                st.write(f'<script>navigator.clipboard.writeText("{msg["content"].encode("unicode_escape").decode()}");</script>', unsafe_allow_html=True)

# 4. BOTTOM UI (Plus on Right + Search Bar)

# Plus Icon (Right Side)
with st.popover("➕"):
    st.markdown("### Attach 📂")
    uploaded_file = st.file_uploader("Upload", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")

# Search Bar (Default width minus right padding)
prompt = st.chat_input("Ask Nexus... ✨")

# 5. LOGIC (Direct Solve)
if prompt:
    img_b64 = None
    if uploaded_file and uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    backend_url = "https://web-production-68d0e.up.railway.app/ask"
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        with st.spinner("Solving... 🧠"):
            try:
                # Direct instruction to backend
                res = requests.post(backend_url, json={"user_input": f"Directly solve: {prompt}", "image_b64": img_b64}, timeout=120)
                if res.status_code == 200:
                    answer = res.json().get("response")
                    for word in answer.split():
                        full_res += word + " "
                        time.sleep(0.03)
                        placeholder.markdown(full_res + "▌")
                    placeholder.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                    st.rerun()
                else:
                    st.error("Engine Busy!")
            except Exception as e:
                st.error(f"Error: {e}")
                
