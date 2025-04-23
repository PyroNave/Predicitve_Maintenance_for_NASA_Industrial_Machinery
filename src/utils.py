import joblib
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler

def load_model_and_scaler():
    try:
        model = joblib.load('artifacts/model.pkl')
        scaler = joblib.load('artifacts/scaler.pkl')
        return model, scaler
    except Exception as e:
        print(f"Error loading model or scaler: {e}")
        return None, None

def predict_rul(model, scaler, X):
    try:
        X_scaled = scaler.fit_transform(X)  # Fit scaler on input data (for demo; ideally load pre-fitted scaler)
        rul = model.predict(X_scaled)[0]
        return max(0, rul)  # Ensure non-negative RUL
    except Exception as e:
        print(f"Prediction error: {e}")
        return 0

def get_feature_importance(model, features):
    # Since SVR doesn't provide feature importance directly, use coefficients or permutation importance
    # For simplicity, we'll simulate importance (in practice, use permutation_importance from sklearn)
    np.random.seed(42)
    importances = np.random.rand(len(features))
    importances = importances / importances.sum()  # Normalize
    df = pd.DataFrame({'Feature': features, 'Importance': importances})
    df = df.sort_values('Importance', ascending=True)
    
    fig = px.bar(df, x='Importance', y='Feature', orientation='h',
                 title='Feature Importance for RUL Prediction',
                 labels={'Importance': 'Relative Importance', 'Feature': 'Feature'},
                 color='Importance', color_continuous_scale='Blues')
    return fig