import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Custom CSS for Professional UI & Attachment Icons
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #000000; }
    .stChatMessage { border-radius: 15px; border: 1px solid #f0f2f6; margin-bottom: 10px; }
    .stChatInputContainer { padding-bottom: 20px; }
    
    /* Style for Attachment Buttons */
    .attachment-btn {
        display: flex;
        align-items: center;
        padding: 10px;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin-bottom: 5px;
        cursor: pointer;
        border: 1px solid #e9ecef;
    }
    .attachment-btn:hover { background-color: #e2e6ea; }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")
st.caption("Advanced Assistant with File Support | Developed by Sanjeev")

# 3. Sidebar Attachment Menu (As per your Screenshot)
with st.sidebar:
    st.header("📎 Attachments")
    st.write("Upload or take a photo for Nexus to analyze:")
    
    # 📸 Camera Input
    cam_file = st.camera_input("📷 Camera")
    
    # 🖼️ Gallery / Files
    uploaded_file = st.file_uploader("📂 Gallery / Files", type=['png', 'jpg', 'jpeg', 'pdf', 'txt', 'py', 'cpp'])
    
    # ☁️ Drive/Notebooks Placeholder (Simulation)
    st.write("---")
    if st.button("🔗 Google Drive"):
        st.warning("Drive connection coming soon!")
    if st.button("📓 Notebooks"):
        st.info("Notebook integration in progress.")
        
    st.write("---")
    if st.button("🗑️ Clear Chat Memory"):
        st.session_state.messages = []
        st.rerun()

# 4. Initialize Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "file_name" in message:
            st.caption(f"📎 Attached: {message['file_name']}")

# 6. Chat Logic
if prompt := st.chat_input("Kaise ho Sanjeev? Kuch puchiye..."):
    
    # Check if a file was uploaded or photo taken
    file_info = None
    if cam_file:
        file_info = "Photo from Camera"
    elif uploaded_file:
        file_info = uploaded_file.name

    # Add user message to history
    user_msg = {"role": "user", "content": prompt}
    if file_info:
        user_msg["file_name"] = file_info
    
    st.session_state.messages.append(user_msg)
    
    with st.chat_message("user"):
        st.markdown(prompt)
        if file_info:
            st.caption(f"📎 Attached: {file_info}")

    # Railway Backend URL
    backend_url = "https://web-production-68d0e.up.railway.app/ask" 
    
    with st.chat_message("assistant"):
        with st.spinner("Nexus is thinking... 🧠"):
            try:
                # Note: Sending only text for now, Image analysis can be added later in backend
                response = requests.post(backend_url, json={"user_input": prompt}, timeout=60)
                
                if response.status_code == 200:
                    answer = response.json().get("response")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Nexus Engine Error. Check Railway logs.")
            except Exception as e:
                st.error("Connection failed!")

