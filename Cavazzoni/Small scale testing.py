import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

phs = 9000
DTR = 0
TEB = 0
days = 30

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
print(dfrec)
# dfrec.to_csv('C:/Users/donal/Documents/Github/Modified-Energy-Cascade/Cavazzoni/SST_OUT.csv')
# print(dfrec.loc[:, 'TEB'])

sns.set_theme()

fig1 = sns.lineplot(x=day, y=dfrec.loc[:,'TEB'])
fig1_data = pd.DataFrame({'Day' = dfrec.loc[:, 'Day']})
plt.show()