
import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "real_airline_fraud_model.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_fraud(
    amount,
    account_age_days,
    failed_attempts,
    session_time_seconds
):
    data = pd.DataFrame([{
        "amount": amount,
        "account_age_days": account_age_days,
        "failed_attempts": failed_attempts,
        "session_time_seconds": session_time_seconds
    }])

    prediction = int(model.predict(data)[0])

    probabilities = model.predict_proba(data)[0]

    confidence = float(
        probabilities[list(model.classes_).index(prediction)] * 100
    )

    return {
        "risk": "HIGH" if prediction == 1 else "LOW",
        "confidence": round(confidence, 2)
    }
