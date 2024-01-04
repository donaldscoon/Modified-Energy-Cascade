from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib import ProblemSpec

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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
#     #     # this saves each of the sample parameters.
#     #     # Columns are Temp, Humidity, CO2, PPFD, H
#         np.savetxt("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/SOBOL_parameters.txt", sp.samples)
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
#     df_AMI_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/GSUA_AMI_out/data/GSUA_AMI_Simulations.csv')
#     df_BOS_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/GSUA_BOS_out/data/GSUA_BOS_Simulations.csv')
#     df_CAV_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/GSUA_CAV_out/data/GSUA_CAV_Simulations.csv')

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
#         for item in outputs:        # loop for output names
#             output_short_name = item[0]
#             output_long_name = item[1]
#             output_unit = item[2]
#             # Loading specific outputs for GSUA analysis 
#             Y = np.loadtxt(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/GSUA_{model_short_name}_out/data/GSUA_{model_short_name}_data_{output_short_name}.txt') # done to match the SALib example, imports the text file result
#             # print(Y)
#             sp.set_results(Y)
#             # forgive me, I want the output files to contain everything, even the constant/nonexistent outputs
#             # there are ignore warning statements up at the top because I took out this section.
#             # this file may not truly overwrite itself completely, delete to be sure. I can't figure out why or how to avoid that
#             # with open("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/results/constant_outputs.txt", "a") as f:
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
#             with open(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/results/full_out/{model_short_name}_{output_short_name}_SOBOL_results.txt', 'w') as f:
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
#     sobol_S1_out_df.to_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/results/sobol_S1_out.csv', index=False) # exports entire final data frame to a CSV
#     sobol_S2_out_df.to_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/results/sobol_S2_out.csv', index=False) # exports entire final data frame to a CSV
#     sobol_ST_out_df.to_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/results/sobol_ST_out.csv', index=False) # exports entire final data frame to a CSV

# # Executes this program/function
# if __name__ ==('__main__'):
#     ANALYZE()

