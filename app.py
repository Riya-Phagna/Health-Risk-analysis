import streamlit as st
import numpy as np
import joblib


@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()


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
st.markdown("## 🧾 Patient Health Details")

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        age = st.slider(
            "🎂 Age (years)",
            min_value=1,
            max_value=100,
            value=35,
            help="Age is a major cardiovascular risk factor (WHO, 2023)"
        )

        bp = st.slider(
            "🩸 Blood Pressure (mmHg)",
            min_value=80,
            max_value=200,
            value=120,
            help="Systolic blood pressure"
        )

    with col2:
        chol = st.slider(
            "🧪 Cholesterol (mg/dL)",
            min_value=100,
            max_value=350,
            value=200,
            help="Total cholesterol level"
        )

        bmi = st.slider(
            "⚖️ BMI",
            min_value=10.0,
            max_value=45.0,
            value=23.0,
            step=0.1,
            help="Body Mass Index"
        )

st.markdown("---")


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
  tips = research_based_suggestions(age, bp, chol, bmi)

  def research_based_suggestions(age, bp, chol, bmi):
       tips = []

    if bp >= 130:
        tips.append(
            "🩸 **Blood Pressure Control**: American Heart Association (2022) recommends reducing salt intake and doing 150 minutes/week of moderate exercise to lower BP."
        )

    if chol >= 200:
        tips.append(
            "🧪 **Cholesterol Management**: Harvard Medical School research shows replacing saturated fats with nuts, olive oil, and fish can reduce LDL cholesterol."
        )

    if bmi >= 25:
        tips.append(
            "⚖️ **Weight Management**: WHO studies indicate that losing 5–10% body weight significantly reduces cardiovascular risk."
        )

    if age >= 45:
        tips.append(
            "🧓 **Age-Based Screening**: The Lancet (2021) recommends regular cardiovascular screening after age 45."
        )

    if not tips:
        tips.append(
            "✅ **Healthy Profile**: Your values are within recommended limits. Maintain physical activity, balanced diet, and regular health checkups (WHO)."
        )

    return tips



# -------------------- FOOTER --------------------
st.markdown(
    "<hr><center style='color:gray;'>Developed by Riya Phagna • Streamlit ML Health App</center>",
    unsafe_allow_html=True
)
