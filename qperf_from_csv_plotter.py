import pandas as pd
import matplotlib.pyplot as plt

df_bw=pd.read_csv("tcp_test_batman/qperf_bw3.csv")
df_lat=pd.read_csv("tcp_test_batman/qperf_lat3.csv")  

plt.plot(range(len(df_bw['send_bw'])), df_bw['send_bw']) 
plt.xlabel("Run number")
plt.ylabel("Bandwith [Gb/s]")
plt.figure()
plt.plot(range(len(df_lat['latency'])), df_lat['latency']) 
plt.xlabel("Run number")
plt.ylabel("Latency [us]")
                              
