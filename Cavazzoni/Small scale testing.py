import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

phs = 9000
DTR = 0
TEB = 0
days = 10

dfinit = pd.DataFrame(
    {
        'Day': [days],
        'DTR': [DTR],
        'TEB': [TEB],
        'Photosynthesis': [phs],
    }, index=[0])
dfrec = pd.DataFrame({})

for day in range(days+1):
    DTR += 2
    TEB += 1
    dfts = pd.DataFrame({
            'Day': [day],
            'DTR': [DTR],
            'TEB': [TEB],
            'Photosynthesis': [phs],
            })
    dfrec = pd.concat([dfrec, dfts], ignore_index=True)

dfrec.plot(x='Day', y=['DTR', 'TEB'], marker='o')
plt.show()