import numpy as np
import pickle
from datetime import datetime, timedelta
import pandas as pd
import json
from pathlib import Path
import os
import streamlit as st
import ollama
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import sqlite3
import requests
from urllib.parse import quote
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from datetime import datetime
from PIL import Image
import streamlit as st

import urllib.parse
CLIENT_ID = "23V288"
CLIENT_SECRET = "65024027d5fbfc604e53f9c12d097c8c"
REDIRECT_URI = "http://localhost:8501"



def get_db():
    conn = sqlite3.connect("users.db", check_same_thread=False)
    return conn

conn = get_db()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
""")
conn.commit()
import streamlit as st
# Initialize session variable
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# ===============================
# LOGIN PAGE
# ===============================
# ================= LOGIN PAGE =================
import base64
from pathlib import Path

# ---------- helper to load background ----------
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

# ---------- login check ----------
if not st.session_state.get("logged_in", False):

    # ====== LOAD BACKGROUND IMAGE ======
    img_path = Path("assets/healnet_login.jfif")  # your file name
    img_base64 = get_base64_image(img_path)

    if img_base64:
        st.markdown(f"""
        <style>
        .stApp {{
            background: url("data:image/jfif;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* glass login card */
        .login-card {{
            background: rgba(255,255,255,0.12);
            backdrop-filter: blur(14px);
            padding: 40px;
            border-radius: 20px;
            width: 400px;
            margin: auto;
            margin-top: 80px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.25);
        }}

        .login-title {{
            text-align: center;
            color: white;
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 25px;
        }}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Login image not found in assets folder")

    # ====== LOGIN CARD START ======
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔐 HealNet Login</div>', unsafe_allow_html=True)

    name = st.text_input("Username *", key="login_fullname")
    email = st.text_input("Email ID *", key="login_email")

    login_btn = st.button("Login", use_container_width=True)

    if login_btn:
        if not name.strip():
            st.error("Name is required")
        elif not email.strip():
            st.error("Email is required")
        else:
            try:
                cursor.execute(
                    "INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)",
                    (name, email)
                )
                conn.commit()

                st.session_state["logged_in"] = True
                st.session_state["user_name"] = name
                st.rerun()

            except Exception:
                st.error("Login failed")

    st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

st.markdown("""
<style>

/* ===== Fix grey text visibility ===== */
body, .stApp {
    color: white !important;
}

/* labels, help text, captions */
label, .stMarkdown, .stText, .stCaption {
    color: white !important;
}

/* metric labels */
[data-testid="stMetricLabel"] {
    color: white !important;
}

/* sidebar text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* expander + radio + select text */
.stRadio label,
.stSelectbox label,
.stSlider label,
.stTextInput label {
    color: white !important;
}

/* small grey helper text */
small, span {
    color: #E5E7EB !important;
}

</style>
""", unsafe_allow_html=True)
# PAGE CONFIG
# =====================================================



# symptom database
SYMPTOM_DB = {
    "fever": ["Flu", "COVID-19", "Malaria"],
    "cough": ["Common Cold", "Flu", "Bronchitis"],
    "headache": ["Migraine", "Stress", "Hypertension"],
    "chest pain": ["Heart Disease", "Anxiety", "Acid Reflux"],
    "fatigue": ["Anemia", "Diabetes", "Depression"],
    "shortness of breath": ["Asthma", "Heart Disease", "COVID-19"],
}

def analyze_symptoms(symptom_text):
    symptom_text = symptom_text.lower()
    scores = {}

    for symptom, conditions in SYMPTOM_DB.items():
        if symptom in symptom_text:
            for condition in conditions:
                scores[condition] = scores.get(condition, 0) + 1

    if not scores:
        return {}

    total = sum(scores.values())
    return {k: round((v / total) * 100, 2) for k, v in scores.items()}
def predict_future(values, months):
    X = np.array(range(len(values))).reshape(-1, 1)
    y = np.array(values)

    model = LinearRegression()
    model.fit(X, y)

    future_X = np.array(
        range(len(values), len(values) + len(months))
    ).reshape(-1, 1)

    predictions = model.predict(future_X)
    return predictions



# ================================================
# PAGE CONFIGURATION
# ================================================
st.set_page_config(
    page_title="HealNet - Predict. Prevent. Personalize.",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* Make all labels white */
label {
    color: #FFFFFF !important;
    font-weight: 500;
}

/* Slider labels */
.stSlider label {
    color: #FFFFFF !important;
}

/* Number input labels */
.stNumberInput label {
    color: #FFFFFF !important;
}

/* Selectbox labels */
.stSelectbox label {
    color: #FFFFFF !important;
}

/* Improve small helper text */
.css-1cpxqw2, .css-10trblm {
    color: #E2E8F0 !important;
}

/* Fix metric titles */
[data-testid="stMetricLabel"] {
    color: #FFFFFF !important;
}



</style>
""", unsafe_allow_html=True)
    

# ================================================
# PROFESSIONAL STYLING
# ================================================
st.markdown("""
<style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root Variables */
    :root {
        --primary-color: #2D5BFF;
        --secondary-color: #00D9C0;
        --accent-color: #FF6B9D;
        --dark-bg: #0A0E27;
        --card-bg: #141B3D;
        --text-primary: #FFFFFF;
        --text-secondary: #A0AEC0;
        --success-color: #00D9C0;
        --warning-color: #FFB800;
        --danger-color: #FF4757;
        --gradient-1: linear-gradient(135deg, #2D5BFF 0%, #00D9C0 100%);
        --gradient-2: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-3: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    
    
  
    
    /* ===== CRITICAL: FORCE TEXT VISIBILITY IN ALL COMPONENTS ===== */
    
    /* Metric boxes - force visible text */
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricDelta"] {
        color: #FFFFFF !important;
    }
    
    /* Info/Success/Warning/Error boxes - black text on light background */
    .stAlert {
        color: #000000 !important;
    }
    
    .stAlert > div,
    .stAlert > div > div,
    .stAlert p,
    .stAlert span {
        color: #000000 !important;
    }
    
    /* Dataframe text - black on white */
    .stDataFrame,
    .stDataFrame *,
    [data-testid="stDataFrame"] * {
        color: #000000 !important;
    }
    
    
   
    
    .stSelectbox [data-baseweb="select"] div {
        color: #FFFFFF !important;
    }
    
    /* File uploader */
    .stFileUploader {
        background-color: rgba(255,255,255,0.05) !important;
    }
    
    .stFileUploader label,
    .stFileUploader div {
        color: #FFFFFF !important;
    }
    
    /* Custom colored boxes - force black text */
    div[style*="background-color:#f0f2f6"],
    div[style*="background-color:#f0f2f6"] *,
    div[style*="background: linear-gradient(135deg, #f093fb"],
    div[style*="background: linear-gradient(135deg, #4facfe"],
    div[style*="background: linear-gradient(135deg, #a8edea"] {
        color: #000000 !important;
    }
    
    /* Wearable cards text override */
    div[style*="background: linear-gradient(135deg, #f093fb"] div,
    div[style*="background: linear-gradient(135deg, #4facfe"] div,
    div[style*="background: linear-gradient(135deg, #a8edea"] div {
        color: #FFFFFF !important;
    }
    
    /* Sleep card specifically (light background) */
    div[style*="background: linear-gradient(135deg, #a8edea"] div {
        color: #2D3748 !important;
    }
    
    /* Hero Section */
    .hero-section {
        background: var(--gradient-1);
        padding: 3rem 2rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(45, 91, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 8s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1) rotate(0deg); }
        50% { transform: scale(1.1) rotate(180deg); }
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    .logo {
        font-family: 'Sora', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin: 0;
        letter-spacing: -0.02em;
        text-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    .tagline {
        font-family: 'Sora', sans-serif;
        font-size: 1.3rem;
        font-weight: 300;
        color: rgba(255,255,255,0.95);
        margin: 0.5rem 0 0 0;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }
    
    .company {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.8);
        margin-top: 1rem;
        font-weight: 500;
    }
    
    /* Card Styles */
    .metric-card {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-1);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(45, 91, 255, 0.4);
    }
    
    .metric-title {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'Sora', sans-serif;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-subtitle {
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
    }
    
    /* Risk Assessment Cards */
    .risk-card {
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .risk-low {
        background: linear-gradient(135deg, rgba(0, 217, 192, 0.15) 0%, rgba(0, 217, 192, 0.05) 100%);
        border: 2px solid var(--success-color);
    }
    
    .risk-moderate {
        background: linear-gradient(135deg, rgba(255, 184, 0, 0.15) 0%, rgba(255, 184, 0, 0.05) 100%);
        border: 2px solid var(--warning-color);
    }
    
    .risk-high {
        background: linear-gradient(135deg, rgba(255, 71, 87, 0.15) 0%, rgba(255, 71, 87, 0.05) 100%);
        border: 2px solid var(--danger-color);
    }
    
    .risk-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .risk-title {
        font-family: 'Sora', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: var(--text-primary);
    }
    
    .risk-description {
        font-size: 1.1rem;
        color: var(--text-secondary);
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    
    /* Recommendation List */
    .recommendation-list {
        list-style: none;
        padding: 0;
        margin: 1.5rem 0;
    }
    
    .recommendation-list li {
        padding: 1rem;
        margin: 0.8rem 0;
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        border-left: 4px solid var(--primary-color);
        color: var(--text-primary);
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .recommendation-list li:hover {
        background: rgba(255,255,255,0.08);
        transform: translateX(5px);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: var(--gradient-1);
        color: white;
        border: none;
        padding: 1.2rem 2rem;
        border-radius: 16px;
        font-size: 1.1rem;
        font-weight: 700;
        font-family: 'Sora', sans-serif;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(45, 91, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(45, 91, 255, 0.5);
    }
    
    /* Input Styling */
    .stSlider {
        padding: 1rem 0;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--dark-bg) 0%, var(--card-bg) 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: var(--text-primary);
    }
    
    /* Feature Cards in Sidebar */
    .feature-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.05);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: var(--primary-color);
        box-shadow: 0 8px 30px rgba(45, 91, 255, 0.2);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-family: 'Sora', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        font-size: 0.9rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }
    
    /* Progress Bar */
    .progress-container {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        height: 12px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 100%;
        background: var(--gradient-1);
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-item {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.05);
        text-align: center;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        font-family: 'Sora', sans-serif;
        color: var(--primary-color);
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: var(--card-bg);
        padding: 1rem;
        border-radius: 16px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary);
        font-weight: 600;
        font-size: 1rem;
        padding: 1rem 1.5rem;
        border-radius: 12px;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--gradient-1);
        color: white;
    }
    
    /* Alert Boxes */
    .custom-alert {
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        border-left: 4px solid;
        background: rgba(255,255,255,0.03);
    }
    
    .alert-info {
        border-color: var(--primary-color);
    }
    
    .alert-success {
        border-color: var(--success-color);
    }
    
    .alert-warning {
        border-color: var(--warning-color);
    }
    
    .alert-danger {
        border-color: var(--danger-color);
    }
    
    /* Timeline */
    .timeline {
        position: relative;
        padding: 2rem 0;
    }
    
    .timeline-item {
        position: relative;
        padding-left: 3rem;
        padding-bottom: 2rem;
        border-left: 2px solid rgba(255,255,255,0.1);
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 0;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: var(--primary-color);
        box-shadow: 0 0 20px rgba(45, 91, 255, 0.5);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 3rem 0;
        color: var(--text-secondary);
        font-size: 0.9rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        margin-top: 4rem;
    }
    
    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
        color: var(--primary-color);
    }
    
    /* Loading Animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top-color: var(--primary-color);
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Input Labels - Black */
    label[data-testid="stWidgetLabel"] {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* Slider values - white */
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"],
    .stSlider [data-testid="stThumbValue"] {
        color: #FFFFFF !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .logo {
            font-size: 2.5rem;
        }
        
        .tagline {
            font-size: 1rem;
        }
        
        .stats-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* ===== SELECTBOX MAIN BOX ===== */
.stSelectbox [data-baseweb="select"] > div {
    background-color: white !important;
    color: black !important;
}

/* Selected value text */
.stSelectbox [data-baseweb="select"] span {
    color: black !important;
}

/* ===== DROPDOWN MENU (Portal Layer Fix) ===== */
div[data-baseweb="menu"] {
    background-color: white !important;
}

div[data-baseweb="menu"] div {
    color: black !important;
}

/* Hover effect */
div[data-baseweb="menu"] div:hover {
    background-color: #E2E8F0 !important;
    color: black !important;
}

</style>
""", unsafe_allow_html=True)

# ================================================
# DATA PERSISTENCE (Session State)
# ================================================
if 'health_history' not in st.session_state:
    st.session_state.health_history = []

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'name': '',
        'age': 35,
        'gender': 'Select',
        'height': 170,
        'weight': 70
    }

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# ================================================
# MODEL LOADING
# ================================================
@st.cache_resource
def load_model():
    try:
        with open("model.pkl", "rb") as file:
            return pickle.load(file)
    except:
        return None

model = load_model()

# ================================================
# UTILITY FUNCTIONS
# ================================================
def calculate_bmi(weight, height):
    """Calculate bmi from weight (kg) and height (cm)"""
    height_m = height / 100
    return weight / (height_m ** 2)

def show_loading_animation(message="Analyzing..."):
    """Display a professional loading animation"""
    return st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: center; padding: 2rem;">
        <div class="loading"></div>
        <span style="margin-left: 1rem; color: var(--text-primary); font-weight: 600;">
            {message}
        </span>
    </div>
    """, unsafe_allow_html=True)

# ================================================
# ADVANCED RISK ASSESSMENT WITH ML
# ================================================
def assess_risk(age, bp, chol, bmi, gender="Select"):
    """Enhanced risk assessment with multiple factors"""
    score = 0
    risk_factors = []
    
    # Age factor
    if age >= 60:
        score += 2
        risk_factors.append("Advanced age (60+)")
    elif age >= 45:
        score += 1
        risk_factors.append("Middle age (45-59)")
    
    # Blood pressure factor (Systolic)
    if bp >= 180:
        score += 4
        risk_factors.append("Stage 2 Hypertension (BP ≥ 180)")
    elif bp >= 140:
        score += 3
        risk_factors.append("Stage 1 Hypertension (BP 140-179)")
    elif bp >= 130:
        score += 2
        risk_factors.append("Elevated BP (130-139)")
    elif bp >= 120:
        score += 1
        risk_factors.append("Pre-hypertension (120-129)")
    
    # chol factor
    if chol >= 240:
        score += 3
        risk_factors.append("High cholesterol (≥ 240 mg/dL)")
    elif chol >= 200:
        score += 2
        risk_factors.append("Borderline high cholesterol (200-239 mg/dL)")
    elif chol >= 180:
        score += 1
        risk_factors.append("Slightly elevated cholesterol")
    
    # bmi factor
    if bmi >= 35:
        score += 4
        risk_factors.append("Obesity Class II (bmi ≥ 35)")
    elif bmi >= 30:
        score += 3
        risk_factors.append("Obesity Class I (bmi 30-34.9)")
    elif bmi >= 25:
        score += 2
        risk_factors.append("Overweight (bmi 25-29.9)")
    elif bmi >= 23:
        score += 1
        risk_factors.append("Upper normal bmi")
    
    # Gender factor (men have slightly higher cardiovascular risk)
    if gender == "Male" and age >= 45:
        score += 0.5
    
    # ML probability (if model is available)
    ml_prob = 0
    ml_confidence = "N/A"
    
    if model is not None:
        try:
            ml_prob = model.predict_proba(
                np.array([[age, bp, chol, bmi]])
            )[0][1]
            ml_confidence = f"{ml_prob*100:.1f}%"
        except:
            ml_prob = 0
            ml_confidence = "Model Error"
    
    # Final risk decision (hybrid approach)
    if score >= 8 or ml_prob >= 0.70:
        risk_level = "High"
        risk_percentage = max(score * 8.5, ml_prob * 100)
    elif score >= 5 or ml_prob >= 0.40:
        risk_level = "Moderate"
        risk_percentage = max(score * 7.5, ml_prob * 100)
    else:
        risk_level = "Low"
        risk_percentage = max(score * 6, ml_prob * 100)
    
    risk_percentage = min(risk_percentage, 95)  # Cap at 95%
    
    return {
        'level': risk_level,
        'score': score,
        'percentage': risk_percentage,
        'ml_probability': ml_confidence,
        'factors': risk_factors
    }

# ================================================
# PERSONALIZED RECOMMENDATIONS
# ================================================
def get_recommendations(risk_data, age, bp, chol, bmi):
    """Generate personalized health recommendations"""
    recommendations = {
        'immediate': [],
        'lifestyle': [],
        'dietary': [],
        'exercise': [],
        'monitoring': []
    }
    
    risk_level = risk_data['level']
    
    # Immediate Actions
    if risk_level == "High":
        recommendations['immediate'] = [
            "🏥 Schedule an appointment with your healthcare provider within 48 hours",
            "💊 Discuss medication options with your doctor",
            "📊 Request comprehensive cardiovascular screening",
            "🚨 Monitor symptoms daily and seek emergency care if needed"
        ]
    elif risk_level == "Moderate":
        recommendations['immediate'] = [
            "👨‍⚕️ Schedule a medical consultation within 2 weeks",
            "📋 Get a full health panel including lipid profile",
            "📱 Start tracking daily health metrics"
        ]
    else:
        recommendations['immediate'] = [
            "✅ Maintain regular annual checkups",
            "📊 Continue monitoring health parameters quarterly"
        ]
    
    # Lifestyle Recommendations
    if bp >= 140:
        recommendations['lifestyle'].append("🧘 Practice stress reduction techniques (meditation, yoga)")
        recommendations['lifestyle'].append("😴 Ensure 7-8 hours of quality sleep per night")
        recommendations['lifestyle'].append("🚭 Avoid tobacco and limit alcohol consumption")
    
    if bmi >= 25:
        recommendations['lifestyle'].append("⚖️ Aim for gradual weight loss (0.5-1 kg per week)")
        recommendations['lifestyle'].append("🎯 Set realistic weight goals with professional guidance")
    
    recommendations['lifestyle'].append("💧 Stay well-hydrated (8-10 glasses of water daily)")
    
    # Dietary Recommendations
    if chol >= 200:
        recommendations['dietary'].extend([
            "🥗 Increase fiber intake (oats, beans, fruits, vegetables)",
            "🐟 Include omega-3 rich foods (salmon, mackerel, walnuts)",
            "🚫 Limit saturated fats and trans fats",
            "🥑 Choose healthy fats (olive oil, avocados, nuts)"
        ])
    
    if bp >= 130:
        recommendations['dietary'].extend([
            "🧂 Reduce sodium intake to less than 2,300 mg per day",
            "🍌 Increase potassium-rich foods (bananas, spinach, sweet potatoes)",
            "🥬 Follow DASH diet principles"
        ])
    
    recommendations['dietary'].append("🍎 Eat a variety of colorful fruits and vegetables")
    recommendations['dietary'].append("🍗 Choose lean proteins and limit red meat")
    
    # Exercise Recommendations
    if risk_level == "High":
        recommendations['exercise'].extend([
            "🚶 Start with gentle walking (10-15 minutes daily)",
            "👨‍⚕️ Consult doctor before beginning any exercise program",
            "📈 Gradually increase activity as approved by healthcare provider"
        ])
    elif risk_level == "Moderate":
        recommendations['exercise'].extend([
            "🏃 Aim for 30 minutes of moderate activity 5 days per week",
            "💪 Include strength training 2-3 times per week",
            "🚴 Try various activities: walking, cycling, swimming"
        ])
    else:
        recommendations['exercise'].extend([
            "🏋️ Maintain 150+ minutes of moderate exercise weekly",
            "🏃‍♂️ Include both cardio and strength training",
            "🧘 Add flexibility and balance exercises"
        ])
    
    # Monitoring Recommendations
    if bp >= 130:
        recommendations['monitoring'].append("🩺 Check blood pressure weekly at home")
    
    if chol >= 200:
        recommendations['monitoring'].append("🧪 Monitor cholesterol levels every 3 months")
    
    if bmi >= 25:
        recommendations['monitoring'].append("⚖️ Track weight weekly")
    
    recommendations['monitoring'].append("📱 Use health tracking apps to log progress")
    recommendations['monitoring'].append("📊 Keep a health journal")
    
    return recommendations

# ================================================
# HEALTH INSIGHTS & ANALYTICS
# ================================================
def generate_health_insights(risk_data, age, bp, chol, bmi):
    """Generate detailed health insights"""
    insights = []
    
    # bmi Category
    if bmi < 18.5:
        bmi_category = "Underweight"
        bmi_advice = "Consider consulting a nutritionist to achieve a healthy weight."
    elif bmi < 25:
        bmi_category = "Normal Weight"
        bmi_advice = "Excellent! Maintain your current healthy weight."
    elif bmi < 30:
        bmi_category = "Overweight"
        bmi_advice = "Focus on balanced nutrition and regular physical activity."
    elif bmi < 35:
        bmi_category = "Obese (Class I)"
        bmi_advice = "Medical supervision recommended for weight management."
    else:
        bmi_category = "Obese (Class II)"
        bmi_advice = "Urgent medical attention advised for comprehensive weight management."
    
    insights.append({
        'title': 'Body Mass Index',
        'value': f"{bmi:.1f}",
        'category': bmi_category,
        'advice': bmi_advice
    })
    
    # bp Category
    if bp < 120:
        bp_category = "Normal"
        bp_advice = "Your blood pressure is in the optimal range."
    elif bp < 130:
        bp_category = "Elevated"
        bp_advice = "Lifestyle changes can help prevent hypertension."
    elif bp < 140:
        bp_category = "Stage 1 Hypertension"
        bp_advice = "Lifestyle changes and possible medication needed."
    elif bp < 180:
        bp_category = "Stage 2 Hypertension"
        bp_advice = "Medical treatment required. Consult doctor immediately."
    else:
        bp_category = "Hypertensive Crisis"
        bp_advice = "Seek emergency medical attention right away."
    
    insights.append({
        'title': 'bp',
        'value': f"{bp} mmHg",
        'category': bp_category,
        'advice': bp_advice
    })
    
    # chol Category
    if chol < 200:
        chol_category = "Desirable"
        chol_advice = "Keep up the good work with healthy lifestyle choices."
    elif chol < 240:
        chol_category = "Borderline High"
        chol_advice = "Diet and exercise changes recommended."
    else:
        chol_category = "High"
        chol_advice = "Medical intervention may be necessary. Consult your doctor."
    
    insights.append({
        'title': 'chol',
        'value': f"{chol} mg/dL",
        'category': chol_category,
        'advice': chol_advice
    })
    
    # Age-Related Risk
    if age < 40:
        age_risk = "Low"
        age_advice = "Focus on preventive health and building healthy habits."
    elif age < 55:
        age_risk = "Moderate"
        age_advice = "Regular health screenings become more important."
    else:
        age_risk = "Elevated"
        age_advice = "Comprehensive annual health assessments recommended."
    
    insights.append({
        'title': 'Age-Related Risk',
        'value': f"{age} years",
        'category': age_risk,
        'advice': age_advice
    })
    
    return insights

# ================================================
# ================================================
# INITIALIZE THEME (ONLY ONCE)
# ================================================
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# ================================================
# SIDEBAR - USER PROFILE & NAVIGATION
# ================================================

with st.sidebar:

    st.markdown('<h2 style="color:white;">👤 User Profile</h2>', unsafe_allow_html=True)

    st.session_state.user_profile['name'] = st.text_input(
        "Name",
        value=st.session_state.user_profile['name'],
        key="sidebar_name"
    )

    st.session_state.user_profile['gender'] = st.selectbox(
        "Gender",
        ["Select", "Male", "Female", "Other"],
        index=["Select", "Male", "Female", "Other"].index(
            st.session_state.user_profile['gender']
        ),
        key="sidebar_gender"
    )

    st.divider()

    # ================= THEME =================
    st.markdown('<h3 style="color:white;">🎨 Appearance</h3>', unsafe_allow_html=True)

    theme_toggle = st.toggle(
        "Light Mode",
        value=(st.session_state.theme == "light"),
        key="theme_toggle_sidebar"
    )

    st.session_state.theme = "light" if theme_toggle else "dark"

    st.divider()

    # ================= QUICK STATS =================
    st.markdown('<h3 style="color:white;">📊 Quick Stats</h3>', unsafe_allow_html=True)

    total_assessments = len(st.session_state.health_history)
    st.metric("Total Assessments", total_assessments)

    if total_assessments > 0:
        last_risk = st.session_state.health_history[-1]['risk_level']
        st.metric("Last Risk Level", last_risk)

    st.divider()

    # ================= FEATURE CARDS (RESTORED) =================
    st.markdown('<h3 style="color:white; margin-top:1rem;">✨ Features</h3>', unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI-Powered Analysis</div>
        <div class="feature-description">
            Machine learning algorithms provide accurate risk predictions
        </div>
    </div>

    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Comprehensive Insights</div>
        <div class="feature-description">
            Detailed breakdown of all health parameters
        </div>
    </div>

    <div class="feature-card">
        <div class="feature-icon">💡</div>
        <div class="feature-title">Personalized Tips</div>
        <div class="feature-description">
            Customized recommendations based on your profile
        </div>
    </div>

    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-title">Track Progress</div>
        <div class="feature-description">
            Monitor your health journey over time
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="text-align:center; font-size:0.85rem; color:#A0AEC0;">
        <p><strong>HealNet v2.0</strong></p>
        <p>©️ 2026 IoTrenetics Solutions Pvt Ltd</p>
        <p>🔒 Your data is secure and private</p>
    </div>
    """, unsafe_allow_html=True)


# ================================================
# THEME STYLE (OUTSIDE SIDEBAR)
# ================================================
if st.session_state.theme == "dark":
    st.markdown("""
    <style>
    .stApp {
        background: #0A0E27 !important;
    }
    label[data-testid="stWidgetLabel"] {
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    }
    label[data-testid="stWidgetLabel"] {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
# ================================================
# MAIN CONTENT
# ================================================

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <h1 class="logo">🩺 HealNet</h1>
        <p class="tagline">Predict. Prevent. Personalize.</p>
        <p class="company">By IoTrenetics Solutions Private Limited</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Tab Navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏥 Health Assessment", "📊 Detailed Analysis", "📈 Progress Tracker", "🔗 Connected Health", "ℹ️ About"])

# ================================================
# TAB 1: HEALTH ASSESSMENT
# ================================================
with tab1:
    st.markdown('<h2 style="font-family: Sora; color: white; margin-top: 2rem;">Enter Your Health Parameters</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: var(--text-secondary); margin-bottom: 2rem;">Provide accurate information for the best assessment</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        age = st.slider("👤 Age (years)", 18, 100, st.session_state.user_profile['age'], 1,
                       help="Your current age in years")
        st.session_state.user_profile['age'] = age
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        bp = st.slider("🩺 bp - Systolic (mmHg)", 90, 200, 120, 1,
                      help="The upper number in your blood pressure reading")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        height = st.slider("📏 Height (cm)", 140, 220, st.session_state.user_profile['height'], 1,
                         help="Your height in centimeters")
        st.session_state.user_profile['height'] = height
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        chol = st.slider("🧪 Total chol (mg/dL)", 120, 350, 180, 1,
                        help="Your total cholesterol level")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        weight = st.slider("⚖️ Weight (kg)", 40, 150, st.session_state.user_profile['weight'], 1,
                          help="Your current weight in kilograms")
        st.session_state.user_profile['weight'] = weight
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Calculate bmi
        bmi = calculate_bmi(weight, height)
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-title">Body Mass Index (bmi)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{bmi:.1f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-subtitle">Automatically calculated</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    # Quick Health Summary Card (if history exists)
    if len(st.session_state.health_history) > 0:
        latest = st.session_state.health_history[-1]
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 20px; margin: 2rem 0;">
            <h3 style="color: white; margin-bottom: 1rem;">📊 Your Last Assessment</h3>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Risk Level</div>
                <div style="color: white; font-size: 1.8rem; font-weight: 700;">{latest['risk_level']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">bp</div>
                <div style="color: white; font-size: 1.8rem; font-weight: 700;">{latest['bp']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">chol</div>
                <div style="color: white; font-size: 1.8rem; font-weight: 700;">{latest['chol']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">bmi</div>
                <div style="color: white; font-size: 1.8rem; font-weight: 700;">{latest['bmi']:.1f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Assessment Button
    if st.button("🔍 Analyze My Health Risk", use_container_width=True):
        loading_placeholder = st.empty()
        with loading_placeholder:
            show_loading_animation("Analyzing your health data...")
        
        import time
        time.sleep(1.5)  # Simulate processing
        loading_placeholder.empty()
        
        # Perform risk assessment
        risk_data = assess_risk(age, bp, chol, bmi, st.session_state.user_profile['gender'])
        
        # Save to history
        st.session_state.health_history.append({
            'timestamp': datetime.now(),
            'age': age,
            'bp': bp,
            'chol': chol,
            'bmi': bmi,
            'weight': weight,
            'height': height,
            'risk_level': risk_data['level'],
            'risk_percentage': risk_data['percentage']
        })
        
        # Display Results
        st.markdown('<br><br>', unsafe_allow_html=True)
        
        # Risk Level Card
        risk_class = f"risk-{risk_data['level'].lower()}"
        risk_icons = {"Low": "✅", "Moderate": "⚠️", "High": "🚨"}
        risk_colors = {"Low": "#00D9C0", "Moderate": "#FFB800", "High": "#FF4757"}
        
        st.markdown(f"""
        <div class="risk-card {risk_class}">
            <div class="risk-icon">{risk_icons[risk_data['level']]}</div>
            <div class="risk-title" style="color: {risk_colors[risk_data['level']]};">
                {risk_data['level']} Health Risk
            </div>
            <div class="risk-description">
                Based on your health parameters, your risk assessment is complete.
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {risk_data['percentage']}%;"></div>
            </div>
            <p style="text-align: center; color: var(--text-secondary); margin-top: 0.5rem;">
                Risk Score: {risk_data['percentage']:.1f}%
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Risk Factors
        if risk_data['factors']:
            st.markdown('<h3 style="font-family: Sora; color: white; margin-top: 2rem;">⚠️ Identified Risk Factors</h3>', unsafe_allow_html=True)
            for factor in risk_data['factors']:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.03); padding: 1rem; margin: 0.5rem 0; 
                            border-radius: 12px; border-left: 4px solid {risk_colors[risk_data['level']]};">
                    • {factor}
                </div>
                """, unsafe_allow_html=True)
        
        # Recommendations
        st.markdown('<h3 style="font-family: Sora; color: white; margin-top: 2rem;">💡 Personalized Recommendations</h3>', unsafe_allow_html=True)
        
        recommendations = get_recommendations(risk_data, age, bp, chol, bmi)
        
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            if recommendations['immediate']:
                st.markdown('<h4 style="color: var(--accent-color);">🚨 Immediate Actions</h4>', unsafe_allow_html=True)
                for rec in recommendations['immediate']:
                    st.markdown(f'<div class="recommendation-list"><li>{rec}</li></div>', unsafe_allow_html=True)
            
            if recommendations['dietary']:
                st.markdown('<h4 style="color: var(--success-color); margin-top: 2rem;">🍎 Dietary Changes</h4>', unsafe_allow_html=True)
                for rec in recommendations['dietary'][:4]:
                    st.markdown(f'<div class="recommendation-list"><li>{rec}</li></div>', unsafe_allow_html=True)
        
        with rec_col2:
            if recommendations['lifestyle']:
                st.markdown('<h4 style="color: var(--warning-color);">🌟 Lifestyle Modifications</h4>', unsafe_allow_html=True)
                for rec in recommendations['lifestyle']:
                    st.markdown(f'<div class="recommendation-list"><li>{rec}</li></div>', unsafe_allow_html=True)
            
            if recommendations['exercise']:
                st.markdown('<h4 style="color: var(--primary-color); margin-top: 2rem;">💪 Exercise Plan</h4>', unsafe_allow_html=True)
                for rec in recommendations['exercise']:
                    st.markdown(f'<div class="recommendation-list"><li>{rec}</li></div>', unsafe_allow_html=True)
        
        # Scientific References
        st.markdown('<br><br>', unsafe_allow_html=True)
        st.markdown("""
        <div class="custom-alert alert-info">
            <strong>📚 Evidence-Based Guidelines</strong><br>
            This assessment follows clinical guidelines from: American Heart Association (AHA), 
            World Health Organization (WHO), National Institutes of Health (NIH), 
            American College of Cardiology (ACC), and The Lancet medical journal.
        </div>
        """, unsafe_allow_html=True)
        
        # Disclaimer
        st.markdown("""
        <div class="custom-alert alert-warning" style="margin-top: 1rem;">
            <strong>⚠️ Important Medical Disclaimer</strong><br>
            This tool provides educational health risk estimates and is not a substitute for 
            professional medical advice, diagnosis, or treatment. Always consult qualified 
            healthcare professionals for medical decisions.
        </div>
        """, unsafe_allow_html=True)

# ================================================
# TAB 2: DETAILED ANALYSIS
# ================================================
with tab2:
    st.markdown('<h2 style="font-family: Sora; color: white; margin-top: 2rem;">📊 Comprehensive Health Analysis</h2>', unsafe_allow_html=True)
    
    if len(st.session_state.health_history) > 0:
        latest = st.session_state.health_history[-1]
        
        # Generate insights
        insights = generate_health_insights(
            {'level': latest['risk_level']},
            latest['age'],
            latest['bp'],
            latest['chol'],
            latest['bmi']
        )
        
        # Display insights in a grid
        st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
        
        for insight in insights:
            color_map = {
                'Normal': '#00D9C0',
                'Desirable': '#00D9C0',
                'Low': '#00D9C0',
                'Elevated': '#FFB800',
                'Moderate': '#FFB800',
                'Borderline High': '#FFB800',
                'Overweight': '#FFB800',
                'High': '#FF4757',
                'Stage 1 Hypertension': '#FF4757',
                'Stage 2 Hypertension': '#FF4757',
                'Hypertensive Crisis': '#FF4757',
                'Obese (Class I)': '#FF4757',
                'Obese (Class II)': '#FF4757',
                'Underweight': '#FFB800'
            }
            
            category_color = color_map.get(insight['category'], '#2D5BFF')
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{insight['title']}</div>
                <div class="metric-value">{insight['value']}</div>
                <div style="color: {category_color}; font-weight: 600; margin: 0.5rem 0;">
                    {insight['category']}
                </div>
                <div class="metric-subtitle">{insight['advice']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Health Score Breakdown
        st.markdown('<br><br>', unsafe_allow_html=True)
        st.markdown('<h3 style="font-family: Sora; color: white;">🎯 Health Score Components</h3>', unsafe_allow_html=True)
        
        # Calculate individual component scores (0-100 scale)
        bp_score = max(0, 100 - (latest['bp'] - 90) * 0.9)
        chol_score = max(0, 100 - (latest['chol'] - 120) * 0.4)
        bmi_score = max(0, 100 - abs(latest['bmi'] - 22) * 4)
        age_score = max(0, 100 - (latest['age'] - 18) * 0.8)
        
        score_data = {
            'bp': bp_score,
            'chol': chol_score,
            'bmi': bmi_score,
            'Age Factor': age_score
        }
        
        for component, score in score_data.items():
            score_color = '#00D9C0' if score >= 70 else '#FFB800' if score >= 40 else '#FF4757'
            st.markdown(f"""
            <div style="margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: white; font-weight: 600;">{component}</span>
                    <span style="color: {score_color}; font-weight: 700;">{score:.0f}/100</span>
                </div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {score}%; background: {score_color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Health Timeline
        st.markdown('<br><br>', unsafe_allow_html=True)
        st.markdown('<h3 style="font-family: Sora; color: white;">📅 Assessment Timeline</h3>', unsafe_allow_html=True)
        
        if len(st.session_state.health_history) > 1:
            st.markdown('<div class="timeline">', unsafe_allow_html=True)
            for i, assessment in enumerate(reversed(st.session_state.health_history[-5:])):  # Last 5 assessments
                risk_color = {'Low': '#00D9C0', 'Moderate': '#FFB800', 'High': '#FF4757'}[assessment['risk_level']]
                st.markdown(f"""
                <div class="timeline-item">
                    <div style="color: {risk_color}; font-weight: 700; font-size: 1.1rem;">
                        {assessment['risk_level']} Risk - {assessment['risk_percentage']:.1f}%
                    </div>
                    <div style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.3rem;">
                        {assessment['timestamp'].strftime('%B %d, %Y at %I:%M %p')}
                    </div>
                    <div style="color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.5rem;">
                        BP: {assessment['bp']} | Chol: {assessment['chol']} | bmi: {assessment['bmi']:.1f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Complete more assessments to see your health timeline.")
    
    else:
        st.info("📋 Complete your first health assessment to see detailed analysis here."
)



# =====================================================
with tab2:

    import pandas as pd
    import sqlite3
    import plotly.graph_objects as go
    from datetime import datetime

    # =====================================================
    # SESSION STATE SAFETY INITIALIZATION
    # =====================================================
    if "health_history" not in st.session_state:
        st.session_state.health_history = []

    # =====================================================
    # PART 1: SESSION-BASED HEALTH INSIGHTS
    # =====================================================
    if len(st.session_state.health_history) > 0:

        latest = st.session_state.health_history[-1]
        latest.get("bp", latest.get("bp"))

        st.markdown("### 🧠 AI Health Insights")

        # Example scoring logic (you can replace with your AI model)
        def generate_health_insights(bp, chol, bmi):

            insights = []

            # bp
            if bp < 120:
                insights.append({
                    "title": "bp",
                    "value": f"{bp} mmHg",
                    "category": "Normal",
                    "advice": "Healthy blood pressure level."
                })
            elif bp < 140:
                insights.append({
                    "title": "bp",
                    "value": f"{bp} mmHg",
                    "category": "Elevated",
                    "advice": "Monitor regularly and reduce sodium intake."
                })
            else:
                insights.append({
                    "title": "bp",
                    "value": f"{bp} mmHg",
                    "category": "High",
                    "advice": "Consult a physician immediately."
                })

            # chol
            if chol < 200:
                chol_status = "Normal"
            elif chol < 240:
                chol_status = "Borderline High"
            else:
                chol_status = "High"

            insights.append({
                "title": "chol",
                "value": f"{chol} mg/dL",
                "category": chol_status,
                "advice": "Maintain balanced diet & regular exercise."
            })

            # bmi
            if bmi < 18.5:
                bmi_status = "Underweight"
            elif bmi < 25:
                bmi_status = "Normal"
            elif bmi < 30:
                bmi_status = "Overweight"
            else:
                bmi_status = "Obese"

            insights.append({
                "title": "bmi",
                "value": f"{bmi}",
                "category": bmi_status,
                "advice": "Maintain optimal weight range."
            })

            return insights

        insights = generate_health_insights(
            latest["bp"],
            latest["chol"],
            latest["bmi"]
        )

        for insight in insights:
            st.info(
                f"**{insight['title']}**: {insight['value']}  \n"
                f"Status: {insight['category']}  \n"
                f"Advice: {insight['advice']}"
            )

    else:
        st.info("Complete your first health assessment to see detailed analysis here.")

    # =====================================================
    # PART 2: COMPARATIVE ANALYTICS (DATABASE BASED)
    # =====================================================
    st.markdown(
     "<h2 style='color:#FFFFFF;'>📊 Comparative Analytics</h2>",
     unsafe_allow_html=True
)

    conn = sqlite3.connect("health_data.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        bp REAL,
        cholesterol REAL,
        bmi REAL,
        date TEXT
    )
    """)

    conn.commit()

    df = pd.read_sql_query("SELECT * FROM health_records", conn)

    if not df.empty:

        latest_db = df.iloc[-1]

        # Peer group filter
        peer_group = df[
            (df["gender"] == latest_db["gender"]) &
            (df["age"].between(latest_db["age"] - 5, latest_db["age"] + 5))
        ]

        peer_group = peer_group[peer_group["id"] != latest_db["id"]]

        if len(peer_group) >= 3:

            st.success("Anonymous comparison with similar age & gender group")

            def calculate_percentile(value, series):
                return round((series < value).mean() * 100, 1)

            bp_percentile = calculate_percentile(
                latest_db["bp"],
                peer_group["bp"]
            )

            chol_percentile = calculate_percentile(
                latest_db["cholesterol"],
                peer_group["cholesterol"]
            )

            bmi_percentile = calculate_percentile(
                latest_db["bmi"],
                peer_group["bmi"]
            )

            p1, p2, p3 = st.columns(3)

            with p1:
                st.metric("BP Percentile", f"{bp_percentile}%")

            with p2:
                st.metric("chol Percentile", f"{chol_percentile}%")

            with p3:
                st.metric("bmi Percentile", f"{bmi_percentile}%")

            # Bar Chart
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=["bp", "chol", "bmi"],
                y=[
                    latest_db["bp"],
                    latest_db["cholesterol"],
                    latest_db["bmi"]
                ],
                name="You"
            ))

            fig.add_trace(go.Bar(
                x=["bp", "chol", "bmi"],
                y=[
                    peer_group["bp"].mean(),
                    peer_group["cholesterol"].mean(),
                    peer_group["bmi"].mean()
                ],
                name="Peer Average"
            ))

            fig.update_layout(
                template="plotly_white",
                barmode="group",
                title="Your Health vs Similar Peer Group"
            )

            st.plotly_chart(fig, use_container_width=True)

            st.caption(
                "🔒 Data shown is fully anonymized and aggregated. "
                "Individual peer data is never displayed."
            )

        else:
            st.warning(
                "⚠ Not enough similar users for comparison yet. "
                "Add at least 3 users with similar age and gender."
            )

    else:
        st.info("No health records available in database yet.")


# ================================================
# TAB 3: PROGRESS TRACKER
# ================================================
with tab3:
    st.markdown('<h2 style="font-family: Sora; color: white; margin-top: 2rem;">📈 Your Health Journey</h2>', unsafe_allow_html=True)
    
    if len(st.session_state.health_history) >= 2:
        # Create a DataFrame for visualization
        history_df = pd.DataFrame(st.session_state.health_history)
        history_df['date'] = pd.to_datetime(history_df['timestamp'])
        
        # Trend indicators
        col1, col2, col3, col4 = st.columns(4)
        
        bp_change = history_df['bp'].iloc[-1] - history_df['bp'].iloc[-2]
        chol_change = history_df['chol'].iloc[-1] - history_df['chol'].iloc[-2]
        bmi_change = history_df['bmi'].iloc[-1] - history_df['bmi'].iloc[-2]
        risk_change = history_df['risk_percentage'].iloc[-1] - history_df['risk_percentage'].iloc[-2]
        
        with col1:
            st.markdown(f"""
            <div class="stat-item">
                <div class="stat-value" style="color: {'#FF4757' if bp_change > 0 else '#00D9C0'};">
                    {bp_change:+.0f}
                </div>
                <div class="stat-label">Blood Pressure Change</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-item">
                <div class="stat-value" style="color: {'#FF4757' if chol_change > 0 else '#00D9C0'};">
                    {chol_change:+.0f}
                </div>
                <div class="stat-label">chol Change</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-item">
                <div class="stat-value" style="color: {'#FF4757' if bmi_change > 0 else '#00D9C0'};">
                    {bmi_change:+.1f}
                </div>
                <div class="stat-label">bmi Change</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stat-item">
                <div class="stat-value" style="color: {'#FF4757' if risk_change > 0 else '#00D9C0'};">
                    {risk_change:+.1f}%
                </div>
                <div class="stat-label">Risk Score Change</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<br><br>', unsafe_allow_html=True)
        
        # Progress Summary
        st.markdown('<h3 style="font-family: Sora; color: white;">📊 Assessment Summary</h3>', unsafe_allow_html=True)
        
        # Display recent assessments
        st.dataframe(
            history_df[['date', 'age', 'bp', 'chol', 'bmi', 'risk_level', 'risk_percentage']].tail(10).sort_values('date', ascending=False),
            use_container_width=True,
            hide_index=True
        )
        
        # Export option
        st.markdown('<br>', unsafe_allow_html=True)
        if st.button("📥 Export Health Data (CSV)", use_container_width=True):
            csv = history_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"healnet_health_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Health Goals Section
        st.markdown('<br><br>', unsafe_allow_html=True)
        st.markdown('<h3 style="font-family: Sora; color: white;">🎯 Set Health Goals</h3>', unsafe_allow_html=True)
        
        goal_col1, goal_col2 = st.columns(2)
        
        with goal_col1:
            target_bp = st.number_input("Target Blood Pressure", 90, 140, 120)
            target_chol = st.number_input("Target chol", 120, 200, 180)
        
        with goal_col2:
            target_bmi = st.number_input("Target bmi", 18.5, 25.0, 22.0, 0.1)
            target_date = st.date_input("Target Date", datetime.now() + timedelta(days=90))
        
        if st.button("💾 Save Goals", use_container_width=True):
            st.session_state.user_profile['goals'] = {
                'bp': target_bp,
                'chol': target_chol,
                'bmi': target_bmi,
                'target_date': target_date
            }
            st.success("✅ Health goals saved successfully!")
    
    else:
        st.info("📊 Complete at least 2 assessments to track your progress over time.")

# ================================================
# TAB 4: CONNECTED HEALTH (Wearables, Lab Reports, AI, etc.)
# ================================================
with tab4:
    st.markdown('<h2 style="font-family: Sora; color: white; margin-top: 2rem;">🔗 Connected Health Ecosystem</h2>', unsafe_allow_html=True)
    
    # Section 1: Wearable Integration
    st.markdown("---")
    st.markdown("## 🔗 Wearable Integration")
    
    redirect_uri_encoded = quote("http://localhost:8501", safe="")
    auth_url = (
        "https://www.fitbit.com/oauth2/authorize"
        f"?response_type=code"
        f"&client_id=23V288"
        f"&redirect_uri=http://localhost:8501"
        f"&scope=activity%20heartrate%20sleep%20profile"
    )
    
    st.markdown(f"[🔐 Click here to authorize Fitbit]({auth_url})")
    
    # Handle OAuth callback
    query_params = st.query_params
    
    if "code" in query_params:
        code = query_params["code"]
        
        token_url = "https://api.fitbit.com/oauth2/token"
        
        response = requests.post(
            token_url,
            data={
                "client_id": CLIENT_ID,
                "grant_type": "authorization_code",
                "redirect_uri": REDIRECT_URI,
                "code": code,
            },
            auth=(CLIENT_ID, CLIENT_SECRET),
        )
        
        token_data = response.json()
        access_token = token_data.get("access_token")
        st.session_state["access_token"] = access_token
        st.success("✅ Access token received!")
    
    # Fetch and display wearable data
    if "access_token" in st.session_state:
        headers = {
            "Authorization": f"Bearer {st.session_state['access_token']}"
        }
        
        # Heart Rate
        hr_response = requests.get(
            "https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json",
            headers=headers
        ).json()
        
        try:
            resting_hr = hr_response["activities-heart"][0]["value"]["restingHeartRate"]
        except:
            resting_hr = None
        
        # Steps
        steps_response = requests.get(
            "https://api.fitbit.com/1/user/-/activities/steps/date/today/1d.json",
            headers=headers
        ).json()
        
        try:
            steps = steps_response["activities-steps"][0]["value"]
        except:
            steps = None
        
        # Sleep
        sleep_response = requests.get(
            "https://api.fitbit.com/1.2/user/-/sleep/date/today.json",
            headers=headers
        ).json()
        
        try:
            sleep_minutes = sleep_response["summary"]["totalMinutesAsleep"]
        except:
            sleep_minutes = None
        
        # Display wearable data with improved design
        st.markdown("### 📊 Wearable Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                padding: 2rem;
                border-radius: 16px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);
            ">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">❤️</div>
                <div style="color: white; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">
                    {resting_hr if resting_hr else "N/A"}
                </div>
                <div style="color: rgba(255,255,255,0.9); font-size: 1rem; text-transform: uppercase; letter-spacing: 0.1em;">
                    Resting Heart Rate
                </div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.85rem; margin-top: 0.5rem;">
                    beats per minute
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                padding: 2rem;
                border-radius: 16px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
            ">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">👣</div>
                <div style="color: white; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">
                    {steps if steps else "N/A"}
                </div>
                <div style="color: rgba(255,255,255,0.9); font-size: 1rem; text-transform: uppercase; letter-spacing: 0.1em;">
                    Steps Today
                </div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.85rem; margin-top: 0.5rem;">
                    Goal: 10,000 steps
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            sleep_hours = round(sleep_minutes / 60, 1) if sleep_minutes else 0
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                padding: 2rem;
                border-radius: 16px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(168, 237, 234, 0.3);
            ">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">😴</div>
                <div style="color: #2D3748; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">
                    {sleep_hours if sleep_minutes else "N/A"}
                </div>
                <div style="color: #2D3748; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.1em;">
                    Sleep Duration
                </div>
                <div style="color: #4A5568; font-size: 0.85rem; margin-top: 0.5rem;">
                    hours last night
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Section 2: Lab Report Upload
    st.markdown("---")
    st.markdown("## 🧪 Lab Report Upload & Analysis")
    
    uploaded_file = st.file_uploader(
        "Upload Lab Report (PDF or Image)",
        type=["pdf", "png", "jpg", "jpeg"]
    )
    
    if uploaded_file is not None:
        import pytesseract
        from PIL import Image
        import fitz  # PyMuPDF
        import re
        
        def extract_text_from_file(file):
            if file.type == "application/pdf":
                pdf = fitz.open(stream=file.read(), filetype="pdf")
                text = ""
                for page in pdf:
                    text += page.get_text()
                return text
            else:
                image = Image.open(file)
                return pytesseract.image_to_string(image)
        
        def extract_parameters(text):
            patterns = {
                "Hemoglobin": r"Hemoglobin\s*[:\-]?\s*(\d+\.?\d*)",
                "WBC": r"WBC\s*[:\-]?\s*(\d+\.?\d*)",
                "RBC": r"RBC\s*[:\-]?\s*(\d+\.?\d*)",
                "Platelets": r"Platelets\s*[:\-]?\s*(\d+\.?\d*)",
                "Glucose": r"Glucose\s*[:\-]?\s*(\d+\.?\d*)",
                "chol": r"chol\s*[:\-]?\s*(\d+\.?\d*)",
            }
            
            results = {}
            
            for key, pattern in patterns.items():
                match = re.search(pattern, text, re.IGNORECASE)
                results[key] = float(match.group(1)) if match else None
            
            return results
        
        def analyze_results(results):
            normal_ranges = {
                "Hemoglobin": (12, 17),
                "WBC": (4000, 11000),
                "RBC": (4, 6),
                "Platelets": (150000, 450000),
                "Glucose": (70, 100),
                "chol": (0, 200),
            }
            
            alerts = {}
            
            for param, value in results.items():
                if value is None:
                    alerts[param] = "Not Found"
                    continue
                
                low, high = normal_ranges.get(param, (None, None))
                
                if low is not None and value < low:
                    alerts[param] = "Low"
                elif high is not None and value > high:
                    alerts[param] = "High"
                else:
                    alerts[param] = "Normal"
            
            return alerts
        
        extracted_text = extract_text_from_file(uploaded_file)
        results = extract_parameters(extracted_text)
        alerts = analyze_results(results)
        
        st.markdown("### 📊 Extracted Parameters")
        
        for param, value in results.items():
            status = alerts[param]
            
            if status == "High" or status == "Low":
                st.error(f"{param}: {value} ({status})")
            elif status == "Normal":
                st.success(f"{param}: {value} (Normal)")
            else:
                st.warning(f"{param}: Not Found")
    
    # Section 3: Symptom Checker
    st.markdown("---")
    st.markdown("## 🩺 Symptom Checker & Diagnosis Support")
    
    symptoms = st.text_area("Enter your symptoms (e.g., fever, cough, headache)")
    
    if st.button("Analyze Symptoms"):
        results = analyze_symptoms(symptoms)
        if results:
            st.markdown("### 📋 Possible Conditions")
            for condition, probability in results.items():
                st.write(f"*{condition}* — {probability}%")
        else:
            st.info("No matches found. Please describe your symptoms more clearly.")
        
        st.warning("⚠️ This is not a medical diagnosis. Always consult a doctor.")
    
    # Section 4: Predictive Health Trends
    st.markdown("---")
    st.markdown("## 📈 Predictive Health Trends")
    
    metric = st.selectbox(
        "Select Health Metric",
        ["Blood Pressure", "Blood Sugar", "bmi"]
    )
    
    past_values = st.text_input(
        "Enter last 6 values (comma-separated)",
        placeholder="120, 122, 125, 130, 135, 140"
    )
    
    if st.button("Predict Future Health"):
        try:
            values = [float(v.strip()) for v in past_values.split(",")]
            
            if len(values) < 4:
                st.warning("Please enter at least 4 past values")
            else:
                months = [3, 6, 12]
                predictions = predict_future(values, months)
                
                st.markdown("### 🔮 Predicted Values")
                for m, p in zip(months, predictions):
                    st.write(f"*After {m} months:* {round(p, 2)}")
                
                # Plot
                fig, ax = plt.subplots()
                ax.plot(
                    range(len(values)),
                    values,
                    marker="o",
                    label="Past Data"
                )
                
                ax.plot(
                    range(len(values), len(values) + len(months)),
                    predictions,
                    marker="o",
                    linestyle="--",
                    label="Predicted"
                )
                
                ax.set_title(f"{metric} Trend Prediction")
                ax.set_xlabel("Time")
                ax.set_ylabel(metric)
                ax.legend()
                
                st.pyplot(fig)
                
                st.markdown("### 🛠 Recommended Interventions")
                
                if predictions[-1] > values[-1]:
                    st.warning(
                        "- Improve diet\n"
                        "- Increase physical activity\n"
                        "- Reduce stress\n"
                        "- Regular medical checkups"
                    )
                else:
                    st.success(
                        "- Maintain current lifestyle\n"
                        "- Continue healthy habits\n"
                        "- Monitor regularly"
                    )
        
        except Exception as e:
            st.error("Invalid input format. Please enter numbers only.")
 
  
  
# Section 5: AI Health Assistant
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; margin: 2rem 0;">
        <h2 style="color: white; margin-bottom: 1rem;">🧠 AI Health Assistant</h2>
        <p style="color: rgba(255,255,255,0.9);">Ask me anything about your health</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"""
            <div style="background: rgba(45, 91, 255, 0.1); padding: 1rem; 
                        border-radius: 12px; margin: 0.5rem 0; border-left: 4px solid #2D5BFF;">
                <strong style="color: #2D5BFF;">You:</strong> <span style="color: white;">{message['content']}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: rgba(0, 217, 192, 0.1); padding: 1rem; 
                        border-radius: 12px; margin: 0.5rem 0; border-left: 4px solid #00D9C0;">
                <strong style="color: #00D9C0;">AI:</strong> <span style="color: white;">{message['content']}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Input field
    question = st.text_input("Ask your health question", key="ai_question")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        ask_button = st.button("🚀 Ask AI", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear Chat", use_container_width=True)
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()
    
    if ask_button and question.strip():
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": question})
        
        with st.spinner("AI is thinking..."):
            try:
                response = ollama.chat(
                    model="phi3",
                    messages=[
                        {"role": "system", "content": "You are a helpful medical assistant. Provide concise, accurate health information. Always advise consulting a doctor for medical decisions."},
                        {"role": "user", "content": question}
                    ],
                    options={"num_predict": 250}
                )
                
                answer = response["message"]["content"]
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("💡 Make sure Ollama is running with: ollama run phi3")
    
    # Section 6: Additional Services
    st.markdown("---")
    st.markdown("## 🏥 Additional Services")
    
    service_col1, service_col2 = st.columns(2)
    
    with service_col1:
        st.markdown("### 🎥 Video Consultation")
        room_name = "health_consult_room"
        jitsi_url = f"https://meet.jit.si/{room_name}"
        st.markdown(f"[🎥 Start Video Consultation]({jitsi_url})")
        
        st.markdown("### 📅 Book Appointment")
        conn_appt = sqlite3.connect("appointments.db")
        c_appt = conn_appt.cursor()
        c_appt.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            name TEXT,
            doctor TEXT,
            date TEXT
        )
        """)
        conn_appt.commit()
        
        appt_name = st.text_input("Your Name", key="appt_name")
        doctor = st.selectbox("Select Doctor", ["Dr. Smith", "Dr. Patel", "Dr. Khan"])
        appt_date = st.date_input("Select Date")
        
        if st.button("Book Appointment"):
            c_appt.execute("INSERT INTO appointments VALUES (?, ?, ?)",
                          (appt_name, doctor, str(appt_date)))
            conn_appt.commit()
            st.success("✅ Appointment Booked!")
    
    with service_col2:
        st.markdown("### 💊 Prescription Upload")
        prescription = st.file_uploader("Upload Prescription", type=["pdf"], key="prescription_upload")
        
        if prescription:
            prescription_dir = Path("prescriptions")
            prescription_dir.mkdir(exist_ok=True)
            with open(prescription_dir / prescription.name, "wb") as f:
                f.write(prescription.getbuffer())
            st.success("✅ Prescription saved securely!")
        
        st.markdown("### 💊 Medication Reminder")
        conn_med = sqlite3.connect("medications.db")
        c_med = conn_med.cursor()
        c_med.execute("""
        CREATE TABLE IF NOT EXISTS meds (
            name TEXT,
            dosage TEXT,
            time TEXT
        )
        """)
        
        med_name = st.text_input("Medicine Name")
        dosage = st.text_input("Dosage (e.g., 500mg)")
        med_time = st.time_input("Reminder Time")
        
        if st.button("Save Reminder"):
            c_med.execute("INSERT INTO meds VALUES (?, ?, ?)",
                         (med_name, dosage, str(med_time)))
            conn_med.commit()
            st.success("✅ Reminder Saved!")
    
    # Section 7: Personalization
    st.markdown("---")
    st.markdown("## 🥗 Personalized Plans")
    
    plan_col1, plan_col2 = st.columns(2)
    
    with plan_col1:
        st.markdown("### 🍎 Diet Plan")
        condition = st.selectbox(
            "Select Health Condition",
            ["Diabetes", "Hypertension", "High chol", "Weight Loss", "General Fitness"]
        )
        
        calories = st.number_input("Target Daily Calories", 1200, 3500, 2000)
        
        def generate_diet(condition, calories):
            if condition == "Diabetes":
                return {
                    "Breakfast": "Oatmeal + Nuts + Boiled Egg",
                    "Lunch": "Grilled Chicken + Brown Rice + Salad",
                    "Dinner": "Steamed Vegetables + Paneer/Tofu",
                    "Avoid": "Sugar, White Bread, Soda"
                }
            elif condition == "Hypertension":
                return {
                    "Breakfast": "Banana + Low-fat Milk",
                    "Lunch": "Grilled Fish + Quinoa",
                    "Dinner": "Vegetable Soup + Whole Grain Toast",
                    "Avoid": "Salt, Processed Food"
                }
            else:
                return {
                    "Breakfast": "Eggs + Toast",
                    "Lunch": "Chicken + Rice",
                    "Dinner": "Salad + Protein",
                    "Avoid": "Junk Food"
                }
        
        plan = generate_diet(condition, calories)
        
        st.markdown("#### 📋 Your Plan")
        for key, value in plan.items():
            st.write(f"*{key}:* {value}")
    
    with plan_col2:
        st.markdown("### 🏋️ Workout Plan")
        goal = st.selectbox(
            "Fitness Goal",
            ["Weight Loss", "Muscle Gain", "Heart Health", "General Fitness"]
        )
        
        def workout_plan(goal):
            if goal == "Weight Loss":
                return [
                    "30 min Brisk Walking",
                    "15 min HIIT",
                    "Core exercises (Plank 3x30s)"
                ]
            elif goal == "Muscle Gain":
                return [
                    "Bench Press 3x10",
                    "Squats 3x12",
                    "Deadlift 3x8"
                ]
            else:
                return [
                    "20 min Cardio",
                    "Stretching",
                    "Light Strength Training"
                ]
        
        workout = workout_plan(goal)
        
        st.markdown("#### 📋 Your Workout")
        for exercise in workout:
            st.write("•", exercise)
        
        st.markdown("#### 🎥 Exercise Video Guide")
        st.video("https://www.youtube.com/watch?v=ml6cT4AZdqI")
    #Secction 8: ANALYTICS

# =====================================================
# SESSION INITIALIZATION
# =====================================================
if "health_data" not in st.session_state:
    st.session_state.health_data = pd.DataFrame(
        columns=["Date", "Blood Pressure", "chol", "bmi"]
    )

# =====================================================
# MEDICAL UI STYLING
# =====================================================
st.markdown("""
<style>
.stApp {
    background-color: #F7FAFC;
}

.medical-card {
    background: #FFFFFF;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    margin-bottom: 20px;
}

.section-title {
    font-size: 20px;
    font-weight: 600;
    color: #2B6CB0;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================



# ================================================
# TAB 5: ABOUT
# ================================================
with tab5:
    st.markdown('<h2 style="font-family: Sora; color: white; margin-top: 2rem;">About HealNet</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: var(--primary-color); font-family: Sora;">🩺 What is HealNet?</h3>
        <p style="color: var(--text-secondary); line-height: 1.8;">
            HealNet is an advanced health risk prediction system that combines clinical guidelines 
            with machine learning to provide personalized health assessments. Our mission is to 
            empower individuals with actionable health insights.
        </p>
    </div>
    
    <div class="metric-card">
        <h3 style="color: var(--secondary-color); font-family: Sora;">🎯 Our Mission</h3>
        <p style="color: var(--text-secondary); line-height: 1.8;">
            <strong>Predict:</strong> Use advanced algorithms to identify health risks early<br>
            <strong>Prevent:</strong> Provide actionable recommendations to prevent disease<br>
            <strong>Personalize:</strong> Deliver tailored health guidance for each individual
        </p>
    </div>
    
    <div class="metric-card">
        <h3 style="color: var(--accent-color); font-family: Sora;">🔬 How It Works</h3>
        <p style="color: var(--text-secondary); line-height: 1.8;">
            HealNet analyzes multiple health parameters including age, blood pressure, cholesterol, 
            and bmi using a hybrid approach:
        </p>
        <ul style="color: var(--text-secondary); line-height: 1.8;">
            <li><strong>Clinical Scoring:</strong> Evidence-based risk factors from medical guidelines</li>
            <li><strong>Machine Learning:</strong> Advanced predictive models trained on health data</li>
            <li><strong>Personalization:</strong> Customized recommendations based on your unique profile</li>
        </ul>
    </div>
    
    <div class="metric-card">
        <h3 style="color: var(--warning-color); font-family: Sora;">📚 Evidence-Based Approach</h3>
        <p style="color: var(--text-secondary); line-height: 1.8;">
            Our assessment criteria are based on guidelines from:
        </p>
        <ul style="color: var(--text-secondary); line-height: 1.8;">
            <li>American Heart Association (AHA)</li>
            <li>World Health Organization (WHO)</li>
            <li>National Institutes of Health (NIH)</li>
            <li>American College of Cardiology (ACC)</li>
            <li>The Lancet Medical Journal</li>
        </ul>
    </div>
    
    <div class="metric-card">
        <h3 style="color: var(--danger-color); font-family: Sora;">⚠️ Important Disclaimers</h3>
        <p style="color: var(--text-secondary); line-height: 1.8;">
            <strong>Not a Medical Device:</strong> HealNet is an educational tool and research platform. 
            It is not intended to diagnose, treat, cure, or prevent any disease.<br><br>
            <strong>Consult Healthcare Professionals:</strong> Always seek advice from qualified 
            healthcare providers for medical decisions.<br><br>
            <strong>Academic Purpose:</strong> This system is developed for research and educational 
            purposes by IoTrenetics Solutions Private Limited.
        </p>
    </div>
    
    <div class="metric-card">
        <h3 style="color: var(--primary-color); font-family: Sora;">🏢 About IoTrenetics Solutions</h3>
        <p style="color: var(--text-secondary); line-height: 1.8;">
            IoTrenetics Solutions Private Limited is a technology company focused on developing 
            innovative healthcare solutions using AI, IoT, and data analytics. We are committed to 
            making healthcare more accessible, predictive, and personalized.
        </p>
    </div>
    
    <div class="metric-card">
        <h3 style="color: var(--secondary-color); font-family: Sora;">📞 Contact & Support</h3>
        <p style="color: var(--text-secondary); line-height: 1.8;">
            <strong>Email:</strong> support@iotrenetics.com<br>
            <strong>Website:</strong> www.iotrenetics.com<br>
            <strong>Version:</strong> HealNet 2.0<br>
            <strong>Last Updated:</strong> February 2026
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<br><br>', unsafe_allow_html=True)
    
    # Privacy & Security
    st.markdown("""
    <div class="custom-alert alert-success">
        <strong>🔒 Privacy & Security</strong><br>
        Your health data is stored locally in your browser session and is never transmitted to 
        external servers. We respect your privacy and maintain strict data confidentiality.
    </div>
    """, unsafe_allow_html=True)

# ================================================
# FOOTER
# ================================================
st.markdown("""
<div class="footer">
    <p style="font-size: 1.1rem; font-weight: 600; margin-bottom: 1rem;">
        🩺 HealNet - Predict. Prevent. Personalize.
    </p>
    <p>
        Made in Bharat by <strong>IoTrenetics Solutions Private Limited</strong>
    </p>
    <p style="margin-top: 0.5rem;">
        ©️ 2026 All Rights Reserved | Version 2.0
    </p>
    <p style="margin-top: 1rem; font-size: 0.85rem;">
        This system is for educational and research purposes only.<br>
        Not intended as a substitute for professional medical advice.
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* ===== FORCE SELECTED VALUE TEXT BLACK ===== */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: white !important;
    color: black !important;
}

/* Selected value (very specific fix) */
.stSelectbox div[data-baseweb="select"] div {
    color: black !important;
}

/* Selected value span */
.stSelectbox div[data-baseweb="select"] span {
    color: black !important;
}

/* Dropdown menu container */
div[data-baseweb="menu"] {
    background-color: white !important;
}

/* Dropdown options */
div[data-baseweb="menu"] div {
    color: black !important;
}

/* Hover */
div[data-baseweb="menu"] div:hover {
    background-color: #E2E8F0 !important;
    color: black !important;
}

</style>
""", unsafe_allow_html=True)