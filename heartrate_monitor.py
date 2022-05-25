from max30102 import MAX30102
import hrcalc
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
import csv

# graph
# import dash
# from dash import html
# from dash import dcc
# from dash.dependencies import Input, Output
# import pandas as pd
# import plotly.express as px


class HeartRateMonitor(object):
    """
    A class that encapsulates the max30102 device into a thread
    """

    LOOP_TIME = 0.01
    
    def __init__(self, print_raw=False, print_result=False):
        self.bpm = 0
        if print_raw is True:
            print('IR, Red')
        self.print_raw = print_raw
        self.print_result = print_result

    def run_sensor(self):
        raw_headers = ['ir_data','red_data']
        raw_file = 'raw_values.csv'
        raw_vals = []
        
        final_headers = ['bpm','spo2']
        final_file = 'final_values.csv'
        final_vals = []
        
        
        sensor = MAX30102()
        ir_data = []
        red_data = []
        bpms = []
#         
#         res_ir_data = []
#         res_red_data = []
#         res_bpm = []
#         res_spo = []

        # run until told to stop
        while not self._thread.stopped:
            # check if any data is available
            num_bytes = sensor.get_data_present()
            if num_bytes > 0:
                # grab all the data and stash it into arrays
                while num_bytes > 0:
                    red, ir = sensor.read_fifo()
                    num_bytes -= 1
                    ir_data.append(ir)
                    red_data.append(red)
                    if self.print_raw:
                        print("{0}, {1}".format(ir, red))

                while len(ir_data) > 100:
                    ir_data.pop(0)
                    red_data.pop(0)

                if len(ir_data) == 100:
                    bpm, valid_bpm, spo2, valid_spo2 = hrcalc.calc_hr_and_spo2(ir_data, red_data)
                    raw = {"ir_data": np.mean(ir_data), "red_data": np.mean(red_data)}
                    raw_vals.append(raw)               
                    
                    if valid_bpm:
                        bpms.append(bpm)
                        while len(bpms) > 4:
                            bpms.pop(0)
                        self.bpm = np.mean(bpms)
                        if (np.mean(ir_data) < 50000 and np.mean(red_data) < 50000):
                            self.bpm = 0
                            if self.print_result:
                                print("Finger not detected")
                        if self.print_result:
                            print("BPM: {0}, SpO2: {1}".format(self.bpm, spo2))
                            if (self.bpm != -999) and (spo2 != -999):
                                final = {"bpm": self.bpm, "spo2": spo2}
                                final_vals.append(final)
            
            time.sleep(self.LOOP_TIME)
        
        with open(raw_file,'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = raw_headers)
            writer.writeheader()
            writer.writerows(raw_vals)
        
        with open(final_file,'w') as csvfile:
            writerf = csv.DictWriter(csvfile, fieldnames = final_headers)
            writerf.writeheader()
            writerf.writerows(final_vals)
        
        sensor.shutdown()
#     @app.callback(Output('live-graph', 'figure'),[ Input('graph-update', 'n_intervals') ]
# 
# 
#     def update_graph_scatter(n):
#         X.append(X[-1]+1)
#         Y.append(Y[-1]+Y[-1] * random.uniform(-0.1,0.1))
# 
#         data = plotly.graph_objs.Scatter(
#                 x=list(X),
#                 y=list(Y),
#                 name='Scatter',
#                 mode= 'lines+markers'
#         )
# 
#         return {'data': [data],
#                 'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [min(Y),max(Y)]),)}
    
    def start_sensor(self):
        self._thread = threading.Thread(target=self.run_sensor)
        self._thread.stopped = False
        self._thread.start()

    def stop_sensor(self, timeout=2.0):
        self._thread.stopped = True
        self.bpm = 0
        self._thread.join(timeout)


