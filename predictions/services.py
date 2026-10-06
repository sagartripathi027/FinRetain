import os
import joblib
import pandas as pd
from django.conf import settings
from .models import Prediction, RetentionRecommendation

MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml', 'models', 'churn_pipeline.joblib')

_cached_pipeline = None

def get_ml_pipeline():
    global _cached_pipeline
    if _cached_pipeline is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model artifact not found at {MODEL_PATH}")
        _cached_pipeline = joblib.load(MODEL_PATH)
    return _cached_pipeline

def classify_risk(probability):
    if probability < 0.30:
        return 'LOW'
    elif probability <= 0.70:
        return 'MEDIUM'
    else:
        return 'HIGH'

def generate_recommendation(risk_level, customer):
    """
    Basic rule-based retention recommendation logic.
    """
    if risk_level == 'HIGH':
        rec = "Prioritize customer retention outreach."
        reason = "High predicted churn risk."
        if customer.complaints > 0:
            rec = "Assign to specialized support immediately."
            reason += f" Elevated complaints ({customer.complaints}) indicate dissatisfaction."
        elif customer.service_usage < 0.3:
            rec = "Offer personalized feature walkthrough."
            reason += " Low service usage indicates failure to realize product value."
    elif risk_level == 'MEDIUM':
        rec = "Schedule engagement follow-up."
        reason = "Medium predicted churn risk."
        if customer.transaction_frequency < 5:
            rec = "Send targeted transaction fee discount."
            reason += " Transaction frequency is low; incentivize activity."
    else:
        rec = "Maintain normal engagement."
        reason = "Low churn risk."
        if customer.tenure > 24:
            rec = "Send loyalty appreciation reward."
            reason += " Customer is a long-term user."

    return rec, reason

def run_churn_prediction(customer):
    """
    Main service flow connecting Django to the ML pipeline.
    Produces prediction, risk level, basic recommendation, and persists them.
    """
    try:
        pipeline = get_ml_pipeline()
    except Exception as e:
        raise RuntimeError(f"Failed to load ML pipeline: {str(e)}")

    # 1. Build Feature Payload
    # Explicit mapping from Django Customer fields to ML Features
    features = {
        'tenure': [customer.tenure],
        'balance': [float(customer.balance)],
        'transaction_frequency': [customer.transaction_frequency],
        'complaints': [customer.complaints],
        'service_usage': [customer.service_usage],
    }
    df = pd.DataFrame(features)

    # 2. ML Inference
    try:
        y_pred = pipeline.predict(df)[0]
        # predict_proba returns [[prob_class0, prob_class1]]
        y_prob = pipeline.predict_proba(df)[0][1] 
    except Exception as e:
        raise RuntimeError(f"ML inference failed: {str(e)}")

    # 3. Risk Classification
    risk_level = classify_risk(y_prob)

    # 4. Generate Recommendation
    rec_text, rec_reason = generate_recommendation(risk_level, customer)

    # 5. Save to Database
    prediction = Prediction.objects.create(
        customer=customer,
        churn_probability=y_prob,
        risk_level=risk_level,
        prediction=bool(y_pred)
    )

    RetentionRecommendation.objects.create(
        prediction=prediction,
        recommendation=rec_text,
        reason=rec_reason
    )

    return prediction

