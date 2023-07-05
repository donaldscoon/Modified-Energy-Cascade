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
models = [
         ["AMI"], 
         ["BOS"], 
         ["CAV"]
         ]

problem = {
    'num_vars': 5,
    'names': ['Temp','RH','CO2', 'PPFD', 'H'],
    'bounds': [[20,40],       # Temperature
               [60, 90],      # Relative Humidity
               [300, 500],    # Atmo CO2 Concentration
               [200,500],     # PPFD Level
               [0,24]]        # Photoperiod
               }

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

""" I would like to find a way to state the length of
the simulations here that is fed into the models automatically."""


##########################################################
######################### Run Models #####################
##########################################################


# if __name__ == '__main__':
    # MEC_CAV_GSUA.RUN_SIM()      # Runs just the simulations for the Cavazzoni Model
    # MEC_CAV_GSUA.RUN_CHART()    # Runs just the charting for the Cavazzoni Model
    # MEC_CAV_GSUA.RUN_FULL()     # Runs both the simulations and charting for the Cavazzoni Model

# # Boscheri Verison Placeholder
#     MEC_BOS_GSUA.RUN_SIM()      # Runs just the simulations for the Boscheri Model
#     MEC_BOS_GSUA.RUN_CHART()    # Runs just the charting for the Boscheri Model
#     MEC_BOS_GSUA.RUN_FULL()     # Runs both the simulations and charting for the Boscheri Model

# # Amitrano Version Placeholder
#     MEC_AMI_GSUA.RUN_SIM()      # Runs just the simulations for the Amitrano Model
#     MEC_AMI_GSUA.RUN_CHART()    # Runs just the charting for the Amitrano Model
#     MEC_AMI_GSUA.RUN_FULL()     # Runs both the simulations and charting for the Amitrano Model



###########################################################
#################### Analysis #############################
###########################################################

# Create dataframes for each models GSUA runs
df_CAV_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_CAV_out/data/GSUA_CAV_Simulations.csv')
# Boscheri Verison Placeholder
# Amitrano Version Placeholder

# Loading specific outputs for GSUA analysis 

# Perhaps I can make a fancy loop here to generate everything needed, then dump them all into charts?

Y = np.loadtxt('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_CAV_out/data/GSUA_CAV_data_DTR.txt') # done to match the SALib example, imports the text file result

Si = sobol.analyze(problem, Y)
# print(Si)
# Still need a way to save these results...

Si.plot()
plt.show()
plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_CAV_out/figures/CAV_Box_and_Whisker.png', bbox_inches='tight') #there are many options for savefig


# print("Temp-RH:", Si['S2'][0,1])
# print("Temp-CO2:", Si['S2'][0,2])
# print("RH-CO2:", Si['S2'][1,2])

###########################################################
#################### VISUALIZATIONS #######################
###########################################################

# use the completed visualizations for each model version to create an overlay of all three here