def CHART():

    ami_c = '#2A119B'
    bos_c = '#067300'
    cav_c = '#8C0004'

    S1_df = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/results/sobol_S1_out.csv')    
    S2_df = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/results/sobol_S2_out.csv')    
    ST_df = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/results/sobol_ST_out.csv')    

    S1_ST_DF = pd.concat([S1_df, ST_df], axis=1) #combining the S1 and S2 dataframes for better looping

    # this creates a dataframe of S2 results that exlcudes all the NaN output rows
    index_list = [1,2,3,4,7,8,9,13,14,19]
    S2_small_df = S2_df.loc[S2_df.index[index_list]]
    # print(S2_small_df)
    
    # ''' ##########################################################
    # SINGLE MODEL SOBOL OUTPUTS 
    # ###########################################################'''
    # for item in models:                 # loop for model names
    #     model_short_name = item[0]
    #     model_long_name = item[1]
    #     for item in outputs:   # loop for outputs
    #         output_short_name = item[0]
    #         output_long_name = item[1]
    #         output_unit = item[2]
    #         for item in sobol_tests:
    #             sobol_short_name = item [0]
    #             sobol_long_name = item [1]
    #             # sets the color of each model for that loop.
    #             if model_short_name == 'AMI':
    #                 color = ami_c
    #             elif model_short_name == 'BOS':
    #                 color = bos_c
    #             elif model_short_name == 'CAV':
    #                 color = cav_c
    #             # print(model_short_name, output_short_name)
    #             # # this if/else statment sets up loop for S1 and ST to share code
    #             if sobol_short_name == 'S2':
    #                 # Check if the column contains all NaN values
    #                 column_name = f'{model_short_name}_{output_short_name}_{sobol_short_name}'
    #                 confidence = f'{model_short_name}_{output_short_name}_{sobol_short_name}_conf'
    #                 # Check for discrepancies and update values (ALL of this because for some reason AMI_ALPHA_S2 is zeros and the confidences are NaN \_O.o_/ )
    #                 mask1 = S2_small_df[f'{column_name}'].isna() & ~S2_small_df[f'{confidence}'].isna()
    #                 mask2 = ~S2_small_df[f'{column_name}'].isna() & S2_small_df[f'{confidence}'].isna()

    #                 # Set NaN values in 'column1' where 'column2' has NaN
    #                 S2_small_df.loc[mask2, f'{column_name}'] = np.nan

    #                 # Set NaN values in 'column2' where 'column1' has NaN
    #                 S2_small_df.loc[mask1, f'{confidence}'] = np.nan
                    
    #                 if not S2_small_df[column_name].isna().all():
    #                     fig, ax = plt.subplots()
                        
    #                     X = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #                     Y = S2_small_df[column_name]
    #                     ciY = S2_small_df[confidence]
    
    #                     plt.errorbar(X, Y, yerr=ciY, fmt = 'o', label= '95% CI', color=color, elinewidth=.75, capsize=2, capthick=.75)

    #                     ax.scatter(X, Y)
    #                     plt.xticks((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), ('TEMPxRH', 'TEMPxCO2', 'TEMPxPPFD', 'TEMPxH', 'RHxCO2',
    #                                                                     'RHxPPFD', 'RHxH', 'CO2xPPFD', 'CO2xH', 'PPFDxH'), rotation = 90)
    #                     plt.ylabel('Percent of Output Explained')
    #                     plt.xlabel('Equation Inputs')
    #                     plt.title(f'{sobol_long_name} Results of {model_short_name} {output_short_name}')
    #                     plt.show()
    #                     # plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/GSUA_{model_short_name}_out/figures/sobol/{sobol_short_name}_{model_short_name}_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
    #                     # plt.close()
    #             else:     # S1 and ST charting
    #                 # Check if the column contains all NaN values
    #                 column_name = f'{model_short_name}_{output_short_name}_{sobol_short_name}'
    #                 confidence = f'{model_short_name}_{output_short_name}_{sobol_short_name}_conf'
    #                 if not S1_ST_DF[column_name].isna().all():
    #                     fig, ax = plt.subplots()
                        
    #                     X = [1, 2, 3, 4, 5]
    #                     Y = S1_ST_DF[column_name]
    #                     ciY = S1_ST_DF[confidence]
    #                     plt.errorbar(X, Y, yerr=ciY, fmt = 'o', color=color, elinewidth=.75, capsize=2, capthick=.75)

    #                     ax.scatter(X, Y)
    #                     plt.xticks((1, 2, 3, 4, 5), ('TEMP', 'RH', 'CO2', 'PPFD', 'H'))
    #                     plt.ylabel('Percent of Output Explained')
    #                     plt.xlabel('Equation Inputs')
    #                     plt.title(f'{sobol_long_name} Results of {model_short_name} {output_short_name}')
    #                     plt.show()
    #                     # plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/GSUA_{model_short_name}_out/figures/sobol/{sobol_short_name}_{model_short_name}_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
    #                     # plt.close()



    ''' ##########################################################
    MULTIMODEL SOBOL OUTPUTS 
    ##########################################################'''

    for item in sobol_tests:    #loop for sobol tests
        sobol_short_name = item [0]
        sobol_long_name = item [1]
        for item in outputs:   # loop for outputs
            output_short_name = item[0]
            output_long_name = item[1]
            output_unit = item[2]
            fig, ax = plt.subplots()    
            for item in models:                 # loop for model names
                model_short_name = item[0]
                model_long_name = item[1]

                
                # assign color by model
                if model_short_name == 'AMI':
                    color = ami_c
                    X_S1_ST = [0.8, 1.8, 2.8, 3.8, 4.8]
                    X_S2 = [.8, 1.8, 2.8, 3.8, 4.8, 5.8, 6.8, 7.8, 8.8, 9.8]
                elif model_short_name == 'BOS':
                    color = bos_c
                    X_S1_ST = [1.0, 2.0, 3.0, 4.0, 5.0]
                    X_S2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                elif model_short_name == 'CAV':
                    color = cav_c
                    X_S1_ST = [1.2, 2.2, 3.2, 4.2, 5.2]
                    X_S2 = [1.2, 2.2, 3.2, 4.2, 5.2, 6.2, 7.2, 8.2, 9.2, 10.2]

                # This section builds the charts
                column_name = f'{model_short_name}_{output_short_name}_{sobol_short_name}'
                confidence = f'{model_short_name}_{output_short_name}_{sobol_short_name}_conf'

                if sobol_short_name == 'S2': # Charting for the S2 Results
                    Y = S2_small_df[column_name]
                    ciY = S2_small_df[confidence]
                    ciY = np.nan_to_num(ciY, nan=0)
                    plt.errorbar(X_S2, Y, yerr=ciY, fmt='o', color=color, elinewidth=.75, capsize=2, capthick=.75)
                    ax.scatter(X_S2, Y, color=color, label=f'{model_short_name}')
                else: # Charting for the S1 and ST resuls
                    Y = S1_ST_DF[column_name]
                    ciY = S1_ST_DF[confidence]
                    ciY = np.nan_to_num(ciY, nan=0)
                    plt.errorbar(X_S1_ST, Y, yerr=ciY, fmt = 'o', color=color, elinewidth=.75, capsize=2, capthick=.75)
                    ax.scatter(X_S1_ST, Y, color = color, label = f'{model_short_name}')

            #this section adds the labels and displays/saves them
            if sobol_short_name == 'S2':
                plt.xticks((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), ('TEMPxRH', 'TEMPxCO2', 'TEMPxPPFD', 'TEMPxH', 'RHxCO2',
                                                             'RHxPPFD', 'RHxH', 'CO2xPPFD', 'CO2xH', 'PPFDxH'), rotation = 90)
                plt.ylabel('Percent of Output Explained')
                # plt.xlabel('Input Interaction')
                plt.legend()
                plt.title(f'{sobol_long_name} Results of {output_long_name}')
                plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/figures/Sobol/{sobol_short_name}_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
                # plt.show()
                # plt.close()
            else:
                plt.xticks((1, 2, 3, 4, 5), ('TEMP', 'RH', 'CO2', 'PPFD', 'H'))
                plt.ylabel('Percent of Output Explained')
                # plt.xlabel('Input Interaction')
                plt.legend()
                plt.title(f'{sobol_long_name} Results of {output_long_name}')
                plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Indiv-Model/figures/Sobol/{sobol_short_name}_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
                # plt.show()
                # plt.close()

if __name__==('__main__'):
    CHART()
