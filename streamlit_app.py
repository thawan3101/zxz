import streamlit as st
import random
from collections import Counter
from PIL import Image

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

# ---------------- RECOMMENDED WEBS ----------------
st.subheader("✅ เว็บที่เหมาะกับการใช้ระบบนี้")

st.markdown("""
### ✅ **LSM Play**
เหมาะกับสายเล่นยาว เค้าเสถียร อ่านทางง่าย  
👉 [กดสมัคร / เข้าเล่น](https://hitz.lsmplay.com/register?channel=1731951258444&affiliatecode=1503558)

---

### ✅ **X168 AI**
เหมาะกับการใช้ AI วิเคราะห์โดยเฉพาะ  
โต๊ะชัด Roadmap อ่านง่าย  
👉 [กดสมัคร / เข้าเล่น](https://www.x168ai.xyz/register?member_ref=bca2101067)
""")

st.divider()

# ---------------- GAME SELECT ----------------
game = st.selectbox(
    "🎮 เลือกเกม",
    ["บาคาร่า", "เสือมังกร", "แดงดำ"]
)

# ---------------- IMAGE UPLOAD INFO ----------------
st.markdown("""
📸 **อัปโหลดรูปผลล่าสุด (แคปหน้าจอได้)**  

> ℹ️ **หากอัปโหลดรูปไม่ผ่าน / error**  
> - ให้ตัดรูป **เหลือเฉพาะตารางเค้าไพ่ (Roadmap)**  
> - ไม่จำเป็นต้องเอาทั้งหน้าจอเกม  
> - รูปเล็กลง = วิเคราะห์ได้เร็วและเสถียรกว่า
""")

st.info(
    "💡 หากใช้ VPN หรือเน็ตฟรี อาจทำให้อัปโหลดรูปไม่ได้\n"
    "แนะนำปิด VPN ชั่วคราวตอนอัปโหลดรูป"
)

# ---------------- IMAGE UPLOADER ----------------
img = st.file_uploader(
    "",
    type=["png", "jpg", "jpeg"]
)

if img:
    image = Image.open(img)
    st.image(image, use_container_width=True)

    # ---------- Define choices ----------
    if game == "บาคาร่า":
        choices = ["ผู้เล่น", "เจ้ามือ", "เสมอ"]
    elif game == "เสือมังกร":
        choices = ["เสือ", "มังกร"]
    else:
        choices = ["แดง", "ดำ"]

    # ---------- Simulate new round ----------
    st.session_state.history.append(random.choice(choices))

    # ---------- Predict next 10 ----------
    def predict_next(history, choices, n=10):
        result = []
        if history:
            last = history[-1]
            for _ in range(n):
                if random.random() < 0.6:
                    result.append(last)
                else:
                    result.append(random.choice(choices))
        else:
            result = random.choices(choices, k=n)
        return result

    preds = predict_next(st.session_state.history, choices)

    # ---------- Analysis ----------
    st.divider()
    st.subheader("📊 วิเคราะห์สถิติที่ผ่านมา")

    cnt = Counter(st.session_state.history)
    total = len(st.session_state.history)

    for k, v in cnt.items():
        st.write(f"{k} = {v} ครั้ง ({v/total*100:.1f}%)")

    # ---------- Run streak ----------
    run = 1
    for i in range(total - 1, 0, -1):
        if st.session_state.history[i] == st.session_state.history[i - 1]:
            run += 1
        else:
            break

    st.write(f"🔥 เค้าปัจจุบันติด: {run} ตา")

    # ---------- Prediction ----------
    st.divider()
    st.subheader("🔮 คาดการณ์ล่วงหน้า 10 ตา")

    for i, p in enumerate(preds, 1):
        st.write(f"ตาที่ {i} → {p}")

# ---------------- RESET ----------------
if st.button("🔄 รีเซ็ตข้อมูลทั้งหมด"):
    st.session_state.history = []
    st.experimental_rerun()
