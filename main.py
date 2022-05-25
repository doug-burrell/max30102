# sensor
from heartrate_monitor import HeartRateMonitor
import time
import argparse

# graph
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

parser = argparse.ArgumentParser(description="Read and print data from MAX30102")
parser.add_argument("-r", "--raw", action="store_true",
                    help="print raw data instead of calculation result")
parser.add_argument("-t", "--time", type=int, default=30,
                    help="duration in seconds to read from sensor, default 30")
args = parser.parse_args()

print('sensor starting...')
hrm = HeartRateMonitor(print_raw=args.raw, print_result=(not args.raw))
hrm.start_sensor()
print(hrm) # test

df_bar = pd.DataFrame()

try:
    time.sleep(args.time)
except KeyboardInterrupt:
    print('keyboard interrupt detected, exiting...')

hrm.stop_sensor()
print('sensor stoped!')