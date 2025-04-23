import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
from app_components import (
    header, input_form, prediction_card, prediction_history_table,
    model_details, feature_importance_plot, prediction_trend_plot, footer
)
from utils import load_model_and_scaler, predict_rul, get_feature_importance
import pandas as pd
import base64
import io

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[
    'https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css',
    '/assets/tailwind.css'
])

server = app.server

# Load model and scaler
model, scaler = load_model_and_scaler()

# Features expected by the model (updated to include all features the model was trained on)
FEATURES = ['setting1', 'setting2', 'setting3'] + [f'sensor{i}' for i in range(1, 22)]

# App layout with space-themed background and tabs
app.layout = html.Div(className='min-h-screen flex flex-col', style={
    'backgroundImage': 'url(/assets/space_background.jpg)',
    'backgroundSize': 'cover',
    'backgroundPosition': 'center',
    'backgroundAttachment': 'fixed'
}, children=[
    header(),
    html.Main(className='container mx-auto p-6 flex-grow', children=[
        dcc.Tabs(id='tabs', value='input-tab', className='custom-tabs', children=[
            dcc.Tab(label='Input & Prediction', value='input-tab', className='custom-tab', selected_className='custom-tab--selected', children=[
                html.Div(className='bg-gray-800 bg-opacity-90 p-6 rounded-lg shadow-lg mt-4', children=[
                    input_form(),
                    prediction_card()
                ])
            ]),
            dcc.Tab(label='Analysis', value='analysis-tab', className='custom-tab', selected_className='custom-tab--selected', children=[
                html.Div(className='mt-4 space-y-6', children=[
                    feature_importance_plot(),
                    prediction_trend_plot(),
                    model_details()
                ])
            ]),
            dcc.Tab(label='History', value='history-tab', className='custom-tab', selected_className='custom-tab--selected', children=[
                html.Div(className='mt-4', children=[
                    prediction_history_table()
                ])
            ])
        ])
    ]),
    footer(),
    # Stores
    dcc.Store(id='uploaded-data', data=None),
    dcc.Store(id='prediction-history', data=[])
])

# Callback to process uploaded CSV
@app.callback(
    [
        Output('uploaded-data', 'data'),
        Output('upload-feedback', 'children')
    ],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def process_upload(contents, filename):
    if contents is None:
        return None, "Please upload a CSV file."

    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

        # Validate required columns
        required_columns = ['unit', 'cycle'] + FEATURES
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return None, f"Error: Missing required columns: {', '.join(missing_columns)}"

        # Validate data types
        for col in FEATURES:
            if not pd.api.types.is_numeric_dtype(df[col]):
                return None, f"Error: Column '{col}' must contain numeric values."

        return df.to_dict('records'), f"Successfully uploaded {filename}."
    except Exception as e:
        return None, f"Error processing file: {str(e)}"

# Callback to update prediction and plots
@app.callback(
    [
        Output('prediction-output', 'children'),
        Output('feature-importance-plot', 'figure'),
        Output('prediction-trend-plot', 'figure'),
        Output('prediction-history', 'data'),
        Output('prediction-history-table', 'children')
    ],
    [
        Input('predict-button', 'n_clicks'),
        Input('reset-history-button', 'n_clicks')
    ],
    [
        State('uploaded-data', 'data'),
        State('equipment-name', 'value'),
        State('prediction-history', 'data')
    ]
)
def update_output(predict_clicks, reset_clicks, uploaded_data, equipment_name, prediction_history):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    # Reset history if reset button clicked
    if triggered_id == 'reset-history-button':
        return "Prediction history reset.", {}, {}, [], html.P("No predictions yet.", className='text-gray-300')

    # Handle prediction
    if triggered_id != 'predict-button' or predict_clicks is None or uploaded_data is None:
        return "Upload a CSV file and click Predict.", {}, {}, prediction_history, html.P("No predictions yet.", className='text-gray-300')

    try:
        df = pd.DataFrame(uploaded_data)
        # Predict RUL using the full DataFrame
        rul = predict_rul(model, scaler, df)
        prediction_text = f"Predicted RUL: {rul:.2f} cycles"

        # Update prediction history with equipment name
        equipment_name = equipment_name if equipment_name else "Unnamed Equipment"
        prediction_entry = {
            'equipment': equipment_name,
            'unit': int(df['unit'].iloc[0]),  # Ensure integer
            'cycle': int(df['cycle'].iloc[0]),  # Ensure integer
            'rul': float(rul)  # Ensure float
        }
        prediction_history.append(prediction_entry)
        if len(prediction_history) > 50:  # Limit history to 50 entries
            prediction_history = prediction_history[-50:]

        # Generate plots
        feature_importance_fig = get_feature_importance(model, FEATURES)
        history_df = pd.DataFrame(prediction_history)
        trend_fig = px.line(
            history_df, 
            x='cycle', 
            y='rul', 
            color='unit',
            title='RUL Prediction Trend', 
            labels={'cycle': 'Cycle', 'rul': 'Predicted RUL'},
            line_shape='linear'
        )
        trend_fig.update_traces(mode='lines+markers')
        trend_fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            title_font_color='#ffffff'
        )

        # Generate history table
        history_table = dash_table.DataTable(
            data=history_df.to_dict('records'),
            columns=[
                {'name': 'Equipment', 'id': 'equipment'},
                {'name': 'Unit', 'id': 'unit'},
                {'name': 'Cycle', 'id': 'cycle'},
                {'name': 'Predicted RUL', 'id': 'rul'}
            ],
            style_table={'overflowX': 'auto'},
            style_cell={
                'backgroundColor': 'rgba(55, 65, 81, 0.9)',
                'color': 'white',
                'border': '1px solid #4B5563'
            },
            style_header={
                'backgroundColor': 'rgba(31, 41, 55, 0.9)',
                'color': 'white',
                'fontWeight': 'bold'
            }
        )

        return prediction_text, feature_importance_fig, trend_fig, prediction_history, history_table
    except Exception as e:
        print(f"Callback error: {str(e)}")
        return f"Prediction error: {str(e)}", {}, {}, prediction_history, html.P("No predictions yet.", className='text-gray-300')

# Callback to download prediction report
@app.callback(
    Output('download-report', 'data'),
    Input('prediction-history', 'data'),
    prevent_initial_call=True
)
def download_report(prediction_history):
    if not prediction_history:
        return None

    df = pd.DataFrame(prediction_history)
    csv_string = df.to_csv(index=False)
    return dict(content=csv_string, filename='prediction_report.csv')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)