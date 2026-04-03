import streamlit as st
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Nexus Flow AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Professional UI (Gemini-style Bottom Search) ---
st.markdown("""
    <style>
    /* White Theme Overrides */
    .stApp {
        background-color: #ffffff;
        color: #1f1f1f;
    }
    
    /* Main Chat Container */
    .main .block-container {
        padding-bottom: 100px;
    }

    /* Professional Message Bubbles */
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        max-width: 85%;
    }

    /* Fixed Bottom Search Bar Container */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        z-index: 1000;
        background-color: #ffffff;
        border-radius: 50px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        padding: 5px;
    }

    /* Hide redundant UI elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Progress Bar and Thinking Style */
    .stProgress > div > div > div > div {
        background-color: #4285F4;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "General"

# --- Sidebar for Advanced Modes ---
with st.sidebar:
    st.title("Nexus Flow Settings")
    st.session_state.mode = st.selectbox(
        "Select AI Mode",
        ["General", "Study", "Coding Expert", "Reasoning & Thinking", "Creative Writing", "Knowledge", "Life Mode"]
    )
    st.info(f"Current Mode: {st.session_state.mode} 🚀")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# --- Chat Engine Logic (Next Level Features) ---
def get_ai_response(user_input, mode):
    # Simulated thinking process for advanced reasoning
    if mode == "Reasoning & Thinking":
        with st.status("Analyzing and Reasoning...", expanded=True):
            st.write("Checking logical consistency... 🧠")
            time.sleep(1)
            st.write("Verifying facts and data... 🔍")
            time.sleep(1)
            st.write("Synthesizing final answer... ✨")
    
    # Mode-based Response Customization
    response_prefix = ""
    if mode == "Coding Expert":
        response_prefix = "💻 **Nexus Code Pro:** \n\n"
    elif mode == "Study":
        response_prefix = "📖 **Academic Assistant:** \n\n"
    elif mode == "General":
        response_prefix = "✨ "

    # Mock response logic (Replace with your Gemini/OpenAI API call)
    # Adding emojis automatically as requested
    return f"{response_prefix}Maine aapka sawal '{user_input}' samajh liya hai. Main aapki help karne ke liye taiyar hoon! ✅ 🚀"

# --- Chat Display ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input (Bottom Search Bar) ---
if prompt := st.chat_input("Ask Nexus Flow anything..."):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response
    with st.chat_message("assistant"):
        response = get_ai_response(prompt, st.session_state.mode)
        
        # Expert Response Simulation (Non-Talkative & Direct)
        full_response = ""
        placeholder = st.empty()
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Video/Coding Expert Metadata ---
if st.session_state.mode == "Coding Expert":
    st.caption("Nexus Flow is currently in Code Expert mode. Optimized for Python, C++, and Web Dev. ⚡")
    
