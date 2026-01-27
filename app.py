import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Health Risk Analysis", layout="centered")

# Load model
with open("health_risk_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("🩺 Health Risk Analysis System")
st.write("AI-based preliminary health risk prediction")

# Inputs
age = st.number_input("Age", min_value=1, max_value=120, value=30)
bp = st.number_input("Blood Pressure", min_value=50.0, max_value=200.0, value=120.0)
chol = st.number_input("Cholesterol Level", min_value=100.0, max_value=400.0, value=180.0)
bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=22.0)

# Prediction
if st.button("Predict Risk"):
    input_data = np.array([[age, bp, chol, bmi]])  # 🔥 4 FEATURES
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error("⚠️ High Health Risk Detected")
    else:
        st.success("✅ Low Health Risk")
