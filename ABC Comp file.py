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
g_A = 2.5           # atmospheric aerodynamic conductance ewert eq 4-27 no citations



##################################################
################ Pull in the data ################
##################################################

ami = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/MEC_AMI_OUT_comp.csv")
bos_tot = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/BOS_OUT_comp.csv")
bos_avg = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/BOS_OUT_AVG_comp.csv")
cav = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/MEC_CAV_OUT_comp.csv")

bigdf = pd.merge(pd.merge(pd.merge(bos_avg, bos_tot, on='Day'), ami, on='Day'), cav, on='Day')
bigdf.to_csv('C:/Users/donal/Documents/Github/Modified-Energy-Cascade/ABC_comp.csv') # exports final data frame to a CSV
# print(bigdf)

##################################################
###############   Start Charting  ################
##################################################

######## Alpha and Beta Comparison ##############
fig, ax = plt.subplots()
ax.plot(bigdf['Day'], bigdf['AMI_alpha'],       marker='o', color='lightgreen',     label='AMI α')
ax.plot(bigdf['Day'], bigdf['AMI_beta'],        marker='o', color='green',          label='AMI β')
ax.plot(bigdf['Day'], bigdf['BOS_AVG_ALPHA'],   marker='o', color='lightblue',      label='BOS α')
ax.plot(bigdf['Day'], bigdf['BOS_AVG_BETA'],    marker='o', color='blue',           label='BOS β')
ax.plot(bigdf['Day'], bigdf['CAV_ALPHA'],       marker='o', color='gold',           label='CAV α')
ax.plot(bigdf['Day'], bigdf['CAV_BETA'],        marker='o', color='goldenrod',      label='CAV β')
ax.set_ylabel('Unsure about units')
ax.set_xlabel('Days After Emergence')
plt.figlegend(bbox_to_anchor=(-0.21, 0.39, 0.5, 0.5))
plt.title('Alpha and Beta Comparison')
plt.savefig('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/Comparison Charts/Alpha_Beta_Comparison.png') #there are many options for savefig
plt.show()

####################### A, CQY, CUE, ###################################
fig, ax = plt.subplots()
ax.plot(bigdf['Day'], bigdf['BOS_AVG_A'],      marker='o', color='lightblue',  label='BOS A')
ax.plot(bigdf['Day'], bigdf['BOS_AVG_CUE_24'], marker='o', color='blue',       label='BOS CUE')
ax.plot(bigdf['Day'], bigdf['CAV_A'],          marker='o', color='gold',       label='CAV A')
ax.plot(bigdf['Day'], bigdf['CAV_CUE_24'],     marker='^', color='goldenrod',  label='CAV CUE')
ax.set_ylabel('Fractional')
ax2 = ax.twinx()
ax2.plot(bigdf['Day'], bigdf['BOS_AVG_CQY'],    marker='o', color='deepskyblue',label='BOS CQY')
ax2.plot(bigdf['Day'], bigdf['CAV_CQY'],        marker='^', color='khaki',  label='CAV CQY')
ax2.set_facecolor('darkred')
ax2.set_ylabel('μmol$_{Carbon}$ μmol$_{Photon}^{-1}$', color='darkred')
ax2.tick_params(axis='y',labelcolor='darkred')
ax.set_xlabel('Days After Emergence')
plt.figlegend(bbox_to_anchor=(0.40, -0.1, 0.5, 0.5))
plt.title('A CUE CQY Comparison')
plt.savefig('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/Comparison Charts/A_CUE_CQY_Comparison.png', bbox_inches='tight') #there are many options for savefig
plt.show()

########### Conductances #########################
fig, ax = plt.subplots()
ax.plot(bigdf['Day'], bigdf['AMI_g_S'],     marker='o', color='green',      label='AMI g$_S$')
ax.plot(bigdf['Day'], bigdf['AMI_g_C'],     marker='o', color='lightgreen', label='AMI g$_C$')
ax.plot(bigdf['Day'], bigdf['BOS_AVG_g_S'], marker='o', color='blue',       label='BOS g$_S$')
ax.plot(bigdf['Day'], bigdf['BOS_AVG_g_C'], marker='o', color='lightblue',  label='BOS g$_C$')
ax.plot(bigdf['Day'], bigdf['CAV_g_S'],     marker='o', color='goldenrod',  label='CAV g$_S$')
ax.plot(bigdf['Day'], bigdf['CAV_g_C'],     marker='o', color='gold',       label='CAV g$_C$')
ax.set_ylabel('mol$_{water}$ m$^{-2}$ second $^{-1}$')
ax.set_xlabel('Days After Emergence')
plt.figlegend(bbox_to_anchor=(-0.185, 0.39, 0.5, 0.5))
plt.title('Conductances')
plt.savefig('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/Comparison Charts/Conductances_Comparison.png') #there are many options for savefig
plt.show()

################### Photosynthesis #####################
fig, ax = plt.subplots()
ax.plot(bigdf['Day'], bigdf['AMI_P_GROSS'],     marker='o', color='green',      label='AMI P$_{GROSS}$')
ax.plot(bigdf['Day'], bigdf['AMI_P_NET'],       marker='o', color='lightgreen', label='AMI P$_{NET}$')
ax.plot(bigdf['Day'], bigdf['BOS_AVG_P_NET'],   marker='o', color='lightblue',  label='BOS P$_{NET}$')
ax.plot(bigdf['Day'], bigdf['CAV_P_GROSS'],     marker='o', color='goldenrod',  label='CAV P$_{GROSS}$')
ax.plot(bigdf['Day'], bigdf['CAV_P_NET'],       marker='o', color='gold',       label='CAV P$_{NET}$')
ax.set_ylabel('μmol$_{Carbon}$ m$^{-2}$ second$^{-1}$')
ax.set_xlabel('Days After Emergence')
plt.figlegend(bbox_to_anchor=(-0.16, 0.39, 0.5, 0.5))
plt.title('Photosynthesis')
plt.savefig('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/Comparison Charts/Photosynthesis_Comparison.png') #there are many options for savefig
plt.show()

