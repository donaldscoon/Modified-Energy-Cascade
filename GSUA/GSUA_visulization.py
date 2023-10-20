from SALib import ProblemSpec
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import naming_function

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
    model_inputs = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_parameters.txt", sep=" ", names=['TEMP', 'RH', 'CO2', 'PPFD', 'H', 'STRU'])
    df_AMI_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_AMI_out/data/GSUA_AMI_Simulations.csv')
    df_BOS_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_BOS_out/data/GSUA_BOS_Simulations.csv')
    df_CAV_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_CAV_out/data/GSUA_CAV_Simulations.csv')

    ##############################################
    ########### Input  Historgram ################
    ##############################################
    # for item in mec_inputs:        # loop for inputs
    #     input_short_name = item[0]
    #     input_long_name = item[1]
    #     input_unit = item[2]
    #     input_sample_name = item[3]
    #     fig, ax = plt.subplots()
    #     ax.hist(model_inputs[f'{input_sample_name}'], 15, density=True, histtype='bar', color='#2A119B', edgecolor='white')
    #     ax.set_ylabel('Frequency')
    #     ax.set_xlabel(f'{input_unit}')
    #     ax.set_title(f'{input_long_name} Frequency')
    #     plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_Histogram_{input_sample_name}', bbox_inches='tight') #there are many options for savefig
    #     # plt.show()



    #####################################################
    ############## Input x Output #######################
    #####################################################

    # for item in mec_inputs:        # loop for inputs
    #     input_short_name = item[0]
    #     input_long_name = item[1]
    #     input_unit = item[2]
    #     for item in outputs:   # loop for outputs
    #         output_short_name = item[0]
    #         output_long_name = item[1]
    #         output_unit = item[2]
    #         """This chart bulding stuff works!, but is there a better way?"""
    #         AMI_DATA = df_AMI_sims[['Simulation', output_short_name, input_short_name]]
    #         BOS_DATA = df_BOS_sims[['Simulation', output_short_name, input_short_name]]
    #         CAV_DATA = df_CAV_sims[['Simulation', output_short_name, input_short_name]]
    #         AMI_DATA = AMI_DATA.sort_values(input_short_name, ascending=True)
    #         BOS_DATA = BOS_DATA.sort_values(input_short_name, ascending=True)
    #         CAV_DATA = CAV_DATA.sort_values(input_short_name, ascending=True)
            
    #         xA = AMI_DATA[[input_short_name]].values.flatten()       # the flatten converts the df to a 1D array, needed for trendline
    #         yA = AMI_DATA[[output_short_name]].values.flatten()      # the flatten converts the df to a 1D array, needed for trendline
    #         xB = BOS_DATA[[input_short_name]].values.flatten()       # the flatten converts the df to a 1D array, needed for trendline
    #         yB = BOS_DATA[[output_short_name]].values.flatten()      # the flatten converts the df to a 1D array, needed for trendline
    #         xC = CAV_DATA[[input_short_name]].values.flatten()       # the flatten converts the df to a 1D array, needed for trendline
    #         yC = CAV_DATA[[output_short_name]].values.flatten()      # the flatten converts the df to a 1D array, needed for trendline
    #         fig, ax = plt.subplots()
    #         ax.scatter(xA, yA, marker='o', label='AMI', color='#A798EC')
    #         ax.scatter(xB, yB, marker='s', label='BOS', color='#96F391')
    #         ax.scatter(xC, yC, marker='^', label='CAV', color='#FE989A')
    #         ax.set_ylabel(f'{output_unit}')
    #         ax.set_xlabel(f'{input_long_name} ({input_unit})')
    #         plt.title(f'MEC {output_long_name} outputs')

    #         # calc the trendline
    #         zA = np.polyfit(xA, yA, 2) # 1 is linear, 2 is quadratic!
    #         zB = np.polyfit(xB, yB, 2) # 1 is linear, 2 is quadratic!
    #         zC = np.polyfit(xC, yC, 2) # 1 is linear, 2 is quadratic!
    #         pA = np.poly1d(zA)
    #         pB = np.poly1d(zB)
    #         pC = np.poly1d(zC)

    #         plt.plot(xA,pA(xA), color="#0000FF")
    #         plt.plot(xB,pB(xB), color="darkgreen")
    #         plt.plot(xC,pC(xC), color="#FF0000")
    #         plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/scatter/MEC_Scatter_{input_short_name}_X_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
    #         # plt.show()
    #         plt.close()

    #         # HISTOGRAM OF OUTPUTS
    #         labels = ['AMI','BOS', 'CAV']
    #         data = yA, yB, yC
    #         fig, ax = plt.subplots()
    #         bplot = ax.boxplot(data, vert=True, patch_artist=True, labels=labels, showfliers=False, meanline=True)
    #         ax.set_title(f'{output_long_name}')
    #         ax.set_ylabel(f'{output_unit}')
    #         light_colors = ['#A798EC', '#96F391', '#FE989A']
    #         for patch, light_colors in zip(bplot['boxes'], light_colors):
    #             patch.set_facecolor(light_colors)
    #         plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/histogram/MEC_Histogram_{output_short_name}.png', bbox_inches='tight') #there are many options for savefig
    #         plt.close()
    #         # plt.show()
            



