
def normalize_inputs(age, cholesterol, systolic_bp, bmi):
    age_n = min(age / 100, 1)
    chol_n = min(cholesterol / 300, 1)
    bp_n = min(systolic_bp / 200, 1)
    bmi_n = min(bmi / 40, 1)
    return age_n, chol_n, bp_n, bmi_n


def calculate_risk_score(age, cholesterol, systolic_bp, bmi):
    age_n, chol_n, bp_n, bmi_n = normalize_inputs(
        age, cholesterol, systolic_bp, bmi
    )

    risk_score = (
        0.30 * age_n +
        0.30 * chol_n +
        0.25 * bp_n +
        0.15 * bmi_n
    )

    return round(risk_score, 2)


def classify_risk(risk_score):
    if risk_score < 0.35:
        return "Low"
    elif risk_score < 0.65:
        return "Moderate"
    else:
        return "High"


SUGGESTIONS = {
    "Low": [
        "Maintain Mediterranean or DASH diet (NIH)",
        "150 minutes/week physical activity (WHO)",
        "Annual BP and cholesterol screening (AHA)",
        "Maintain BMI below 25"
    ],
    "Moderate": [
        "Adopt DASH or Mediterranean diet (AHA)",
        "Reduce sodium intake below 2g/day (AHA)",
        "Home blood pressure monitoring advised",
        "Lipid profile every 6 months",
        "Schedule physician consultation"
    ],
    "High": [
        "Immediate physician consultation (AHA)",
        "Medication evaluation advised (ACC)",
        "Strict DASH diet required",
        "Smoking and alcohol cessation (WHO)",
        "Daily blood pressure monitoring"
    ]
}


def assess_health_risk(age, cholesterol, systolic_bp, bmi):
    score = calculate_risk_score(age, cholesterol, systolic_bp, bmi)
    level = classify_risk(score)
    suggestions = SUGGESTIONS[level]
    return score, level, suggestions
