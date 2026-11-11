from datasets import load_dataset
import pandas as pd

dataset = load_dataset(
    "analytical-community/airline_fraud_transactions"
)

df = dataset["train"].to_pandas()

print(df.head())
print("\nColumns:")
print(df.columns)

df.to_csv(
    "real_airline_fraud.csv",
    index=False
)

print("Dataset Downloaded Successfully")