# Executes this program/function
if __name__ ==('__main__'):
    GSUA_CHARTS()

"""God this is painful. I need to find a way to parse the output. """

# #####################
# ###### P_NET ########
# #####################

# # X is arbitrary number to arrange,
# # Y is the value of the interactions,
# # ci is the confidence intervals

# '''Total order interactions'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8]
# xB = [1, 2, 3, 4, 5]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2]
# yA = [0, 0, 0, 0.873, 0.167]
# ciA = [0, 0, 0, 0.292, 0.079]
# yB = [0, 0, 0.013, 1.015, 0]
# ciB = [0, 0, 0.008, 0.240, 0]
# yC = [0, 0, 0.013, 0.992, 0.044]
# ciC = [0, 0, 0.007, 0.259, 0.018]

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5), ('TEMP', 'RH', 'CO2', 'PPFD', 'H'))
# plt.title('Total Order Effects on Net Photosynthesis')
# # plt.show()
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_ST_P_NET.png", bbox_inches='tight')


# '''First order interactions'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8]
# xB = [1, 2, 3, 4, 5]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2]
# yA = [0, 0, 0, 0.875, 0.064]
# ciA= [0, 0, 0, 0.286, 0.140]
# yB = [0, 0, 0.035, 1.018, 0]
# ciB= [0, 0, 0.040, 0.313, 0]
# yC = [0, 0, 0.037, 0.982, 0.008]
# ciC= [0, 0, 0.047, 0.302, 0.074]

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5), ('TEMP', 'RH', 'CO2', 'PPFD', 'H'))
# plt.title('1st Order Effects on Net Photosynthesis')
# # plt.show()
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_S1_P_NET.png", bbox_inches='tight')


# '''2nd Order Effects on Net Photosythesis'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8, 5.8, 6.8, 7.8, 8.8, 9.8]
# xB = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2, 6.2, 7.2, 8.2, 9.2, 10.2]
# yA = [0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.005]
# ciA= [0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.425]
# yB = [0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, -0.034, -0.017, 0.017]
# ciB= [0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.082, 0.066, 0.370]
# yC = [0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, -0.043, -0.027, 0.016]
# ciC= [0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.091, 0.076, 0.383]

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), ('TEMPxRH', 'TEMPxCO2', 'TEMPxPPFD', 'TEMPxH',
#                                              'RHxCO2',  'RHxCO2',   'RHxH',      'CO2xPPFD',
#                                              'CO2xH',   'PPFDxH'), rotation = 90)
# plt.title('2nd Order Effects on Net Photosynthesis')
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_S2_P_NET.png", bbox_inches='tight')
# # plt.show()

# ###########################
# ######## g_S      #########
# ###########################

# '''Total order interactions'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8]
# xB = [1, 2, 3, 4, 5]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2]
# yA = [0.203351, 0.082412, 0.224088, 0.359466, 0.062973]
# ciA= [0.160217, 0.061703, 0.136246, 0.278845, 0.040913]
# yB = [0.240784, 0.095836, 0.153885, 0.450163, 0]
# ciB= [0.176207, 0.067689, 0.07595, 0.35218, 0]
# yC = [0.236476, 0.088897, 0.152936, 0.428091, 0.017313]
# ciC= [0.140453, 0.053091, 0.07678, 0.26117, 0.009588]

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5), ('TEMP', 'RH', 'CO2', 'PPFD', 'H'))
# plt.title('Total Order Effects on Stomatal Conductance')
# # plt.show()
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_ST_g_s.png", bbox_inches='tight')


