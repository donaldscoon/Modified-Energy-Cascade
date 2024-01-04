from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.analyze import morris
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
##############   #################
##########################################################

gen_path, indiv_path, structure_path = naming_function.path_names()

ami_c = '#2A119B'
bos_c = '#067300'
cav_c = '#8C0004'

elinewidth, capsize, capthick = naming_function.conf_bars()

###########################################################
#################### Analysis #############################
###########################################################

def ANALYZE(GSUA_type, models, inputs, outputs):
    sp = naming_function.prob_spec(GSUA_type)

    if GSUA_type == 'Individual':
        # Create dataframes for each models GSUA runs
        df_AMI_sims = pd.read_csv(f'{indiv_path}/GSUA_AMI_out/data/GSUA_AMI_Simulations.csv')
        # df_BOS_sims = pd.read_csv(f'{indiv_path}/GSUA_BOS_out/data/GSUA_BOS_Simulations.csv')
        df_CAV_sims = pd.read_csv(f'{indiv_path}/GSUA_CAV_out/data/GSUA_CAV_Simulations.csv')

        X_df = pd.read_csv(f'{gen_path}INDIV_SOBOL_parameters.txt',
                        names= ['TEMP', 'RH', 'CO2', 'PPFD', 'H'], sep=' ')
        N = X_df['H'].nunique() # N = number of levels resulting from SOBOL Sampling
        X = np.loadtxt(f'{gen_path}INDIV_SOBOL_parameters.txt')

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
                Y = np.loadtxt(f'{indiv_path}/GSUA_{model_short_name}_out/data/GSUA_{model_short_name}_data_{output_short_name}.txt') # done to match the SALib example, imports the text file result
                EE = SALib.analyze.morris.analyze(sp, X, Y, conf_level=0.95, num_levels=N) # analyzes the Elementary effects for each models ouput

                with open(f'{indiv_path}results/full_out/{model_short_name}_{output_short_name}_EE_results.txt', 'w') as f:
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
        EE_out_df.to_csv(f'{indiv_path}results/EE_out.csv', index=False)


    if GSUA_type == 'Structure':
        # Create Input dataframe
        X_df = pd.read_csv(f'{gen_path}STRUCTURE_SOBOL_parameters.txt',
                        names= ['TEMP', 'RH', 'CO2', 'PPFD', 'H', 'STRU'], sep=' ')
        N = X_df['H'].nunique() # N = number of levels resulting from SOBOL Sampling
        X = np.loadtxt(f'{gen_path}STRUCTURE_SOBOL_parameters.txt')

        # Create Output dataframe
        df_sims = pd.read_csv(f'{structure_path}GSUA_simulations.csv')
        EE_out_df = pd.DataFrame({'Index': ['TEMP', 'RH', 'CO2', 'PPFD', 'H', 'STRU']})
        EE_out_df.set_index('Index')


        for item in outputs:        # loop for output names
            output_short_name = item[0]
            output_long_name = item[1]
            output_unit = item[2]
            
            # Loading specific outputs for Morris EE analysis 
            Y = df_sims[f'{output_short_name}'].to_numpy()
            EE = SALib.analyze.morris.analyze(sp, X, Y, conf_level=0.95, num_levels=N) # analyzes the Elementary effects for each models ouput

            with open(f'{structure_path}results/full_out/EE/{output_short_name}_EE_results.txt', 'w') as f:
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
        EE_out_df.to_csv(f'{structure_path}results/EE_out.csv', index=False)


