from SALib import ProblemSpec
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import naming_function

# warnings.filterwarnings("ignore", category=np.RankWarning)

##########################################################
############## Defining the Model Inputs #################
##########################################################

inputs = naming_function.mec_input_names()
outputs = naming_function.mec_output_names()
models = naming_function.model_names()
sp = naming_function.prob_spec()

ami_c = '#2A119B'
bos_c = '#067300'
cav_c = '#8C0004'

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

import numpy as np

def GSUA_CHARTS():
    model_inputs = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/SOBOL_parameters.txt", sep=" ", names=['TEMP', 'RH', 'CO2', 'PPFD', 'H', 'STRU'])
    # Combining all the seperate datafiles into one for the anaylsis portion
    AMI_df = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/GSUA_AMI_out/data/GSUA_AMI_Simulations.csv", header=None)
    AMI_df_label = ['Timestep','skip?','SIM_NUM', 'H','A','ALPHA','BETA','CQY','CUE_24',
                     'DCG','CGR','TCB','TEB','DOP','VP_SAT','VP_AIR','VPD','P_GROSS',
                     'P_NET','g_S','g_A','g_C','DTR','TEMP','T_DARK','RH','CO2','PPFD', 'STRU']
    AMI_df.columns = AMI_df_label
    BOS_df = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/GSUA_BOS_out/data/GSUA_BOS_Simulations.csv", header=None)
    BOS_df_label = ['SIM_NUM','Timestep','H','Diurnal', 'A','ALPHA','BETA','CQY',
                     'CUE_24','DCG','CGR','DWCGR','TCB','TEB',
                     'VP_SAT','VP_AIR','VPD','P_NET','P_GROSS',
                     'DOP','DOC','g_S','g_A','g_C','DTR',
                     'DCO2C','DCO2P','DNC', 'DWC','TEMP',
                     'T_DARK','RH','CO2','PPFD', 'STRU']
    BOS_df.columns = BOS_df_label
    CAV_df = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/GSUA_CAV_out/data/GSUA_CAV_Simulations.csv", header=None)
    CAV_df_label = ['SIM_NUM','Timestep','H','A','ALPHA','BETA','CQY','CUE_24','DCG',
                     'CGR','TCB','TEB','DOP','VP_SAT','VP_AIR','VPD','P_GROSS',
                     'P_NET','g_S','g_A','g_C','DTR','TEMP','T_DARK','RH','CO2','PPFD', 'STRU']
    CAV_df.columns = CAV_df_label
    

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
        plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/figures/MEC_Histogram_{hist_long_name[i]}', bbox_inches='tight') #there are many options for savefig
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
            """This chart bulding stuff works!, but is there a better way?"""
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
            plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/figures/scatter/Scatter_{input_short_name}_X_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
            # plt.show()
            plt.close()

            # HISTOGRAM OF OUTPUTS
            labels = ['AMI','BOS', 'CAV']
            data = yA, yB, yC
            fig, ax = plt.subplots()
            bplot = ax.boxplot(data, vert=True, patch_artist=True, labels=labels, showfliers=False, meanline=True)
            ax.set_title(f'{output_long_name}')
            ax.set_ylabel(f'{output_unit}')
            light_colors = ['#A798EC', '#96F391', '#FE989A']
            for patch, light_colors in zip(bplot['boxes'], light_colors):
                patch.set_facecolor(light_colors)
            plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/figures/histogram/output_histogram_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
            plt.close()
            # plt.show()
            

# Executes this program/function
if __name__ ==('__main__'):
    GSUA_CHARTS()
