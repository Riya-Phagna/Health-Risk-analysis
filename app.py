import streamlit as st
import pickle
import numpy as np

st.markdown("""
<style>
body {
    background-color: #f5f7fb;
    font-family: 'Segoe UI', sans-serif;
}
.main {
    background-color: #ffffff;
    padding: 30px;
    border-radius: 12px;
}
h1, h2, h3 {
    color: #1f2c56;
}
.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 100%;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)



# Load model
st.set_page_config(
    page_title="Health Risk Analysis System",
    page_icon="🩺",
    layout="centered"
)
# Load trained model
with open("health_risk_model.pkl", "rb") as f:
    model = pickle.load(f)

st.markdown("""
<div style="text-align:center">
    <h1>🩺 Health Risk Analysis System</h1>
    <p style="font-size:17px;color:gray;">
        AI-powered health risk prediction using Machine Learning
    </p>
</div>
""", unsafe_allow_html=True)


# Input Card
st.markdown("### 🧾 Enter Patient Details")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age (years)", 1, 100, 30)
    bp = st.slider("Blood Pressure (mmHg)", 50, 200, 120)

with col2:
    chol = st.slider("Cholesterol (mg/dL)", 100, 350, 180)
    bmi = st.slider("BMI", 10.0, 45.0, 22.0)


# Predict Button (Centered)
predict = st.button("🔍 Predict Health Risk", use_container_width=True)

if predict:
    input_data = np.array([[age, bp, chol, bmi]])
    prediction = model.predict(input_data)[0]

    st.subheader("📊 Prediction Result")

    if prediction == 1:
        st.error("🚨 **High Health Risk Detected**")
        st.markdown(
            "⚠️ **Recommendation:** Please consult a healthcare professional immediately."
        )
    else:
        st.success("✅ **Low Health Risk Detected**")
        st.markdown(
            "🎉 **Good news!** Maintain a healthy lifestyle and regular checkups."
        )

st.markdown("### 🧠 Evidence-Based Health Guidance")

tips = research_based_suggestions(age, bp, chol, bmi)

for t in tips:
    st.write(t)

def research_based_suggestions(age, bp, chol, bmi):
    advice = []

    # Blood Pressure — AHA
    if bp >= 130:
        advice.append(
            "• Blood pressure is in the hypertensive range. "
            "According to the American Heart Association, regular exercise, "
            "reduced sodium intake, and stress management are recommended."
        )
    elif bp >= 120:
        advice.append(
            "• Blood pressure is slightly elevated. Monitoring and lifestyle control are advised."
        )

    # Cholesterol — NIH
    if chol >= 240:
        advice.append(
            "• Cholesterol level is high. NIH guidelines suggest limiting saturated fats "
            "and increasing fiber intake."
        )
    elif chol >= 200:
        advice.append(
            "• Cholesterol is borderline high. Dietary monitoring is recommended."
        )

    # BMI — WHO
    if bmi >= 30:
        advice.append(
            "• BMI falls under obesity category (WHO). Weight reduction through diet "
            "and physical activity is advised."
        )
    elif bmi >= 25:
        advice.append(
            "• BMI indicates overweight. Regular aerobic activity is recommended."
        )
    elif bmi < 18.5:
        advice.append(
            "• BMI indicates underweight. Nutritional improvement may be required."
        )

    # Normal
    if not advice:
        advice.append(
            "• All health indicators are within normal limits according to WHO and AHA guidelines."
        )

    return advice

    return tips


# Footer / Disclaimer
st.caption(
    "⚕️ *Disclaimer: This tool is for educational purposes only and should not replace professional medical advice.*"
)
