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
# Boscheri Verison Placeholder
# Amitrano Version Placeholder



###########################################################
#################### Analysis #############################
###########################################################

# Create dataframes for each models GSUA runs
df_CAV_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_CAV_out/data/GSUA_CAV_Simulations.csv')
# Boscheri Verison Placeholder
# Amitrano Version Placeholder

# Loading specific outputs for GSUA analysis 
"""Perhaps I can make a fancy loop here to generate everything needed, then dump them all into charts?"""
Y = np.loadtxt('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_CAV_out/data/GSUA_CAV_data_DTR.txt') # done to match the SALib example, imports the text file result

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

u = "\u00B5"        # unicode for the micro symbol
# This list of lists defines the short name, full name and units for the inputs/outputs used in charts.
mec_ouputs = [  
            ["A", "Absorption", ""],
            ["CQY", "Canopy Quantum Yield", u+"mol$_{fixed}$ "+u+"mol$_{aborbed}$"],
            ["CUE_24", "Carbon Use Efficiency", ""],
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

for item in mec_inputs:        # this allows easy injection of labels into chart elements
    input_short_name = item[0]
    input_long_name = item[1]
    input_unit = item[2]
    for label in mec_ouputs:
        output_short_name = label[0]
        output_long_name = label[1]
        output_unit = label[2]

        """This chart bulding stuff works!"""
        VIS_GSUA = df_CAV_sims[['Simulation', output_short_name, input_short_name]]
        VIS_GSUA = VIS_GSUA.sort_values(input_short_name, ascending=True)
        x = VIS_GSUA[[input_short_name]]
        x = x.values.flatten()
        y = VIS_GSUA[[output_short_name]]
        y = y.values.flatten()
        fig, ax = plt.subplots()
        ax.scatter(x, y)
        ax.set_ylabel(output_long_name)
        ax.set_xlabel(input_long_name)
        plt.title(f'{input_short_name} x {output_short_name}')
        # plt.axhline(y=np.nanmean(y), color='red', linestyle='--', linewidth=3, label='Avg')     # just the straight average of the DTR for all simulations

        # calc the trendline
        z = np.polyfit(x, y, 2) # 1 is linear, 2 is quadratic! the flatten converts the df to a 1D array
        p = np.poly1d(z)
        plt.plot(x,p(x),"red")

        # fit a linear curve and estimate its y-values and their error.
        # a, b = np.polyfit(x, y, deg=1)
        # y_err = x.std() * np.sqrt(1/len(x) + (x - x.mean())**2 / np.sum((x - x.mean())**2))

        # trying to add a shaded region to represent XX quantity of the simulations

        # plt.plot(x,p(x)*(1.95),"green")
        # plt.plot(x,p(x)*(.05),"green")
        # the line equation:
        # print("y=%fx+(%f)"%(z[0],z[1]))

        plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_CAV_out/figures/{input_short_name} x {output_short_name}.png', bbox_inches='tight') #there are many options for savefig
        # in the likely rare event all of these need to be viewed...
        # plt.show()