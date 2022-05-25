from heartrate_monitor import HeartRateMonitor
import time
import argparse
import dash

from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


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

try:
    time.sleep(args.time)
except KeyboardInterrupt:
    print('keyboard interrupt detected, exiting...')


hrm.stop_sensor()
print('sensor stopped!')

## plot
# df_raw = pd.read_csv('raw_values.csv')
# plt.plot(df_raw)
df_final = pd.read_csv('final_values.csv')
plt.plot(df_final)

plt.show()