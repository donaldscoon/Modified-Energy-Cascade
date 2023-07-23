'''
Going to try and run a small scale version of the MEC through GSUA before doing the whole thing.
'''

from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib import ProblemSpec
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

import MEC_AMI_GSUA
import MEC_BOS_GSUA
import MEC_CAV_GSUA
import GSUA_visulization


##########################################################
############## Defining the Model Inputs #################
##########################################################
# -------------------------------------------------------------------------------------
""" YO YO YO YO YO YO BIG CODING GENIUS
I Think you should make the models/inputs/ouputs defining and lists a function...
go for it buddy! """
# -------------------------------------------------------------------------------------

models = [
         ["AMI", "Amitrano"], 
         ["BOS", "Boscheri"], 
         ["CAV", "Cavazzoni"]
         ]

# this is leftover from before I figured out the better method
# problem = {
#     'num_vars': 5,
#     'names': ['Temp','RH','CO2', 'PPFD', 'H'],
#     'bounds': [[5,40],       # Temperature
#                [35,100],      # Relative Humidity
#                [330,1300],    # Atmo CO2 Concentration
#                [0,1100],     # PPFD Level
#                [0,24]]        # Photoperiod
#                }

u = "\u00B5"        # unicode for the micro symbol

mec_outputs = [  
            ["A", "Absorption", ""],
            ["CQY", "Canopy Quantum Yield", u+"mol$_{fixed}$ "+u+"mol$_{aborbed}$"],
            ["CUE_24", "Carbon Use Efficiency", ""],
            ["ALPHA", "A*CQY*CUE_24", ""],
            ["BETA", "A*CQY", ""],
            ["DCG", "Daily Carbon Gain", "mol$_{carbon}$ m$^{-2}$ day$^{-1}$"],
            ["CGR", "Crop Growth Rate", "grams m$^{-2}$ day$^{-1}$"],
            ["TCB", "Total Crop Biomass", "grams m$^{-2}$"],
            ["TEB", "Total Edible Biomass", "grams m$^{-2}$"],
            ["VP_SAT", "Saturated Moisture Vapor Pressure", "kPa"],
            ["VP_AIR", "Actual Moisture Vapor Pressure", "kPa"],
            ["VPD", "Vapor Pressure Deficit", "kPa"],
            ["P_GROSS", "Gross Canopy Photosynthesis", u+"mol$_{carbon}$ m$^{-2}$ second$^{-1}$"],
            ["P_NET", "Net Canopy Photosynthesis", u+"mol$_{carbon}$ m$^{-2}$ second$^{-1}$"],
            ["g_S", "Stomatal Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$"],
            ["g_A", "Atmospheric Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$"],
            ["g_C", "Canopy Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$"],
            ["DTR", "Daily Tranpiration Rate", "L$_{water}$ m$^{-2}$ day$^{-1}$"]
]

mec_inputs = [
            ["T_LIGHT", "Light Cycle Temperature", "Degrees Celsius"],
            ["T_DARK", "Dark Cycle Temperature", "Degrees Celsius"],
            ["RH", "Relative Humidity", "%"],
            ["CO2", "CO$_{2}$ Concentration", u+"mol$_{carbon}$ mol$_{air}$"],
            ["PPFD", "Photosynthetic Photon Flux", u+"mol$_{photons}$ m$^{-2}$ second$^{-1}$"],
            ["H", "Photoperiod", "hours day$^{-1}$"]
]

sp = ProblemSpec({
    'names': ['TEMP', 'RH', 'CO2', 'PPFD', 'H'],
    'bounds': [[5,40,0.68571],      # Temperature
               [35,100,0.92308],    # Relative Humidity
               [330,1300,0.82474],  # Atmo CO2 Concentration
               [0,1100,0.27273],    # PPFD Level
               [0,24, 0.66667]],    # Photoperiod
    'dists': ['triang',             # Temperature
              'triang',             # Relative Humidity
              'triang',             # Atmo CO2
              'triang',             # PPFD
              'triang'],            # Photoperiod
    'outputs': ['Y']
})


##########################################################
############## Generate the Samples ######################
##########################################################
""" 
    If needed this step of generating parameters may be skipped
    once generated and the simulations performed. The output 
    files will be able to be used for the analysis and charting
"""

sim_start=datetime.now()
print("Generating the samples")
param_values = sp.sample_sobol(2**6, calc_second_order=True) # sobol sampling 2**6 generates 768 samples
# print(sp.samples)

