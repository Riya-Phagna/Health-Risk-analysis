import streamlit as st
import numpy as np
import pickle

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Health Risk Analysis",
    page_icon="🩺",
    layout="centered"
)

import streamlit as st
import pickle

@st.cache_resource
def load_model_safe():
    try:
        with open("model.pkl", "rb") as f:
            return pickle.load(f), "ml"
    except Exception:
        return None, "rule"

model, model_mode = load_model_safe()


# ---------------- RULE-BASED FALLBACK ----------------
def rule_based_risk(bmi, cholesterol):
    if bmi >= 30 or cholesterol >= 240:
        return "High Risk"
    elif bmi >= 25 or cholesterol >= 200:
        return "Medium Risk"
    else:
        return "Low Risk"

# ---------------- UI ----------------



# ---------------- UI ----------------
st.title("🩺 AI-powered Health Risk Prediction")
st.caption("Hybrid ML + Clinical Rule Based Assessment")

st.markdown("## 📋 Patient Health Details")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("🧓 Age (years)", 18, 80, 35)
    bp = st.slider("🩸 Blood Pressure (mmHg)", 80, 200, 120)

with col2:
    chol = st.slider("🧪 Cholesterol (mg/dL)", 100, 350, 180)
    bmi = st.slider("⚖️ BMI", 12.0, 45.0, 23.0)

# ---------------- Hybrid Risk Logic ----------------
def assess_risk(age, bp, chol, bmi):
    """
    Hybrid logic:
    - Clinical risk points → Risk Level
    - ML model → Confidence score
    """

    # ----- Clinical Risk Scoring -----
    risk_points = 0

    if bp >= 130:
        risk_points += 1
    if chol >= 200:
        risk_points += 1
    if bmi >= 25:
        risk_points += 1
    if age >= 45:
        risk_points += 1

    # ----- Risk Level -----
    if risk_points <= 1:
        risk_level = "Low"
        color = "#2ecc71"
    elif risk_points == 2:
        risk_level = "Mild"
        color = "#f39c12"
    else:
        risk_level = "High"
        color = "#e74c3c"

    # ----- ML Probability (Confidence only) -----
    input_data = np.array([[age, bp, chol, bmi]])
    prob = model.predict_proba(input_data)[0][1]
    confidence = round(prob * 100, 2)

    return risk_level, confidence, color, risk_points

# ---------------- Research-Based Suggestions ----------------
def research_based_suggestions(risk_level):
    if risk_level == "Low":
        return [
            "🟢 **Healthy Lifestyle Maintenance** — WHO (2022): Continue regular physical activity (150 min/week) and balanced diet.",
            "🥗 **Preventive Nutrition** — Harvard T.H. Chan: High fiber & fruits reduce long-term cardiovascular risk.",
            "🩺 **Routine Screening** — CDC: Annual BP & cholesterol checks recommended."
        ]

    elif risk_level == "Mild":
        return [
            "🟡 **Early Cardiovascular Prevention** — American Heart Association (2021): Reduce sodium & increase aerobic exercise.",
            "🥑 **Dietary Fat Modification** — Harvard Medical School: Replace saturated fats with olive oil, nuts, and fish.",
            "📉 **Weight Control** — WHO: 5–10% weight reduction lowers cardiometabolic risk."
        ]

    else:  # High Risk
        return [
            "🔴 **Clinical Intervention Required** — The Lancet (2020): High BP & cholesterol require medical supervision.",
            "💊 **Medication + Lifestyle** — American College of Cardiology: Combined therapy significantly reduces heart events.",
            "🚭 **Risk Factor Elimination** — NIH: Smoking cessation & stress control dramatically lower mortality."
        ]

# ---------------- Prediction ----------------
if st.button("🔍 Predict Health Risk"):
    risk_level, confidence, color, points = assess_risk(age, bp, chol, bmi)

    st.markdown("## 📊 Prediction Result")

    st.markdown(
        f"""
        <div style="
            background-color:{color};
            padding:18px;
            border-radius:14px;
            color:white;
            font-size:20px;
            text-align:center;
            font-weight:bold;">
            {risk_level} Health Risk
            <br>
            <span style="font-size:14px;">ML Confidence: {confidence}%</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 🩺 Personalized Health Suggestions")

    tips = research_based_suggestions(risk_level)
    cols = st.columns(len(tips))

    for col, tip in zip(cols, tips):
        with col:
            st.markdown(
                f"""
                <div style="
                    background:#f9f9f9;
                    padding:15px;
                    border-radius:12px;
                    border-left:6px solid {color};
                    box-shadow:0px 4px 8px rgba(0,0,0,0.08);
                    min-height:160px;">
                    {tip}
                </div>
                """,
                unsafe_allow_html=True
            )

# ---------------- Footer ----------------
st.markdown("---")
st.caption("Developed by Riya Phagna • Streamlit ML Health App")
