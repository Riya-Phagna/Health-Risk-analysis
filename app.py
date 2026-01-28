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

st.markdown("---")

# Footer / Disclaimer
st.caption(
    "⚕️ *Disclaimer: This tool is for educational purposes only and should not replace professional medical advice.*"
)
