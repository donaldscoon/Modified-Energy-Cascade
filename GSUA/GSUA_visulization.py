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
            ["P_GROSS", "Gross Photosynthesis", u+"mol$_{carbon}$ m$^{-2}$ second$^{-1}$"],
            ["P_NET", "Net Photosynthesis", u+"mol$_{carbon}$ m$^{-2}$ second$^{-1}$"],
            ["g_S", "Stomatal Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$"],
            ["g_A", "Atmospheric Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$"],
            ["g_C", "Canopy Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$"],
            ["DTR", "Daily Tranpiration Rate", "L$_{water}$ m$^{-2}$ day$^{-1}$"]
]

mec_inputs = [
            ["T_LIGHT", "Light Cycle Temperature", "Degrees Celsius", 'TEMP'],
            ["T_DARK", "Dark Cycle Temperature", "Degrees Celsius", 'TEMP'],
            ["RH", "Relative Humidity", "%", 'RH'],
            ["CO2", "CO$_{2}$ Concentration", u+"mol$_{carbon}$ mol$_{air}$", 'CO2'],
            ["PPFD", "Photosynthetic Photon Flux", u+"mol$_{photons}$ m$^{-2}$ second$^{-1}$", 'PPFD'],
            ["H", "Photoperiod", "hours day$^{-1}$", 'H']
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

def GSUA_CHARTS():
    model_inputs = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_parameters.txt", sep=" ", names=['TEMP', 'RH', 'CO2', 'PPFD', 'H'])
    df_AMI_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_AMI_out/data/GSUA_AMI_Simulations.csv')
    df_BOS_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_BOS_out/data/GSUA_BOS_Simulations.csv')
    df_CAV_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_CAV_out/data/GSUA_CAV_Simulations.csv')

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

    ##############################################
    ########### Input  Historgram ################
    ##############################################
    for item in mec_inputs:        # loop for inputs
        input_short_name = item[0]
        input_long_name = item[1]
        input_unit = item[2]
        input_sample_name = item[3]
        fig, ax = plt.subplots()
        ax.hist(model_inputs[f'{input_sample_name}'], 15, density=True, histtype='bar', color='#2A119B', edgecolor='black')
        ax.set_ylabel('Frequency')
        ax.set_xlabel(f'{input_unit}')
        ax.set_title(f'{input_long_name}')
        plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_Histogram_{input_sample_name}', bbox_inches='tight') #there are many options for savefig
        # plt.show()

    #####################################################
    ############## Input x Output #######################
    #####################################################

    for item in mec_inputs:        # loop for inputs
        input_short_name = item[0]
        input_long_name = item[1]
        input_unit = item[2]
        for item in mec_outputs:   # loop for outputs
            output_short_name = item[0]
            output_long_name = item[1]
            output_unit = item[2]
            """This chart bulding stuff works!, but is there a better way?"""
            AMI_DATA = df_AMI_sims[['Simulation', output_short_name, input_short_name]]
            BOS_DATA = df_BOS_sims[['Simulation', output_short_name, input_short_name]]
            CAV_DATA = df_CAV_sims[['Simulation', output_short_name, input_short_name]]
            AMI_DATA = AMI_DATA.sort_values(input_short_name, ascending=True)
            BOS_DATA = BOS_DATA.sort_values(input_short_name, ascending=True)
            CAV_DATA = CAV_DATA.sort_values(input_short_name, ascending=True)
            xA = AMI_DATA[[input_short_name]].values.flatten()       # the flatten converts the df to a 1D array, needed for trendline
            yA = AMI_DATA[[output_short_name]].values.flatten()      # the flatten converts the df to a 1D array, needed for trendline
            xB = BOS_DATA[[input_short_name]].values.flatten()       # the flatten converts the df to a 1D array, needed for trendline
            yB = BOS_DATA[[output_short_name]].values.flatten()      # the flatten converts the df to a 1D array, needed for trendline
            xC = CAV_DATA[[input_short_name]].values.flatten()       # the flatten converts the df to a 1D array, needed for trendline
            yC = CAV_DATA[[output_short_name]].values.flatten()      # the flatten converts the df to a 1D array, needed for trendline
            fig, ax = plt.subplots()
            ax.scatter(xA, yA, color='blue', marker='o', label='AMI')
            ax.scatter(xB, yB, color='green', marker='s', label='BOS')
            ax.scatter(xC, yC, color='red', marker='^', label='CAV')
            ax.set_ylabel(f'{output_long_name} ({output_unit})')
            ax.set_xlabel(f'{input_long_name} ({input_unit})')
            # plt.title(f'{input_long_name} x {output_long_name}')

            # calc the trendline
            zA = np.polyfit(xA, yA, 2) # 1 is linear, 2 is quadratic!
            zB = np.polyfit(xB, yB, 2) # 1 is linear, 2 is quadratic!
            zC = np.polyfit(xC, yC, 2) # 1 is linear, 2 is quadratic!
            pA = np.poly1d(zA)
            pB = np.poly1d(zB)
            pC = np.poly1d(zC)
            plt.plot(xA,pA(xA),"darkblue")
            plt.plot(xB,pB(xB),"darkgreen")
            plt.plot(xC,pC(xC),"darkred")
            plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_Scatter_{input_short_name}_X_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
            # plt.show()
            plt.close()

# Executes this program/function
if __name__ ==('__main__'):
    GSUA_CHARTS()