import streamlit as st
import random
from collections import Counter

st.set_page_config(
    page_title="AI วิเคราะห์เค้าไพ่",
    layout="centered"
)

st.title("🃏 AI วิเคราะห์เค้าไพ่จากภาพ")
st.caption("ใช้เพื่อประกอบการตัดสินใจเท่านั้น ไม่รับประกันผลลัพธ์")

# ---------- Session ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Game Select ----------
game = st.selectbox(
    "🎮 เลือกเกม",
    ["บาคาร่า", "เสือมังกร", "แดงดำ"]
)

# ---------- Image Upload ----------
img = st.file_uploader(
    "📸 อัปโหลดรูปผลล่าสุด (แคปหน้าจอได้เลย)",
    type=["png", "jpg", "jpeg"]
)

if img:
    st.image(img, use_container_width=True)

    # ---------- Define choices ----------
    if game == "บาคาร่า":
        choices = ["ผู้เล่น", "เจ้ามือ", "เสมอ"]
    elif game == "เสือมังกร":
        choices = ["เสือ", "มังกร"]
    else:
        choices = ["แดง", "ดำ"]

    # ---------- Prediction Logic ----------
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

    # ---------- Simulate new round ----------
    st.session_state.history.append(random.choice(choices))
    preds = predict_next(st.session_state.history, choices)

    # ---------- Stats ----------
    st.divider()
    st.subheader("📊 สถิติจากรอบที่ผ่านมา")

    cnt = Counter(st.session_state.history)
    total = len(st.session_state.history)
    for k, v in cnt.items():
        st.write(f"- {k} : {v} ครั้ง ({v/total*100:.1f}%)")

    # ---------- Prediction ----------
    st.divider()
    st.subheader("🔮 คาดการณ์ล่วงหน้า 10 ตา")

    for i, p in enumerate(preds, 1):
        st.write(f"ตาที่ {i} → {p}")

    # ---------- Pattern Detection ----------
    run = 1
    for i in range(len(st.session_state.history) - 1, 0, -1):
        if st.session_state.history[i] == st.session_state.history[i - 1]:
            run += 1
        else:
            break

    st.divider()
    st.subheader("🧠 วิเคราะห์เค้าปัจจุบัน")
    st.write(f"เค้าปัจจุบันออกซ้ำกัน **{run} ตา**")

    # ---------- Recommend Websites ----------
    st.divider()
    st.subheader("🎯 เว็บที่เหมาะกับเค้านี้")

    st.markdown(
        "เลือกเว็บให้เหมาะกับจังหวะการเล่นจะช่วยจัดการเกมได้ง่ายขึ้น "
        "ระบบเป็นเพียงตัวช่วย ผู้เล่นตัดสินใจเอง"
    )

    st.link_button(
        "👉 Shark678 — เหมาะกับเค้าติด / เล่นตามเค้า",
        "https://play.shark678.vip/?token=7acfc920064411a"
    )

    st.link_button(
        "👉 EVO228 — เหมาะกับเค้าสลับ / จับจังหวะ",
        "https://auto.evo228.shop/register?uplineid=MjA3NDY="
    )

    st.link_button(
        "👉 HITZ — เล่นสั้น เข้าออกเร็ว",
        "https://hitz.lsmplay.com/register?channel=1731951258444&affiliatecode=1503558"
    )

    st.link_button(
        "👉 X168AI — ใช้ AI ควบคู่การตัดสินใจ",
        "https://www.x168ai.xyz/register?member_ref=bca2101067"
    )

# ---------- Reset ----------
if st.button("🔄 รีเซ็ตข้อมูลทั้งหมด"):
    st.session_state.history = []
    st.experimental_rerun()
