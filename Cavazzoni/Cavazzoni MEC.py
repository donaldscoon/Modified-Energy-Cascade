# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 12:33:34 2023

@author: donal

Written to recreate the MEC authored by Jones and Cavazzoni. Created using the 
Life Support Baseline Values and Assumptions Document by Ewert 2020

End goal is global sensitivity and uncertainty analysis of this version and comparison against others. 

Maybe one day I modify the structure to accept flags like a real program

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##################################################
################## MODEL INPUTS ##################
##################################################
PPFD = 560          # umol/m^2/sec, needs to accept inputs
CO2 = 419.5         # umol CO2 / mol air,needs to accept  inputs
H = 16              # photoperiod defined as 16 in Cavazonni 2001
T_LIGHT = 23        # Light Cycle Average Temperature ewert table 4-111 or user input
T_DARK = 23         # Dark Cycle Average Temperature ewert table 4-111 or user input
RH = .675           # relative humidty as a fraction bounded between 0 and 1. The 0.675 is a number pulled from a Dr. GH VPD table as ideal for lettuce
P_ATM = 101         # atmospheric pressure placeholder is gainesville FL value

##################################################
################# INTIALIZATION  #################
##################################################
t = 0               # time in days
res = 1             # model resolution (in days)
i = 0               # matrix/loop counter

##################################################
#################### CONSTANTS ###################
##################################################
BCF = 0.40          # Biomass carbon fraction ewert table 4-113
XFRT = 0.95         # edible biomass fraction ewert table 4-112
OPF = 1.08          # Oxygen production fraction ewert table 4-113
g_A = 2.5           # atmospheric aerodynamic conductance ewert eq 4-27 no citations
A_max = 0.93        # maximum fraction of PPF Absorbtion ewert pg 180
t_M = 30            # time at harvest/maturity ewert table 4-112
t_Q = 50            # onset of senescence placeholder value ewert table 4-112
t_E = 1             # time at onset of organ formation ewert table 4-112
MW_W = 18.015       # Molecular weight of water, ewert table 4-110
CQY_min = 0         # N/A minimum canopy quantum yield ewert table 4-99
CUE_max = 0.625     # maximum carbon use efficiency ewert table 4-99
CUE_min = 0         # N/A minimum carbon use efficiency ewert table 4-99
D_PG = 24           # the plants diurnal cycle length assumed 24 in cavazzoni 2001
p_W = 998.23        # density of water at 20 C, ewert table 4-110
n = 2.5             # Ewert table 4-97 crop specific


##################################################
################ Data Management #################
##################################################
df_records = pd.DataFrame({})

"""These matrices may need to become obsolete with
   the new dataframes I'm about to introduce. :) """
ts_to_harvest = int(t_M/res)             # calcs the timesteps needed to set up the matrix for each ts
matrix = range(ts_to_harvest) + np.ones(ts_to_harvest)      # only works with whole numbers of ts_to_harvest
TCB = 0                                 # starting crop biomass
Biomass_mat = np.zeros(ts_to_harvest)             # matrix for TCB storage
TEB = 0                                 # starting total edible biomass
edible_mat = np.zeros(ts_to_harvest)              # matrix for TEB storage



##################################################
############# SUPPLEMENTAL EQUATIONS #############
##################################################
""" Multipolynomial Regression Fits Ewert Table 4-100 """
# used in the calculation of A_max and CQY_max

c1 = (1/PPFD)*(1/CO2)
c2 = (1/PPFD)
c3 = (CO2/PPFD)
c4 = (CO2**2/PPFD)
c5 = (CO2**3/PPFD)
c6 = (1/CO2)
c7 = 1
c8 = CO2
c9 = (CO2**2)
c10 = (CO2**3)
c11 = PPFD*(1/CO2)
c12 = PPFD
c13 = PPFD*CO2
c14 = PPFD*(CO2**2)
c15 = PPFD*(CO2**3)
c16 = (PPFD**2)*(1/CO2)
c17 = (PPFD**2)
c18 = (PPFD**2)*CO2
c19 = (PPFD**2)*(CO2**2)
c20 = (PPFD**2)*(CO2**3)
c21 = (PPFD**3)*(1/CO2)
c22 = (PPFD**3)
c23 = (PPFD**3)*CO2
c24 = (PPFD**3)*(CO2**2)
c25 = (PPFD**3)*(CO2**3)


