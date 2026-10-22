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

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding: 0rem; margin: 0rem; max-width: 100% !important; }
    iframe { border: none !important; width: 100% !important; min-height: 100vh !important; }
    </style>
""", unsafe_allow_html=True)

DATA_PATH = "data_store.json"

def get_store():
    if not os.path.exists(DATA_PATH):
        init_data = {"exams": [], "submissions": [], "teachers": {}}
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(init_data, f, ensure_ascii=False, indent=2)
        return init_data
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"exams": [], "submissions": [], "teachers": {}}

def update_store(data):
    try:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Lỗi ghi file:", e)

# Bộ xử lý API đồng bộ đa thiết bị
qp = st.query_params
if "api" in qp:
    api_cmd = qp["api"]
    store = get_store()
    
    if api_cmd == "save_exam":
        try:
            payload = json.loads(qp.get("data", "{}"))
            exams = [e for e in store.get("exams", []) if e.get("id") != payload.get("id")]
            exams.insert(0, payload)
            store["exams"] = exams
            update_store(store)
            st.json({"status": "success", "count": len(exams)})
            st.stop()
        except Exception as err:
            st.json({"status": "error", "msg": str(err)})
            st.stop()
            
    elif api_cmd == "save_sub":
        try:
            payload = json.loads(qp.get("data", "{}"))
            subs = [s for s in store.get("submissions", []) if s.get("id") != payload.get("id")]
            subs.insert(0, payload)
            store["submissions"] = subs
            update_store(store)
            st.json({"status": "success"})
            st.stop()
        except Exception as err:
            st.json({"status": "error", "msg": str(err)})
            st.stop()
            
    elif api_cmd == "fetch_all":
        st.json(store)
        st.stop()

# Đọc tệp index.html và truyền dữ liệu máy chủ vào giao diện
current_data = get_store()
bootstrap_script = f"""
<script>
    window.__SERVER_BOOTSTRAP__ = {json.dumps(current_data, ensure_ascii=False)};
</script>
"""

try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    if "<head>" in html_content:
        rendered_html = html_content.replace("<head>", f"<head>{bootstrap_script}", 1)
    else:
        rendered_html = bootstrap_script + html_content

    components.html(rendered_html, height=980, scrolling=True)
except FileNotFoundError:
    st.error("Không tìm thấy tệp index.html trong thư mục ứng dụng!")
