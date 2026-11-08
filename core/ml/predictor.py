import joblib
import os

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "airline_fraud_model.pkl"
)

model = joblib.load(MODEL_PATH)

def predict_fraud(
    seats,
    amount,
    days_before_travel,
    previous_bookings
):

    data = [[
        seats,
        amount,
        days_before_travel,
        previous_bookings
    ]]

    result = model.predict(data)

    if result[0] == 1:
        return "High Risk"

    return "Low Risk"