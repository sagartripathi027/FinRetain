from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from features import NUMERICAL_FEATURES, CATEGORICAL_FEATURES

def get_preprocessor():
    """Builds and returns the scikit-learn preprocessing ColumnTransformer."""
    
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERICAL_FEATURES),
        ]
    )
    
    return preprocessor
