import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

phs = 50
DTR = 0
TEB = 0

t = 0               # time in days
res = 1             # model resolution (in hours)
t_M = 10            # time to harvest (days)
i = 0               # matrix/loop counter
I = 1               # boscheri "I is equal to 1 and 0 during the photoperiod (day) and dark period (night)"

dfrec = pd.DataFrame({})
df_day = pd.DataFrame({})

ts_to_harvest = int(t_M*24/res)             # calcs the timesteps needed to set up the matrix for each ts
day = 0

while t <= ts_to_harvest:
    DTR += 2*day
    TEB += 1
    if (t % 24) == 0:                       # this if statement counts the days by checking if the ts/24 is a whole number
        day += 1
        if t == 0:                          # need this because 0/24 = 0 triggering day counter
            day = 0
    dfts = pd.DataFrame({
            'ts': [t],
            'Day': [day],
            'DTR': [DTR],
            'TEB': [TEB],
            'Photo': [phs],
            })
    dfrec = pd.concat([dfrec, dfts], ignore_index=True)
    df_day = dfrec.groupby(['Day']).sum()
    t += 1
print(df_day)
# print(dfrec)

# full_chart = dfrec.plot(x='ts', marker='o')
# full_chart.set_ylabel('ALL THE UNITS!')
# plt.title('ALL THE DATA!')
# plt.show()