def CHART(GSUA_type, models, inputs, outputs):

    ### All of these creates a single point for all the legend entries!
    temp_point = Line2D([0], [0], linestyle= '', color='black', marker= 'o', label='TEMP' )
    rh_point   = Line2D([0], [0], linestyle= '', color='black', marker= 's', label='RH' )
    CO2_point  = Line2D([0], [0], linestyle= '', color='black', marker= '*', label='CO2' )
    PPFD_point = Line2D([0], [0], linestyle= '', color='black', marker= '^', label='PPFD' )
    H_point    = Line2D([0], [0], linestyle= '', color='black', marker= 'd', label='H' )
    STRU_point = Line2D([0], [0], linestyle= '', color='black', marker= 'P', label='STRU')
    SEM_line   = Line2D([0], [0], linestyle= '--', color='black', label='+- 2 SEM')
    AMI_patch  = mpatches.Patch(color='#2A119B', label='AMI')
    BOS_patch  = mpatches.Patch(color='#067300', label='BOS')
    CAV_patch  = mpatches.Patch(color='#8C0004', label='CAV')

    if GSUA_type == 'Individual':
        onetoone_legend_single_model = [temp_point, rh_point, CO2_point, PPFD_point, H_point]
        onetoone_legend_multi_model  = [AMI_patch, BOS_patch, CAV_patch, temp_point, rh_point, CO2_point, PPFD_point, H_point]
        SEM_legend_single_model      = [temp_point, rh_point, CO2_point, PPFD_point, H_point, SEM_line]
        SEM_legend_multi_model       = [AMI_patch, BOS_patch, CAV_patch, temp_point, rh_point, CO2_point, PPFD_point, H_point, SEM_line]
        markers = ['o', 's', '*', '^', 'd']

        # read in the data
        EE_out_df = pd.read_csv(f'{indiv_path}/results/EE_out.csv')

        '''##########################################################
        mu star by sigma with a 1/1 line MULTIMODEL
        ########################################################'''
        for item in outputs:   # loop for outputs
            output_short_name = item[0]
            output_long_name = item[1]
            output_unit = item[2]

            plt.figure() # creates the figure for each output type, which is then iterated by model.
            for item in models:                 # loop for model names
                model_short_name = item[0]
                model_long_name = item[1]

                # sets the color of each model for that loop.
                if model_short_name == 'AMI':
                    color = ami_c
                elif model_short_name == 'BOS':
                    color = bos_c
                elif model_short_name == 'CAV':
                    color = cav_c
                # print(model_short_name, output_short_name)
                X = EE_out_df[f'{model_short_name}_{output_short_name}_mu_star']
                Y = EE_out_df[f'{model_short_name}_{output_short_name}_sigma']
                X_conf = EE_out_df[f'{model_short_name}_{output_short_name}__mu_star_conf']

                # Check if both X and Y have all zero values
                if not all(x == 0 for x in X) or not all(y == 0 for y in Y):
                    for i, marker in enumerate(markers):
                        # Extract data
                        mu_star = X[i]
                        sigma = Y[i]
                        mu_star_conf = X_conf[i]

                        # Create the scatter plot
                        plt.scatter(mu_star, sigma,    s=50, marker= 'o', color= color)

                        # Adding Confidences
                        plt.errorbar(mu_star,  sigma, xerr=mu_star_conf, ecolor=color, elinewidth=elinewidth, capsize=capsize, capthick=capthick)
        
                        # Add a 1:1 line
                        # min_val = min(min(X), min(Y))
                        max_val = max(max(X), max(Y))
                        plt.plot([0, max_val], [0, max_val], color='gray', linestyle='-')

            # Set the labels and title
            plt.xlabel('mu*')
            plt.ylabel('sigma')
            plt.title(f'EE of {output_short_name}')
            plt.legend(handles=onetoone_legend_multi_model)
            # plt.show()
            plt.savefig(f'{indiv_path}figures/Elementary_Effects/EE_1-1_{output_short_name}_multimodel.png', bbox_inches='tight') #there are many options for savefig
            plt.close()

        '''##########################################################
        mu star by sigma with a 1/1 line SINGLE MODEL
        #########################################################'''
        for item in models:                 # loop for model names
            model_short_name = item[0]
            model_long_name = item[1]
            for item in outputs:   # loop for outputs
                output_short_name = item[0]
                output_long_name = item[1]
                output_unit = item[2]

                plt.figure() # creates the figure for each output type, which is then iterated by model.

                # sets the color of each model for that loop.
                if model_short_name == 'AMI':
                    color = ami_c
                elif model_short_name == 'BOS':
                    color = bos_c
                elif model_short_name == 'CAV':
                    color = cav_c
                # print(model_short_name, output_short_name)
                X = EE_out_df[f'{model_short_name}_{output_short_name}_mu_star']
                Y = EE_out_df[f'{model_short_name}_{output_short_name}_sigma']
                X_conf = EE_out_df[f'{model_short_name}_{output_short_name}__mu_star_conf']

                # Check if both X and Y have all zero values
                if not all(x == 0 for x in X) or not all(y == 0 for y in Y):
                    for i, marker in enumerate(markers):
                        # Extract data
                        mu_star = X[i]
                        sigma = Y[i]
                        mu_star_conf = X_conf[i]

                        # Create the scatter plot
                        plt.scatter(mu_star, sigma,    s=50, marker= 'o', color= color)

                        # Adding Confidences
                        plt.errorbar(mu_star,  sigma, xerr=mu_star_conf, ecolor=color, elinewidth=elinewidth, capsize=capsize, capthick=capthick)
        
                    # Add a 1:1 line
                    # min_val = min(min(X), min(Y))
                    max_val = max(max(X), max(Y))
                    plt.plot([0, max_val], [0, max_val], color='gray', linestyle='-')

                # Set the labels and title
                plt.xlabel('mu*')
                plt.ylabel('sigma')
                plt.title(f'EE of {model_short_name}_{output_short_name}')
                plt.legend(handles=onetoone_legend_single_model)
                # plt.show()
                plt.savefig(f'{indiv_path}GSUA_{model_short_name}_out/figures/EE/EE_1-1{model_short_name}_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
                plt.close()

        '''###############################################################################
        mu by sigma with the V MULTIMODEL
        ###############################################################################'''

        for item in outputs:   # loop for outputs
            output_short_name = item[0]
            output_long_name = item[1]
            output_unit = item[2]
            fig, ax = plt.subplots() # creates the figure for each output type, which is then iterated by model.
            for item in models:                 # loop for model names
                model_short_name = item[0]
                model_long_name = item[1]

                # sets the color of each model for that loop.
                if model_short_name == 'AMI':
                    color = ami_c
                elif model_short_name == 'BOS':
                    color = bos_c
                elif model_short_name == 'CAV':
                    color = cav_c
                # print(model_short_name, output_short_name)
                X = EE_out_df[f'{model_short_name}_{output_short_name}_mu']
                Y = EE_out_df[f'{model_short_name}_{output_short_name}_sigma']

                # Check if both X and Y have all zero values
                if not all(x == 0 for x in X) or not all(y == 0 for y in Y):
                    for i, marker in enumerate(markers):
                        # Extract data
                        mu = X[i]
                        sigma = Y[i]                

                        # Create the scatter plot
                        plt.scatter(mu, sigma,    s=50, marker= marker, color= color)
                
                        # Add +-2SEM LINES
                        # calc SD of mu, 
                        mu_sd = EE_out_df[f'{model_short_name}_{output_short_name}_mu'].std()

                        # calc sqrt of N, 
                        denom = np.emath.sqrt(128)
                        pos2_SEM = 2*(mu_sd/denom)
                        neg2_SEM = -2*(mu_sd/denom)

                        # I still don't fully understand how this centers the x axis to 0 but it does!
                        x_max = np.abs(ax.get_xlim()).max()
                        ax.set_xlim(xmin=-x_max, xmax=x_max)

                        # Add lines from (0, 0) to SEM values
                        plt.plot([0, neg2_SEM], [0, max(Y)], color=color, linestyle='--')
                        plt.plot([0, pos2_SEM], [0, max(Y)], color=color, linestyle='--')
            
            # Set the labels and title
            plt.xlabel('mu')
            plt.ylabel('sigma')
            plt.title(f'EE of {output_short_name}')
            plt.legend(handles=SEM_legend_multi_model)
            # plt.show()
            plt.savefig(f'{indiv_path}/figures/Elementary_Effects/EE_SEM_{output_short_name}_multimodel.png', bbox_inches='tight') #there are many options for savefig
            plt.close()

        '''###############################################################################
        mu by sigma with the V SINGLE MODEL
        ###############################################################################'''

        for item in models:                 # loop for model names
            model_short_name = item[0]
            model_long_name = item[1]
            for item in outputs:   # loop for outputs
                output_short_name = item[0]
                output_long_name = item[1]
                output_unit = item[2]
                fig, ax = plt.subplots() # creates the figure for each output type, which is then iterated by model.

                # sets the color of each model for that loop.
                if model_short_name == 'AMI':
                    color = ami_c
                elif model_short_name == 'BOS':
                    color = bos_c
                elif model_short_name == 'CAV':
                    color = cav_c
                # print(model_short_name, output_short_name)
                X = EE_out_df[f'{model_short_name}_{output_short_name}_mu']
                Y = EE_out_df[f'{model_short_name}_{output_short_name}_sigma']

                # Check if both X and Y have all zero values
                if not all(x == 0 for x in X) or not all(y == 0 for y in Y):
                    for i, marker in enumerate(markers):
                        # Extract data
                        mu = X[i]
                        sigma = Y[i]                

                        # Create the scatter plot
                        plt.scatter(mu, sigma,    s=50, marker= marker, color= color)
                
                        # Add +-2SEM LINES
                        # calc SD of mu, 
                        mu_sd = EE_out_df[f'{model_short_name}_{output_short_name}_mu'].std()

                        # calc sqrt of N, 
                        denom = np.emath.sqrt(128)
                        pos2_SEM = 2*(mu_sd/denom)
                        neg2_SEM = -2*(mu_sd/denom)

                        # I still don't fully understand how this centers the x axis to 0 but it does!
                        x_max = np.abs(ax.get_xlim()).max()
                        ax.set_xlim(xmin=-x_max, xmax=x_max)

                        # Add lines from (0, 0) to SEM values
                        plt.plot([0, neg2_SEM], [0, max(Y)], color=color, linestyle='--')
                        plt.plot([0, pos2_SEM], [0, max(Y)], color=color, linestyle='--')
            
                    # Set the labels and title
                    plt.xlabel('mu')
                    plt.ylabel('sigma')
                    plt.title(f'EE of {model_short_name}_{output_short_name}')
                    plt.legend(handles=SEM_legend_single_model)
                    # plt.show()
                    plt.savefig(f'{indiv_path}/GSUA_{model_short_name}_out/figures/EE/EE_SEM_{model_short_name}_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
                    plt.close()

    if GSUA_type =='Structure':
        onetoone_legend = [temp_point, rh_point, CO2_point, PPFD_point, H_point, STRU_point]
        SEM_legend = [temp_point, rh_point, CO2_point, PPFD_point, H_point, STRU_point, SEM_line]
        EE_out_df = pd.read_csv(f'{structure_path}results/EE_out.csv')
        markers = ['o', 's', '*', '^', 'd', 'P']
            
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
                for i, marker in enumerate(markers):
                    # Extract data
                    mu_star = X[i]
                    sigma = Y[i]
                    mu_star_conf = X_conf[i]

                    # Create scatter plot
                    plt.scatter(mu_star, sigma, s=50, marker=marker, color='black')

                    # Adding Confidence bars
                    plt.errorbar(mu_star, sigma, xerr=mu_star_conf, ecolor='black', elinewidth=elinewidth, capsize=capsize, capthick=capthick)

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
                plt.savefig(f'{structure_path}figures/Elementary_Effects/EE_1-1_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
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
                for i, marker in enumerate(markers):
                    # Extract data
                    mu = X[i]
                    sigma = Y[i]                

                    # Create the scatter plot
                    plt.scatter(mu, sigma,    s=50, marker= marker, color= 'black')
            
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
                plt.savefig(f'{structure_path}figures/Elementary_Effects/EE_SEM_{output_short_name}_multimodel.png', bbox_inches='tight') #there are many options for savefig
                plt.close()

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