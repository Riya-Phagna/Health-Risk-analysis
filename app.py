import streamlit as st
import numpy as np
import pickle

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="AI-powered Health Risk Prediction",
    layout="centered"
)

st.title("🩺 AI-powered Health Risk Prediction using Machine Learning")

# --------------------------------------------------
# Safe model loading (OPTIONAL – app works without it)
# --------------------------------------------------
@st.cache_resource
def load_model():
    try:
        with open("model.pkl", "rb") as f:
            return pickle.load(f)
    except Exception:
        return None  # fallback to rule-based logic

model = load_model()

# --------------------------------------------------
# HYBRID RISK ASSESSMENT FUNCTION
# --------------------------------------------------
def assess_risk(age, bp, chol, bmi):
    """
    Hybrid logic:
    - Rule-based medical scoring (primary)
    - ML probability (secondary, optional)
    """

    score = 0

    # ---- AGE ----
    if age >= 60:
        score += 2
    elif age >= 45:
        score += 1

    # ---- BLOOD PRESSURE (Systolic) ----
    if bp >= 140:
        score += 3
    elif bp >= 130:
        score += 2
    elif bp >= 120:
        score += 1

    # ---- CHOLESTEROL ----
    if chol >= 240:
        score += 3
    elif chol >= 200:
        score += 2
    elif chol >= 180:
        score += 1

    # ---- BMI ----
    if bmi >= 30:
        score += 3
    elif bmi >= 25:
        score += 2
    elif bmi >= 23:
        score += 1

    # --------------------------------------------------
    # ML probability (if model exists)
    # --------------------------------------------------
    ml_prob = 0.0
    if model is not None:
        try:
            input_data = np.array([[age, bp, chol, bmi]])
            ml_prob = model.predict_proba(input_data)[0][1]  # risk class
        except Exception:
            ml_prob = 0.0

    # --------------------------------------------------
    # FINAL HYBRID DECISION
    # --------------------------------------------------
    if score >= 7 or ml_prob >= 0.65:
        risk_level = "HIGH"
        color = "red"
    elif score >= 4 or ml_prob >= 0.35:
        risk_level = "MODERATE"
        color = "orange"
    else:
        risk_level = "LOW"
        color = "green"

    confidence = round(max(score / 10, ml_prob) * 100, 1)

    return risk_level, confidence, color, score

# --------------------------------------------------
# UI INPUTS
# --------------------------------------------------
st.header("📋 Patient Health Details")

age = st.slider("Age (years)", 18, 80, 35)
chol = st.slider("Cholesterol (mg/dL)", 120, 320, 180)
bp = st.slider("Blood Pressure – Systolic (mmHg)", 90, 200, 120)
bmi = st.slider("BMI", 15.0, 40.0, 23.0)

# --------------------------------------------------
# PREDICTION BUTTON
# --------------------------------------------------
if st.button("🔍 Predict Health Risk"):
    risk, confidence, color, score = assess_risk(age, bp, chol, bmi)

    st.markdown(
        f"""
        ### 🧠 Risk Level: <span style="color:{color}">{risk}</span>
        **Confidence:** {confidence}%  
        **Risk Score:** {score}/10
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # --------------------------------------------------
    # RESEARCH-BASED SUGGESTIONS
    # --------------------------------------------------
    if risk == "LOW":
        st.success("🟢 Low Health Risk")

        st.markdown("""
**Recommendations (Preventive Care):**
- Maintain balanced diet (WHO dietary guidelines)
- 150 minutes/week of moderate exercise (WHO, 2020)
- Annual BP & cholesterol screening
- Maintain BMI between 18.5–24.9

📚 *Sources:*  
WHO Physical Activity Guidelines, 2020  
NIH Preventive Health Reports
""")

    elif risk == "MODERATE":
        st.warning("🟡 Moderate Health Risk")

        st.markdown("""
**Recommendations (Risk Reduction):**
- DASH or Mediterranean diet (AHA, 2019)
- Reduce sodium intake (<1500 mg/day)
- Weight reduction of 5–7% if overweight
- BP & lipid monitoring every 6 months

📚 *Sources:*  
American Heart Association (AHA)  
NEJM – Lifestyle Interventions & CVD Risk
""")

    else:
        st.error("🔴 High Health Risk")

        st.markdown("""
**Recommendations (Clinical Attention Required):**
- Consult physician / cardiologist
- Possible pharmacological intervention
- Strict BP & lipid management
- Supervised physical activity plan

📚 *Sources:*  
ACC/AHA Hypertension Guidelines  
The Lancet – Cardiovascular Risk Management
""")

    st.info("⚠️ This tool is for educational purposes only and not a medical diagnosis.")
