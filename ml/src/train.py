import os
import sys

# Ensure current dir is in sys.path
sys.path.append(os.path.dirname(__file__))

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from features import get_features, TARGET
from preprocessing import get_preprocessor
from evaluate import evaluate_model
from ingestion import load_and_combine_csvs

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data/raw')
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/churn_pipeline.joblib')

def load_data():
    """Loads and combines all CSVs from the raw data directory."""
    return load_and_combine_csvs(DATA_DIR, is_training=True)

def train_and_evaluate():
    print("Loading data...")
    df = load_data()
    
    print(f"Dataset loaded. Shape: {df.shape}")
    print(f"Class distribution:\n{df[TARGET].value_counts(normalize=True)}")
    
    X = df[get_features()]
    y = df[TARGET]
    
    # Train / Test Split using stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    preprocessor = get_preprocessor()
    
    # Define models
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, class_weight='balanced', max_iter=1000),
        'Random Forest': RandomForestClassifier(random_state=42, class_weight='balanced', n_estimators=100)
    }
    
    best_model = None
    best_score = -1
    best_name = ""
    
    for name, clf in models.items():
        print(f"\nTraining {name}...")
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', clf)
        ])
        
        pipeline.fit(X_train, y_train)
        
        metrics = evaluate_model(pipeline, X_test, y_test, model_name=name)
        
        # Consider ROC-AUC and F1. We'll use F1 for practical selection.
        score = metrics['f1']
        
        if score > best_score:
            best_score = score
            best_model = pipeline
            best_name = name
            
    print(f"\nBest Model: {best_name} (F1: {best_score:.4f})")
    
    # Ensure models directory exists
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # Save the pipeline
    joblib.dump(best_model, MODEL_PATH)
    print(f"Model successfully saved to {MODEL_PATH}")
    
    # Feature interpretability info
    if best_name == 'Logistic Regression':
        classifier = best_model.named_steps['classifier']
        print("\nLogistic Regression Coefficients (Feature Importance):")
        for feature, coef in zip(get_features(), classifier.coef_[0]):
            print(f"  {feature}: {coef:.4f}")
    elif best_name == 'Random Forest':
        classifier = best_model.named_steps['classifier']
        print("\nRandom Forest Feature Importances:")
        for feature, imp in zip(get_features(), classifier.feature_importances_):
            print(f"  {feature}: {imp:.4f}")

if __name__ == "__main__":
    train_and_evaluate()
