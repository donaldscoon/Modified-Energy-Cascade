import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

phs = 9000
DTR = 0
TEB = 0
days = 10


T_LIST = [24.87, 24.84, 24.87, 24.84, 24.85, 
           24.87, 24.72, 24.87, 24.74, 24.74, 
           24.07, 23.93, 23.83, 23.89, 23.58, 
           23.88, 24.09, 24.21, 24.03, 23.73, 
           24.02, 24.02, 24.02]

dfinit = pd.DataFrame(
    {
        'Day': [days],
        'DTR': [DTR],
        'TEB': [TEB],
        'Photosynthesis': [phs],
    }, index=[0])
dfrec = pd.DataFrame({})

for day in range(days+1):
    DTR += 2*day
    TEB += 1
    dfts = pd.DataFrame({
            'Day': [day],
            'DTR': [DTR],
            'TEB': [TEB],
            'Photo': [phs],
            })
    dfrec = pd.concat([dfrec, dfts], ignore_index=True)
    
print(dfrec)    
# fig, ax = plt.subplots()
# ax.plot(dfrec['Day'],dfrec['TEB'],color = 'blue')
# ax.tick_params(axis='y',labelcolor='blue')
# ax2=ax.twinx()
# ax2.plot(dfrec['Day'],dfrec['DTR'],color = 'green')
# plt.show()