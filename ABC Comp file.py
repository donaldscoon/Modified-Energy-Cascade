import pandas as pd
import matplotlib.pyplot as plt
import numpy as mp

##################################################
################## MODEL INPUTS ##################
##################################################
PPFD = 314.54       # found at Amitrano 2020 table 2 but used decimal value in GN excel
CO2 = 370           # value used in Amitranos excel
H = 12              # Amitrano 2020 table 2
T_LIGHT = 24.35105263 # AVG from amitranos GN exp
RH = 0.810470947      # AVG from amitranos GN exp
t = 1               # time in days
res = 1             # model resolution (in days)  boscheri was hourly and totaled or averaged for the day
i = 0               # matrix/loop counter


##################################################
################ Pull in the data ################
##################################################

ami = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/MEC_AMI_OUT_comp.csv")
bos_tot = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/BOS_OUT_comp.csv")
bos_avg = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/BOS_OUT_AVG_comp.csv")
cav = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/MEC_CAV_OUT_comp.csv")


bigdf = pd.merge(pd.merge(pd.merge(bos_avg, bos_tot, on='Day'), ami, on='Day'), cav, on='Day')
# print(bigdf)

##################################################
###############   Start Charting  ################
##################################################
# VP_chart_data = df_records[['Timestep', 'VP_AIR', 'VP_SAT', 'VPD']]
# VP_chart = VP_chart_data.plot(x='Timestep', marker='o')
# VP_chart.set_ylabel('kPa')
# plt.title('Vapor Pressures')
# plt.show()

abchart_data = bigdf[['Day', 'AMI_alpha', 'AMI_beta']]