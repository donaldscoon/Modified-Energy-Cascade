from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib import ProblemSpec

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import warnings
import naming_function


warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)


##########################################################
############## Defining the Model Inputs #################
##########################################################

inputs = naming_function.mec_input_names()
outputs = naming_function.mec_output_names()
models = naming_function.model_names()
sp = naming_function.prob_spec()

sobol_tests = [
         ["ST", "Total Order"], 
         ["S1", "1st Order"], 
         ["S2", "2nd Order"]
         ]

# def SAMPLE():
#     param_values = sp.sample_sobol(2**6, calc_second_order=True) # sobol sampling 2**6 generates 768 samples

#     for i, X in enumerate(sp.samples):
#         X[5] = random.randint(1, 3)    # forces the sim structure distribution to dicrete uniform
#     #     # this saves each of the sample parameters.
#     #     # Columns are Temp, Humidity, CO2, PPFD, H
#         np.savetxt("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/SOBOL_parameters.txt", sp.samples)
#         SIM_TEMP = X[0]
#         SIM_RH   = X[1]
#         SIM_CO2  = X[2]
#         SIM_PPFD = X[3]
#         SIM_H    = X[4]
#         SIM_STRU = X[5]
#         SIM_NUM = i

# # Executes this program/function
# if __name__ ==('__main__'):
#     SAMPLE()

def ANALYZE():
    # Create dataframe
    df_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_simulations.csv')

    sobol_ST_out_df = pd.DataFrame({'Index': ['TEMP', 'RH', 'CO2', 'PPFD', 'H', 'STRU']})
    sobol_ST_out_df.set_index('Index')
    sobol_S1_out_df = pd.DataFrame({'Index': ['TEMP', 'RH', 'CO2', 'PPFD', 'H', 'STRU']})
    sobol_S1_out_df.set_index('Index')
    sobol_S2_out_df = pd.DataFrame({'Index': ['TEMPxTEMP', 'TEMPxRH', 'TEMPxCO2', 'TEMPxPPFD', 'TEMPxH', 'TEMPxSTRU',
                                              'RHxTEMP', 'RHxRH', 'RHxCO2', 'RHxPPFD', 'RHxH', 'RHxSTRU',
                                              'CO2xTEMP', 'CO2xRH', 'CO2xCO2', 'CO2xPPFD', 'CO2xH', 'CO2xSTRU',
                                              'PPFDxTEMP', 'PPFDxRH', 'PPFDxCO2', 'PPFDxPPFD', 'PPFDxH', 'PPFDxSTRU',
                                              'HxTEMP', 'HxRH', 'HxCO2', 'HxPPFD', 'HxH', 'HxSTRU',
                                              'STRUxTEMP', 'STRUxRH', 'STRUxCO2', 'STRUxPPFD', 'STRUxH', 'STRUxSTRU']})
    sobol_S2_out_df.set_index('Index')


    for item in outputs:        # loop for output names
        output_short_name = item[0]
        output_long_name = item[1]
        output_unit = item[2]
        # Loading specific outputs for GSUA analysis 
        Y = df_sims[f'{output_short_name}'].to_numpy()
        sp.set_results(Y)

##################################### Sobol Analysis ###############################################
        sp.analyze_sobol()

        # First Order Analysis
        S1_output_key = f'{output_short_name}_S1'
        S1_CONF_output_key = f'{output_short_name}_S1_conf'
        sobol_S1_out_df[S1_output_key] = sp.analysis['S1'].flatten().tolist()
        sobol_S1_out_df[S1_CONF_output_key] = sp.analysis['S1_conf'].flatten().tolist()

        # Second Order Analysis
        S2_output_key = f'{output_short_name}_S2'
        S2_CONF_output_key = f'{output_short_name}_S2_conf'
        sobol_S2_out_df[S2_output_key] = sp.analysis['S2'].flatten().tolist()
        sobol_S2_out_df[S2_CONF_output_key] = sp.analysis['S2_conf'].flatten().tolist()

        # Total Order Analysis
        ST_output_key = f'{output_short_name}_ST'
        ST_CONF_output_key = f'{output_short_name}_ST_conf'
        sobol_ST_out_df[ST_output_key] = sp.analysis['ST'].flatten().tolist()
        sobol_ST_out_df[ST_CONF_output_key] = sp.analysis['ST_conf'].flatten().tolist()


    # # # Saving all of these to CSV's
    # sobol_S1_out_df.to_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/sobol_S1_out.csv', index=False) # exports entire final data frame to a CSV
    # sobol_S2_out_df.to_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/sobol_S2_out.csv', index=False) # exports entire final data frame to a CSV
    # sobol_ST_out_df.to_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/sobol_ST_out.csv', index=False) # exports entire final data frame to a CSV