# '''First order interactions'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8]
# xB = [1, 2, 3, 4, 5]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2]
# yA = [0.218326, 0.095018, 0.165191, 0.226777, 0.05046]
# ciA= [0.229367, 0.112021, 0.30198, 0.161722, 0.058584]
# yB = [0.22847, 0.100263, 0.163066, 0.296736, 0]
# ciB= [0.227079, 0.119202, 0.238653, 0.187154, 0]
# yC = [0.250475, 0.109484, 0.143409, 0.286707, 0.020507]
# ciC= [0.203858, 0.114024, 0.235367, 0.173932, 0.028939]

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5), ('TEMP', 'RH', 'CO2', 'PPFD', 'H'))
# plt.title('1st Order Effects on Stomatal Conductance')
# # plt.show()
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_S1_g_S.png", bbox_inches='tight')


# '''2nd Order Effects on Net Photosythesis'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8, 5.8, 6.8, 7.8, 8.8, 9.8]
# xB = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2, 6.2, 7.2, 8.2, 9.2, 10.2]
# yA = [-0.094213, -0.037701, 0.000859, -0.087277, -0.11674, -0.019268, -0.051328, 0.184024, 0.013447, -0.013646]
# ciA= [0.22867, 0.228037, 0.253553, 0.2234, 0.267995, 0.237504, 0.194319, 0.755283, 0.56606, 0.221013]
# yB = [-0.071227, -0.001128, 0.086512, -0.056399, -0.079914, -0.009733, 0.001974, -0.020333, -0.087466, 0.050103]
# ciB= [0.263734, 0.255288, 0.361648, 0.255657, 0.306839, 0.243123, 0.254276, 0.441845, 0.378588, 0.256338]
# yC = [-0.095443, -0.037667, 0.029396, -0.088613, -0.108224, -0.025803, -0.043392, 0.018837, -0.059768, 0.035454]
# ciC= [0.246628, 0.245508, 0.256454, 0.240315, 0.281885, 0.231793, 0.224463, 0.479359, 0.406405, 0.230222]

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), ('TEMPxRH', 'TEMPxCO2', 'TEMPxPPFD', 'TEMPxH',
#                                              'RHxCO2',  'RHxCO2',   'RHxH',      'CO2xPPFD',
#                                              'CO2xH',   'PPFDxH'), rotation = 90)
# plt.title('2nd Order Effects on Stomatal Conductance')
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_S2_g_S.png", bbox_inches='tight')
# # plt.show()

# ###########################
# ######## g_C      #########
# ###########################

# '''Total order interactions'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8]
# xB = [1, 2, 3, 4, 5]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2]
# yA = [0.277183, 0.044635, 0.068351, 0.435722, 0.033809]
# ciA= [0.132442, 0.042013, 0.046922, 0.351973, 0.04052]
# yB = [0.045088, 0.009679, 0.001828, 0.639677, 0]
# ciB= [0.075487, 0.023026, 0.004005, 0.52462, 0]
# yC = [0.052174, 0.011005, 0.002197, 0.655045, 0.002285]
# ciC= [0.06979, 0.021209, 0.00403, 0.535692, 0.003464]

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5), ('TEMP', 'RH', 'CO2', 'PPFD', 'H'))
# plt.title('Total Order Effects on Canopy Conductance')
# # plt.show()
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_ST_g_C.png", bbox_inches='tight')


# '''First order interactions'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8]
# xB = [1, 2, 3, 4, 5]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2]
# yA = [0.159288, 0.018477, -0.017403, 0.569955, 0.025405]
# ciA= [0.364374, 0.042768, 0.064516, 0.606662, 0.040464]
# yB = [0.015597, 0.007643, -0.00225, 0.778666, 0]
# ciB= [0.129908, 0.023246, 0.011923, 0.904666, 0]
# yC = [0.037959, 0.007255, -0.002319, 0.782914, -0.000434]
# ciC= [0.110814, 0.017025, 0.01294, 0.895775, 0.00898]

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5), ('TEMP', 'RH', 'CO2', 'PPFD', 'H'))
# plt.title('1st Order Effects on Canopy Conductance')
# # plt.show()
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_S1_g_C.png", bbox_inches='tight')


