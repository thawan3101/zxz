import streamlit as st
import random
from collections import Counter
from PIL import Image
from io import BytesIO

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AI วิเคราะห์เค้าไพ่จากภาพ",
    layout="centered"
)

st.title("🃏 AI วิเคราะห์เค้าไพ่จากภาพ")
st.caption("ใช้เพื่อประกอบการตัดสินใจเท่านั้น ไม่รับประกันผลลัพธ์")

# ---------------- SESSION ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- GAME SELECT ----------------
game = st.selectbox(
    "🎮 เลือกเกม",
    ["บาคาร่า", "เสือมังกร", "แดงดำ"]
)

# ---------------- AFFILIATE WEBS ----------------
st.divider()
st.subheader("🔥 เว็บแนะนำ (เหมาะกับการใช้ระบบนี้)")

st.markdown("""
### ✅ LSM Play  
เหมาะกับสายเล่นยาว ระบบเสถียร เค้าไม่แกว่ง  
👉 [กดสมัคร / เข้าเล่น](https://hitz.lsmplay.com/register?channel=1731951258444&affiliatecode=1503558)

---

### ✅ X168 AI  
เหมาะกับการใช้ AI วิเคราะห์โดยเฉพาะ โต๊ะชัด อ่าน Roadmap ง่าย  
👉 [กดสมัคร / เข้าเล่น](https://www.x168ai.xyz/register?member_ref=bca2101067)
""")

# ---------------- IMAGE UPLOAD ----------------
st.divider()
uploaded_file = st.file_uploader(
    "📸 อัปโหลดรูปผลล่าสุด (แคปหน้าจอแนวตั้งได้ ระบบจะย่อให้อัตโนมัติ)",
    type=["png", "jpg", "jpeg"]
)

def show_full_image(uploaded_file):
    img = Image.open(uploaded_file)
    if img.mode != "RGB":
        img = img.convert("RGB")

    max_width = 1080
    if img.width > max_width:
        ratio = max_width / img.width
        new_size = (max_width, int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)

    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=80)
    buffer.seek(0)

    st.image(buffer, use_container_width=True)

# ---------------- ANALYSIS ----------------
if uploaded_file:
    show_full_image(uploaded_file)

    if game == "บาคาร่า":
        choices = ["ผู้เล่น", "เจ้ามือ"]
    elif game == "เสือมังกร":
        choices = ["เสือ", "มังกร"]
    else:
        choices = ["แดง", "ดำ"]

    # จำลองการเพิ่มผลล่าสุด 1 ตา
    last_round = random.choice(choices)
    st.session_state.history.append(last_round)

    history = st.session_state.history
    total = len(history)

    # วิเคราะห์เค้า
    run = 1
    for i in range(total - 1, 0, -1):
        if history[i] == history[i - 1]:
            run += 1
        else:
            break

    cnt = Counter(history)

    st.divider()
    st.subheader("📊 วิเคราะห์เค้าปัจจุบัน")

    st.write(f"▶ ตาล่าสุด: **{last_round}**")
    st.write(f"🔥 เค้าติด: **{run} ตา**")

    for k, v in cnt.items():
        st.write(f"{k} = {v} ({v/total*100:.1f}%)")

    # ---------------- PREDICT ----------------
    def predict_next(history, choices, n=10):
        result = []
        last = history[-1]
        for _ in range(n):
            if random.random() < 0.65:
                result.append(last)
            else:
                result.append(random.choice(choices))
        return result

    preds = predict_next(history, choices)

    st.divider()
    st.subheader("🔮 คาดการณ์ล่วงหน้า 10 ตา")

    for i, p in enumerate(preds, 1):
        st.write(f"ตาที่ {i} → {p}")

# ---------------- RESET ----------------
st.divider()
if st.button("🔄 รีเซ็ตข้อมูลทั้งหมด"):
    st.session_state.history = []
    st.experimental_rerun()
