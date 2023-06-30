'''
Going to try and run a small scale version of the MEC through GSUA before doing the whole thing.
'''

from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import MEC_CAV_GSUA


##########################################################
############## Defining the Model Inputs #################
##########################################################

problem = {
    'num_vars': 5,
    'names': ['Temp','RH','CO2', 'PPFD', 'H'],
    'bounds': [[20,40],       # Temperature
               [60, 90],      # Relative Humidity
               [300, 500],    # Atmo CO2 Concentration
               [200,500],     # PPFD Level
               [0,24]]        # Photoperiod
               }

mec_outputs = ["CQY","CUE_24","DCG",
               "CGR","TCB","TEB",
               "VP_SAT","VP_AIR","VPD",
               "P_GROSS","P_NET","g_S",
               "g_A","g_C","DTR",
               "T_LIGHT","T_DARK","RH",
               "CO2"]

##########################################################
############## Generate the Samples ######################
##########################################################
""" 
    If needed this step of generating parameters may be skipped
    once generated and the simulations performed. The output 
    files will be able to be used for the analysis and charting
"""

# param_values = saltelli.sample(problem, 2**5)      # 2**5 = 32 for 256 samples
# # print(param_values.shape)                    # The samples generates N*((2*D)+2) samples
# df_sims = pd.DataFrame({})
# for i, X in enumerate(param_values):
#     # print(i, X)
#     # this saves each of the 8192 sample parameters.
#     # Columns are Temp, Humidity, CO2, PPFD, H
#     np.savetxt("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_parameters.txt", param_values)
#     SIM_TEMP = X[0]
#     SIM_RH   = X[1]
#     SIM_CO2  = X[2]
#     SIM_PPFD = X[3]
#     SIM_H    = X[4]
#     SIM_NUM = i

##########################################################
######################### Run Model ######################
##########################################################

# if __name__ == '__main__':
#     MEC_CAV_GSUA.RUN_CAV()      # Runs the Cavazzoni utilizing the GSUA_parameters.txt



###########################################################
#################### Analysis #############################
###########################################################

# Create dataframes for each models GSUA runs
df_CAV_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_CAV_out/GSUA_CAV_Simulations.csv')
# Boscheri Verison Placeholder
# Amitrano Version Placeholder

# Loading specific outputs for GSUA analysis 
"""Perhaps I can make a fancy loop here to generate everything needed, then dump them all into charts?"""
Y = np.loadtxt('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_CAV_out/GSUA_CAV_data_DTR.txt') # done to match the SALib example, imports the text file result

# Si = sobol.analyze(problem, Y)
# print(Si)
# """Still need a way to save these results..."""

# Si.plot()
# plt.show()

# print("Temp-RH:", Si['S2'][0,1])
# print("Temp-CO2:", Si['S2'][0,2])
# print("RH-CO2:", Si['S2'][1,2])

###########################################################
#################### VISUALIZATIONS #######################
###########################################################

"""This chart bulding stuff works!"""
VIS_GSUA = df_CAV_sims[['Simulation', 'DTR', 'T_LIGHT', 'RH', 'CO2']]
VIS_GSUA = VIS_GSUA.sort_values('RH', ascending=True)
x = VIS_GSUA[['RH']]
x = x.values.flatten()
y = VIS_GSUA[['DTR']]
y = y.values.flatten()
fig, ax = plt.subplots()
ax.scatter(x, y)
ax.set_ylabel('Daily Transpiration Rate')
ax.set_xlabel('Relative Humidity')

# plt.axhline(y=np.nanmean(y), color='red', linestyle='--', linewidth=3, label='Avg')     # just the straight average of the DTR for all simulations

# calc the trendline
z = np.polyfit(x, y, 1) # 1 is linear, 2 is quadratic! the flatten converts the df to a 1D array
p = np.poly1d(z)
plt.plot(x,p(x),"red")

# fit a linear curve and estimate its y-values and their error.
a, b = np.polyfit(x, y, deg=1)
y_err = x.std() * np.sqrt(1/len(x) + (x - x.mean())**2 / np.sum((x - x.mean())**2))

# trying to add a shaded region to represent XX quantity of the simulations
fig, ax = plt.subplots()
ax.plot(x, y, '-')
ax.fill_between(x, y - y_err, y + y_err, alpha=0.2)
ax.plot(x, y, 'o', color='tab:brown')


# plt.plot(x,p(x)*(1.95),"green")
# plt.plot(x,p(x)*(.05),"green")
# the line equation:
print("y=%fx+(%f)"%(z[0],z[1]))
plt.show()
