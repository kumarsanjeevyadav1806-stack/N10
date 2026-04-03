import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Advanced CSS to Hide Default Input and Style Custom Bar
st.markdown("""
    <style>
    /* Global White Theme */
    .stApp { background-color: white; color: black; }
    
    /* Padding for chat history */
    .main .block-container {
        padding-bottom: 150px !important;
        max-width: 800px;
    }

    /* ChatGPT Style Chat Bubbles */
    .stChatMessage { 
        border-radius: 18px; 
        background-color: #f7f7f8; 
        margin-bottom: 12px;
    }

    /* HIDING ORIGINAL CHAT INPUT - VERY IMPORTANT */
    .stChatInput { display: none !important; }

    /* OUR CUSTOM GEMINI BAR (Fixed at Bottom) */
    .gemini-footer {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 750px;
        background: #f0f4f9;
        border-radius: 35px;
        padding: 5px 15px;
        display: flex;
        align-items: center;
        z-index: 9999;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
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

# 4. GEMINI STYLE BOTTOM UI (Fixed & Aligned)
# Yahan hum columns ka use kar rahe hain jo Streamlit ke "Bottom" block mein default align honge
with st.container():
    # Humne layout ko columns mein dala hai jo screen ke bottom par chipka rahega
    col_plus, col_input = st.columns([0.15, 0.85])
    
    with col_plus:
        with st.popover("➕"):
            st.markdown("### Attach 📂")
            uploaded_file = st.file_uploader("Upload", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")
    
    with col_input:
        # Gemini ki tarah "Enter" dabane par message jayega
        prompt = st.text_input("", placeholder="Ask Nexus anything... ✨", key="nexus_input", label_visibility="collapsed")

# 5. LOGIC (Direct Solve)
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
                # Direct Solve instruction
                payload = {"user_input": f"Solve directly: {prompt}", "image_b64": img_b64}
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
                    st.rerun() # To clear text input
                else:
                    st.error("Engine Busy! 🛑")
            except Exception as e:
                st.error(f"Error: {e} ⚠️")

# Sidebar
with st.sidebar:
    st.title("🕒 Activity")
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()
        
