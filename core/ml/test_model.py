from predictor import predict_fraud

sample_data = [
    1000,
    0.5,
    -1.2,
    2.1,
    -0.8,
    1.0,
    0.2,
    -0.3,
    0.6,
    -1.1,
    0.4,
    0.2,
    -0.7,
    0.1,
    0.8,
    -0.2,
    0.3,
    -1.4,
    0.6,
    0.1,
    -0.5,
    1.2,
    -0.9,
    0.7,
    0.4,
    -1.0,
    0.2,
    0.1,
    -0.4,
    0.5
]

print(predict_fraud(sample_data))