""" Canopy Closure t_A """
# t_A coefficients (tac) values originate from EWert table 4-115 
tac1 = 0
tac2 = 1.0289*(10**4)
tac3 = -3.7018
tac4  = 0 
tac5 = 3.6648*(10**-7)
tac6 = 0
tac7 = 1.7571
tac8 = 0
tac9 = 2.3127*(10**-6)
tac10 = 0
tac11 = 1.8760
tac12 = 0
tac13 = 0
tac14 = 0
tac15 = 0
tac16 = 0
tac17 = 0
tac18 = 0
tac19 = 0
tac20 = 0
tac21 = 0
tac22 = 0
tac23 = 0
tac24 = 0
tac25 = 0

# each term in the t_A Ewert eq 4-30
t_A_1 = tac1*c1
t_A_2 = tac2*c2
t_A_3 = tac3*c3
t_A_4 = tac4*c4
t_A_5 = tac5*c5
t_A_6 = tac6*c6
t_A_7 = tac7*c7
t_A_8 = tac8*c8
t_A_9 = tac9*c9
t_A_10 = tac10*c10
t_A_11 = tac11*c11
t_A_12 = tac12*c12
t_A_13 = tac13*c13
t_A_14 = tac14*c14
t_A_15 = tac15*c15
t_A_16 = tac16*c16
t_A_17 = tac17*c17
t_A_18 = tac18*c18
t_A_19 = tac19*c19
t_A_20 = tac20*c20
t_A_21 = tac21*c21
t_A_22 = tac22*c22
t_A_23 = tac23*c23
t_A_24 = tac24*c24
t_A_25 = tac25*c25

# the calculation of canopy closure ewert eq 4-30
t_A = (t_A_1 + t_A_2 + t_A_3 + t_A_4 + t_A_5 + 
       t_A_6 + t_A_7 + t_A_8 + t_A_9 + t_A_10 + 
       t_A_11 + t_A_12 + t_A_13 + t_A_14 + t_A_15 + 
       t_A_16 + t_A_17 + t_A_18 + t_A_19 + t_A_20 + 
       t_A_21 + t_A_22 + t_A_23 + t_A_24 + t_A_25)

""" Canopy Quantum Yield Equation """
# CQY_max Coefficients ewert table 4-102
CQY_m_c_1 = 0
CQY_m_c_2 = 0
CQY_m_c_3 = 0
CQY_m_c_4 = 0
CQY_m_c_5 = 0
CQY_m_c_6 = 0
CQY_m_c_7 = 4.4763*(10**-2)
CQY_m_c_8 = 5.163*(10**-5)
CQY_m_c_9 = -2.075*(10**-8)
CQY_m_c_10 = 0
CQY_m_c_11 = 0
CQY_m_c_12 = -1.1701*(10**-5)
CQY_m_c_13 = 0
CQY_m_c_14 = 0
CQY_m_c_15 = 0
CQY_m_c_16 = 0
CQY_m_c_17 = 0
CQY_m_c_18 = -1.9731*(10**-11)
CQY_m_c_19 = 8.9265*(10**-15)
CQY_m_c_20 = 0
CQY_m_c_21 = 0
CQY_m_c_22 = 0
CQY_m_c_23 = 0
CQY_m_c_24 = 0
CQY_m_c_25 = 0

