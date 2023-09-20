from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib import ProblemSpec

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)


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
    # Notation [min, max, peak as % of that range]
    # for example, with  Temp the range is 35. 54.286% of that would equal 19, 
    # which would actually give a peak at 24 since the range starts at 5.
    'bounds': [[5,40,0.54286],      # Temperature Peak at 24 
               [35,100,0.38461],    # Relative Humidity Peak at 60
               [330,1300,0.48453],  # Atmo CO2 Concentration Peak at 800
               [0,1100,0.27273],    # PPFD Level Peak at 300
               [0,24, 0.66667]],    # Photoperiod Peak at 16
    'dists': ['triang',             # Temperature
              'triang',             # Relative Humidity
              'triang',             # Atmo CO2
              'triang',             # PPFD
              'triang'],            # Photoperiod
    'outputs': ['Y']
})

sobol_tests = [
         ["ST", "Total Order"], 
         ["S1", "1st Order"], 
         ["S2", "2nd Order"]
         ]

# def SAMPLE():
#     param_values = sp.sample_sobol(2**6, calc_second_order=True) # sobol sampling 2**6 generates 768 samples

#     for i, X in enumerate(sp.samples):
#     #     # this saves each of the sample parameters.
#     #     # Columns are Temp, Humidity, CO2, PPFD, H
#         np.savetxt("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/SOBOL_parameters.txt", sp.samples)
#         SIM_TEMP = X[0]
#         SIM_RH   = X[1]
#         SIM_CO2  = X[2]
#         SIM_PPFD = X[3]
#         SIM_H    = X[4]
#         SIM_NUM = i

# # Executes this program/function
# if __name__ ==('__main__'):
#     SAMPLE()

# def ANALYZE():
#     # Create dataframes for each models GSUA runs
#     df_AMI_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_AMI_out/data/GSUA_AMI_Simulations.csv')
#     df_BOS_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_BOS_out/data/GSUA_BOS_Simulations.csv')
#     df_CAV_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_CAV_out/data/GSUA_CAV_Simulations.csv')

#     sobol_ST_out_df = pd.DataFrame({'Index': ['TEMP', 'RH', 'CO2', 'PPFD', 'H']})
#     sobol_ST_out_df.set_index('Index')
#     sobol_S1_out_df = pd.DataFrame({'Index': ['TEMP', 'RH', 'CO2', 'PPFD', 'H']})
#     sobol_S1_out_df.set_index('Index')
#     sobol_S2_out_df = pd.DataFrame({'Index': ['TEMPxTEMP', 'TEMPxRH', 'TEMPxCO2', 'TEMPxPPFD', 'TEMPxH',
#                                               'RHxTEMP', 'RHxRH', 'RHxCO2', 'RHxPPFD', 'RHxH',
#                                               'CO2xTEMP', 'CO2xRH', 'CO2xCO2', 'CO2xPPFD', 'CO2xH',
#                                               'PPFDxTEMP', 'PPFDxRH', 'PPFDxCO2', 'PPFDxPPFD', 'PPFDxH',
#                                               'HxTEMP', 'HxRH', 'HxCO2', 'HxPPFD', 'HxH']})
#     sobol_S2_out_df.set_index('Index')


#     for item in models:                 # loop for model names
#         model_short_name = item[0]
#         model_long_name = item[1]
#         for item in mec_outputs:        # loop for output names
#             output_short_name = item[0]
#             output_long_name = item[1]
#             output_unit = item[2]
#             # Loading specific outputs for GSUA analysis 
#             Y = np.loadtxt(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_{model_short_name}_out/data/GSUA_{model_short_name}_data_{output_short_name}.txt') # done to match the SALib example, imports the text file result
#             # print(Y)
#             sp.set_results(Y)
#             # forgive me, I want the output files to contain everything, even the constant/nonexistent outputs
#             # there are ignore warning statements up at the top because I took out this section.
#             # this file may not truly overwrite itself completely, delete to be sure. I can't figure out why or how to avoid that
#             # with open("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/constant_outputs.txt", "a") as f:
#             #     if Y[0] == Y[20]: # identifying constant outputs
#             #         # if identified here it does not mean that they are constant throughout the simulation
#             #         # just that the final value is constant such as CUE_24 which hits a max  
#             #         f.write(f'{model_short_name} {output_short_name} \n')    # writing them to a text file
#             #         continue
#             # f.close()

#     ##################################### Sobol Analysis ###############################################
#             sp.analyze_sobol()

