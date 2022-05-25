from heartrate_monitor import HeartRateMonitor
import time
import argparse
import dash
import pandas as pd
import matplotlib.pyplot as plt

t = 30

parser = argparse.ArgumentParser(description="Read and print data from MAX30102")
parser.add_argument("-r", "--raw", action="store_true",
                    help="print raw data instead of calculation result")
args = parser.parse_args()

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

## plot
# df_raw = pd.read_csv('raw_values.csv')
# plt.plot(df_raw)
# df_final = pd.read_csv('final_values.csv')
# plt.plot(df_final)

# plt.show()