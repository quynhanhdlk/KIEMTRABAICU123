import streamlit as st
import streamlit.components.v1 as components

# Thiết lập cấu hình trang hiển thị toàn màn hình
st.set_page_config(
    page_title="Kiểm Tra Bài Cũ - Hệ thống thông minh",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ẩn thanh header và footer mặc định của Streamlit để giao diện đẹp mắt
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
    }
    iframe {
        border: none !important;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Đọc toàn bộ mã HTML của ứng dụng từ tệp index.html cùng thư mục
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
except FileNotFoundError:
    st.error("Không tìm thấy tệp index.html! Hãy đảm bảo đã đặt tệp index.html cùng thư mục với app.py.")
    html_code = ""

if html_code:
    # Nhúng và render ứng dụng với chiều cao phù hợp
    components.html(html_code, height=920, scrolling=True)