# '''2nd Order Effects on Net Photosythesis'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8, 5.8, 6.8, 7.8, 8.8, 9.8]
# xB = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2, 6.2, 7.2, 8.2, 9.2, 10.2]
# yA = [0.331429, 0.227392, 0.186742, 0.308162, -0.003936, 0.015667, -0.017275, 0.135158, 0.173947, -0.233026]
# ciA= [0.743834, 0.553474, 0.679261, 0.70714, 0.142908, 0.170426, 0.176313, 0.253924, 0.295512, 0.597683]
# yB = [0.138667, 0.139972, 0.104223, 0.139959, -0.052505, -0.046542, -0.053518, 0.0186, 0.014572, -0.217337]
# ciB= [0.229375, 0.224764, 0.259003, 0.225907, 0.082069, 0.078371, 0.081242, 0.023888, 0.025132, 1.10839]
# yC = [0.08673, 0.089954, 0.050556, 0.089183, -0.03702, -0.035879, -0.036716, 0.016322, 0.009175, -0.209509]
# ciC= [0.184585, 0.18084, 0.221328, 0.181903, 0.070438, 0.077498, 0.070684, 0.026054, 0.028569, 1.054556]

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), ('TEMPxRH', 'TEMPxCO2', 'TEMPxPPFD', 'TEMPxH',
#                                              'RHxCO2',  'RHxCO2',   'RHxH',      'CO2xPPFD',
#                                              'CO2xH',   'PPFDxH'), rotation = 90)
# plt.title('2nd Order Effects on Canopy Conductance')
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_S2_g_C.png", bbox_inches='tight')
# # plt.show()


# ###########################
# ########    DTR   #########
# ###########################

# '''Total order interactions'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8]
# xB = [1, 2, 3, 4, 5]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2]
# yA = [0.532039, 0.13436, 0.001144, 0.009532, 0.347455]
# ciA= [0.293241, 0.08078, 0.000816, 0.006139, 0.200646]
# yB = [0.466896, 0.124277, 0.000089, 0.037143, 0.352208]
# ciB= [0.298177, 0.07094, 0.000058, 0.034366, 0.194551]
# yC = [0.463952, 0.125294, 0.000138, 0.050157, 0.339835]
# ciC= [0.268025, 0.07, 0.000074, 0.032343, 0.210922]

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5), ('TEMP', 'RH', 'CO2', 'PPFD', 'H'))
# plt.title('Total Order Effects on Daily Transpiration Rate')
# # plt.show()
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_ST_DTR.png", bbox_inches='tight')


# '''First order interactions'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8]
# xB = [1, 2, 3, 4, 5]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2]
# yA = [0.340312, 0.086133, -0.002188, 0.013242, 0.207436]
# ciA= [0.286131, 0.12226, 0.010614, 0.028784, 0.231634]
# yB = [0.306618, 0.077491, -0.000653, 0.050511, 0.220884]
# ciB= [0.283585, 0.129338, 0.003837, 0.069027, 0.198864]
# yC = [0.310733, 0.078421, -0.000155, 0.059749, 0.208342]
# ciC= [0.290377, 0.135346, 0.00511, 0.062912, 0.193133]

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5), ('TEMP', 'RH', 'CO2', 'PPFD', 'H'))
# plt.title('1st Order Effects on Daily Transpiration Rate')
# # plt.show()
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_S1_DTR.png", bbox_inches='tight')


# '''2nd Order Effects on Net Photosythesis'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8, 5.8, 6.8, 7.8, 8.8, 9.8]
# xB = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2, 6.2, 7.2, 8.2, 9.2, 10.2]
# yA = [0.215629, 0.250724, 0.240951, 0.401755, 0.098164, 0.090832, 0.098724, -0.003175, -0.001237, -0.002352]
# ciA= [0.411232, 0.365664, 0.390219, 0.429607, 0.202084, 0.201031, 0.264813, 0.021559, 0.023854, 0.048751]
# yB = [0.202825, 0.238087, 0.213999, 0.383917, 0.100235, 0.091922, 0.101678, -0.001639, -0.001361, -0.009885]
# ciB= [0.341632, 0.314587, 0.34378, 0.381982, 0.197874, 0.198588, 0.250565, 0.006283, 0.006634, 0.089251]
# yC = [0.187864, 0.224172, 0.200181, 0.364159, 0.102893, 0.09224, 0.109479, -0.003163, -0.003181, -0.009393]
# ciC= [0.309704, 0.292674, 0.355998, 0.33657, 0.202666, 0.204695, 0.257784, 0.00824, 0.00853, 0.087397]

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), ('TEMPxRH', 'TEMPxCO2', 'TEMPxPPFD', 'TEMPxH',
#                                              'RHxCO2',  'RHxCO2',   'RHxH',      'CO2xPPFD',
#                                              'CO2xH',   'PPFDxH'), rotation = 90)
# plt.title('2nd Order Effects on Daily Transpiration Rate')
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_S2_DTR.png", bbox_inches='tight')
# # plt.show()

# #########################################
# ############# TEB #######################
# #########################################

# '''Total order interactions'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8]
# # xB = [1, 2, 3, 4, 5]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2]
# yA = [0, 0, 0, 0.675554, 0.408258]
# ciA= [0, 0, 0, 0.21016, 0.162826]
# # yB = []
# # ciB= []
# yC = [0, 0, 0.01271, 0.817626, 0.298098]
# ciC= [0, 0, 0.007627, 0.232201, 0.133595]

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5), ('TEMP', 'RH', 'CO2', 'PPFD', 'H'))
# plt.title('Total Order Effects on Total Edible Biomass')
# # plt.show()
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_ST_TEB.png", bbox_inches='tight')


