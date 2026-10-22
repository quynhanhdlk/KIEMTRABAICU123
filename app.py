import streamlit as st
import streamlit.components.v1 as components
import json
import os

st.set_page_config(
    page_title="Kiểm Tra Bài Cũ - Hệ thống thông minh",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ẩn thanh header/footer mặc định của Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding: 0rem; margin: 0rem; }
    iframe { border: none !important; width: 100% !important; min-height: 98vh !important; }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "app_shared_data.json"

# Khởi tạo tệp dữ liệu chung nếu chưa có
if not os.path.exists(DATA_FILE):
    initial_db = {"exams": [], "submissions": [], "teachers": {}}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(initial_db, f, ensure_ascii=False, indent=2)

def read_db():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"exams": [], "submissions": [], "teachers": {}}

def write_db(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Lỗi ghi file:", e)

# Nhận các yêu cầu lưu / đọc dữ liệu từ client
params = st.query_params
if "action" in params:
    act = params["action"]
    db = read_db()
    
    if act == "save_exam":
        try:
            exam_data = json.loads(params.get("payload", "{}"))
            # Thêm hoặc cập nhật đề
            exams = [e for e in db.get("exams", []) if e.get("id") != exam_data.get("id")]
            exams.insert(0, exam_data)
            db["exams"] = exams
            write_db(db)
            st.json({"status": "ok", "count": len(exams)})
            st.stop()
        except Exception as e:
            st.json({"status": "error", "msg": str(e)})
            st.stop()

    elif act == "save_sub":
        try:
            sub_data = json.loads(params.get("payload", "{}"))
            subs = [s for s in db.get("submissions", []) if s.get("id") != sub_data.get("id")]
            subs.insert(0, sub_data)
            db["submissions"] = subs
            write_db(db)
            st.json({"status": "ok"})
            st.stop()
        except Exception as e:
            st.json({"status": "error", "msg": str(e)})
            st.stop()

    elif act == "get_db":
        st.json(db)
        st.stop()

# Đọc mã nguồn index.html và tiêm dữ liệu máy chủ vào trước khi hiển thị
current_db = read_db()
db_injection = f"""
<script>
    window.SERVER_DATA = {json.dumps(current_db, ensure_ascii=False)};
</script>
"""

try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    full_html = html_code.replace("<head>", f"<head>{db_injection}", 1)
    components.html(full_html, height=950, scrolling=True)
except FileNotFoundError:
    st.error("Không tìm thấy tệp index.html!")
