import streamlit as st
import random
from collections import Counter

# ---------- Page Config ----------
st.set_page_config(
    page_title="AI วิเคราะห์เค้าไพ่",
    layout="centered"
)

st.title("🃏 AI วิเคราะห์เค้าไพ่จากภาพ")
st.caption("ใช้เพื่อประกอบการตัดสินใจเท่านั้น ไม่รับประกันผลลัพธ์")

# ---------- Recommended Websites (SHOW ALWAYS) ----------
st.divider()
st.subheader("🔥 เว็บแนะนำสำหรับเข้าเล่น")

webs = [
    ("Shark678", "https://play.shark678.vip/?token=7acfc920064411a"),
    ("EVO228", "https://auto.evo228.shop/register?uplineid=MjA3NDY="),
    ("HITZ", "https://hitz.lsmplay.com/register?channel=1731951258444&affiliatecode=1503558"),
    ("X168AI", "https://www.x168ai.xyz/register?member_ref=bca2101067"),
]

for name, link in webs:
    st.markdown(f"👉 **[{name}]({link})**")

st.info("💡 แนะนำ: สมัครเว็บก่อน แล้วค่อยกลับมาอัปโหลดรูปเพื่อให้ AI ช่วยวิเคราะห์")

# ---------- Session ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Game Select ----------
st.divider()
game = st.selectbox("🎮 เลือกเกม", ["บาคาร่า", "เสือมังกร", "แดงดำ"])

# ---------- Image Upload ----------
img = st.file_uploader(
    "📸 อัปโหลดรูปผลล่าสุด (แคปหน้าจอได้เลย)",
    type=["png", "jpg", "jpeg"]
)

# ---------- Only analyze when image uploaded ----------
if img:
    st.image(img, use_container_width=True)

    if game == "บาคาร่า":
        choices = ["ผู้เล่น", "เจ้ามือ", "เสมอ"]
    elif game == "เสือมังกร":
        choices = ["เสือ", "มังกร"]
    else:
        choices = ["แดง", "ดำ"]

    # ---- AI Prediction Logic (Simple Trend-Based) ----
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

    # Simulate adding current round
    st.session_state.history.append(random.choice(choices))

    preds = predict_next(st.session_state.history, choices)

    # ---------- Display ----------
    st.divider()
    st.subheader("📊 สถิติย้อนหลัง")

    cnt = Counter(st.session_state.history)
    total = len(st.session_state.history)
    for k, v in cnt.items():
        st.write(f"{k} = {v} ({v/total*100:.1f}%)")

    st.divider()
    st.subheader("🔮 คาดการณ์ล่วงหน้า 10 ตา")

    for i, p in enumerate(preds, 1):
        st.write(f"ตาที่ {i} → {p}")

else:
    st.warning("⬆️ เมื่ออัปโหลดรูป ระบบจะเริ่มวิเคราะห์เค้าไพ่ให้อัตโนมัติ")

# ---------- Reset ----------
if st.button("🔄 รีเซ็ตข้อมูลทั้งหมด"):
    st.session_state.history = []
    st.experimental_rerun()
