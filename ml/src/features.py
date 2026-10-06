# Define feature definitions to keep them consistent across the pipeline

NUMERICAL_FEATURES = [
    'tenure', 
    'balance', 
    'transaction_frequency', 
    'complaints', 
    'service_usage'
]

CATEGORICAL_FEATURES = []

TARGET = 'churn'

def get_features():
    return NUMERICAL_FEATURES + CATEGORICAL_FEATURES
