import streamlit as st
import numpy as np
import pickle

# --------------------------------------------------
# PAGE CONFIG (DO NOT CHANGE TITLE)
# --------------------------------------------------
st.set_page_config(
    page_title="HealNet",
    page_icon="🩺",
    layout="centered"
)

# --------------------------------------------------
# SIMPLE & CLEAN STYLING
# --------------------------------------------------
st.markdown("""
<style>
.main-card {
    background-color: #ffffff;
    padding: 28px;
    border-radius: 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
}
.step {
    font-size: 18px;
    font-weight: 600;
    margin-top: 15px;
}
.help-text {
    color: #6b7280;
    font-size: 14px;
}
.low-box {
    background: #eafaf1;
    padding: 18px;
    border-radius: 12px;
    border-left: 6px solid #22c55e;
}
.mid-box {
    background: #fff7ed;
    padding: 18px;
    border-radius: 12px;
    border-left: 6px solid #f59e0b;
}
.high-box {
    background: #fdecea;
    padding: 18px;
    border-radius: 12px;
    border-left: 6px solid #ef4444;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# BRAND HEADER (KEEP TITLE)
# --------------------------------------------------
st.markdown("<div class='main-card'>", unsafe_allow_html=True)

st.markdown("## 🩺 **HealNet**")
st.caption("By **IoTrenetics Solutions Pvt. Ltd.**")

st.markdown(
    "This tool helps you understand your **overall health risk** using basic health details."
)

st.divider()

# --------------------------------------------------
# SAFE MODEL LOADING (OPTIONAL)
# --------------------------------------------------
@st.cache_resource
def load_model():
    try:
        with open("model.pkl", "rb") as f:
            return pickle.load(f)
    except Exception:
        return None

model = load_model()

# --------------------------------------------------
# HYBRID RISK LOGIC (UNCHANGED)
# --------------------------------------------------
def assess_risk(age, bp, chol, bmi):
    score = 0

    if age >= 60:
        score += 2
    elif age >= 45:
        score += 1

    if bp >= 140:
        score += 3
    elif bp >= 130:
        score += 2
    elif bp >= 120:
        score += 1

    if chol >= 240:
        score += 3
    elif chol >= 200:
        score += 2
    elif chol >= 180:
        score += 1

    if bmi >= 30:
        score += 3
    elif bmi >= 25:
        score += 2
    elif bmi >= 23:
        score += 1

    ml_prob = 0.0
    if model is not None:
        try:
            ml_prob = model.predict_proba(
                np.array([[age, bp, chol, bmi]])
            )[0][1]
        except Exception:
            ml_prob = 0.0

    if score >= 7 or ml_prob >= 0.65:
        return "High"
    elif score >= 4 or ml_prob >= 0.35:
        return "Moderate"
    else:
        return "Low"

# --------------------------------------------------
# STEP-BY-STEP INPUTS (NON-TECHNICAL)
# --------------------------------------------------
st.markdown("### 🧾 Step 1: Enter Your Details")

age = st.slider(
    "👤 Your Age",
    18, 80, 35,
    help="Select your age in years"
)

bp = st.slider(
    "❤️ Blood Pressure (upper number)",
    90, 200, 120,
    help="Example: 120 in 120/80"
)

chol = st.slider(
    "🧪 Cholesterol Level",
    120, 320, 180,
    help="Normal is usually below 200"
)

bmi = st.slider(
    "⚖️ Body Weight (BMI)",
    15.0, 40.0, 23.0,
    help="BMI is based on height & weight"
)

st.divider()

# --------------------------------------------------
# RESULT BUTTON
# --------------------------------------------------
if st.button("🔍 Check My Health Risk"):
    risk = assess_risk(age, bp, chol, bmi)

    st.markdown("### 📊 Your Health Result")

    if risk == "Low":
        st.markdown("""
        <div class="low-box">
        <b>🟢 Low Health Risk</b><br><br>
        Your health values are mostly within a safe range.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
**What this means for you:**
- Keep your current lifestyle
- Eat healthy and stay active
- Do regular yearly checkups

📚 WHO & NIH Preventive Health Guidelines
""")

    elif risk == "Moderate":
        st.markdown("""
        <div class="mid-box">
        <b>🟡 Moderate Health Risk</b><br><br>
        Some values need attention, but it can be improved.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
**What this means for you:**
- Reduce oily & salty food
- Walk or exercise daily
- Monitor BP and cholesterol

📚 American Heart Association, NEJM
""")

    else:
        st.markdown("""
        <div class="high-box">
        <b>🔴 High Health Risk</b><br><br>
        Medical attention is strongly recommended.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
**What this means for you:**
- Consult a doctor soon
- Follow medical advice strictly
- Lifestyle changes are important

📚 ACC/AHA & The Lancet
""")

    st.info("⚠️ HealNet provides health guidance only. It is not a medical diagnosis.")

st.markdown("</div>", unsafe_allow_html=True)