# CQY_max Terms ewert eq 4-22
CQY_m_t_1 = CQY_m_c_1*c1
CQY_m_t_2 = CQY_m_c_2*c2
CQY_m_t_3 = CQY_m_c_3*c3
CQY_m_t_4 = CQY_m_c_4*c4
CQY_m_t_5 = CQY_m_c_5*c5
CQY_m_t_6 = CQY_m_c_6*c6
CQY_m_t_7 = CQY_m_c_7*c7
CQY_m_t_8 = CQY_m_c_8*c8
CQY_m_t_9 = CQY_m_c_9*c9
CQY_m_t_10 = CQY_m_c_10*c10
CQY_m_t_11 = CQY_m_c_11*c11
CQY_m_t_12 = CQY_m_c_12*c12
CQY_m_t_13 = CQY_m_c_13*c13
CQY_m_t_14 = CQY_m_c_14*c14
CQY_m_t_15 = CQY_m_c_15*c15
CQY_m_t_16 = CQY_m_c_16*c16
CQY_m_t_17 = CQY_m_c_17*c17
CQY_m_t_18 = CQY_m_c_18*c18
CQY_m_t_19 = CQY_m_c_19*c19
CQY_m_t_20 = CQY_m_c_20*c20
CQY_m_t_21 = CQY_m_c_21*c21
CQY_m_t_22 = CQY_m_c_22*c22
CQY_m_t_23 = CQY_m_c_23*c23
CQY_m_t_24 = CQY_m_c_24*c24
CQY_m_t_25 = CQY_m_c_25*c25

# CQY_max Calculation ewert eq 4-22
CQY_max = (CQY_m_t_1 + CQY_m_t_2 + CQY_m_t_3 + CQY_m_t_4 + CQY_m_t_5 +
           CQY_m_t_6 + CQY_m_t_7 + CQY_m_t_8 + CQY_m_t_9 + CQY_m_t_10 + 
           CQY_m_t_11 + CQY_m_t_12 + CQY_m_t_13 + CQY_m_t_14 + CQY_m_t_15 + 
           CQY_m_t_16 + CQY_m_t_17 + CQY_m_t_18 + CQY_m_t_19 + CQY_m_t_20 + 
           CQY_m_t_21 + CQY_m_t_22 + CQY_m_t_23 + CQY_m_t_24 + CQY_m_t_25)

