from heartrate_monitor import HeartRateMonitor
import time
import argparse
import dash
import pandas as pd
import matplotlib.pyplot as plt
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


t = 30

parser = argparse.ArgumentParser(description="Read and print data from MAX30102")
parser.add_argument("-r", "--raw", action="store_true",
                    help="print raw data instead of calculation result")
args = parser.parse_args()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



print('sensor starting...')
hrm = HeartRateMonitor()
hrm = HeartRateMonitor(print_raw=args.raw, print_result=(not args.raw))
hrm.start_sensor()

try:
    time.sleep(t)
except KeyboardInterrupt:
    print('keyboard interrupt detected, exiting...')


hrm.stop_sensor()
print('sensor stopped!')

# ---  plot
df_raw = pd.read_csv('raw_values.csv')
fig_raw_i = px.line(df_raw['ir_data'])
fig_raw_r = px.line(df_raw['red_data'])
fig_raw = px.line(df_raw)

df_final = pd.read_csv('final_values.csv')
fig_bpm = px.line(df_final['bpm'])
fig_spo2 = px.line(df_final['spo2'])

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.Div([
            html.H1(children='Sensor infrarrojo'),

            html.Div(children='''
                Información obtenida del sensor
            '''),

            dcc.Graph(
                id='graph-i',
                figure=fig_raw_i
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children='Sensor emisor'),

            html.Div(children='''
                Información obtenida del sensor
            '''),
            dcc.Graph(
                id='graph-r',
                figure=fig_raw_r
            ),  
        ], className='six columns'),
    ], className='row'),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children='Gráfica de sensores'),

        html.Div(children='''
            Comparación de valores ir - red
        '''),

        dcc.Graph(
            id='graph-raw',
            figure=fig_raw
        ),  
    ], className='row'),
     html.Div([
        html.Div([
            html.H1(children='BPM'),

            html.Div(children='''
                :)
            '''),

            dcc.Graph(
                id='graph-bpm',
                figure=fig_bpm
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children='Porcentaje de oxigenación'),

            html.Div(children='''
                SPO2
            '''),

            dcc.Graph(
                id='graph-spo2',
                figure=fig_spo2
            ),  
        ], className='six columns'),
    ], className='row')
])

if __name__ == '__main__':
    app.run_server(debug=True)