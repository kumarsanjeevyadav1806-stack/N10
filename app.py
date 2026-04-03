import streamlit as st
import requests

st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# Gemini UI Styling
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #f0f2f6; }
    .sidebar-history { font-size: 14px; color: #555; padding: 5px; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")
st.caption("Permanent Memory: Chat history saved for months and years.")

backend_url = "https://web-production-68d0e.up.railway.app"

# --- LOAD LONG TERM HISTORY ---
if "messages" not in st.session_state:
    try:
        # Fetching history from Backend SQLite
        res = requests.get(f"{backend_url}/history")
        if res.status_code == 200:
            st.session_state.messages = res.json()
        else:
            st.session_state.messages = []
    except:
        st.session_state.messages = []

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- GEMINI STYLE ICONS & INPUT ---
st.markdown('<div style="display:flex; gap:10px; margin-bottom:-10px;">📸 🖼️ 📂</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Ask Nexus anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching memory... 🧠"):
            try:
                response = requests.post(f"{backend_url}/ask", json={"user_input": prompt}, timeout=90)
                if response.status_code == 200:
                    answer = response.json().get("response")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Server connection lost!")
            except Exception as e:
                st.error(f"Error: {e}")

# Sidebar for Recent Chats (Gemini Style)
with st.sidebar:
    st.title("🕒 Recent Activity")
    st.write("---")
    # Display last 5 user prompts as "Recents"
    recents = [m['content'][:25] + "..." for m in st.session_state.messages if m['role'] == 'user'][-5:]
    for r in reversed(recents):
        st.markdown(f"💬 {r}")
    
    st.write("---")
    if st.button("🗑️ Clear Permanent History"):
        # You'd need a delete endpoint to clear DB, for now reset UI
        st.session_state.messages = []
        st.rerun()
        
