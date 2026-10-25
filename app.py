import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Kiểm Tra Bài Cũ - Hệ thống thông minh",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding: 0rem; margin: 0rem; max-width: 100% !important; }
    iframe { border: none !important; width: 100% !important; min-height: 100vh !important; }
    </style>
""", unsafe_allow_html=True)

# Lấy an toàn API Key từ Secrets của Streamlit nếu có
api_key = ""
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = os.environ.get("GEMINI_API_KEY", "")

try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # Nạp mã API Key vào file HTML nếu có
    html_code = html_code.replace("{{GEMINI_API_KEY}}", api_key)
    components.html(html_code, height=980, scrolling=True)
except FileNotFoundError:
    st.error("Không tìm thấy tệp index.html trong repository!")
