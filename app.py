import streamlit as st
import requests
import base64
import time

# 1. Page Configuration (Mobile-first layout)
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Ultra-Advanced CSS (Perfect Gemini Look & ChatGPT Response Style)
st.markdown("""
    <style>
    /* White Background & Clear Text */
    .stApp { background-color: white; color: black; }
    
    /* Ensuring Main content scrollable above the bottom bar */
    .main .block-container {
        padding-bottom: 180px !important;
        max-width: 800px;
    }

    /* ChatGPT Style Chat Bubbles */
    .stChatMessage { 
        border-radius: 20px; 
        border: none; 
        background-color: #f7f7f8; 
        padding: 20px; 
        margin-bottom: 15px;
        line-height: 1.6;
    }
    
    /* Plus Icon Container Fixed at Bottom */
    div[data-testid="stPopover"] {
        position: fixed;
        bottom: 40px;
        left: 20px;
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
        transition: 0.3s ease;
    }
    
    div[data-testid="stPopover"] > button:hover {
        background-color: #d3e3fd !important;
        transform: scale(1.05);
    }

    /* Fixed Bottom Search Bar Adjustment */
    /* Streamlit input is fixed via CSS and moved right for plus icon */
    .stChatInput {
        position: fixed;
        bottom: 25px;
        padding-left: 75px !important; /* Gemini space for plus icon */
        z-index: 1000;
    }
    
    /* Copy Button Styling */
    .copy-btn { margin-top: 10px; cursor: pointer; color: blue; font-size: 14px; }
    
    /* Hide default footer */
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")

# 3. Memory & Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History with Copy Button
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            # Add Direct Copy Feature
            if st.button(f"📋 Copy", key=f"copy_{i}"):
                st.write(f'<script>navigator.clipboard.writeText("{msg["content"].encode("unicode_escape").decode()}");</script>', unsafe_allow_html=True)

# 4. BOTTOM UI (Plus Icon Menu & Search Input)

# Plus Icon (Fixed Left Side)
with st.popover("➕"):
    st.markdown("### Attach Files 📂")
    uploaded_file = st.file_uploader("Upload Image or Document", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' is attached! ✅")

# Search Input (Niche Fixed)
prompt = st.chat_input("Ask Gemini...")

# 5. LOGIC (Advanced Code Interpreter + Direct Solve)
if prompt:
    # 1. Image handling
    img_b64 = None
    if uploaded_file and uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    # 2. Append User Message
    st.session_state.messages.append({"role": "user", "content": f"👤 {prompt}"})
    with st.chat_message("user"):
        st.markdown(f"👤 {prompt}")

    # 3. Call Backend
    backend_url = "https://web-production-68d0e.up.railway.app/ask"
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Analyzing... 🧠"):
            try:
                # Direct Solve Instructions added to system context in payload
                enhanced_prompt = f"System: Provide optimized code or fix errors. Do not explain features. Just solve it directly. Input: {prompt}"
                payload = {"user_input": enhanced_prompt, "image_b64": img_b64}
                
                response = requests.post(backend_url, json=payload, timeout=90)
                
                if response.status_code == 200:
                    answer = response.json().get("response")
                    
                    # ChatGPT "Typing Effect" simulation ✍️
                    for word in answer.split():
                        full_response += word + " "
                        time.sleep(0.04)
                        message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    st.rerun() # Refresh for Copy Button to show up
                else:
                    st.error("Engine Timeout! Please try again. 🛑")
            except:
                st.error("Connection Failed. Make sure Railway is running.")

# Sidebar
with st.sidebar:
    st.title("⚙️ Nexus Flow Memory")
    if st.button("🗑️ Reset All Chats"):
        st.session_state.messages = []
        st.rerun()
    st.info("Nexus is now in **Advanced Mode**. Memory, Vision, and Internet are enabled.")
    