#             # this saving the results part is still pretty garbage, 
#             # diverted them to a special folder just in case though. 
#             with open(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/full_out/{model_short_name}_{output_short_name}_SOBOL_results.txt', 'w') as f:
#                 results_df = sp.to_df()
#                 f.write(str(results_df))
#             f.close

#             # First Order Analysis
#             S1_output_key = f'{model_short_name}_{output_short_name}_S1'
#             S1_CONF_output_key = f'{model_short_name}_{output_short_name}_S1_conf'
#             sobol_S1_out_df[S1_output_key] = sp.analysis['S1'].flatten().tolist()
#             sobol_S1_out_df[S1_CONF_output_key] = sp.analysis['S1_conf'].flatten().tolist()

#             # Second Order Analysis
#             S2_output_key = f'{model_short_name}_{output_short_name}_S2'
#             S2_CONF_output_key = f'{model_short_name}_{output_short_name}_S2_conf'
#             sobol_S2_out_df[S2_output_key] = sp.analysis['S2'].flatten().tolist()
#             sobol_S2_out_df[S2_CONF_output_key] = sp.analysis['S2_conf'].flatten().tolist()

#             # Total Order Analysis
#             ST_output_key = f'{model_short_name}_{output_short_name}_ST'
#             ST_CONF_output_key = f'{model_short_name}_{output_short_name}_ST_conf'
#             sobol_ST_out_df[ST_output_key] = sp.analysis['ST'].flatten().tolist()
#             sobol_ST_out_df[ST_CONF_output_key] = sp.analysis['ST_conf'].flatten().tolist()


#     # # Saving all of these to CSV's
#     sobol_S1_out_df.to_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/sobol_S1_out.csv', index=False) # exports entire final data frame to a CSV
#     sobol_S2_out_df.to_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/sobol_S2_out.csv', index=False) # exports entire final data frame to a CSV
#     sobol_ST_out_df.to_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/sobol_ST_out.csv', index=False) # exports entire final data frame to a CSV

# # Executes this program/function
# if __name__ ==('__main__'):
#     ANALYZE()

def CHART():

    ami_c = '#2A119B'
    bos_c = '#067300'
    cav_c = '#8C0004'

    S1_df = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/sobol_S1_out.csv')    
    S2_df = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/sobol_S2_out.csv')    
    ST_df = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/sobol_ST_out.csv')    

    S1_ST_DF = pd.concat([S1_df, ST_df], axis=1) #combining the S1 and S2 dataframes for better looping

    ''' ##########################################################
    SINGLE MODEL SOBOL OUTPUTS 
    ###########################################################'''
    for item in models:                 # loop for model names
        model_short_name = item[0]
        model_long_name = item[1]
        for item in mec_outputs:   # loop for outputs
            output_short_name = item[0]
            output_long_name = item[1]
            output_unit = item[2]
            for item in sobol_tests:
                sobol_short_name = item [0]
                sobol_long_name = item [1]
                # sets the color of each model for that loop.
                if model_short_name == 'AMI':
                    color = ami_c
                elif model_short_name == 'BOS':
                    color = bos_c
                elif model_short_name == 'CAV':
                    color = cav_c

                # # this if statment sets up loop for S1 and ST to share code
                if sobol_short_name == 'S2':
                    print('Later Gator!')
                    '''##################################
                    ############ DONT FORGET THIS###################
                    ##########################################'''
                else:
                   # Check if the column contains all NaN values
                    column_name = f'{model_short_name}_{output_short_name}_{sobol_short_name}'
                    if not S1_ST_DF[column_name].isna().all():
                        fig, ax = plt.subplots()

                        X = [1, 2, 3, 4, 5]
                        Y = S1_ST_DF[column_name]
                    # # # plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=color)

                        ax.scatter(X, Y)
                        plt.xticks((1, 2, 3, 4, 5), ('TEMP', 'RH', 'CO2', 'PPFD', 'H'))
                        plt.show()
                    else:
                        print(f"Skipping '{column_name}' because it contains all NaN values")
                    # ax.scatter(X, Y)




    ''' ##########################################################
    MULTIMODEL SOBOL OUTPUTS 
    ###########################################################'''


    # for item in mec_outputs:   # loop for outputs
    #     output_short_name = item[0]
    #     output_long_name = item[1]
    #     output_unit = item[2]
    #     fig, ax = plt.subplots() # creates the figure for each output type, which is then iterated by model.
    #     for item in models:                 # loop for model names
    #         model_short_name = item[0]
    #         model_long_name = item[1]





if __name__==('__main__'):
    CHART()

