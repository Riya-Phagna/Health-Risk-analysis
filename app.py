import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Health Risk Analysis", layout="centered")

# Load model
st.set_page_config(
    page_title="Health Risk Analysis System",
    page_icon="🩺",
    layout="centered"
)

st.markdown(
    """
    <h1 style='text-align: center;'>🩺 Health Risk Analysis System</h1>
    <p style='text-align: center; color: grey;'>
    AI-based preliminary health risk prediction
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

st.subheader("📋 Enter Patient Details")

age = st.number_input("Age (years)", min_value=1, max_value=120, step=1)
bp = st.number_input("Blood Pressure (mmHg)", min_value=50, max_value=250)
chol = st.number_input("Cholesterol Level (mg/dL)", min_value=100, max_value=400)
bmi = st.number_input("BMI", min_value=10.0, max_value=50.0)

st.divider()

if st.button("🔍 Predict Health Risk"):
    input_data = np.array([[age, bp, chol, bmi]])
    prediction = model.predict(input_data)[0]

    st.subheader("📊 Prediction Result")

    if prediction == 1:
        st.error("🚨 **High Health Risk Detected**")
        st.info("Please consult a healthcare professional.")
    else:
        st.success("✅ **Low Health Risk**")
        st.info("Maintain a healthy lifestyle.")

st.divider()
st.caption("⚠️ For educational purposes only. Not a medical diagnosis.")
