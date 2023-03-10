import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

phs = 50
DTR = 0
TEB = 0

t = 0               # time in days
res = 1             # model resolution (in hours)
t_M = 5            # time to harvest (days)
i = 0               # matrix/loop counter
I = 0               # boscheri "I is equal to 1 and 0 during the photoperiod (day) and dark period (night)"
H = 16              # length of photo period
night_len = 24 - H    # length of night
day_len = 24 - night_len  # length of day
pp_count = 0        # photoperiod counter

dfrec = pd.DataFrame({})
df_day = pd.DataFrame({})

ts_to_harvest = int(t_M*24/res)             # calcs the timesteps needed to set up the matrix for each ts
day = 0

while t <= ts_to_harvest:
    if I == 0 and pp_count == night_len:    # turns night to day
        I = 1
        pp_count = 0
    elif I == 1 and pp_count == day_len:    # turns day to night
        I = 0
        pp_count = 0
    if (t % 24) == 0:                       # this if statement counts the days by checking if the ts/24 is a whole number
        day += 1
        if t == 0:                          # need this because 0/24 = 0 triggering day counter
            day = 0
    DTR += 2*day
    TEB += 1
    dfts = pd.DataFrame({
            'ts': [t],
            'Day': [day],
            'I': [I],
            'DTR': [DTR],
            'TEB': [TEB],
            'Photo': [phs],
            })
    dfrec = pd.concat([dfrec, dfts], ignore_index=True)
    df_day = dfrec.groupby(['Day']).sum()
    pp_count += 1
    print(t, day)
    t += 1

# print(df_day)
# print(dfrec)

# full_chart = dfrec.plot(x='ts', marker='o')
# full_chart.set_ylabel('ALL THE UNITS!')
# plt.title('ALL THE DATA!')
# plt.show()