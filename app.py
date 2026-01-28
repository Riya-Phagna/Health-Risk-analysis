import streamlit as st
import pickle
import numpy as np

# Load model
st.set_page_config(
    page_title="Health Risk Analysis System",
    page_icon="🩺",
    layout="centered"
)
# Load trained model
with open("health_risk_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("🫀 Health Risk Analysis System")
st.caption("AI-powered health risk prediction using Decision Tree")

st.markdown("---")

# Input Card
st.subheader("📋 Enter Patient Details")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age (years)", min_value=1, max_value=120, value=30)
    bp = st.number_input("Blood Pressure (mmHg)", min_value=50, max_value=200, value=120)

with col2:
    chol = st.number_input("Cholesterol Level (mg/dL)", min_value=100, max_value=400, value=180)
    bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=22.5)

st.markdown("---")

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

st.markdown("---")

# Footer / Disclaimer
st.caption(
    "⚕️ *Disclaimer: This tool is for educational purposes only and should not replace professional medical advice.*"
)
