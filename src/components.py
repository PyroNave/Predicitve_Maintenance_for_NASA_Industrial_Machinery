from dash import html, dcc

def header():
    return html.Header(className='bg-blue-800 text-white p-6', children=[
        html.H1('NASA Turbofan Jet Engine Predictive Maintenance', className='text-3xl font-bold'),
        html.P('Predict Remaining Useful Life (RUL) using Machine Learning', className='text-lg')
    ])

def input_form():
    input_fields = [
        ('Unit Number', 'unit-input', 'number', 1, 1),  # Added step=1
        ('Cycle', 'cycle-input', 'number', 1, 1),      # Added step=1
        ('Setting 1', 'setting1-input', 'number', 0.0, 0.001),
        ('Setting 2', 'setting2-input', 'number', 0.0, 0.001),
        ('Setting 3', 'setting3-input', 'number', 100.0, 0.1),
        ('Sensor 1', 'sensor1-input', 'number', 518.67, 0.01),
        ('Sensor 2', 'sensor2-input', 'number', 642.0, 0.01),
        ('Sensor 3', 'sensor3-input', 'number', 1589.0, 0.01),
        ('Sensor 4', 'sensor4-input', 'number', 1400.0, 0.01),
        ('Sensor 7', 'sensor7-input', 'number', 554.0, 0.01),
        ('Sensor 8', 'sensor8-input', 'number', 2388.0, 0.01),
        ('Sensor 9', 'sensor9-input', 'number', 9046.0, 0.01),
        ('Sensor 11', 'sensor11-input', 'number', 47.0, 0.01),
        ('Sensor 12', 'sensor12-input', 'number', 522.0, 0.01),
        ('Sensor 13', 'sensor13-input', 'number', 2388.0, 0.01),
        ('Sensor 14', 'sensor14-input', 'number', 8138.0, 0.01),
        ('Sensor 15', 'sensor15-input', 'number', 8.4, 0.001),
        ('Sensor 17', 'sensor17-input', 'number', 392.0, 0.1),
        ('Sensor 20', 'sensor20-input', 'number', 39.0, 0.01),
        ('Sensor 21', 'sensor21-input', 'number', 23.4, 0.001)
    ]

    return html.Div(children=[
        html.H2('Input Engine Parameters', className='text-xl font-semibold mb-4 text-gray-800'),
        html.Div(className='grid grid-cols-2 gap-4', children=[
            html.Div(children=[
                html.Label(label, className='block text-sm font-medium text-gray-700'),
                dcc.Input(id=input_id, type=input_type, value=default, step=step,
                         className='mt-1 block w-full border border-gray-300 rounded-md p-2')
            ]) for label, input_id, input_type, default, step in input_fields
        ]),
        html.Button('Predict RUL', id='predict-button',
                   className='mt-4 bg-blue-600 text-white font-semibold py-2 px-4 rounded-md hover:bg-blue-700')
    ])

def prediction_card():
    return html.Div(className='mt-6 p-4 bg-blue-50 rounded-lg', children=[
        html.H2('Prediction Result', className='text-lg font-semibold text-gray-800'),
        html.P(id='prediction-output', className='text-xl text-blue-800 font-bold')
    ])

def feature_importance_plot():
    return dcc.Graph(id='feature-importance-plot')

def prediction_trend_plot():
    return dcc.Graph(id='prediction-trend-plot')

def footer():
    return html.Footer(className='bg-gray-800 text-white text-center p-4 mt-6', children=[
        html.P('© 2025 Predictive Maintenance Project | Powered by Dash & Render')
    ])