# param_values = saltelli.sample(problem, 2**6)      # according to an equation from meeting with carpena I need 768 this outs 768 samples
# print(param_values.shape)                    # The samples generates N*((2*D)+2) samples
for i, X in enumerate(sp.samples):
    # print(i, X)
#     # this saves each of the sample parameters.
#     # Columns are Temp, Humidity, CO2, PPFD, H
    np.savetxt("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_parameters.txt", sp.samples)
    SIM_TEMP = X[0]
    SIM_RH   = X[1]
    SIM_CO2  = X[2]
    SIM_PPFD = X[3]
    SIM_H    = X[4]
    SIM_NUM = i

print('sobol sampling completed, proceeding to the simulations')
# """ I would like to find a way to state the length of
# the simulations here that is fed into the models automatically."""


##########################################################
######################### Run Models #####################
##########################################################

if __name__ == '__main__':
#     # MEC_AMI_GSUA.RUN_SIM()      # Runs just the simulations for the Amitrano Model
#     # MEC_BOS_GSUA.RUN_SIM()      # Runs just the simulations for the Boscheri Model
#     # MEC_CAV_GSUA.RUN_SIM()      # Runs just the simulations for the Cavazzoni Model

#     # MEC_AMI_GSUA.RUN_CHART()    # Runs just the charting for the Amitrano Model
#     # MEC_BOS_GSUA.RUN_CHART()    # Runs just the charting for the Boscheri Model
#     # MEC_CAV_GSUA.RUN_CHART()    # Runs just the charting for the Cavazzoni Model

    MEC_AMI_GSUA.RUN_FULL()     # Runs both the simulations and charting for the Amitrano Model
    MEC_BOS_GSUA.RUN_FULL()     # Runs both the simulations and charting for the Boscheri Model
    MEC_CAV_GSUA.RUN_FULL()     # Runs both the simulations and charting for the Cavazzoni Model
    sim_time = datetime.now()-sim_start
    print(f"All three models have run. It took {sim_time}")

###########################################################
#################### Analysis #############################
###########################################################
print("Beginning Analysis of simulations")
analysis_start=datetime.now()

# Create dataframes for each models GSUA runs
df_AMI_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_AMI_out/data/GSUA_AMI_Simulations.csv')
df_BOS_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_BOS_out/data/GSUA_BOS_Simulations.csv')
df_CAV_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_CAV_out/data/GSUA_CAV_Simulations.csv')

for item in models:                 # loop for model names
    model_short_name = item[0]
    model_long_name = item[1]
    for item in mec_outputs:        # loop for output names
        output_short_name = item[0]
        output_long_name = item[1]
        output_unit = item[2]
        # Loading specific outputs for GSUA analysis 
        Y = np.loadtxt(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_{model_short_name}_out/data/GSUA_{model_short_name}_data_{output_short_name}.txt') # done to match the SALib example, imports the text file result
        # print(Y)
        sp.set_results(Y)

        # this file may not truly overwrite itself completely, delete to be sure
        with open("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/constant_outputs.txt", "a") as f:
            if Y[0] == Y[20]: # identifying constant outputs
                # if identified here it does not mean that they are constant throughout the simulation
                # just that the final value is constant such as CUE_24 which hits a max  
                f.write(f'{model_short_name} {output_short_name} \n')    # writing them to a text file
                continue
        f.close()

        sp.set_results(Y)
        sp.analyze_sobol()
        # print(f'{model_short_name}_{output_short_name}_ST', sp.analysis['ST'])
        # print(f'{model_short_name}_{output_short_name}_S1', sp.analysis['S1'])
        # print(f'{model_short_name}_{output_short_name}_S2', sp.analysis['S2'])

        # this saving the results part is still pretty garbage. better than nothing though. 
        with open(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/{model_short_name}_{output_short_name}_results.txt', 'a') as f:
            sp.set_results(Y)
            sp.analyze_sobol()
            results_df = sp.to_df()
            f.write(str(results_df))
        f.close
        # print(model_short_name, output_short_name)
        # print(sp)

analysis_time = datetime.now()-sim_start
print(f"All three models analyzed. It took {analysis_time}")


###########################################################
#################### VISUALIZATIONS #######################
###########################################################

GSUA_visulization.GSUA_CHARTS()

###########################################
############ To Do ########################
###########################################

# line 21