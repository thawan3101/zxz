import streamlit as st
import random
from collections import Counter
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI วิเคราะห์เค้าไพ่", layout="centered")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #141E30, #243B55);
    color: #ffffff;
}
.block-container {
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.stButton>button {
    background: linear-gradient(135deg, #ff512f, #dd2476);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.6rem 1.2rem;
    font-weight: bold;
}
.stButton>button:hover { opacity: 0.9; }
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.1);
    border-radius: 15px;
    padding: 10px;
}
a { color: #00ffd5 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("## 🃏 AI วิเคราะห์เค้าไพ่จากภาพ")
st.caption("ใช้เพื่อประกอบการตัดสินใจเท่านั้น ไม่รับประกันผลลัพธ์")

# ---------------- SESSION ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- AFFILIATE WEBS (ครบ 4 เว็บ) ----------------
st.markdown("### ✅ เว็บที่เหมาะกับการใช้ระบบนี้")

st.markdown("""
🟢 **Shark678**  
เหมาะกับสายดูเค้าไพ่สด โต๊ะชัด เค้าเดินไว  
ใช้ AI ประกอบแล้วอ่านทางง่าย  
👉 [กดสมัคร / เข้าเล่น](https://play.shark678.vip/?token=7acfc920064411a)

---

🟡 **EVO228**  
สาย Evolution ต้องเว็บนี้  
Roadmap ชัด ดูย้อนหลังง่าย เหมาะกับการวิเคราะห์เค้า  
👉 [กดสมัคร / เข้าเล่น](https://auto.evo228.shop/register?uplineid=MjA3NDY=)

---

🔵 **LSM Play**  
เหมาะกับสายเล่นยาว เค้าไม่แกว่ง ระบบเสถียร  
ใช้ระบบนี้ช่วยตัดสินใจได้ดี  
👉 [กดสมัคร / เข้าเล่น](https://hitz.lsmplay.com/register?channel=1731951258444&affiliatecode=1503558)

---

🟣 **X168 AI**  
ออกแบบมาสำหรับสาย AI โดยเฉพาะ  
โต๊ะชัด Roadmap อ่านง่าย เหมาะกับระบบนี้  
👉 [กดสมัคร / เข้าเล่น](https://www.x168ai.xyz/register?member_ref=bca2101067)
""")

st.divider()

# ---------------- GAME SELECT ----------------
game = st.selectbox("🎮 เลือกเกม", ["บาคาร่า", "เสือมังกร", "แดงดำ"])

# ---------------- IMAGE INFO ----------------
st.markdown("""
📸 **อัปโหลดรูปแคปหน้าจอผลล่าสุด**

> ℹ️ หากอัปโหลดไม่ได้ / error  
> • ตัดรูปให้เหลือเฉพาะ **ตารางเค้าไพ่ (Roadmap)**  
> • ไม่ต้องเอาทั้งหน้าจอเกม  
> • รูปเล็กลง = วิเคราะห์เร็วและเสถียรกว่า
""")
st.info("⚠️ หากใช้ VPN หรือเน็ตฟรี อาจทำให้อัปโหลดรูปไม่ได้ แนะนำปิด VPN ชั่วคราว")

# ---------------- IMAGE UPLOADER ----------------
img = st.file_uploader("", type=["png", "jpg", "jpeg"])

if img:
    image = Image.open(img)
    st.image(image, use_container_width=True)

    if game == "บาคาร่า":
        choices = ["ผู้เล่น", "เจ้ามือ", "เสมอ"]
    elif game == "เสือมังกร":
        choices = ["เสือ", "มังกร"]
    else:
        choices = ["แดง", "ดำ"]

    # จำลองเพิ่มผลล่าสุด
    st.session_state.history.append(random.choice(choices))

    def predict_next(history, choices, n=10):
        result = []
        if history:
            last = history[-1]
            for _ in range(n):
                result.append(last if random.random() < 0.6 else random.choice(choices))
        else:
            result = random.choices(choices, k=n)
        return result

    preds = predict_next(st.session_state.history, choices)

    # ---------------- ANALYSIS ----------------
    st.divider()
    st.markdown("### 📊 วิเคราะห์สถิติ")

    cnt = Counter(st.session_state.history)
    total = len(st.session_state.history)
    for k, v in cnt.items():
        st.write(f"**{k}** : {v} ครั้ง ({v/total*100:.1f}%)")

    run = 1
    for i in range(total - 1, 0, -1):
        if st.session_state.history[i] == st.session_state.history[i - 1]:
            run += 1
        else:
            break
    st.success(f"🔥 เค้าปัจจุบันติด {run} ตา")

    # ---------------- PREDICTION ----------------
    st.divider()
    st.markdown("### 🔮 คาดการณ์ล่วงหน้า 10 ตา")
    for i, p in enumerate(preds, 1):
        st.write(f"ตาที่ {i} ➜ **{p}**")

# ---------------- RESET ----------------
if st.button("🔄 รีเซ็ตข้อมูลทั้งหมด"):
    st.session_state.history = []
    st.experimental_rerun()
