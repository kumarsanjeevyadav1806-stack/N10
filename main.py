import streamlit as st
import base64

# 1. Page Config
st.set_page_config(page_title="Nexus Flow AI", layout="centered")

# 2. Gemini Style CSS (The Magic)
st.markdown("""
    <style>
    /* White Theme */
    .stApp { background-color: white; color: black; }
    
    /* Messages area ko niche se khali rakhein taaki input bar ke piche na chhupen */
    .main .block-container {
        padding-bottom: 150px !important;
        max-width: 800px;
    }

    /* Asli Gemini Bottom Bar UI */
    /* Hum Streamlit ke 'Bottom Block' container ko target kar rahe hain */
    [data-testid="stBottomBlockContainer"] {
        background-color: white !important;
        border-top: 1px solid #f0f2f6;
        padding: 10px 5% 30px 5% !important;
    }

    /* Force Columns Side-by-Side (Mobile Fix) */
    [data-testid="column"] {
        width: fit-content !important;
        flex: unset !important;
        min-width: unset !important;
    }

    /* Gemini Plus Icon Style */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 48px !important;
        height: 48px !important;
        background-color: #f0f4f9 !important;
        border: none !important;
        font-size: 24px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-top: 5px;
    }

    /* Clean Search Input */
    .stChatInput {
        border-radius: 28px !important;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. Layout (Plus Icon aur Search Bar Ek Hi Line Mein)
# Streamlit ka 'st.chat_input' hamesha bottom mein rehta hai, 
# lekin use plus ke sath align karne ke liye hum Columns ka use karenge jo 'st.container' ke andar honge.

with st.container():
    # Columns create karein: ek chota plus ke liye, ek bada search ke liye
    col_plus, col_search = st.columns([0.15, 0.85])
    
    with col_plus:
        # Gemini Style Slide-up Menu
        with st.popover("➕"):
            st.markdown("### Attach Files")
            st.radio("Options", ["📷 Camera", "🖼️ Gallery", "📎 Files"], label_visibility="collapsed")
            uploaded_file = st.file_uploader("Upload", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

    with col_search:
        # Yahan search bar hamesha plus ke bagal mein rahega
        prompt = st.chat_input("Ask Gemini...")

# 4. Logic (Testing)
if prompt:
    st.write(f"Sanjeev, aapne pucha: {prompt}")
    
