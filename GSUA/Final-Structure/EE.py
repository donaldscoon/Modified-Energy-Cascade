from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.sample import morris
from matplotlib.lines import Line2D

import SALib as SALib
import numpy as np
import matplotlib.patches as mpatches
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
sp = naming_function.prob_spec()

###########################################################
#################### Analysis #############################
###########################################################

def ANALYZE():

    # Create dataframe
    df_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/GSUA_simulations.csv')

    N = 128 # number of unique levels resulting from the sobol sampling
    X = np.loadtxt('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/SOBOL_parameters.txt')

    EE_out_df = pd.DataFrame({'Index': ['TEMP', 'RH', 'CO2', 'PPFD', 'H', 'STRU']})
    EE_out_df.set_index('Index')


    for item in outputs:        # loop for output names
        output_short_name = item[0]
        output_long_name = item[1]
        output_unit = item[2]
        # Loading specific outputs for Morris EE analysis 
        Y = df_sims[f'{output_short_name}'].to_numpy()
        EE = SALib.analyze.morris.analyze(sp, X, Y, conf_level=0.95, num_levels=N) # analyzes the Elementary effects for each models ouput

        with open(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/results/full_out/EE/{output_short_name}_EE_results.txt', 'w') as f:
            results_df = EE.to_df()
            f.write(str(results_df))
        f.close

        # create a big ol honking dataframe
        mu_output_key = f'{output_short_name}_mu'
        mu_star_output_key = f'{output_short_name}_mu_star'
        mu_star_conf_output_key = f'{output_short_name}__mu_star_conf'
        sigma_output_key = f'{output_short_name}_sigma'

        EE_out_df[mu_output_key] = EE['mu']
        EE_out_df[mu_star_output_key] = EE['mu_star']
        EE_out_df[mu_star_conf_output_key] = EE['mu_star_conf']
        EE_out_df[sigma_output_key] = EE['sigma']
    EE_out_df.to_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/results/EE_out.csv', index=False)

# Executes this program/function
if __name__ ==('__main__'):
    ANALYZE()

def CHART():
    
    ### All of these creates a single point for all the legend entries!
    temp_point = Line2D([0], [0], linestyle= '', color='black', marker= 'o', label='TEMP' )
    rh_point   = Line2D([0], [0], linestyle= '', color='black', marker= 's', label='RH' )
    CO2_point  = Line2D([0], [0], linestyle= '', color='black', marker= '*', label='CO2' )
    PPFD_point = Line2D([0], [0], linestyle= '', color='black', marker= '^', label='PPFD' )
    H_point    = Line2D([0], [0], linestyle= '', color='black', marker= 'd', label='H' )
    STRU_point = Line2D([0], [0], linestyle= '', color='black', marker= 'P', label='STRU')
    SEM_line   = Line2D([0], [0], linestyle= '--', color='black', label='+- 2 SEM')

    onetoone_legend = [temp_point, rh_point, CO2_point, PPFD_point, H_point, STRU_point]
    SEM_legend = [temp_point, rh_point, CO2_point, PPFD_point, H_point, STRU_point, SEM_line]

    # read in the data
    EE_out_df = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/results/EE_out.csv')

    '''##########################################################
     mu star by sigma with a 1/1 line MULTIMODEL
     ########################################################'''
    for item in outputs:   # loop for outputs
        output_short_name = item[0]
        output_long_name = item[1]
        output_unit = item[2]
        
        plt.figure() # creates the figure for each output type, which is then iterated by model.

        # print(model_short_name, output_short_name)
        X = EE_out_df[f'{output_short_name}_mu_star']
        Y = EE_out_df[f'{output_short_name}_sigma']
        X_conf = EE_out_df[f'{output_short_name}__mu_star_conf']

        # Check if both X and Y have all zero values
        if not all(x == 0 for x in X) or not all(y == 0 for y in Y):
                
            # define which points correspond to which inputs
            mu_star_temp = X[0]
            mu_star_rh   = X[1]
            mu_star_CO2  = X[2]
            mu_star_PPFD = X[3]
            mu_star_H    = X[4]
            mu_star_STRU = X[5]

            sigma_temp   = Y[0]
            sigma_rh     = Y[1]
            sigma_CO2    = Y[2]
            sigma_PPFD   = Y[3]
            sigma_H      = Y[4]
            sigma_STRU   = Y[5]

            mu_star_temp_conf        = X_conf[0]
            mu_star_rh_conf          = X_conf[1]
            mu_star_CO2_conf         = X_conf[2]
            mu_star_PPFD_conf        = X_conf[3]
            mu_star_H_conf           = X_conf[4]
            mu_star_STRU_conf        = X_conf[5]

            # Create the scatter plot
            plt.scatter(mu_star_temp, sigma_temp,    s=50, marker= 'o', color= "black")
            plt.scatter(mu_star_rh, sigma_rh,        s=50, marker= 's', color= "black")
            plt.scatter(mu_star_CO2, sigma_CO2,      s=50, marker= '*', color= "black")
            plt.scatter(mu_star_PPFD, sigma_PPFD,    s=50, marker= '^', color= "black")
            plt.scatter(mu_star_H, sigma_H,          s=50, marker= 'd', color= "black")
            plt.scatter(mu_star_STRU, sigma_STRU,    s=50, marker= 'P', color= "black")
            
            # Adding Confidences
            plt.errorbar(mu_star_temp,  sigma_temp, xerr=mu_star_temp_conf, ecolor='black', elinewidth=.5, capsize=2, capthick=.5)
            plt.errorbar(mu_star_rh,    sigma_rh,   xerr=mu_star_rh_conf,   ecolor='black', elinewidth=.5, capsize=2, capthick=.5)
            plt.errorbar(mu_star_CO2,   sigma_CO2,  xerr=mu_star_CO2_conf,  ecolor='black', elinewidth=.5, capsize=2, capthick=.5)
            plt.errorbar(mu_star_PPFD,  sigma_PPFD, xerr=mu_star_PPFD_conf, ecolor='black', elinewidth=.5, capsize=2, capthick=.5)
            plt.errorbar(mu_star_H,     sigma_H,    xerr=mu_star_H_conf,    ecolor='black', elinewidth=.5, capsize=2, capthick=.5)
            plt.errorbar(mu_star_STRU,  sigma_STRU, xerr=mu_star_STRU_conf, ecolor='black', elinewidth=.5, capsize=2, capthick=.5)

            # Add a 1:1 line
            # min_val = min(min(X), min(Y))
            max_val = max(max(X), max(Y))
            plt.plot([0, max_val], [0, max_val], color='gray', linestyle='-')

        # Set the labels and title
        plt.xlabel('mu*')
        plt.ylabel('sigma')
        plt.title(f'EE of {output_short_name}')
        plt.legend(handles= onetoone_legend)
        # plt.show()
        plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/figures/Elementary_Effects/EE_1-1_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
        plt.close()

    '''###############################################################################
    mu by sigma with the V MULTIMODEL
    ###############################################################################'''

    for item in outputs:   # loop for outputs
        output_short_name = item[0]
        output_long_name = item[1]
        output_unit = item[2]

        fig, ax = plt.subplots() # creates the figure for each output type, which is then iterated by model.

        # print(model_short_name, output_short_name)
        X = EE_out_df[f'{output_short_name}_mu']
        Y = EE_out_df[f'{output_short_name}_sigma']

        # Check if both X and Y have all zero values
        if not all(x == 0 for x in X) or not all(y == 0 for y in Y):
                
            # define which points correspond to which inputs
            mu_temp = X[0]
            mu_rh   = X[1]
            mu_CO2  = X[2]
            mu_PPFD = X[3]
            mu_H    = X[4]
            mu_STRU = X[5]

            sigma_temp   = Y[0]
            sigma_rh     = Y[1]
            sigma_CO2    = Y[2]
            sigma_PPFD   = Y[3]
            sigma_H      = Y[4]
            sigma_STRU   = Y[5]

            # Create the scatter plot
            plt.scatter(mu_temp, sigma_temp,    s=50, marker= 'o', color= 'black')
            plt.scatter(mu_rh, sigma_rh,        s=50, marker= 's', color= 'black')
            plt.scatter(mu_CO2, sigma_CO2,      s=50, marker= '*', color= 'black')
            plt.scatter(mu_PPFD, sigma_PPFD,    s=50, marker= '^', color= 'black')
            plt.scatter(mu_H, sigma_H,          s=50, marker= 'd', color= 'black')
            plt.scatter(mu_STRU, sigma_STRU,    s=50, marker= 'P', color= 'black')
     
            # Add +-2SEM LINES
            # calc SD of mu, 
            mu_sd = EE_out_df[f'{output_short_name}_mu'].std()

            # calc sqrt of N, 
            denom = np.emath.sqrt(128)
            pos2_SEM = 2*(mu_sd/denom)
            neg2_SEM = -2*(mu_sd/denom)

            # I still don't fully understand how this centers the x axis to 0 but it does!
            x_max = np.abs(ax.get_xlim()).max()
            ax.set_xlim(xmin=-x_max, xmax=x_max)

            # Add lines from (0, 0) to SEM values
            plt.plot([0, neg2_SEM], [0, max(Y)], color='black', linestyle='--')
            plt.plot([0, pos2_SEM], [0, max(Y)], color='black', linestyle='--')

        # Set the labels and title
        plt.xlabel('mu')
        plt.ylabel('sigma')
        plt.title(f'EE of {output_short_name}')
        plt.legend(handles = SEM_legend)
        # plt.show()
        plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/figures/Elementary_Effects/EE_SEM_{output_short_name}_multimodel.png', bbox_inches='tight') #there are many options for savefig
        plt.close()

# Executes this program/function
if __name__ ==('__main__'):
    CHART()

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

# From the same paper listed above 
# . Morris (1991) suggested plotting two lines corresponding to μ ¼2 standard errors of 
# the mean (SEM) ¼ 2σ=sqrtðrÞ. All the parameters that are inside the wedge formed by these
#  two lines in μ − σ space can be considered to be involved in parameter interactions.
# """