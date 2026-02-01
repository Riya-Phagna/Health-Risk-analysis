import streamlit as st
import numpy as np
import joblib

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Health Risk Analysis",
    page_icon="🩺",
    layout="wide"
)

# ------------------ LOAD MODEL ------------------
model = joblib.load("model.pkl")

# ------------------ TITLE ------------------
st.markdown(
    "<h1 style='text-align:center;'>🩺 AI-Powered Health Risk Analysis</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;color:gray;'>Machine Learning based health risk prediction</p>",
    unsafe_allow_html=True
)

st.divider()

# ------------------ INPUT UI ------------------
st.markdown("## 📋 Patient Health Details")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("🎂 Age (years)", 1, 100, 35)
    bp = st.slider("🩸 Blood Pressure (mmHg)", 80, 200, 110)

with col2:
    chol = st.slider("🧪 Cholesterol (mg/dL)", 100, 300, 200)
    bmi = st.slider("⚖️ BMI", 10.0, 45.0, 23.0)

st.divider()

# ------------------ PREDICTION ------------------
if st.button("🔍 Predict Health Risk"):

    # Prepare input
    input_data = np.array([[age, bp, chol, bmi]])

    # Model prediction
    probability = model.predict_proba(input_data)
    risk_score = probability[0][1]  # probability of higher risk

    # ------------------ RISK LEVEL LOGIC ------------------
    if risk_score < 0.33:
        risk_level = "Low"
        color = "#2ecc71"
    elif risk_score < 0.66:
        risk_level = "Mild"
        color = "#f1c40f"
    else:
        risk_level = "High"
        color = "#e74c3c"

    # ------------------ DISPLAY RESULT ------------------
    st.markdown("## 📊 Prediction Result")

    st.markdown(
        f"""
        <div style="
            background-color:{color};
            padding:20px;
            border-radius:12px;
            color:white;
            text-align:center;
            font-size:22px;
            font-weight:bold;">
            {risk_level} Health Risk<br>
            Risk Probability: {risk_score*100:.1f}%
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ------------------ RESEARCH-BASED SUGGESTIONS ------------------
    st.markdown("## 🧠 Research-Based Health Suggestions")

    if risk_level == "Low":
        tips = [
            "Maintain regular physical activity (150 min/week) — WHO 2020",
            "Continue balanced diet with fruits & vegetables — CDC",
            "Annual health screening recommended — NIH"
        ]

    elif risk_level == "Mild":
        tips = [
            "Reduce salt intake to <5g/day — WHO Hypertension Guideline",
            "Adopt DASH or Mediterranean diet — AHA",
            "Increase aerobic exercise to improve heart health — Mayo Clinic"
        ]

    else:  # High Risk
        tips = [
            "Consult a physician for cardiovascular assessment — AHA",
            "Strict cholesterol control through diet & medication — NIH",
            "Weight reduction shown to reduce BP & diabetes risk — The Lancet"
        ]

    cols = st.columns(len(tips))

    for col, tip in zip(cols, tips):
        with col:
            st.markdown(
                f"""
                <div style="
                    background-color:#f9f9f9;
                    padding:15px;
                    border-radius:12px;
                    border-left:6px solid {color};
                    box-shadow:0px 4px 8px rgba(0,0,0,0.08);
                    min-height:140px;">
                    ✅ <b>{tip}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ------------------ REFERENCES ------------------
    st.markdown("### 📚 References")
    st.markdown("""
    - World Health Organization (WHO) – Cardiovascular Disease Guidelines  
    - American Heart Association (AHA)  
    - Centers for Disease Control and Prevention (CDC)  
    - National Institutes of Health (NIH)  
    - The Lancet – Lifestyle & Cardiovascular Risk Studies  
    """)

st.divider()

st.markdown(
    "<p style='text-align:center;color:gray;'>Developed by Riya Phagna • Streamlit ML Health App</p>",
    unsafe_allow_html=True
)
