from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.sample import morris
from SALib import ProblemSpec


import SALib as SALib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
import naming_function

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)


##########################################################
############## Defining the Model Inputs #################
##########################################################

inputs = naming_function.mec_input_names()
outputs = naming_function.mec_output_names()
models = naming_function.model_names()
sp = naming_function.prob_spec()

###########################################################
#################### Analysis #############################
###########################################################

def ANALYZE():

    # Create dataframes for each models GSUA runs
    df_AMI_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_AMI_out/data/GSUA_AMI_Simulations.csv')
    df_BOS_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_BOS_out/data/GSUA_BOS_Simulations.csv')
    df_CAV_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_CAV_out/data/GSUA_CAV_Simulations.csv')

    N = 128 # number of unique levels resulting from the sobol sampling
    X = np.loadtxt('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/SOBOL_parameters.txt')

    EE_out_df = pd.DataFrame({'Index': ['TEMP', 'RH', 'CO2', 'PPFD', 'H']})
    EE_out_df.set_index('Index')

    for item in models:                 # loop for model names
        model_short_name = item[0]
        model_long_name = item[1]
        for item in outputs:        # loop for output names
            output_short_name = item[0]
            output_long_name = item[1]
            output_unit = item[2]
            # Loading specific outputs for Morris EE analysis 
            Y = np.loadtxt(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_{model_short_name}_out/data/GSUA_{model_short_name}_data_{output_short_name}.txt') # done to match the SALib example, imports the text file result
            EE = SALib.analyze.morris.analyze(sp, X, Y, conf_level=0.95, num_levels=N) # analyzes the Elementary effects for each models ouput

            with open(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/full_out/{model_short_name}_{output_short_name}_EE_results.txt', 'w') as f:
                results_df = EE.to_df()
                f.write(str(results_df))
            f.close

            # create a big ol honking dataframe
            mu_output_key = f'{model_short_name}_{output_short_name}_mu'
            mu_star_output_key = f'{model_short_name}_{output_short_name}_mu_star'
            mu_star_conf_output_key = f'{model_short_name}_{output_short_name}__mu_star_conf'
            sigma_output_key = f'{model_short_name}_{output_short_name}_sigma'

            EE_out_df[mu_output_key] = EE['mu']
            EE_out_df[mu_star_output_key] = EE['mu_star']
            EE_out_df[mu_star_conf_output_key] = EE['mu_star_conf']
            EE_out_df[sigma_output_key] = EE['sigma']
    EE_out_df.to_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/EE_out.csv', index=False)

# Executes this program/function
if __name__ ==('__main__'):
    ANALYZE()

# def CHART():
#     ami_c = '#2A119B'
#     bos_c = '#067300'
#     cav_c = '#8C0004'

    ### SEE EE.py in ASHS GSUA For how this was used!
    # ### All of these creates a single point for all the legend entries!
    # ami_patch = mpatches.Patch(color = ami_c, label = 'Amitrano')
    # bos_patch = mpatches.Patch(color = bos_c, label = 'Boscheri')
    # cav_patch = mpatches.Patch(color = cav_c, label = 'Cavazzoni')
    # temp_point = Line2D([0], [0], linestyle= '', color='black', marker= 'o', label='TEMP' )
    # rh_point   = Line2D([0], [0], linestyle= '', color='black', marker= 's', label='RH' )
    # CO2_point  = Line2D([0], [0], linestyle= '', color='black', marker= '*', label='CO2' )
    # PPFD_point = Line2D([0], [0], linestyle= '', color='black', marker= '^', label='PPFD' )
    # H_point    = Line2D([0], [0], linestyle= '', color='black', marker= 'd', label='H' )
    # SEM_line = Line2D([0], [0], linestyle= '--', color='black', label='+- 2 SEM')

    # onetoone_legend = [ami_patch, bos_patch, cav_patch, temp_point, rh_point,
    #              CO2_point, PPFD_point, H_point]
    # SEM_legend = [ami_patch, bos_patch, cav_patch, temp_point, rh_point,
    #              CO2_point, PPFD_point, H_point, SEM_line]

# # perhaps I can write some kind of script to set these
# # so I don't have to write it out completely each time?
# # symbols differntiate models
# # AMI= 'o' blue
# # BOS= 's' green
# # CAV= '^' red

# # colors differentiate from paletton.com
# #     dark blue   = #2A119B
# #     blue        = #5E46C6
# #     light blue  = #A798EC
# #     dark green  = #067300
# #     green       = #09B600
# #     light green = #96F391
# #     dark red    = #8C0004
# #     red         = #DF0006
# #     light red   = #FE989A

#     # read in the data
#     EE_out_df = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/results/EE_out.csv')

#     '''##########################################################
#      mu star by sigma with a 1/1 line MULTIMODEL
#      #########################################################'''
#     for item in outputs:   # loop for outputs
#         output_short_name = item[0]
#         output_long_name = item[1]
#         output_unit = item[2]

#         plt.figure() # creates the figure for each output type, which is then iterated by model.
#         for item in models:                 # loop for model names
#             model_short_name = item[0]
#             model_long_name = item[1]

#             # sets the color of each model for that loop.
#             if model_short_name == 'AMI':
#                 color = ami_c
#             elif model_short_name == 'BOS':
#                 color = bos_c
#             elif model_short_name == 'CAV':
#                 color = cav_c
#             # print(model_short_name, output_short_name)
#             X = EE_out_df[f'{model_short_name}_{output_short_name}_mu_star']
#             Y = EE_out_df[f'{model_short_name}_{output_short_name}_sigma']

#             # Check if both X and Y have all zero values
#             if not all(x == 0 for x in X) or not all(y == 0 for y in Y):
                    
#                 # define which points correspond to which inputs
#                 mu_star_temp = X[0]
#                 mu_star_rh   = X[1]
#                 mu_star_CO2  = X[2]
#                 mu_star_PPFD = X[3]
#                 mu_star_H    = X[4]

#                 sigma_temp   = Y[0]
#                 sigma_rh     = Y[1]
#                 sigma_CO2    = Y[2]
#                 sigma_PPFD   = Y[3]
#                 sigma_H      = Y[4]

#                 # Create the scatter plot
#                 plt.scatter(mu_star_temp, sigma_temp,    s=50, marker= 'o', color= color, label= f"{model_short_name}_TEMP")
#                 plt.scatter(mu_star_rh, sigma_rh,        s=50, marker= 's', color= color, label= f"{model_short_name}_RH")
#                 plt.scatter(mu_star_CO2, sigma_CO2,      s=50, marker= '*', color= color, label= f"{model_short_name}_CO2")
#                 plt.scatter(mu_star_PPFD, sigma_PPFD,    s=50, marker= '^', color= color, label= f"{model_short_name}_PPFD")
#                 plt.scatter(mu_star_H, sigma_H,          s=50, marker= 'd', color= color, label= f"{model_short_name}_H")

#                 # Add a 1:1 line
#                 # min_val = min(min(X), min(Y))
#                 max_val = max(max(X), max(Y))
#                 plt.plot([0, max_val], [0, max_val], color='gray', linestyle='-')

#         # Set the labels and title
#         plt.xlabel('mu*')
#         plt.ylabel('sigma')
#         plt.title(f'EE of {output_short_name}')
#         plt.legend()
#         # plt.show()
#         plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/Elementary_Effects/EE_1-1_{output_short_name}_multimodel.png', bbox_inches='tight') #there are many options for savefig
#         plt.close()

#     '''##########################################################
#      mu star by sigma with a 1/1 line SINGLE MODEL
#      #########################################################'''
#     for item in models:                 # loop for model names
#         model_short_name = item[0]
#         model_long_name = item[1]
#         for item in outputs:   # loop for outputs
#             output_short_name = item[0]
#             output_long_name = item[1]
#             output_unit = item[2]

#             plt.figure() # creates the figure for each output type, which is then iterated by model.

#             # sets the color of each model for that loop.
#             if model_short_name == 'AMI':
#                 color = ami_c
#             elif model_short_name == 'BOS':
#                 color = bos_c
#             elif model_short_name == 'CAV':
#                 color = cav_c
#             # print(model_short_name, output_short_name)
#             X = EE_out_df[f'{model_short_name}_{output_short_name}_mu_star']
#             Y = EE_out_df[f'{model_short_name}_{output_short_name}_sigma']

#             # Check if both X and Y have all zero values
#             if not all(x == 0 for x in X) or not all(y == 0 for y in Y):
                    
#                 # define which points correspond to which inputs
#                 mu_star_temp = X[0]
#                 mu_star_rh   = X[1]
#                 mu_star_CO2  = X[2]
#                 mu_star_PPFD = X[3]
#                 mu_star_H    = X[4]

#                 sigma_temp   = Y[0]
#                 sigma_rh     = Y[1]
#                 sigma_CO2    = Y[2]
#                 sigma_PPFD   = Y[3]
#                 sigma_H      = Y[4]

#                 # Create the scatter plot
#                 plt.scatter(mu_star_temp, sigma_temp,    s=50, marker= 'o', color= color, label= f"{model_short_name}_TEMP")
#                 plt.scatter(mu_star_rh, sigma_rh,        s=50, marker= 's', color= color, label= f"{model_short_name}_RH")
#                 plt.scatter(mu_star_CO2, sigma_CO2,      s=50, marker= '*', color= color, label= f"{model_short_name}_CO2")
#                 plt.scatter(mu_star_PPFD, sigma_PPFD,    s=50, marker= '^', color= color, label= f"{model_short_name}_PPFD")
#                 plt.scatter(mu_star_H, sigma_H,          s=50, marker= 'd', color= color, label= f"{model_short_name}_H")

#                 # Add a 1:1 line
#                 # min_val = min(min(X), min(Y))
#                 max_val = max(max(X), max(Y))
#                 plt.plot([0, max_val], [0, max_val], color='gray', linestyle='-')

#                 # Set the labels and title
#                 plt.xlabel('mu*')
#                 plt.ylabel('sigma')
#                 plt.title(f'EE of {model_short_name}_{output_short_name}')
#                 plt.legend()
#                 # plt.show()
#                 plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_{model_short_name}_out/figures/EE/EE_1-1{model_short_name}_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
#                 plt.close()

#     '''###############################################################################
#     mu by sigma with the V MULTIMODEL
#     ###############################################################################'''

#     for item in outputs:   # loop for outputs
#         output_short_name = item[0]
#         output_long_name = item[1]
#         output_unit = item[2]
#         fig, ax = plt.subplots() # creates the figure for each output type, which is then iterated by model.
#         for item in models:                 # loop for model names
#             model_short_name = item[0]
#             model_long_name = item[1]

#             # sets the color of each model for that loop.
#             if model_short_name == 'AMI':
#                 color = ami_c
#             elif model_short_name == 'BOS':
#                 color = bos_c
#             elif model_short_name == 'CAV':
#                 color = cav_c
#             # print(model_short_name, output_short_name)
#             X = EE_out_df[f'{model_short_name}_{output_short_name}_mu']
#             Y = EE_out_df[f'{model_short_name}_{output_short_name}_sigma']

#             # Check if both X and Y have all zero values
#             if not all(x == 0 for x in X) or not all(y == 0 for y in Y):
                    
#                 # define which points correspond to which inputs
#                 mu_temp = X[0]
#                 mu_rh   = X[1]
#                 mu_CO2  = X[2]
#                 mu_PPFD = X[3]
#                 mu_H    = X[4]

#                 sigma_temp   = Y[0]
#                 sigma_rh     = Y[1]
#                 sigma_CO2    = Y[2]
#                 sigma_PPFD   = Y[3]
#                 sigma_H      = Y[4]

#                 # Create the scatter plot
#                 plt.scatter(mu_temp, sigma_temp,    s=50, marker= 'o', color= color, label= f"{model_short_name}_TEMP")
#                 plt.scatter(mu_rh, sigma_rh,        s=50, marker= 's', color= color, label= f"{model_short_name}_RH")
#                 plt.scatter(mu_CO2, sigma_CO2,      s=50, marker= '*', color= color, label= f"{model_short_name}_CO2")
#                 plt.scatter(mu_PPFD, sigma_PPFD,    s=50, marker= '^', color= color, label= f"{model_short_name}_PPFD")
#                 plt.scatter(mu_H, sigma_H,          s=50, marker= 'd', color= color, label= f"{model_short_name}_H")

#                 # Add +-2SEM LINES
#                 # calc SD of mu, 
#                 mu_sd = EE_out_df[f'{model_short_name}_{output_short_name}_mu'].std()
#                 # calc sqrt of N, 
#                 denom = np.emath.sqrt(128)
#                 pos2_SEM = 2*(mu_sd/denom)
#                 neg2_SEM = -2*(mu_sd/denom)
#                 # I still don't fully understand how this centers the x axis to 0 but it does!
#                 x_max = np.abs(ax.get_xlim()).max()
#                 ax.set_xlim(xmin=-x_max, xmax=x_max)

#                 # Add lines from (0, 0) to SEM values
#                 plt.plot([0, neg2_SEM], [0, max(Y)], color=color, linestyle='--', label=f'{model_short_name} -2SEM')
#                 plt.plot([0, pos2_SEM], [0, max(Y)], color=color, linestyle='--', label=f'{model_short_name} +2SEM')

#         # Set the labels and title
#         plt.xlabel('mu')
#         plt.ylabel('sigma')
#         plt.title(f'EE of {output_short_name}')
#         plt.legend()
#         # plt.show()
#         plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/Elementary_Effects/EE_SEM_{output_short_name}_multimodel.png', bbox_inches='tight') #there are many options for savefig
#         plt.close()

#     '''###############################################################################
#     mu by sigma with the V SINGLE MODEL
#     ###############################################################################'''

#     for item in models:                 # loop for model names
#         model_short_name = item[0]
#         model_long_name = item[1]
#         for item in outputs:   # loop for outputs
#             output_short_name = item[0]
#             output_long_name = item[1]
#             output_unit = item[2]
#             fig, ax = plt.subplots() # creates the figure for each output type, which is then iterated by model.

#             # sets the color of each model for that loop.
#             if model_short_name == 'AMI':
#                 color = ami_c
#             elif model_short_name == 'BOS':
#                 color = bos_c
#             elif model_short_name == 'CAV':
#                 color = cav_c
#             # print(model_short_name, output_short_name)
#             X = EE_out_df[f'{model_short_name}_{output_short_name}_mu']
#             Y = EE_out_df[f'{model_short_name}_{output_short_name}_sigma']

#             # Check if both X and Y have all zero values
#             if not all(x == 0 for x in X) or not all(y == 0 for y in Y):
                    
#                 # define which points correspond to which inputs
#                 mu_temp = X[0]
#                 mu_rh   = X[1]
#                 mu_CO2  = X[2]
#                 mu_PPFD = X[3]
#                 mu_H    = X[4]

#                 sigma_temp   = Y[0]
#                 sigma_rh     = Y[1]
#                 sigma_CO2    = Y[2]
#                 sigma_PPFD   = Y[3]
#                 sigma_H      = Y[4]

#                 # Create the scatter plot
#                 plt.scatter(mu_temp, sigma_temp,    s=50, marker= 'o', color= color, label= f"{model_short_name}_TEMP")
#                 plt.scatter(mu_rh, sigma_rh,        s=50, marker= 's', color= color, label= f"{model_short_name}_RH")
#                 plt.scatter(mu_CO2, sigma_CO2,      s=50, marker= '*', color= color, label= f"{model_short_name}_CO2")
#                 plt.scatter(mu_PPFD, sigma_PPFD,    s=50, marker= '^', color= color, label= f"{model_short_name}_PPFD")
#                 plt.scatter(mu_H, sigma_H,          s=50, marker= 'd', color= color, label= f"{model_short_name}_H")

#                 # Add +-2SEM LINES
#                 # calc SD of mu, 
#                 mu_sd = EE_out_df[f'{model_short_name}_{output_short_name}_mu'].std()
#                 # calc sqrt of N, 
#                 denom = np.emath.sqrt(128)
#                 pos2_SEM = 2*(mu_sd/denom)
#                 neg2_SEM = -2*(mu_sd/denom)
#                 # I still don't fully understand how this centers the x axis to 0 but it does!
#                 x_max = np.abs(ax.get_xlim()).max()
#                 ax.set_xlim(xmin=-x_max, xmax=x_max)

#                 # Add lines from (0, 0) to SEM values
#                 plt.plot([0, neg2_SEM], [0, max(Y)], color=color, linestyle='--', label=f'{model_short_name} -2SEM')
#                 plt.plot([0, pos2_SEM], [0, max(Y)], color=color, linestyle='--', label=f'{model_short_name} +2SEM')

#                 # Set the labels and title
#                 plt.xlabel('mu')
#                 plt.ylabel('sigma')
#                 plt.title(f'EE of {model_short_name}_{output_short_name}')
#                 plt.legend()
#                 # plt.show()
#                 plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_{model_short_name}_out/figures/EE/EE_SEM_{model_short_name}_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
#                 plt.close()


# # Executes this program/function
# if __name__ ==('__main__'):
#     CHART()

# """ NOTES FROM THE MATLAB CODE `EE_SENMAE_CALC.M`

# Two figures/subplots are produced for each model output.    %
# %             The first subplot is a plot of µ* - ? while the second      %
# %             one consists of µ - ?.                                      %
# %                                                                         %
# %             We plot 1:1 threshold(dotted black)in the first             %
# %             subplot and µ = +/-2 ?/sqrt(r)threshold lines               %
# %             (dotted black)in the second subplot. µ = +/-2 ?/sqrt(r)     %
# %             lines were proposed by Morris (1991)to identify factor with %
# %             dominant non-additive/non-linear effects. 1:1 (i.e. µ*=?)   %
# %             line threshold is based on Khare et al.(2019)               %
# %                                                                         %
# %             Additionally, factors for which µ* = abs(µ) holds true i.e. %
# %             perfectly monotonic effects are indicated by solid red circles%
# %             while rest are indicated by blue asterisk. Also, bootstrapping %
# %             95% CI for µ* and µ are indicated (golden color) on         %
# %             respective subplots.                                        %
# %                                                                         %
# %             Plots are automatically saved as PDF files.                 %
# %                                                                         %
# % References: Khare et al. (2019), Effective Global Sensitivity Analysis  %
# %             of a High-Dimensional Hydrologic and Water Quality Models.  %
# %             Journal of Hydrologic Engineering, 24(1).                   %
# %             DOI: 10.1061/(ASCE)HE.1943-5584.0001726. 
# """