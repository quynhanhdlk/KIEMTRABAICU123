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

# 1. Tự động tìm API Key từ biến môi trường hoặc các file trong thư mục
api_key = os.environ.get("GEMINI_API_KEY", "")

# Nếu chưa có trong môi trường, tự quét các file text / .env bạn đã tải lên repo
if not api_key:
    possible_files = [".env", "api_key.txt", "gemini_key.txt", "key.txt", "GEMINI_API_KEY.txt"]
    for fname in possible_files:
        if os.path.exists(fname):
            with open(fname, "r", encoding="utf-8") as kf:
                content = kf.read().strip()
                # Lọc lấy chuỗi bắt đầu bằng AIzaSy
                for line in content.splitlines():
                    line = line.strip().replace("GEMINI_API_KEY=", "").replace("\"", "").replace("'", "")
                    if line.startswith("AIzaSy"):
                        api_key = line
                        break
            if api_key:
                break

# 2. Đọc tệp index.html và tự động tiêm API Key vào để HTML sử dụng trực tiếp
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # Thay thế biến giữ chỗ trong HTML bằng Key thực tế vừa đọc được
    html_code = html_code.replace("{{GEMINI_API_KEY}}", api_key)
    
    components.html(html_code, height=980, scrolling=True)
except FileNotFoundError:
    st.error("Không tìm thấy tệp index.html trong thư mục gốc!")
