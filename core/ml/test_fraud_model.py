
import joblib
import pandas as pd

# Load trained model
model = joblib.load("real_airline_fraud_model.pkl")

print("Airline Fraud Detection System")
print("--------------------------------")

# Display model information
print("Model:", type(model).__name__)
print("Classes:", model.classes_)
print("Features:", model.feature_names_in_)

# Take user input
amount = float(input("Enter transaction amount: "))
account_age_days = int(input("Enter account age (days): "))
failed_attempts = int(input("Enter failed attempts: "))
session_time_seconds = float(input("Enter session time (seconds): "))

# Prepare input in the correct feature order
input_data = pd.DataFrame([{
    "amount": amount,
    "account_age_days": account_age_days,
    "failed_attempts": failed_attempts,
    "session_time_seconds": session_time_seconds
}])

# Make prediction
prediction = model.predict(input_data)[0]

# Display prediction
print("\n---------- PREDICTION ----------")

if str(prediction).lower() in ["1", "high risk", "fraud"]:
    print("HIGH RISK")
    print("Warning: Suspicious transaction detected!")

elif str(prediction).lower() in ["0", "low risk", "genuine"]:
    print("LOW RISK")
    print("Transaction appears normal.")

else:
    print("Predicted class:", prediction)
    print("Check model.classes_ to configure risk labels.")

# Display prediction confidence
if hasattr(model, "predict_proba"):
    probabilities = model.predict_proba(input_data)[0]

    print("\nPrediction Confidence:")
    for label, probability in zip(model.classes_, probabilities):
        print(f"{label}: {probability * 100:.2f}%")
