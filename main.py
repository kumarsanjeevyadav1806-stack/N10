import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Ultra-Advanced CSS (Bottom Sheet Animation)
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    
    /* Content Padding */
    .main .block-container { padding-bottom: 150px !important; }

    /* Hide default Streamlit elements */
    footer {visibility: hidden;}

    /* Bottom Sheet Styling like your screenshot */
    .menu-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-radius: 30px 30px 0 0;
        padding: 20px;
        z-index: 10001;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.1);
        display: none; /* Initially hidden */
    }

    /* Handle (The grey line at top of menu) */
    .handle {
        width: 40px;
        height: 5px;
        background: #ccc;
        border-radius: 10px;
        margin: 0 auto 20px auto;
    }

    /* Menu Item Design */
    .menu-item {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px;
        font-size: 18px;
        color: #333;
        border-radius: 10px;
    }
    
    /* Plus Button Style */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        background-color: #f0f4f9 !important;
        border: none !important;
        font-size: 24px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
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

# 4. THE BOTTOM SHEET MENU (List Style like Screenshot)
with st.container():
    col_plus, col_input = st.columns([0.15, 0.85])
    
    with col_plus:
        # Hum popover ke andar list style layout bana rahe hain
        with st.popover("➕"):
            st.markdown('<div class="handle"></div>', unsafe_allow_html=True)
            
            # Action selection
            choice = st.radio(
                "Select Action",
                ["📷 Camera", "🖼️ Gallery", "📎 Files", "☁️ Drive", "📓 Notebooks"],
                label_visibility="collapsed"
            )
            
            if choice == "📷 Camera":
                uploaded_file = st.camera_input("Take Photo")
            elif choice == "🖼️ Gallery" or choice == "📎 Files":
                uploaded_file = st.file_uploader("Choose File", type=['png', 'jpg', 'jpeg', 'pdf'])
            else:
                st.info(f"{choice} feature coming soon!")
                uploaded_file = None

    with col_input:
        prompt = st.chat_input("Ask Gemini...")

# 5. LOGIC (Model 90B Fix Included)
if prompt:
    img_b64 = None
    if uploaded_file and hasattr(uploaded_file, 'getvalue'):
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        with st.spinner("Analyzing..."):
            try:
                backend_url = "https://web-production-68d0e.up.railway.app/ask"
                res = requests.post(backend_url, json={"user_input": prompt, "image_b64": img_b64}, timeout=120)
                if res.status_code == 200:
                    answer = res.json().get("response")
                    for word in answer.split():
                        full_res += word + " "
                        time.sleep(0.03)
                        placeholder.markdown(full_res + "▌")
                    placeholder.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
                
