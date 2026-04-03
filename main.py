import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Gemini Style CSS (The Ultimate Look)
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .main .block-container { padding-bottom: 150px !important; }

    /* Bottom Bar Styling */
    [data-testid="stBottomBlockContainer"] {
        background-color: white !important;
        border-top: 1px solid #f0f2f6;
        padding: 10px 5% 30px 5% !important;
    }

    /* Force Side-by-Side */
    [data-testid="column"] {
        width: fit-content !important;
        flex: unset !important;
        min-width: unset !important;
    }

    /* Gemini Plus Icon Overlay Style */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 52px !important;
        height: 52px !important;
        background-color: #f0f4f9 !important;
        border: none !important;
        font-size: 26px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Camera Input Styling to look like a viewfinder */
    [data-testid="stCameraInput"] {
        border-radius: 20px;
        overflow: hidden;
        border: 2px solid #4285f4;
    }

    footer {visibility: hidden;}
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

# 4. ADVANCED BOTTOM UI (Real-App Style)
with st.container():
    col_plus, col_input = st.columns([0.18, 0.82])
    
    with col_plus:
        with st.popover("➕"):
            st.markdown("### Choose Input 📁")
            # Gemini jaisa menu
            choice = st.radio("Select", ["📷 Use Camera", "🖼️ Gallery/Files"], label_visibility="collapsed")
            
            uploaded_file = None
            if choice == "📷 Use Camera":
                # Isse mobile par Rear Camera open hone ki probability badh jati hai
                uploaded_file = st.camera_input("Scan your Question", help="Point at the text or problem")
            else:
                uploaded_file = st.file_uploader("Upload from device", type=['png', 'jpg', 'jpeg', 'pdf'])
            
            if uploaded_file:
                st.success(f"Captured: {uploaded_file.name} ✅")

    with col_input:
        prompt = st.chat_input("Ask Gemini or type 'Solve it'...")

# 5. LOGIC (Processing with Vision)
if prompt:
    img_b64 = None
    # Check if a file was captured/uploaded
    if uploaded_file:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        with st.spinner("Processing with Vision... 🧠"):
            try:
                backend_url = "https://web-production-68d0e.up.railway.app/ask"
                # Always send image if present
                payload = {"user_input": prompt, "image_b64": img_b64}
                res = requests.post(backend_url, json=payload, timeout=120)
                
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
                    st.error("Engine Busy! Please try again.")
            except Exception as e:
                st.error(f"Error: {e}")

# Sidebar
with st.sidebar:
    if st.button("🗑️ Reset All"):
        st.session_state.messages = []
        st.rerun()
        
