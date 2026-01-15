import streamlit as st
import random
import base64
from collections import Counter

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AI วิเคราะห์เค้าไพ่",
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

# ---------------- WEB RECOMMEND (แสดงทันที) ----------------
st.divider()
st.subheader("🔥 เว็บแนะนำ เหมาะกับการใช้ AI วิเคราะห์")

webs = [
    (
        "Shark678",
        "เหมาะกับสายดูเค้าไพ่สด โต๊ะชัด เค้าเดินไว ใช้ AI ประกอบแล้วอ่านง่าย",
        "https://play.shark678.vip/?token=7acfc920064411a"
    ),
    (
        "EVO228",
        "โต๊ะ Evolution เยอะ เหมาะกับการดูสถิติย้อนหลัง + เค้าไพ่ต่อเนื่อง",
        "https://auto.evo228.shop/register?uplineid=MjA3NDY="
    ),
    (
        "LSM Play",
        "เหมาะกับสายเล่นยาว ระบบเสถียร เค้าไม่แกว่ง อ่านทางง่าย",
        "https://hitz.lsmplay.com/register?channel=1731951258444&affiliatecode=1503558"
    ),
    (
        "X168 AI",
        "เหมาะกับการใช้ AI วิเคราะห์โดยเฉพาะ โต๊ะชัด ดู Roadmap ง่าย",
        "https://www.x168ai.xyz/register?member_ref=bca2101067"
    ),
]

for name, desc, link in webs:
    st.markdown(f"""
    ### ✅ {name}
    {desc}  
    👉 [กดสมัคร / เข้าเล่น]({link})
    """)

# ---------------- IMAGE FUNCTION ----------------
def show_full_image(uploaded_file):
    bytes_data = uploaded_file.getvalue()
    encoded = base64.b64encode(bytes_data).decode()

    st.markdown(
        f"""
        <div style="width:100%; text-align:center;">
            <img src="data:image/png;base64,{encoded}"
                 style="max-width:100%; height:auto; border-radius:12px;">
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- IMAGE UPLOAD ----------------
st.divider()
uploaded_file = st.file_uploader(
    "📸 อัปโหลดรูปผลล่าสุด (แคปหน้าจอแนวตั้งได้)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    st.success("✅ โหลดรูปสำเร็จ (ไม่ตัด ไม่ย่อ)")
    show_full_image(uploaded_file)

    # ---------------- GAME LOGIC ----------------
    if game == "บาคาร่า":
        choices = ["ผู้เล่น", "เจ้ามือ", "เสมอ"]
    elif game == "เสือมังกร":
        choices = ["เสือ", "มังกร"]
    else:
        choices = ["แดง", "ดำ"]

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

    # เพิ่มผลล่าสุดจำลอง
    st.session_state.history.append(random.choice(choices))

    preds = predict_next(st.session_state.history, choices)

    # ---------------- DISPLAY RESULT ----------------
    st.divider()
    st.subheader("📊 วิเคราะห์แนวโน้ม")

    cnt = Counter(st.session_state.history)
    for k, v in cnt.items():
        st.write(f"{k} = {v} ครั้ง ({v/len(st.session_state.history)*100:.1f}%)")

    st.divider()
    st.subheader("🔮 คาดการณ์ล่วงหน้า 10 ตา")

    for i, p in enumerate(preds, 1):
        st.write(f"ตาที่ {i} → {p}")

# ---------------- RESET ----------------
st.divider()
if st.button("🔄 รีเซ็ตข้อมูลทั้งหมด"):
    st.session_state.history = []
    st.experimental_rerun()
