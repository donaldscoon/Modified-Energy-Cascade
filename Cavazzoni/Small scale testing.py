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
# print(dfrec)

# DTR_data= dfrec.loc[:,'DTR']
# sns.set_theme()
# figTEB = sns.lineplot(x = dfrec['Day'], y = dfrec['TEB'])
# # # fig1_data = pd.DataFrame({'Day' = dfrec.loc[:, 'Day']})
# plt.show()
