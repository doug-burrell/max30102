import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


# ---- raw data
df_raw = pd.read_csv('raw_values.csv')
plt.subplot(3,2,1)
plt.plot(df_raw['ir_data'])
plt.title('ir_data')

plt.subplot(3,2,2)
plt.plot(df_raw['red_data'])
plt.title('red_data')

plt.subplot(3,2,3)
plt.plot(df_raw)
plt.title('raw data')

# 'x' son muestras
# 'y' resultado


# ---- post calc
df_final = pd.read_csv('final_values.csv')

plt.subplot(3,2,4)
plt.plot(df_final['bpm'])
plt.title('bpm')

plt.subplot(3,2,5)
plt.plot(df_final['spo2'])
plt.title('spo2')

plt.show()