##################################################
################# THE MODEL LOOP #################
##################################################
while t < ts_to_harvest:                 # while time is less than harvest time
    if t < t_A:                  # before canopy closure
        A = A_max*(t/t_A)**n         # Ewert eq 4-14
    else:                        # after canopy closure
        A = A_max                    # Ewert eq 4-14
    if t<= t_Q:                  # before onset of senescence
        CQY = CQY_max                # ewert eq 4-15
        CUE_24 = CUE_max             # ewert eq 4-16
    else: 
        """For lettuce the values of CQY_min and CUE_min 
        are n/a due to the assumption that the canopy does
        not senesce before harvest. I coded them anyways, it
        makes it complete for all the other crops too. For 
        crops other than lettuce remove the break statement."""
        CQY = CQY_max - (CQY_max - CQY_min)*((t-t_Q)/(t_M-t_Q)) # ewert eq 4-15
        CUE_24 = CUE_max - (CUE_max - CUE_min)*((t-t_Q)/(t_M-t_Q)) #ewert eq 4-16
        print("Error: Utilizing CQY and CUE values without definitions")
        break
    DCG = 0.0036*H*CUE_24*A*CQY*PPFD # ewert eq 4-17 number is related to seconds in an hour
    DOP = OPF*DCG                    # ewert eq 4-18
    CGR = 12.01*(DCG/BCF)            # ewert eq 4-19 number is molecular weight of carbon
    TCB += CGR                       # ewert eq 4-20
    if t > t_E:                      # accumilate edible biomass when organ formation begins
        TEB += XFRT*CGR              # ewert eq 4-21
    Biomass_mat[i] = TCB             # matrix that stores past values of TCB
    '''^^^^this will probably be fixed by making t divisable by dt^^^^'''
    '''now it works more, but only if the it results in a whole number'''
    edible_mat[i] = TEB
    VP_SAT = 0.611*np.exp(1)**((17.4*T_LIGHT)/(T_LIGHT+239)) # assumes leaf tempp=air temp. Saturated Vapor Pressure. ewert eq 4-23 numbers likely from Monje 1998
    VP_AIR = VP_SAT*RH               # Atmo Vapor Pressure ewewrt eq 4-23
    VPD = VP_SAT - VP_AIR            # Vapor Pressure Deficit ewert eq 4-23
    P_GROSS = A*CQY*PPFD             # Gross photosynthesis ewert eq 4-24
    P_NET = (((D_PG-H)/D_PG)+((H*CUE_24)/D_PG))*P_GROSS     # Net Photosynthesis ewert eq 4-25
    g_S = (1.717*T_LIGHT-19.96-10.54*VPD)*(P_NET/CO2)        # stomatal conductance the numbers came from monje 1998, only for planophile canopies equation from ewert 4-27
    g_C = (g_A*g_S)/(g_A+g_S)                               # canopy conductance ewert 4-26
    DTR = 3600*H*(MW_W/p_W)*g_C*(VPD/P_ATM)
    dfts = pd.DataFrame({
        'Timestep': [t],
        'A': [A],
        'CQY': [CQY],
        'CUE_24': [CUE_24],
        'DCG': [DCG],
        'CGR': [CGR],
        'TCB': [TCB],
        'TEB': [TEB],
        'VP_SAT': [VP_SAT],
        'VP_AIR': [VP_AIR],
        'VPD': [VPD],
        'P_GROSS': [P_GROSS],
        'P_NET': [P_NET],
        'g_S': [g_S],
        'g_A': [g_A],
        'g_C': [g_C],
        'DTR': [DTR],
        'T_LIGHT': [T_LIGHT],
        'T_DARK': [T_DARK],
        'RH': [RH],
        'CO2': [CO2]
    }) # creates a dataframe of all variables/outputs for each timestep. 
    df_records = pd.concat([df_records, dfts], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
    t += res                          # advance timestep
    i += 1                           # increase matrix index counter

# print(df_records)                    # prints a copy of output in the terminal
# df_records.to_csv('C:/Users/donal/Documents/Github/Modified-Energy-Cascade/Cavazzoni/MEC_CAV_OUT.csv') # exports final data frame to a CSV


############################################################
##################### VISUALIZATIONS #######################
############################################################

# full_chart = df_records.plot(x='Timestep', marker='o')
# full_chart.set_ylabel('ALL THE UNITS!')
# plt.title('ALL THE DATA!')
# plt.show()

################ Canopy Development ########################
# fig, ax = plt.subplots()
# ax.plot(df_records['Timestep'], df_records['CQY'], label='CQY', marker= 'o', color = 'blue')
# ax.plot(df_records['Timestep'], df_records['CUE_24'], label='CUE_24', marker= 'o', color = 'green')
# ax.set_ylabel('Fractional')
# ax2=ax.twinx()
# ax2.plot(df_records['Timestep'], df_records['A'], label='A', marker='o', color = 'red')
# ax2.set_ylabel('umol C / umol photons', color='red')
# ax2.tick_params(axis='y',labelcolor='red')
# fig.legend(['CQY', 'CUE_24', 'A'])
# plt.title('Canopy Development')
# plt.show()

###################### CARBON FLOW ######################
# fig, ax = plt.subplots()
# ax.plot(df_records['Timestep'], df_records['TCB'], marker='o', color='lightgreen')
# ax.plot(df_records['Timestep'], df_records['TEB'], marker='o', color='green')
# ax.set_ylabel(' grams / meter^2', color = 'green')
# ax.tick_params(axis='y', labelcolor='green')
# ax2 = ax.twinx()
# ax2.plot(df_records['Timestep'], df_records['DCG'], marker='o', color='black')
# ax2.set_ylabel(' mol carbon / ((m^2)*Day)')
# fig.legend(['TCB', 'TEB', 'DCG'])
# plt.title('Carbon Flow')
# plt.show()


##################### VAPOR PRESSURES ###################
# VP_chart_data = df_records[['Timestep', 'VP_AIR', 'VP_SAT', 'VPD']]
# VP_chart = VP_chart_data.plot(x='Timestep', marker='o')
# VP_chart.set_ylabel('kPa')
# plt.title('Vapor Pressures')
# plt.show()

################### CODUCTANCE ###########################
# conductance_chart_data = df_records[['Timestep', 'g_S', 'g_A', 'g_C']]
# conductance_chart = conductance_chart_data.plot(x='Timestep', marker='o')
# conductance_chart.set_ylabel('moles of water / (m^2)*s')
# plt.title('Conductances')
# plt.legend(['Stomatal', 'Atmo', 'Canopy'], loc='center right')
# plt.show()

################### PHOTOSYNTHESIS ###########################
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
# plt.title('Carbon Flow')
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

