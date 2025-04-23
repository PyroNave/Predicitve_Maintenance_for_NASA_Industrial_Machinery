from dash import html, dcc
import base64
import pandas as pd

def header():
    return html.Header(
        className='bg-gradient-to-r from-gray-900 to-blue-900 text-white p-6 shadow-lg',
        children=[
            html.Div(className='flex items-center justify-between', children=[
                html.Div(className='flex items-center', children=[
                    html.Img(src='/assets/nasa_logo.png', className='h-12 mr-4'),
                    html.Div([
                        html.H1('NASA Turbofan Jet Engine Predictive Maintenance', className='text-3xl font-bold'),
                        html.P('Predict Remaining Useful Life (RUL) using sensor data', className='text-sm opacity-75')
                    ])
                ]),
                html.A(
                    'Back to NASA.gov',
                    href='https://www.nasa.gov',
                    className='text-blue-300 hover:text-blue-100 transition'
                )
            ])
        ]
    )

def input_form():
    # Realistic sample data based on NASA Turbofan Jet Engine Dataset (FD001), including all sensors
    sample_data = pd.DataFrame([
        {
            'unit': 1, 'cycle': 1, 
            'setting1': -0.0007, 'setting2': -0.0004, 'setting3': 100.0,
            'sensor1': 518.67, 'sensor2': 641.82, 'sensor3': 1589.70, 'sensor4': 1400.60,
            'sensor5': 14.62, 'sensor6': 21.61, 'sensor7': 554.36, 'sensor8': 2388.06,
            'sensor9': 9046.19, 'sensor10': 1.3, 'sensor11': 47.47, 'sensor12': 521.66,
            'sensor13': 2388.02, 'sensor14': 8138.62, 'sensor15': 8.4195, 'sensor16': 0.03,
            'sensor17': 392, 'sensor18': 2388, 'sensor19': 100.0, 'sensor20': 39.06,
            'sensor21': 23.4190
        },
        {
            'unit': 1, 'cycle': 2, 
            'setting1': 0.0019, 'setting2': -0.0003, 'setting3': 100.0,
            'sensor1': 518.67, 'sensor2': 642.15, 'sensor3': 1591.82, 'sensor4': 1403.14,
            'sensor5': 14.62, 'sensor6': 21.61, 'sensor7': 553.75, 'sensor8': 2388.04,
            'sensor9': 9044.07, 'sensor10': 1.3, 'sensor11': 47.49, 'sensor12': 522.28,
            'sensor13': 2388.07, 'sensor14': 8131.49, 'sensor15': 8.4318, 'sensor16': 0.03,
            'sensor17': 392, 'sensor18': 2388, 'sensor19': 100.0, 'sensor20': 39.00,
            'sensor21': 23.4236
        }
    ])
    sample_csv = sample_data.to_csv(index=False)
    encoded_csv = base64.b64encode(sample_csv.encode()).decode()

    return html.Div(
        className='space-y-6',
        children=[
            html.H2('Upload Sensor Data', className='text-2xl font-semibold text-white'),
            html.P(
                'Upload a CSV file with sensor data to predict RUL. The CSV should contain columns: unit, cycle, setting1, setting2, setting3, sensor1, sensor2, ..., sensor21.',
                className='text-gray-300'
            ),
            dcc.Upload(
                id='upload-data',
                children=html.Button(
                    'Upload CSV File',
                    className='bg-blue-600 text-white p-3 rounded-md hover:bg-blue-700 transition'
                ),
                multiple=False,
                accept='.csv',
                className='w-full'
            ),
            html.A(
                'Download Sample CSV',
                id='download-sample',
                download='sample_data.csv',
                href=f'data:text/csv;base64,{encoded_csv}',
                className='text-blue-300 hover:text-blue-100 transition'
            ),
            html.Div(
                className='mb-4',
                children=[
                    html.Label('Equipment Name', className='block text-gray-300 font-medium mb-1'),
                    dcc.Input(
                        id='equipment-name',
                        type='text',
                        value='',
                        placeholder='Enter equipment name (e.g., Engine-001)',
                        className='w-full p-2 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-700 text-white'
                    )
                ]
            ),
            html.Button(
                'Predict RUL',
                id='predict-button',
                n_clicks=0,
                className='w-full bg-orange-600 text-white p-3 rounded-md hover:bg-orange-700 transition'
            ),
            html.Div(id='upload-feedback', className='text-gray-300 mt-2')
        ]
    )

def prediction_card():
    return html.Div(
        className='mt-6 p-6 bg-gray-800 border border-gray-700 rounded-lg',
        children=[
            html.H2('Prediction Result', className='text-xl font-semibold text-white mb-4'),
            html.P(
                id='prediction-output',
                className='text-lg text-gray-200',
                children='Upload a CSV file and click Predict to see the RUL'
            )
        ]
    )

def prediction_history_table():
    return html.Div(
        className='p-6 bg-gray-800 border border-gray-700 rounded-lg',
        children=[
            html.Div(className='flex justify-between items-center mb-4', children=[
                html.H2('Prediction History', className='text-xl font-semibold text-white'),
                html.Button(
                    'Reset History',
                    id='reset-history-button',
                    n_clicks=0,
                    className='bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition'
                )
            ]),
            html.Div(id='prediction-history-table', className='overflow-x-auto'),
            dcc.Download(id='download-report')
        ]
    )

def model_details():
    return html.Div(
        className='p-6 bg-gray-800 border border-gray-700 rounded-lg',
        children=[
            html.H2('Model Details', className='text-xl font-semibold text-white mb-4'),
            html.P('This predictive maintenance model uses a RandomForestRegressor wrapped in a custom PointPredictor class.', className='text-gray-200'),
            html.P('The model was trained on the NASA Turbofan Jet Engine Dataset (FD001–FD004) to predict Remaining Useful Life (RUL).', className='text-gray-200'),
            html.P('Test RMSE: 38.17 (achieved on the test set)', className='text-gray-200 font-semibold'),
            html.P('The model uses 24 features extracted from sensor data, focusing on key operational settings and sensor readings.', className='text-gray-200')
        ]
    )

def feature_importance_plot():
    return html.Div(
        className='p-6 bg-gray-800 border border-gray-700 rounded-lg',
        children=[
            html.H2('Feature Importance', className='text-xl font-semibold text-white mb-4'),
            dcc.Graph(id='feature-importance-plot')
        ]
    )

def prediction_trend_plot():
    return html.Div(
        className='p-6 bg-gray-800 border border-gray-700 rounded-lg',
        children=[
            html.H2('Prediction Trend', className='text-xl font-semibold text-white mb-4'),
            dcc.Graph(id='prediction-trend-plot')
        ]
    )

def footer():
    return html.Footer(
        className='bg-gray-900 text-white p-6 mt-auto',
        children=[
            html.P('© 2025 NASA Turbofan Predictive Maintenance', className='text-center')
        ]
    )