# Executes this program/function
if __name__ ==('__main__'):
    ANALYZE()

# def CHART():

#     S1_df = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/sobol_S1_out.csv')    
#     S2_df = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/sobol_S2_out.csv')    
#     ST_df = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/sobol_ST_out.csv')    

#     S1_ST_DF = pd.concat([S1_df, ST_df], axis=1) #combining the S1 and S2 dataframes for better looping
    
#     # this creates a dataframe of S2 results that exlcudes all the NaN output rows
#     index_list = [1,2,3,4,5,8,9,10,11,15,16,17,22,23,29]
#     S2_small_df = S2_df.loc[S2_df.index[index_list]]

    
#     ''' ##########################################################
#     SINGLE MODEL SOBOL OUTPUTS 
#     ###########################################################'''
#     for item in outputs:   # loop for outputs
#         output_short_name = item[0]
#         output_long_name = item[1]
#         output_unit = item[2]
#         for item in sobol_tests:
#             sobol_short_name = item [0]
#             sobol_long_name = item [1]

#             print(sobol_short_name, output_short_name)
#             # # this if/else statment sets up loop for S1 and ST to share code
#             if sobol_short_name == 'S2':
#                 # Check if the column contains all NaN values
#                 column_name = f'{output_short_name}_{sobol_short_name}'
#                 confidence = f'{output_short_name}_{sobol_short_name}_conf'

#                 # Check for discrepancies and update values (ALL of this because for some reason AMI_ALPHA_S2 is zeros and the confidences are NaN \_O.o_/ )
#                 mask1 = S2_small_df[f'{column_name}'].isna() & ~S2_small_df[f'{confidence}'].isna()
#                 mask2 = ~S2_small_df[f'{column_name}'].isna() & S2_small_df[f'{confidence}'].isna()

#                 # Set NaN values in 'column1' where 'column2' has NaN
#                 S2_small_df.loc[mask2, f'{column_name}'] = np.nan

#                 # Set NaN values in 'column2' where 'column1' has NaN
#                 S2_small_df.loc[mask1, f'{confidence}'] = np.nan
                
#                 if not S2_small_df[column_name].isna().all():
#                     fig, ax = plt.subplots()
                    
#                     X = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
#                     Y = S2_small_df[column_name]
#                     ciY = S2_small_df[confidence]

#                     plt.errorbar(X, Y, yerr=ciY, fmt = 'o', label= '95% CI', color='black')

#                     ax.scatter(X, Y)
#                     plt.xticks((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
#                                ('TEMPxRH', 'TEMPxCO2', 'TEMPxPPFD', 'TEMPxH', 'TEMPxSTRU', 
#                                 'RHxCO2', 'RHxPPFD', 'RHxH', 'RHxSTRU', 'CO2xPPFD', 'CO2xH', 
#                                 'CO2xSTRU', 'PPFDxH', 'PPFDxSTRU','HxSTRU'), rotation = 45)
#                     plt.ylabel('Percent of Output Explained')
#                     plt.xlabel('Equation Inputs')
#                     plt.title(f'{sobol_long_name} Results of {output_short_name}')
#                     # plt.show()
#                     plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/Sobol/{sobol_short_name}_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
#                     plt.close()
#             else:     # S1 and ST charting
#                 # Check if the column contains all NaN values
#                 column_name = f'{output_short_name}_{sobol_short_name}'
#                 confidence = f'{output_short_name}_{sobol_short_name}_conf'
#                 if not S1_ST_DF[column_name].isna().all():
#                     fig, ax = plt.subplots()
                    
#                     X = [1, 2, 3, 4, 5, 6]
#                     Y = S1_ST_DF[column_name]
#                     ciY = S1_ST_DF[confidence]
#                     plt.errorbar(X, Y, yerr=ciY, fmt = 'o', color='black')

#                     ax.scatter(X, Y)
#                     plt.xticks((1, 2, 3, 4, 5, 6), ('TEMP', 'RH', 'CO2', 'PPFD', 'H', 'STRU'))
#                     plt.ylabel('Percent of Output Explained')
#                     plt.xlabel('Equation Input Interactions')
#                     plt.title(f'{sobol_long_name} Results of {output_short_name}')
#                     # plt.show()
#                     plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/Sobol/{sobol_short_name}_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
#                     plt.close()

# if __name__==('__main__'):
#     CHART()

