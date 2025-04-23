import joblib
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler

def load_model_and_scaler():
    try:
        model = joblib.load('artifacts/model.joblib')
        scaler = joblib.load('artifacts/scaler.pkl')
        return model, scaler
    except Exception as e:
        print(f"Error loading model or scaler: {e}")
        return None, None

def predict_rul(model, scaler, df):
    try:
        # Pass the entire DataFrame, including 'unit' and 'cycle', since PointPredictor may need them for preprocessing
        rul = model.predict(df, preprocess=True)
        return max(0, rul[0])  # Ensure non-negative RUL, take first prediction
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        raise  # Re-raise the exception to catch it in the callback for better error reporting

def get_feature_importance(model, features):
    try:
        # Verify that model.regressor is a RandomForestRegressor and has feature_importances_
        if not hasattr(model, 'regressor') or not hasattr(model.regressor, 'feature_importances_'):
            raise AttributeError("Model does not support feature importance.")

        importances = model.regressor.feature_importances_
        # Check if the number of features matches the number of importances
        if len(features) != len(importances):
            raise ValueError(f"Feature length mismatch: {len(features)} features provided, but model has {len(importances)} importances.")

        df = pd.DataFrame({'Feature': features, 'Importance': importances})
        df = df.sort_values('Importance', ascending=True)

        fig = px.bar(df, x='Importance', y='Feature', orientation='h',
                     title='Feature Importance for RUL Prediction',
                     labels={'Importance': 'Relative Importance', 'Feature': 'Feature'},
                     color='Importance', color_continuous_scale='Blues')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            title_font_color='#ffffff'
        )
        return fig
    except Exception as e:
        print(f"Feature importance error: {e}")
        # Return a placeholder plot with an error message
        fig = px.bar(title='Feature Importance Not Available')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            title_font_color='#ffffff'
        )
        return fig