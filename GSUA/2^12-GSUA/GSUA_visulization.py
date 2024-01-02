import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import naming_function

# warnings.filterwarnings("ignore", category=np.RankWarning)

##########################################################
############## Defining the Model Inputs #################
##########################################################

gen_path, indiv_path, structure_path = naming_function.path_names()


ami_c = '#2A119B'
bos_c = '#067300'
cav_c = '#8C0004'

def GSUA_CHARTS(GSUA_type, models, inputs, outputs):

    if GSUA_type == 'Individual':
        df_AMI_sims_label, df_BOS_sims_label, df_CAV_sims_label = naming_function.df_labels(GSUA_type)

        model_inputs = pd.read_csv(f'{gen_path}INDIV_SOBOL_parameters.txt', sep=" ", names=['TEMP', 'RH', 'CO2', 'PPFD', 'H'])
        AMI_df = pd.read_csv(f'{indiv_path}GSUA_AMI_out/data/GSUA_AMI_Simulations.csv', names=df_AMI_sims_label)
        BOS_df = pd.read_csv(f'{indiv_path}GSUA_BOS_out/data/GSUA_BOS_Simulations.csv', names= df_BOS_sims_label)
        CAV_df = pd.read_csv(f'{indiv_path}/GSUA_CAV_out/data/GSUA_CAV_Simulations.csv', names= df_CAV_sims_label)

    if GSUA_type == 'Structure':
        model_inputs = pd.read_csv(f'{gen_path}STRUCTURE_SOBOL_parameters.txt', sep=" ", names=['TEMP', 'RH', 'CO2', 'PPFD', 'H', 'STRU'])
        df_AMI_sims_label, df_BOS_sims_label, df_CAV_sims_label = naming_function.df_labels(GSUA_type)

        # Combining all the seperate datafiles into one for the anaylsis portion
        AMI_df = pd.read_csv(f'{structure_path}GSUA_AMI_out/data/GSUA_AMI_Simulations.csv', names=df_AMI_sims_label)
        BOS_df = pd.read_csv(f'{structure_path}GSUA_BOS_out/data/GSUA_BOS_Simulations.csv', names=df_BOS_sims_label)
        CAV_df = pd.read_csv(f'{structure_path}GSUA_CAV_out/data/GSUA_CAV_Simulations.csv', names=df_CAV_sims_label)

    ##############################################
    ########### Input  Historgram ################
    ##############################################
    # for item in inputs:        # loop for inputs
    column_names = model_inputs.columns
    u = "\u00B5"        # unicode for the micro symbol
    hist_units = ["Degrees Celsius", "Percent", u+"mol$_{carbon}$ mol$_{air}$", u+"mol$_{photons}$ m$^{-2}$ second$^{-1}$", "hours day$^{-1}$", "Stuff"]
    hist_long_name = ["Temperature", "Relative Humidity", "CO$_{2}$ Concentration", "Photosynthetic Photon Flux Density", "Photoperiod", "Structure"]
    for i, column in enumerate(column_names):
        fig, ax = plt.subplots()
        ax.hist(model_inputs[column], bins=20, density=True, histtype='bar', color='#2A119B', edgecolor='white')
        ax.set_ylabel('Frequency')
        ax.set_xlabel(f'{hist_units[i]}')
        ax.set_title(f'{hist_long_name[i]}')
        if GSUA_type =='Individual':
            plt.savefig(f'{indiv_path}figures/MEC_Histogram_{hist_long_name[i]}', bbox_inches='tight') #there are many options for savefig
        if GSUA_type =='Structure':
            plt.savefig(f'{structure_path}figures/MEC_Histogram_{hist_long_name[i]}', bbox_inches='tight') #there are many options for savefig
        # plt.show()

    #####################################################
    ############## Input x Output #######################
    #####################################################
    for item in inputs:        # loop for inputs
        input_short_name = item[0]
        input_long_name = item[1]
        input_unit = item[2]
        for item in outputs:   # loop for outputs
            output_short_name = item[0]
            output_long_name = item[1]
            output_unit = item[2]
            """This chart bulding stuff works!"""
            AMI_DATA = AMI_df[['SIM_NUM', output_short_name, input_short_name]]
            BOS_DATA = BOS_df[['SIM_NUM', output_short_name, input_short_name]]
            CAV_DATA = CAV_df[['SIM_NUM', output_short_name, input_short_name]]
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
            ax.scatter(xA, yA, marker='o', label='AMI', color='#A798EC')
            ax.scatter(xB, yB, marker='s', label='BOS', color='#96F391')
            ax.scatter(xC, yC, marker='^', label='CAV', color='#FE989A')
            ax.set_ylabel(f'{output_unit}')
            ax.set_xlabel(f'{input_long_name} ({input_unit})')
            plt.title(f'{output_long_name} outputs')

            # calc the trendline
            zA = np.polyfit(xA, yA, 2) # 1 is linear, 2 is quadratic!
            zB = np.polyfit(xB, yB, 2) # 1 is linear, 2 is quadratic!
            zC = np.polyfit(xC, yC, 2) # 1 is linear, 2 is quadratic!
            pA = np.poly1d(zA)
            pB = np.poly1d(zB)
            pC = np.poly1d(zC)

            plt.plot(xA,pA(xA), color="#0000FF")
            plt.plot(xB,pB(xB), color="darkgreen")
            plt.plot(xC,pC(xC), color="#FF0000")
            if GSUA_type =='Individual':
                plt.savefig(f'{indiv_path}figures/scatter/Scatter_{input_short_name}_X_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
            if GSUA_type =='Structure':
                plt.savefig(f'{structure_path}figures/scatter/Scatter_{input_short_name}_X_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
            # plt.show()
            plt.close()

            # # Box and Whisker OF OUTPUTS
            labels = ['AMI','BOS', 'CAV']
            data = yA, yB, yC
            
            fig, ax = plt.subplots()
            bplot = ax.boxplot(data, vert=True, patch_artist=True, labels=labels, showfliers=False, meanline=True)
            ax.set_title(f'{output_long_name}')
            ax.set_ylabel(f'{output_unit}')
            light_colors = ['#A798EC', '#96F391', '#FE989A']
            for patch, light_colors in zip(bplot['boxes'], light_colors):
                patch.set_facecolor(light_colors)
            if GSUA_type =='Individual':
                plt.savefig(f'{indiv_path}figures/Box_and_whisker/B&W_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
            if GSUA_type =='Structure':
                plt.savefig(f'{structure_path}figures/Box_and_whisker/B&W_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
            plt.close()
            # plt.show()

            fig, axs = plt.subplots(3,1, figsize=(8,12), sharex=True)
            axs[0].hist(yA, label='AMI', bins=20, density=True, histtype='bar', color='#2A119B', edgecolor='white')
            axs[1].hist(yB, label='BOS', bins=20, density=True, histtype='bar', color='#067300', edgecolor='white')
            axs[2].hist(yC, label='CAV', bins=20, density=True, histtype='bar', color='#8C0004', edgecolor='white')
            
            axs[0].set_title(f'{output_long_name}')
            axs[1].set_ylabel('Frequency')
            axs[2].set_xlabel(f'{output_unit}')
            
            if GSUA_type =='Individual':
                plt.savefig(f'{indiv_path}figures/histogram/histogram_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
            if GSUA_type =='Structure':
                plt.savefig(f'{structure_path}figures/histogram/histogram_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
            plt.close()
            
            # plt.show()