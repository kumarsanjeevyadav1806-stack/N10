import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Advanced CSS to Pin Everything to Bottom
st.markdown("""
    <style>
    /* White Theme */
    .stApp { background-color: white; color: black; }
    
    /* Content Padding so messages don't hide behind the bar */
    .main .block-container {
        padding-bottom: 120px !important;
        max-width: 800px;
    }

    /* ChatGPT Style Chat Bubbles */
    .stChatMessage { 
        border-radius: 18px; 
        background-color: #f7f7f8; 
        margin-bottom: 12px;
    }

    /* THE MAGIC: Pinning the column container to the bottom */
    [data-testid="stVerticalBlock"] > div:last-child {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 20px 10% 40px 10%;
        z-index: 1000;
        border-top: 1px solid #f0f2f6;
    }
    
    /* Plus Button Styling */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        background-color: #f0f4f9 !important;
        border: none !important;
        font-size: 20px !important;
    }

    /* Hide Streamlit Footer */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")

# 3. Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if st.button(f"📋 Copy", key=f"cp_{i}"):
                st.write(f'<script>navigator.clipboard.writeText("{msg["content"].encode("unicode_escape").decode()}");</script>', unsafe_allow_html=True)

# 4. FIXED BOTTOM BAR (Plus + Search Side-by-Side)
# Ye container hamesha screen ke niche hi rahega
with st.container():
    col_plus, col_search = st.columns([0.15, 0.85])
    
    with col_plus:
        with st.popover("➕"):
            st.markdown("### Attach 📂")
            uploaded_file = st.file_uploader("Upload", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")
    
    with col_search:
        # text_input Enter dabane par trigger hota hai
        prompt = st.text_input("", placeholder="Ask Nexus anything... ✨", key="nexus_input", label_visibility="collapsed")

# 5. LOGIC
if prompt:
    img_b64 = None
    if uploaded_file and uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Railway Backend URL
    backend_url = "https://web-production-68d0e.up.railway.app/ask"
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        with st.spinner("Analyzing... 🧠"):
            try:
                # Instruction to backend to be direct
                payload = {"user_input": f"Directly solve: {prompt}", "image_b64": img_b64}
                res = requests.post(backend_url, json=payload, timeout=120)
                
                if res.status_code == 200:
                    answer = res.json().get("response")
                    # Typing Effect ✍️
                    for word in answer.split():
                        full_res += word + " "
                        time.sleep(0.04)
                        placeholder.markdown(full_res + "▌")
                    placeholder.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                    st.rerun() # Refresh to clear input box
                else:
                    st.error("Engine Busy! 🛑")
            except Exception as e:
                st.error(f"Error: {e} ⚠️")

# Sidebar
with st.sidebar:
    st.title("🕒 Activity")
    if st.button("🗑️ Reset All Chats"):
        st.session_state.messages = []
        st.rerun()
        
