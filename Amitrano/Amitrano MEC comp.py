# -*- coding: utf-8 -*-
"""
Created on Mon Feb  20 2023

@author: donal

Written to recreate the MEC authored by Chiara Amitrano

End goal is global sensitivity and uncertainty analysis of this version and comparison against others. 

Maybe one day I modify the structure to accept flags like a real program
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


##################################################
################## MODEL INPUTS ##################
##################################################
PPFD = 314.54       # found at Amitrano 2020 table 2 but used decimal value in GN excel
CO2 = 370           # value used in Amitranos excel
H = 12              # Amitrano 2020 table 2
T_LIGHT = 24        # placeholder value
RH = .675

##################################################
################# INTIALIZATION  #################
##################################################

t = 1               # time in days
res = 1             # model resolution (in days)
i = 0               # matrix/loop counter

##################################################
#################### CONSTANTS ###################
##################################################
BCF = 0.4           # Amitrano 2020 table 2 -> Adeyemi 2018
XFRT = 0.95         # Amitrano 2020 table 2 -> Adeyemi 2018
OPF = 1.08          # Amitrano 2020 table 2 -> Adeyemi 2018
g_A = 2.5           # Amitrano 2020 table 2 -> Amitrano 2019
t_D = 1             # 1 for green, 8 for red initial time of development(days) Amirtrano 2020 CQY experiments
t_Mi = 16           # initial time of maturity (days) Amitrano 2020 table 2
t_M = 23            # time of harvesting (days) Amitrano 2020 table 2
t_E = 1             # time at onset of organ formation Amitrano 2020 same as ewert table 4-112
MWC = 12.01            # molecular weight of carbon amitrano 2020
MW_W = 18.015       # molecular weight of water ewert table 4-110
d_W = 998.23        # water density ewert table 4-110
P_ATM = 101         # atmospheric pressure Number from Amitrano excel
T_LEAF = 24       # experimental data from  amitrano

amin_GN = 0.00691867456539118    # amitrano 2020 calibrated with growth chamber experiment exact value from excel
amin_RN = 0.0069915227965273     # amitrano 2020 calibrated with growth chamber experiment exact value from excel
amin_GON = 0.00342717997911672   # amitrano 2020 calibrated with growth chamber experiment exact value from excel
amin_RON = 0.0027368743949879    # amitrano 2020 calibrated with growth chamber experiment exact value from excel

amax_GN = 0.017148682744336      # amitrano 2020 calibrated with growth chamber experiment exact value from excel
amax_RN = 0.0210442078518921     # amitrano 2020 calibrated with growth chamber experiment exact value from excel    
amax_GON = 0.00952341360955465   # amitrano 2020 calibrated with growth chamber experiment exact value from excel
amax_RON = 0.0108277387986636    # amitrano 2020 calibrated with growth chamber experiment exact value from excel

bmin_GN = 0                      # amitrano 2020 calibrated with growth chamber experiment exact value from excel
bmin_RN = 0.0220120589922702     # amitrano 2020 calibrated with growth chamber experiment exact value from excel
bmin_GON = 0.0486455477321762    # amitrano 2020 calibrated with growth chamber experiment exact value from excel
bmin_RON = 0.0361034591767831    # amitrano 2020 calibrated with growth chamber experiment exact value from excel

bmax_GN = 0.0451765692503675     # amitrano 2020 calibrated with growth chamber experiment exact value from excel
bmax_RN = 0.0284636898862895     # amitrano 2020 calibrated with growth chamber experiment exact value from excel
bmax_GON = 0.0564626043274799    # amitrano 2020 calibrated with growth chamber experiment exact value from excel
bmax_RON = 0.0598757705974144    # amitrano 2020 calibrated with growth chamber experiment exact value from excel

##################################################
################ Data Management #################
##################################################
df_records = pd.DataFrame({})

ts_to_harvest = int(t_M/res)             # calcs the timesteps needed to set up the matrix for each ts
TEB = 8.53                               # this is the only way I could make it match excel WHERE IT FROM??
edible_mat = np.zeros(ts_to_harvest+1)   # matrix for TEB storage

##################################################
############# SUPPLEMENTAL EQUATIONS #############
##################################################

##################################################
################# THE MODEL LOOP #################
##################################################
while t <= ts_to_harvest:                  # while time is less than harvest time
    if t<= t_D:                            # if timestep is before formation of edible organs
        alpha = amin_GN                    # amitrano 2020 eq 15
        beta = bmin_GN                     # amitrano 2020 eq 15
    elif t <= t_Mi:                        # if timestep is after organ formation but before maturity
        alpha = amin_GN+(amax_GN-amin_GN)*(t-t_D)/(t_Mi-t_D)        # amitrano 2020 eq 15
        beta = bmin_GN+(bmax_GN-bmin_GN)*(t-t_D)/(t_Mi-t_D)         # amitrano 2020 eq 15
    else:                                  # all other timesteps
        alpha = amax_GN                    # amitrano 2020 eq 15
        beta = bmax_GN                     # amitrano 2020 eq 15
    DCG = 0.0036*H*alpha*PPFD              # amitrano 2020 eq 4
    DOP = OPF*DCG                          # amitrano 2020 eq 5
    CGR = MWC*DCG/BCF                      # amitrano 2020 eq 6
    if t > t_E:                            # if edible organ formation has begun
        TEB = CGR+TEB                      # Amitrano 2020 GN excel column I
    edible_mat[i] = TEB                    # matrix that stores past values of TEB
    P_GROSS = beta*PPFD                    # amitrano 2020 eq 8
    VP_SAT = 0.611*np.exp(1)**(17.4*T_LEAF/(T_LEAF+239)) # Same as ewert and cavazzoni, though likely from Monje 1998
    VP_AIR = VP_SAT*RH                     # Same as ewert and cavazzoni, though likely from Monje 1998
    VPD = VP_SAT*(1-RH)                    # Same as ewert and cavazzoni, though likely from Monje 1998
    P_NET = (H*alpha/24+beta*(24-H)/24)*PPFD    # Amitrano 2020 eq 9
    g_S = ((1.717*T_LEAF)-19.96-(10.54*VPD))*(P_NET/CO2) # Amitrano 2020 eq 10 (with some nice parenthesis that don't change anything)
    g_C = g_A*g_S/(g_A+g_S)                # Amitrano 2020 eq 10
    DTR = 3600*H*(MW_W/d_W)*g_C*(VPD/P_ATM)

    dfts = pd.DataFrame({
        'Timestep': [t],
        'Photoperiod': [H],
        'PPFD': [PPFD],
        'alpha': [alpha],
        'beta': [beta],
        'DCG': [DCG],
        'DOP': [DOP],
        'CGR': [CGR],
        'TEB': [TEB],
        'P_GROSS': [P_GROSS],
        'P_NET': [P_NET],
        'T_LIGHT': [T_LIGHT],
        'VP_SAT': [VP_SAT],
        'VP_AIR': [VP_AIR],
        'RH': [RH],
        'VPD': [VPD], 
        'g_S': [g_S],
        'g_C': [g_C],
        'DTR': [DTR],
        'g_A': [g_A]
    }) # creates a dataframe of all variables/outputs for each timestep. 
    df_records = pd.concat([df_records, dfts], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
    t += res                         # advance timestep
    i += 1                           # increase matrix index counter

print(df_records)       # Prints entire dataframe
# print(df_records[['Timestep', 'g_S', 'g_C', 'DTR']])                    # prints specific columns
# df_records.to_csv('C:/Users/donal/Documents/Github/Modified-Energy-Cascade/Amitrano/MEC_AMI_OUT.csv') # exports final data frame to a CSV
# print(df_records[['Timestep', 'DTR', 'g_C', 'g_S', 'P_NET']])
# df_records.to_csv('C:/Users/donal/Documents/Github/Modified-Energy-Cascade/Amitrano/MEC_AMICOMP_OUT.csv') # exports final data frame to a CSV

############################################################
##################### VISUALIZATIONS #######################
############################################################

# full_chart = df_records.plot(x='Timestep', marker='o')
# full_chart.set_ylabel('ALL THE UNITS!')
# plt.title('AMI ALL THE DATA!')
# plt.show()

# #################### CARBON FLOW ######################
# fig, ax = plt.subplots()
# ax.plot(df_records['Timestep'], df_records['TEB'], marker='o', color='green')
# ax.set_ylabel(' grams / meter^2', color = 'green')
# ax.tick_params(axis='y', labelcolor='green')
# ax2 = ax.twinx()
# ax2.plot(df_records['Timestep'], df_records['DCG'], marker='o', color='black')
# ax2.set_ylabel(' mol carbon / ((m^2)*Day)')
# fig.legend(['TCB', 'TEB', 'DCG'])
# plt.title('AMI Carbon Flow')
# plt.show()

# ################### VAPOR PRESSURES ###################
# VP_chart_data = df_records[['Timestep', 'VP_AIR', 'VP_SAT', 'VPD']]
# VP_chart = VP_chart_data.plot(x='Timestep', marker='o')
# VP_chart.set_ylabel('kPa')
# plt.title('AMI Vapor Pressures')
# plt.show()

# ################ CODUCTANCE ###########################
# conductance_chart_data = df_records[['Timestep', 'g_S', 'g_A', 'g_C']]
# conductance_chart = conductance_chart_data.plot(x='Timestep', marker='o')
# conductance_chart.set_ylabel('moles of water / (m^2)*s')
# plt.title('AMI Conductances')
# plt.legend(['Stomatal', 'Atmo', 'Canopy'], loc='center right')
# plt.show()

# ################# PHOTOSYNTHESIS ###########################
# fig, ax = plt.subplots()
# ax.plot(df_records['Timestep'], df_records['P_GROSS'], marker='o', color='lightgreen')
# ax.plot(df_records['Timestep'], df_records['P_NET'], marker='o', color='green')
# ax.set_ylabel('umol Carbon / (m^2)*s', color = 'green')
# ax.tick_params(axis='y', labelcolor='green')
# ax2 = ax.twinx()
# ax2.plot(df_records['Timestep'], df_records['CGR'], marker='o', color='black')
# ax2.set_ylabel('grams / ((m^2)*Day)')
# ax2.set_ybound(0, 35)           # This was so P_GROSS and CGR didn't overlap
# fig.legend(['P_GROSS', 'P_NET', 'CGR'])
# plt.title('AMI Carbon Flow')
# plt.show()

# ############################################################
# ##################### NOTES FOR LATER ######################
# ############################################################
"""The dataframe starts recording after the first calculations,
  so its slightly off. Couldn't find a way to insert the intial 
  conditions at the start of the frame or how to start it before
   then add each timestep frame"""

'''this will need lots of adjustments to make it functionable in
    variable environments in real time and represent it'''

'''Interesting her version starts with 0 P_GROSS but 1.09
    P_NET. Cavazzonis doesn't I wonder how large that impact is'''

'''Ill need to fix how the model doubles up at the start. See next note'''

'''What the heck? if I intialize t=0 it duplicates a bunch of first 
    data points, but if I start at t=1 it doesn't...'''