# '''First order interactions'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8]
# # xB = [1, 2, 3, 4, 5]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2]
# yA = [0, 0, 0, 0.599574, 0.432014]
# ciA= [0, 0, 0, 0.311351, 0.19895]
# # yB = []
# # ciB= []
# yC = [0, 0, 0.01949, 0.735811, 0.28511]
# ciC= [0, 0, 0.031709, 0.343739, 0.189536]

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# # ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# # plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5), ('TEMP', 'RH', 'CO2', 'PPFD', 'H'))
# plt.title('1st Order Effects on Total Edible Biomass')
# # plt.show()
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_S1_TEB.png", bbox_inches='tight')


# '''2nd Order Effects on Net Photosythesis'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8, 5.8, 6.8, 7.8, 8.8, 9.8]
# # xB = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2, 6.2, 7.2, 8.2, 9.2, 10.2]
# yA = [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.082964]
# ciA= [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.498697]
# # yB = []
# # ciB= []
# yC = [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.006686, 0.000273, 0.123295]
# ciC= [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.080871, 0.058927, 0.474082]

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# # ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# # plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), ('TEMPxRH', 'TEMPxCO2', 'TEMPxPPFD', 'TEMPxH',
#                                              'RHxCO2',  'RHxCO2',   'RHxH',      'CO2xPPFD',
#                                              'CO2xH',   'PPFDxH'), rotation = 90)
# plt.title('2nd Order Effects on Total Edible Biomass')
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_S2_TEB.png", bbox_inches='tight')
# # plt.show()

# ###########################
# ######## Template #########
# ###########################
# """
# '''Total order interactions'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8]
# xB = [1, 2, 3, 4, 5]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2]
# yA = []
# ciA= []
# yB = []
# ciB= []
# yC = []
# ciC= []

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5), ('TEMP', 'RH', 'CO2', 'PPFD', 'H'))
# plt.title('Total Order Effects on Net Photosynthesis')
# # plt.show()
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_ST_template.png", bbox_inches='tight')


# '''First order interactions'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8]
# xB = [1, 2, 3, 4, 5]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2]
# yA = []
# ciA= []
# yB = []
# ciB= []
# yC = []
# ciC= []

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5), ('TEMP', 'RH', 'CO2', 'PPFD', 'H'))
# plt.title('1st Order Effects on Net Photosynthesis')
# # plt.show()
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_S1_template.png", bbox_inches='tight')


# '''2nd Order Effects on Net Photosythesis'''
# xA = [.8, 1.8, 2.8, 3.8, 4.8, 5.8, 6.8, 7.8, 8.8, 9.8]
# xB = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# xC = [1.2, 2.2, 3.2, 4.2, 5.2, 6.2, 7.2, 8.2, 9.2, 10.2]
# yA = []
# ciA= []
# yB = []
# ciB= []
# yC = []
# ciC= []

# fig, ax = plt.subplots()
# ax.scatter(xA, yA)
# ax.scatter(xB, yB)
# ax.scatter(xC, yC)
# plt.errorbar(xA, yA, yerr=ciA, fmt = 'o', label = "AMI", color=ami_c)
# plt.errorbar(xB, yB, yerr=ciB, fmt = 'o', label = "BOS", color=bos_c)
# plt.errorbar(xC, yC, yerr=ciC, fmt = 'o', label = "CAV", color=cav_c)
# plt.legend()
# plt.xticks((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), ('TEMPxRH', 'TEMPxCO2', 'TEMPxPPFD', 'TEMPxH',
#                                              'RHxCO2',  'RHxCO2',   'RHxH',      'CO2xPPFD',
#                                              'CO2xH',   'PPFDxH'), rotation = 90)
# plt.title('2nd Order Effects on Net Photosynthesis')
# plt.savefig("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/figures/MEC_GSUA_S2_template.png", bbox_inches='tight')
# # plt.show()
# """