import streamlit as st
import numpy as np
import joblib
from risk_logic import assess_health_risk

# UI inputs
age = st.slider(...)
bp = st.slider(...)
chol = st.slider(...)
bmi = st.slider(...)

# button logic
if st.button("Predict Health Risk"):

    input_data = np.array([[age, bp, chol, bmi]])

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)
    risk_score = probability[0][1]





def research_based_suggestions(risk_level, bp, chol, bmi):
    suggestions = []

    if risk_level == "Low":
        suggestions = [
            "Maintain regular physical activity (WHO, 2020)",
            "Continue balanced diet with fruits & vegetables (Harvard Health)",
            "Annual health screening is recommended"
        ]

    elif risk_level == "Mild":
        suggestions = [
            "Reduce salt intake to <5g/day (WHO, 2021)",
            "Engage in at least 150 minutes of exercise/week (AHA)",
            "Monitor blood pressure monthly",
            "Limit saturated fat intake (NIH)"
        ]

    else:  # High
        suggestions = [
            "Consult a physician immediately (AHA Guidelines)",
            "Adopt DASH or Mediterranean diet (NIH)",
            "Avoid smoking & alcohol (WHO)",
            "Daily BP and cholesterol monitoring advised"
        ]

    return suggestions

# Determine risk level text



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
import numpy as np

input_data = np.array([[age, bp, chol, bmi]])


# -------------------- PREDICTION --------------------
if st.button("Predict Health Risk"):

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)
    risk_score = probability[0][1]   # probability of HIGH risk

    if risk_score < 0.4:
        risk_level = "Low"
    elif risk_score < 0.7:
        risk_level = "Mild"
    else:
        risk_level = "High"

    st.success(f"Health Risk Level: {risk_level}")




# ---------- Suggestions UI ----------
# ---------- Research-Based Health Suggestions ----------
st.markdown("## 🩺 Personalized Health Suggestions")

tips = research_based_suggestions(age, bp, chol, bmi)

if tips:
    cols = st.columns(len(tips))

    for col, tip in zip(cols, tips):
        with col:
            st.markdown(
                f"""
                <div style="
                    background-color:#f9f9f9;
                    padding:15px;
                    border-radius:12px;
                    border-left:6px solid #4CAF50;
                    box-shadow:0px 4px 8px rgba(0,0,0,0.08);
                    min-height:140px;">
                    ✅ <b>{tip}</b>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.info("No suggestions available for the given inputs.")


        
def research_based_suggestions(age, bp, chol, bmi):
    tips = []

    if bp >= 130:
        tips.append("🩸 Reduce salt intake and exercise regularly (AHA, 2022).")

    if chol >= 200:
        tips.append("🧪 Replace saturated fats with healthy fats like olive oil (Harvard).")

    if bmi >= 25:
        tips.append("⚖️ Lose 5–10% body weight to reduce heart risk (WHO).")

    if age >= 45:
        tips.append("🧓 Regular cardiovascular screening is recommended (Lancet).")

    if not tips:
        tips.append("✅ Maintain healthy lifestyle and regular checkups.")

    return tips

    # ---------------- Visual Risk Bar ----------------
    st.progress(int(max(probability) * 100))

    # ---------------- Research-Based Suggestions ----------------
    st.markdown("---")
    st.markdown("## 📚 Personalized Health Suggestions (Evidence-Based)")

    suggestions = research_based_suggestions(age, bp, chol, bmi)

    col1, col2 = st.columns(2)

    for i, tip in enumerate(suggestions):
        if i % 2 == 0:
            with col1:
                st.info(tip)
        else:
            with col2:
                st.warning(tip)

    st.caption(
        "📖 Sources: American Heart Association (2022), WHO, Harvard Medical School, The Lancet (2021)"
    )



    # -------------------- HEALTH GUIDANCE -----------------

 


# -------------------- FOOTER --------------------
st.markdown(
    "<hr><center style='color:gray;'>Developed by Riya Phagna • Streamlit ML Health App</center>",
    unsafe_allow_html=True
)

def research_based_suggestions(age, bp, chol, bmi):
    tips = []

    if bp >= 130:
        tips.append(
            "🩺 **Blood Pressure Control**: American Heart Association (2022) recommends reducing salt intake, avoiding processed food, and doing at least 150 minutes/week of moderate exercise."
        )

    if chol >= 200:
        tips.append(
            "🥗 **Cholesterol Management**: Harvard Medical School studies show replacing saturated fats with nuts, olive oil, fruits, and fish can reduce LDL cholesterol."
        )

    if bmi >= 25:
        tips.append(
            "⚖️ **Weight Management**: WHO research indicates that losing 5–10% of body weight significantly reduces cardiovascular risk."
        )

    if age >= 45:
        tips.append(
            "🧠 **Age-Based Screening**: The Lancet (2021) recommends regular cardiovascular screening after age 45 for early risk detection."
        )

    if not tips:
        tips.append(
            "✅ **Healthy Profile**: Your values are within recommended limits. Maintain physical activity, balanced diet, and regular health checkups (WHO)."
        )

    return tips

