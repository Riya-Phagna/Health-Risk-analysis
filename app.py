import streamlit as st
import numpy as np
import pickle

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="HealNet ",
    page_icon="🩺",
    layout="centered"
)

# --------------------------------------------------
# SIMPLE UI STYLING
# --------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #f6f8fc;
}
.main-card {
    background-color: white;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}
.result-low {
    background: #eafaf1;
    padding: 15px;
    border-radius: 10px;
    border-left: 6px solid #2ecc71;
}
.result-mid {
    background: #fff4e5;
    padding: 15px;
    border-radius: 10px;
    border-left: 6px solid #f39c12;
}
.result-high {
    background: #fdecea;
    padding: 15px;
    border-radius: 10px;
    border-left: 6px solid #e74c3c;
}
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER / BRANDING
# --------------------------------------------------
st.markdown("<div class='main-card'>", unsafe_allow_html=True)

st.markdown("## 🩺 **HealNet**")
st.caption("By **IoTrenetics Solutions Pvt. Ltd.**")

st.markdown("---")



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
        return "High", score
    elif score >= 4 or ml_prob >= 0.35:
        return "Moderate", score
    else:
        return "Low", score

# --------------------------------------------------
# USER INPUTS (VERY SIMPLE)
# --------------------------------------------------
st.markdown("### 🧾 Your Health Details")

age = st.slider("Age (in years)", 18, 80, 35)
bp = st.slider("Blood Pressure (upper value)", 90, 200, 120)
chol = st.slider("Cholesterol level", 120, 320, 180)
bmi = st.slider("Body Weight Index (BMI)", 15.0, 40.0, 23.0)

st.markdown("---")

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------
if st.button("🔍 Check My Health Risk"):
    risk, score = assess_risk(age, bp, chol, bmi)

    st.markdown("### 📊 Your Result")

    if risk == "Low":
        st.markdown(f"""
        <div class="result-low">
        <b>🟢 Low Health Risk</b><br>
        Your current health indicators are within a safe range.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
**What you should do:**
- Continue healthy eating habits  
- Stay physically active  
- Regular yearly health checkups  

📚 WHO & NIH Preventive Health Guidelines
""")

    elif risk == "Moderate":
        st.markdown(f"""
        <div class="result-mid">
        <b>🟡 Moderate Health Risk</b><br>
        Some indicators need attention.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
**What you should do:**
- Reduce salt and fatty food  
- Exercise at least 30 minutes daily  
- Monitor BP & cholesterol regularly  

📚 American Heart Association, NEJM
""")

    else:
        st.markdown(f"""
        <div class="result-high">
        <b>🔴 High Health Risk</b><br>
        Medical consultation is recommended.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
**What you should do:**
- Consult a doctor at the earliest  
- Follow medical advice strictly  
- Lifestyle and diet changes are critical  

📚 ACC/AHA & The Lancet
""")

    st.info("⚠️ HealNet is an educational support tool and does not replace medical advice.")

st.markdown("</div>", unsafe_allow_html=True)
