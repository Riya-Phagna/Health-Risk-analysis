import streamlit as st
import pickle
import numpy as np

# Load model

with open("health_risk_model.pkl", "rb") as f:
    model = pickle.load(f)


st.set_page_config(page_title="Health Risk Analysis", layout="centered")

st.title("🩺 Health Risk Analysis System")
st.caption("AI-based preliminary health risk prediction")

age = st.number_input("Age", min_value=1, max_value=120)
bp = st.number_input("Blood Pressure")
chol = st.number_input("Cholesterol Level")

if st.button("Predict Risk"):
    input_data = np.array([[age, bp, chol]])
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error("⚠️ High Health Risk Detected")
    else:
        st.success("✅ Low Health Risk")

st.divider()
st.caption("⚠️ For educational purposes only")
