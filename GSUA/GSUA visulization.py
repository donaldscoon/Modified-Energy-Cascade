from SALib import ProblemSpec
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

models = [
         ["AMI", "Amitrano"], 
         ["BOS", "Boscheri"], 
         ["CAV", "Cavazzoni"]
         ]

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
            ["PPFD", "Photosynthetic Photon Flux", u+"mol$_{fixed}$ m$^{-2}$ second$^{-1}$"],
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

model_inputs = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_parameters.txt", sep=" ", names=['TEMP', 'RH', 'CO2', 'PPFD', 'H'])
df_AMI_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_AMI_out/data/GSUA_AMI_Simulations.csv')
df_BOS_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_BOS_out/data/GSUA_BOS_Simulations.csv')
df_CAV_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_CAV_out/data/GSUA_CAV_Simulations.csv')

# perhaps I can write some kind of script to set these
# so I don't have to write it out completely each time?
# symbols differntiate models
# AMI= 'o'
# BOS= 's'
# CAV= '^'
# colors differentiate parameters from paletton.com
#     dark blue   = #2A119B
#     blue        = #5E46C6
#     light blue  = #A798EC
#     dark green  = #067300
#     green       = #09B600
#     light green = #96F391
#     dark red    = #8C0004
#     red         = #DF0006
#     light red   = #FE989A

##############################################
########### Input  Historgram ########
##############################################

fig, ax = plt.subplots()
ax.hist(model_inputs['TEMP'], 10, density=True, histtype='bar', color='#5E46C6', label='AMI')
ax.legend(prop={'size': 10})
ax.set_title('Temperature')
plt.show()


# for item in models:                 # loop for model names
#     model_short_name = item[0]
#     model_long_name = item[1]
#     for item in mec_inputs:        # loop for inputs
#         input_short_name = item[0]
#         input_long_name = item[1]
#         input_unit = item[2]
#         for item in mec_outputs:       # loop for outputs
#             output_short_name = item[0]
#             output_long_name = item[1]
#             output_unit = item[2]