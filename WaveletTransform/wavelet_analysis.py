import pywt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
plt.style.use('seaborn')

from wavelet_visualize import plot_wavelet, plot_signal, plot_fft_plus_power



# dataset = "sst_nino3.dat"
# df_nino = pd.read_table(dataset,header=None)


dataset = "monsoon.txt"
df_nino = pd.read_table(dataset,skiprows=19,header=None)

print(df_nino.head())

N = df_nino.shape[0]
t0=1871
dt=0.25
time = np.arange(0, N) * dt + t0
# print(time)
signal = df_nino.values.squeeze()
signal = signal- np.mean(signal)

scales = np.arange(1, 128)


plot_signal(time, signal)
plot_fft_plus_power(time, signal)
plot_wavelet(time, signal, scales)