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
H = 12              # Amitrano 2020 table 2
PPFD = 314.54          # found at Amitrano 2020 table 2 but used decimal value in GN excel


##################################################
################# INTIALIZATION  #################
##################################################

t = 0               # time in days
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
MWC = 12            # molecular weight of carbon amitrano 2020

amin_GN = 0.00691867456539118     # amitrano 2020 calibrated with growth chamber experiment
amin_RN = 0.007     # amitrano 2020 calibrated with growth chamber experiment
amin_GON = 0.003    # amitrano 2020 calibrated with growth chamber experiment
amin_RON = 0.003    # amitrano 2020 calibrated with growth chamber experiment

amax_GN = 0.017148682744336     # amitrano 2020 calibrated with growth chamber experiment
amax_RN = 0.021     # amitrano 2020 calibrated with growth chamber experiment    
amax_GON = 0.010    # amitrano 2020 calibrated with growth chamber experiment
amax_RON = 0.011    # amitrano 2020 calibrated with growth chamber experiment

bmin_GN = 0          # amitrano 2020 calibrated with growth chamber experiment
bmin_RN = 0.022      # amitrano 2020 calibrated with growth chamber experiment
bmin_GON = 0.049    # amitrano 2020 calibrated with growth chamber experiment
bmin_RON = 0.036    # amitrano 2020 calibrated with growth chamber experiment

bmax_GN = 0.0451765692503675     # amitrano 2020 calibrated with growth chamber experiment
bmax_RN = 0.028     # amitrano 2020 calibrated with growth chamber experiment
bmax_GON = 0.056    # amitrano 2020 calibrated with growth chamber experiment
bmax_RON = 0.060    # amitrano 2020 calibrated with growth chamber experiment

##################################################
################ Data Management #################
##################################################
df_records = pd.DataFrame({})

ts_to_harvest = int(t_M/res)             # calcs the timesteps needed to set up the matrix for each ts
TEB = 8.53                               # this is the only way I could make it match excel WHERE IT FROM??
edible_mat = np.zeros(ts_to_harvest+1)              # matrix for TEB storage

##################################################
############# SUPPLEMENTAL EQUATIONS #############
##################################################

##################################################
################# THE MODEL LOOP #################
##################################################
while t <= ts_to_harvest:                  # while time is less than harvest time
    if t<= t_D:
        alpha = amin_GN                    # amitrano 2020 eq 15
        beta = bmin_GN                     # amitrano 2020 eq 15
    elif t <= t_Mi:
        alpha = amin_GN+(amax_GN-amin_GN)*(t-t_D)/(t_Mi-t_D)        # amitrano 2020 eq 15
        beta = bmin_GN+(bmax_GN-bmin_GN)*(t-t_D)/(t_Mi-t_D)         # amitrano 2020 eq 15
    else:
        alpha = amax_GN                    # amitrano 2020 eq 15
        beta = bmax_GN                     # amitrano 2020 eq 15
    DCG = 0.0036*H*alpha*PPFD              # amitrano 2020 eq 4
    DOP = OPF*DCG                          # amitrano 2020 eq 5
    CGR = MWC*DCG/BCF                      # amitrano 2020 eq 6
    if t > t_E:                            # if edible organ formation has begun
        TEB = CGR+TEB                      # Amitrano 2020 GN excel column I
    edible_mat[i] = TEB                    # matrix that stores past values of TEB

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

    }) # creates a dataframe of all variables/outputs for each timestep. 
    df_records = pd.concat([df_records, dfts], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
    t += res                         # advance timestep
    i += 1                           # increase matrix index counter

print(df_records)                    # prints a copy of output in the terminal
# df_records.to_csv('C:/Users/donal/Documents/Github/Modified-Energy-Cascade/Cavazzoni/MEC_CAV_OUT.csv') # exports final data frame to a CSV


############################################################
##################### VISUALIZATIONS #######################
############################################################

# full_chart = df_records.plot(x='Timestep', marker='o')
# full_chart.set_ylabel('ALL THE UNITS!')
# plt.title('ALL THE DATA!')
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
"""Ill worry about the visualizations later."""

