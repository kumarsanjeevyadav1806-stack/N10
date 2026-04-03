import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Ultra-Advanced CSS (Gemini Bar + ChatGPT Copy UI)
st.markdown("""
    <style>
    /* White Theme & Global Font */
    .stApp { background-color: white; color: black; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Content Padding for Bottom Bar */
    .main .block-container {
        padding-bottom: 160px !important;
        max-width: 850px;
    }

    /* ChatGPT Style Chat Bubbles */
    .stChatMessage { 
        border-radius: 20px; 
        background-color: #f7f7f8; 
        margin-bottom: 15px;
        border: 1px solid #f0f0f0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }

    /* Fixed Bottom Bar Container */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 25px;
        z-index: 1000;
        padding-left: 75px !important; 
    }

    /* Floating Plus Icon Style */
    div[data-testid="stPopover"] {
        position: fixed;
        bottom: 38px;
        left: 25px;
        z-index: 1001;
    }

    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        background-color: #f0f4f9 !important;
        border: none !important;
        font-size: 24px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    
    div[data-testid="stPopover"] > button:hover {
        background-color: #d3e3fd !important;
        transform: scale(1.05);
    }

    /* Code Block Styling */
    code {
        background-color: #1e1e1e !important;
        color: #d4d4d4 !important;
        padding: 10px !important;
        border-radius: 8px !important;
        display: block;
        overflow-x: auto;
    }
    
    /* Hide Streamlit Footer */
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")
st.caption("Pro Developer Mode | Memory | Internet | Vision")

# 3. Session State for History & Copy
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages with Copy Option
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Direct Copy Button for each message
        if msg["role"] == "assistant":
            st.button(f"📋 Copy Response", key=f"copy_{i}", on_click=lambda text=msg["content"]: st.write(f'<script>navigator.clipboard.writeText("{text.encode("unicode_escape").decode()}");</script>', unsafe_allow_html=True))

# 4. BOTTOM UI (Plus + Search)
with st.popover("➕"):
    st.markdown("### Attachments 📂")
    uploaded_file = st.file_uploader("Photo or PDF", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' is ready! ✅")

prompt = st.chat_input("Ask Nexus to code, fix or search... ✨")

# 5. LOGIC (Advanced Code Expert)
if prompt:
    img_b64 = None
    if uploaded_file and uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    # User message
    st.session_state.messages.append({"role": "user", "content": f"👤 {prompt}"})
    with st.chat_message("user"):
        st.markdown(f"👤 {prompt}")

    backend_url = "https://web-production-68d0e.up.railway.app/ask"
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        with st.spinner("Analyzing with God++ Engine... 🧠"):
            try:
                # Prompt Engineering for Code Expert
                enhanced_prompt = f"Expert Mode: provide optimized code and fix errors. Input: {prompt}"
                payload = {"user_input": enhanced_prompt, "image_b64": img_b64}
                
                res = requests.post(backend_url, json=payload, timeout=120)
                
                if res.status_code == 200:
                    answer = res.json().get("response")
                    
                    # ChatGPT Typing Effect ✍️
                    for word in answer.split():
                        full_res += word + " "
                        time.sleep(0.03)
                        placeholder.markdown(full_res + "▌")
                    placeholder.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                    st.rerun() # Refresh to show copy button
                else:
                    st.error("Engine Timeout! Please try again. 🛑")
            except Exception as e:
                st.error(f"Connection Error: {e} ⚠️")

# Sidebar
with st.sidebar:
    st.title("🕒 Recent Activity")
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.write("🚀 **Features:**\n- Permanent Memory\n- Code Fixer\n- Image Vision\n- Internet Search")
    
