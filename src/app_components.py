from dash import html, dcc

def header():
       return html.Header(
           className='bg-blue-600 text-white p-4 shadow-md',
           children=[
               html.H1('NASA Turbofan Jet Engine Predictive Maintenance', className='text-2xl font-bold'),
               html.P('Predict Remaining Useful Life (RUL) using sensor data', className='text-sm')
           ]
       )

def input_fields():
       fields = [
           {'label': 'Unit Number', 'id': 'unit-input', 'type': 'number', 'value': 1, 'min': 1, 'step': 1},
           {'label': 'Cycle', 'id': 'cycle-input', 'type': 'number', 'value': 1, 'min': 1, 'step': 1},
           {'label': 'Operational Setting 1', 'id': 'setting1-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Operational Setting 2', 'id': 'setting2-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Operational Setting 3', 'id': 'setting3-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Sensor 1', 'id': 'sensor1-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Sensor 2', 'id': 'sensor2-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Sensor 3', 'id': 'sensor3-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Sensor 4', 'id': 'sensor4-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Sensor 7', 'id': 'sensor7-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Sensor 8', 'id': 'sensor8-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Sensor 9', 'id': 'sensor9-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Sensor 11', 'id': 'sensor11-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Sensor 12', 'id': 'sensor12-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Sensor 13', 'id': 'sensor13-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Sensor 14', 'id': 'sensor14-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Sensor 15', 'id': 'sensor15-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Sensor 17', 'id': 'sensor17-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Sensor 20', 'id': 'sensor20-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
           {'label': 'Sensor 21', 'id': 'sensor21-input', 'type': 'number', 'value': 0.0, 'step': 0.01},
       ]

       return [
           html.Div(
               className='mb-4',
               children=[
                   html.Label(field['label'], className='block text-gray-700 font-medium mb-1'),
                   dcc.Input(
                       id=field['id'],
                       type=field['type'],
                       value=field.get('value', 0.0),
                       min=field.get('min', None),
                       step=field.get('step', 0.01),
                       className='w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
                   )
               ]
           ) for field in fields
       ]

def input_form():
       return html.Div(
           className='space-y-4',
           children=[
               html.H2('Input Sensor Data', className='text-xl font-semibold text-gray-800'),
               *input_fields(),
               html.Button(
                   'Predict RUL',
                   id='predict-button',
                   n_clicks=0,
                   className='w-full bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700 transition'
               )
           ]
       )

def prediction_card():
       return html.Div(
           className='mt-6 p-4 bg-gray-50 border rounded-md',
           children=[
               html.H2('Prediction', className='text-xl font-semibold text-gray-800 mb-2'),
               html.P(
                   id='prediction-output',
                   className='text-lg text-gray-700',
                   children='Enter values and click Predict'
               )
           ]
       )

def feature_importance_plot():
       return dcc.Graph(id='feature-importance-plot')

def prediction_trend_plot():
       return dcc.Graph(id='prediction-trend-plot')

def footer():
       return html.Footer(
           className='bg-gray-800 text-white p-4 mt-auto',
           children=[
               html.P('© 2023 NASA Turbofan Predictive Maintenance', className='text-center')
           ]
       )