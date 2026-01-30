import streamlit as st
import numpy as np
import joblib

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Health Risk Analysis System",
    page_icon="🩺",
    layout="centered"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
    body {
        background-color: #f7f9fc;
    }

    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: 700;
        color: #1f2937;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 30px;
    }

    .card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }

    .risk-high {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 20px;
        border-radius: 12px;
        font-size: 20px;
        font-weight: bold;
    }

    .risk-low {
        background-color: #dcfce7;
        color: #065f46;
        padding: 20px;
        border-radius: 12px;
        font-size: 20px;
        font-weight: bold;
    }

    .tip-box {
        background-color: #f0f9ff;
        padding: 18px;
        border-left: 6px solid #0284c7;
        border-radius: 10px;
        margin-bottom: 12px;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- LOAD MODEL --------------------
model = joblib.load("model.pkl")

# -------------------- TITLE --------------------
st.markdown("<div class='main-title'>🩺 Health Risk Analysis System</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-powered health risk prediction using Machine Learning</div>", unsafe_allow_html=True)

# -------------------- INPUT CARD --------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📋 Enter Patient Details")

age = st.slider("Age (years)", 1, 100, 30)
bp = st.slider("Blood Pressure (mmHg)", 60, 200, 120)
chol = st.slider("Cholesterol (mg/dL)", 100, 350, 200)
bmi = st.slider("BMI", 10.0, 45.0, 24.0)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------- PREDICTION --------------------
if st.button("🔍 Predict Health Risk", use_container_width=True):

    input_data = np.array([[age, bp, chol, bmi]])
    prediction = model.predict(input_data)[0]

    # Probability
    prob = model.predict_proba(input_data)[0]
    risk_percent = int(max(prob) * 100)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Prediction Result")

    st.progress(risk_percent)

    if prediction == 1:
        st.markdown(
            f"<div class='risk-high'>🚨 High Health Risk Detected ({risk_percent}%)</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='risk-low'>✅ Low Health Risk ({risk_percent}%)</div>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------- HEALTH GUIDANCE --------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧠 Evidence-Based Health Guidance")

    tips = []

    if bp > 130:
        tips.append("🫀 Reduce salt intake and monitor blood pressure regularly.")

    if chol > 200:
        tips.append("🥗 Follow a low-cholesterol diet (less fried food, more fiber).")

    if bmi > 25:
        tips.append("🏃 Aim for at least 30 minutes of exercise daily.")

    if age > 45:
        tips.append("🩺 Schedule routine health checkups every 6 months.")

    tips.append("💤 Maintain 7–8 hours of quality sleep.")
    tips.append("🚭 Avoid smoking and limit alcohol consumption.")
    tips.append("💧 Drink adequate water daily.")

    for tip in tips:
        st.markdown(f"<div class='tip-box'>{tip}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- FOOTER --------------------
st.markdown(
    "<hr><center style='color:gray;'>Developed by Riya Phagna • Streamlit ML Health App</center>",
    unsafe_allow_html=True
)
