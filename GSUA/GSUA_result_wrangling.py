from SALib import ProblemSpec
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

u = "\u00B5"        # unicode for the micro symbol

models = [
         ["AMI", "Amitrano"], 
         ["BOS", "Boscheri"], 
         ["CAV", "Cavazzoni"]
         ]

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
            ["P_GROSS", "Gross Photosynthesis", u+"mol$_{carbon}$ m$^{-2}$ second$^{-1}$"],
            ["P_NET", "Net Photosynthesis", u+"mol$_{carbon}$ m$^{-2}$ second$^{-1}$"],
            ["g_S", "Stomatal Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$"],
            ["g_A", "Atmospheric Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$"],
            ["g_C", "Canopy Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$"],
            ["DTR", "Daily Tranpiration Rate", "L$_{water}$ m$^{-2}$ day$^{-1}$"]
]

for item in models:                     # loop for model names
    model_short_name = item[0]
    model_long_name = item[1]
    for item in mec_outputs:        # loop for outputs
        output_short_name = item[0]
        output_long_name = item[1]
        output_unit = item[2]
        # print(f'{model_short_name}_{output_short_name}')
        try:
            with open(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/{model_short_name}_{output_short_name}_results.txt', 'r') as reader:
                for line in reader.readlines():
                    # df_records = pd.DataFrame({})
                    print(line, end='')
        except IOError:
            pass
        # with open(f"C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/{model_short_name}_{output_short_name}_results.txt", "r") as f:
        #     print(f)
            # if Y[0] == Y[20]: # identifying constant outputs
                # if identified here it does not mean that they are constant throughout the simulation
                # just that the final value is constant such as CUE_24 which hits a max  
                # f.write(f'{model_short_name} {output_short_name} \n')    # writing them to a text file
                # continue
        # f.close()