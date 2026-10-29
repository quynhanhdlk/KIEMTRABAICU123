import os
import re
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

api_key = ""

# 1. Đọc từ requirements.txt hoặc requirement.txt
for fname in ["requirements.txt", "requirement.txt"]:
    if os.path.exists(fname):
        try:
            with open(fname, "r", encoding="utf-8") as rf:
                content = rf.read()
                match = re.search(r'AIzaSy[A-Za-z0-9_-]{33}', content)
                if match:
                    api_key = match.group(0)
                    break
        except Exception as e:
            pass

# 2. Đọc từ Streamlit Secrets
if not api_key:
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = str(st.secrets["GEMINI_API_KEY"]).strip()
    except Exception:
        pass

# 3. Đọc từ Biến môi trường
if not api_key:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    
    html_code = html_code.replace("{{GEMINI_API_KEY}}", api_key)
    components.html(html_code, height=980, scrolling=True)
except FileNotFoundError:
    st.error("Không tìm thấy tệp index.html trong repository!")
