from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.sample import morris
from SALib import ProblemSpec
from datetime import datetime
from SALib.test_functions import Ishigami


import SALib as SALib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)

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


problem = ProblemSpec({
    'names': ['TEMP', 'RH', 'CO2', 'PPFD', 'H'],
    'num_vars': 5,
    'bounds': [[5,40,0.54286],      # Temperature Peak at 24 
               [35,100,0.38461],    # Relative Humidity Peak at 60
               [330,1300,0.48453],  # Atmo CO2 Concentration Peak at 800
               [0,1100,0.27273],    # PPFD Level Peak at 300
               [0,24, 0.66667]],    # Photoperiod Peak at 16
    'dists': ['triang', 'triang', 'triang', 'triang', 'triang'],
    # 'groups': None
    })

###########################################################
#################### Analysis #############################
###########################################################


# def ANALYZE():

#     # Create dataframes for each models GSUA runs
#     df_AMI_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_AMI_out/data/GSUA_AMI_Simulations.csv')
#     df_BOS_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_BOS_out/data/GSUA_BOS_Simulations.csv')
#     df_CAV_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_CAV_out/data/GSUA_CAV_Simulations.csv')

#     X = np.loadtxt('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/SOBOL_parameters.txt')

#     EE_out_df = pd.DataFrame()

#     for item in models:                 # loop for model names
#         model_short_name = item[0]
#         model_long_name = item[1]
#         for item in mec_outputs:        # loop for output names
#             output_short_name = item[0]
#             output_long_name = item[1]
#             output_unit = item[2]
#             # Loading specific outputs for Morris EE analysis 
#             Y = np.loadtxt(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_{model_short_name}_out/data/GSUA_{model_short_name}_data_{output_short_name}.txt') # done to match the SALib example, imports the text file result
#             EE = SALib.analyze.morris.analyze(problem, X, Y, conf_level=0.95, num_levels=128) # analyzes the Elementary effects for each models ouput

#             with open(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/full_out/{model_short_name}_{output_short_name}_EE_results.txt', 'w') as f:
#                 results_df = EE.to_df()
#                 f.write(str(results_df))
#             f.close

#             # create a big ol honking dataframe
#             mu_output_key = f'{model_short_name}_{output_short_name}_mu'
#             mu_star_output_key = f'{model_short_name}_{output_short_name}_mu_star'
#             mu_star_conf_output_key = f'{model_short_name}_{output_short_name}__mu_star_conf'
#             sigma_output_key = f'{model_short_name}_{output_short_name}_sigma'

#             EE_out_df[mu_output_key] = EE['mu']
#             EE_out_df[mu_star_output_key] = EE['mu_star']
#             EE_out_df[mu_star_conf_output_key] = EE['mu_star_conf']
#             EE_out_df[sigma_output_key] = EE['sigma']
#     EE_out_df.to_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/EE_out.csv', index=False)

# # Executes this program/function
# if __name__ ==('__main__'):
#     ANALYZE()

def CHART():
    ami_c = '#2A119B'
    bos_c = '#067300'
    cav_c = '#8C0004'

# perhaps I can write some kind of script to set these
# so I don't have to write it out completely each time?
# symbols differntiate models
# AMI= 'o' blue
# BOS= 's' green
# CAV= '^' red

# colors differentiate from paletton.com
#     dark blue   = #2A119B
#     blue        = #5E46C6
#     light blue  = #A798EC
#     dark green  = #067300
#     green       = #09B600
#     light green = #96F391
#     dark red    = #8C0004
#     red         = #DF0006
#     light red   = #FE989A

    # read in the data
    EE_out_df = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/EE_out.csv')

    # mu star by sigma with a 1/1 line

    mu_values = EE_out_df['AMI_DTR_mu_star']
    sigma_values = EE_out_df['AMI_DTR_sigma']
    
    mu_temp        = mu_values[0]
    sigma_temp  = sigma_values[0]

    mu_rh        = mu_values[1]
    sigma_rh  = sigma_values[1]

    mu_CO2        = mu_values[2]
    sigma_CO2  = sigma_values[2]

    mu_PPFD        = mu_values[3]
    sigma_PPFD  = sigma_values[3]

    mu_H        = mu_values[4]
    sigma_H  = sigma_values[4]

    # Create the scatter plot
    plt.scatter(mu_temp, sigma_temp,    s=50, color='red', label= "TEMP")
    plt.scatter(mu_rh, sigma_rh,        s=50, color='blue', label= "RH")
    plt.scatter(mu_CO2, sigma_CO2,      s=50, color='green', label= "CO2")
    plt.scatter(mu_PPFD, sigma_PPFD,    s=50, color='yellow', label= "PPFD")
    plt.scatter(mu_H, sigma_H,          s=50, color='black', label= "H")

    # Add a dashed line for the 1-to-1 relationship
    plt.plot([min(mu_values), max(mu_values)], [min(sigma_values), max(sigma_values)], 'k--')

    # Set the labels and title
    plt.xlabel('mu')
    plt.ylabel('sigma')
    plt.title('Scatter Plot of mu vs sigma')
    plt.legend()
    plt.show()

    # mu by sigma with the V
# Executes this program/function
if __name__ ==('__main__'):
    CHART()