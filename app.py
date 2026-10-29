import os
import re
import json
import requests
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

# 1. Tự động tìm và lấy API Key
api_key = ""
if os.path.exists("requirements.txt"):
    try:
        with open("requirements.txt", "r", encoding="utf-8") as rf:
            content = rf.read()
            match = re.search(r'AIzaSy[A-Za-z0-9_-]{33}', content)
            if match:
                api_key = match.group(0)
    except Exception as e:
        print("Lỗi đọc requirements.txt:", e)

if not api_key:
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = str(st.secrets["GEMINI_API_KEY"]).strip()
    except Exception:
        pass

if not api_key:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

# 2. Xử lý yêu cầu gọi AI chấm bài trực tiếp từ Python (Chống lỗi mạng & CORS trình duyệt)
query_params = st.query_params
if "action" in query_params and query_params["action"] == "ai_grade":
    student_name = query_params.get("name", "Em")
    student_answer = query_params.get("answer", "")
    rubric_content = query_params.get("rubric", "")
    exam_question = query_params.get("question", "Kiểm tra bài cũ")

    st.header("🤖 Trạm Xử Lý AI Gemini...")
    
    if not api_key:
        st.error("Chưa cấu hình Gemini API Key trong hệ thống!")
    elif not student_answer:
        st.warning("Học sinh chưa có câu trả lời.")
    else:
        prompt_text = f"""Bạn là một giáo viên có tâm, giàu kinh nghiệm sư phạm, ngôn từ ấm áp, gần gũi, xưng "thầy/cô" và gọi học sinh là "em".

THÔNG TIN BÀI KIỂM TRA:
- Đề bài: {exam_question}
- BÀI LÀM CỦA HỌC SINH ({student_name}):
"{student_answer}"

*** BẢN QUY CHẾ BAREM & MỌI YÊU CẦU CHẤM CỦA GIÁO VIÊN ***:
"""
{rubricContent or "Đánh giá mức độ hiểu bài và nắm vững kiến thức theo thang điểm 10."}
"""

NGUYÊN TẮC:
1. Tuân thủ barem về thang điểm và yêu cầu nhận xét.
2. Học sinh nói qua micro nên hiểu bản chất ý đúng.
3. Nhận xét chân thật, xưng hô tự nhiên (thầy/cô - em), khen ngợi cụ thể và dặn dò ân cần.

TRẢ VỀ DUY NHẤT một chuỗi JSON chuẩn (không chứa markdown ```json, không có text ngoài):
{{"score": "Điểm số ví dụ 8.5/10", "comment": "Lời nhận xét chi tiết"}}"""

        try:
            url = f"[https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=](https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=){api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt_text}]}],
                "generationConfig": {
                    "temperature": 0.35,
                    "responseMimeType": "application/json"
                }
            }
            res = requests.post(url, json=payload, timeout=25)
            if res.ok:
                data = res.json()
                raw_out = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "{}")
                st.code(raw_out, language="json")
                st.success("Đã chấm xong! Bạn có thể quay lại ứng dụng chính.")
            else:
                st.error(f"Lỗi từ Google API: {res.status_code} - {res.text}")
        except Exception as ex:
            st.error(f"Lỗi kết nối: {str(ex)}")
    st.stop()

# 3. Đọc file index.html và render ứng dụng
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    
    html_code = html_code.replace("{{GEMINI_API_KEY}}", api_key)
    components.html(html_code, height=980, scrolling=True)
except FileNotFoundError:
    st.error("Không tìm thấy tệp index.html trong repository!")
