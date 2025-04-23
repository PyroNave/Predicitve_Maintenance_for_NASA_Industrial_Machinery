import dash
from dash import html, dcc
import plotly.express as px
from components import (
    header, input_form, prediction_card, feature_importance_plot, 
    prediction_trend_plot, footer
)
from utils import load_model_and_scaler, predict_rul, get_feature_importance
import pandas as pd



# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[
    'https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css',
    '/assets/tailwind.css'
])

server = app.server

# Load model and scaler
model, scaler = load_model_and_scaler()

# App layout
app.layout = html.Div(className='min-h-screen bg-gray-100 flex flex-col', children=[
    header(),
    html.Main(className='container mx-auto p-6 flex-grow', children=[
        html.Div(className='grid grid-cols-1 md:grid-cols-2 gap-6', children=[
            # Input Form and Prediction
            html.Div(className='bg-white p-6 rounded-lg shadow-lg', children=[
                input_form(),
                prediction_card()
            ]),
            # Feature Importance Plot
            html.Div(className='bg-white p-6 rounded-lg shadow-lg', children=[
                html.H2('Feature Importance', className='text-xl font-semibold mb-4 text-gray-800'),
                dcc.Graph(id='feature-importance-plot')
            ])
        ]),
        # Prediction Trend Plot
        html.Div(className='mt-6 bg-white p-6 rounded-lg shadow-lg', children=[
            html.H2('Prediction Trend', className='text-xl font-semibold mb-4 text-gray-800'),
            dcc.Graph(id='prediction-trend-plot')
        ])
    ]),
    footer(),
    # Store for prediction history
    dcc.Store(id='prediction-history', data=[])
])

# Callback to update prediction and plots
@app.callback(
    [
        dash.dependencies.Output('prediction-output', 'children'),
        dash.dependencies.Output('feature-importance-plot', 'figure'),
        dash.dependencies.Output('prediction-trend-plot', 'figure'),
        dash.dependencies.Output('prediction-history', 'data')
    ],
    [
        dash.dependencies.Input('predict-button', 'n_clicks'),
        dash.dependencies.State('unit-input', 'value'),
        dash.dependencies.State('cycle-input', 'value'),
        dash.dependencies.State('setting1-input', 'value'),
        dash.dependencies.State('setting2-input', 'value'),
        dash.dependencies.State('setting3-input', 'value'),
        dash.dependencies.State('sensor1-input', 'value'),
        dash.dependencies.State('sensor2-input', 'value'),
        dash.dependencies.State('sensor3-input', 'value'),
        dash.dependencies.State('sensor4-input', 'value'),
        dash.dependencies.State('sensor7-input', 'value'),
        dash.dependencies.State('sensor8-input', 'value'),
        dash.dependencies.State('sensor9-input', 'value'),
        dash.dependencies.State('sensor11-input', 'value'),
        dash.dependencies.State('sensor12-input', 'value'),
        dash.dependencies.State('sensor13-input', 'value'),
        dash.dependencies.State('sensor14-input', 'value'),
        dash.dependencies.State('sensor15-input', 'value'),
        dash.dependencies.State('sensor17-input', 'value'),
        dash.dependencies.State('sensor20-input', 'value'),
        dash.dependencies.State('sensor21-input', 'value'),
        dash.dependencies.State('prediction-history', 'data')
    ]
)
def update_output(n_clicks, unit, cycle, setting1, setting2, setting3, sensor1, sensor2, sensor3, sensor4, 
                  sensor7, sensor8, sensor9, sensor11, sensor12, sensor13, sensor14, sensor15, sensor17, 
                  sensor20, sensor21, prediction_history):
    if n_clicks is None:
        return "Enter values and click Predict", {}, {}, prediction_history

    # Create input dictionary
    input_data = {
        'unit': unit, 'cycle': cycle, 'setting1': setting1, 'setting2': setting2, 'setting3': setting3,
        'sensor1': sensor1, 'sensor2': sensor2, 'sensor3': sensor3, 'sensor4': sensor4,
        'sensor7': sensor7, 'sensor8': sensor8, 'sensor9': sensor9, 'sensor11': sensor11,
        'sensor12': sensor12, 'sensor13': sensor13, 'sensor14': sensor14, 'sensor15': sensor15,
        'sensor17': sensor17, 'sensor20': sensor20, 'sensor21': sensor21
    }

    # Filter out None values and create DataFrame
    input_data = {k: v for k, v in input_data.items() if v is not None}
    if len(input_data) < 20:  # Ensure most inputs are provided
        return "Please fill in all required fields", {}, {}, prediction_history

    df = pd.DataFrame([input_data])
    features = ['setting1', 'setting2', 'setting3', 'sensor1', 'sensor2', 'sensor3', 'sensor4',
                'sensor7', 'sensor8', 'sensor9', 'sensor11', 'sensor12', 'sensor13', 'sensor14',
                'sensor15', 'sensor17', 'sensor20', 'sensor21']
    X = df[features]

    # Predict RUL
    rul = predict_rul(model, scaler, X)
    prediction_text = f"Predicted RUL: {rul:.2f} cycles"

    # Update prediction history
    prediction_history.append({'unit': unit, 'cycle': cycle, 'rul': rul})
    if len(prediction_history) > 50:  # Limit history to 50 entries
        prediction_history = prediction_history[-50:]

    # Generate plots
    feature_importance_fig = get_feature_importance(model, features)
    trend_fig = px.line(
        pd.DataFrame(prediction_history), x='cycle', y='rul', color='unit',
        title='RUL Prediction Trend', labels={'cycle': 'Cycle', 'rul': 'Predicted RUL'}
    )

    return prediction_text, feature_importance_fig, trend_fig, prediction_history

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)