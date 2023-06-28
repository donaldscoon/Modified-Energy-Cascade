# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 12:33:34 2023

@author: donal

Written to recreate the MEC authored by Jones and Cavazzoni. Created using the 
Life Support Baseline Values and Assumptions Document by Ewert 2020

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##################################################
################## MODEL INPUTS ##################
##################################################
PPFD = 314          # umol/m^2/sec, Amitrano 2020 Table 2
CO2 = 423.28        # umol CO2 / mol air, April 2023 Mauna Loa Measurement 
H = 16              # hours / day photoperiod, Cavazonni 2001
T_LIGHT = 23        # degrees C, light cycle average temperature, Ewert table 4-111
T_DARK = 23         # degrees C, dark cycle average temperature, Ewert table 4-111
RH = .675           # relative humidty as a fraction bounded between 0 and 1.
P_ATM = 101         # kPa, atmospheric pressure placeholder is gainesville FL value

##################################################
#################### CONSTANTS ###################
##################################################
BCF = 0.40          # fractional, biomass carbon fraction, Ewert table 4-113
XFRT = 0.95         # fractional, edible biomass fraction, Ewert table 4-112
OPF = 1.08          # fractional, Oxygen production fraction, Ewert table 4-113
g_A = 2.5           # mol_water/(m^2*s), atmospheric aerodynamic conductance, Ewert eq 4-27
A_max = 0.93        # fractional, maximum PPF Absorbtion, Ewert pg 180
t_M = 30            # days, timing of harvest/maturity, Ewert table 4-112
t_Q = 50            # days, timing of senescence onset, placeholder value for N/A, Ewert 4-112
t_E = 1             # days, timing of organ formation onset, Ewert table 4-112
MW_W = 18.015       # grams/mol, molecular weight of water, Ewert table 4-110
CQY_min = 0         # umol_Carbon/umol_Photon, minimum canopy quantum yield, placeholder value for N/A, Ewert table 4-99
CUE_max = 0.625     # fractional, maximum carbon use efficiency, Ewert table 4-99
CUE_min = 0         # fractional, minimum carbon use efficiency, placeholder value for N/A, Ewert table 4-99
D_PG = 24           # the plants diurnal cycle length, assumed 24 in cavazzoni 2001
p_W = 998.23        # grams/L density of water at 20 C, Ewert table 4-110
n = 2.5             # crop specific exponent, Ewert table 4-97 

##################################################
################# INTIALIZATION  #################
##################################################
t = 0                                   # time in days
res = 1                                 # model resolution (in days)
df_records = pd.DataFrame({})           # Empty DataFrame for historical records
ts_to_harvest = int(t_M/res)            # calcs the timesteps needed to set up the matrix for each ts
TCB = 0                                 # starting crop biomass
TEB = 0                                 # starting total edible biomass

##################################################
############# SUPPLEMENTAL EQUATIONS #############
##################################################

gen_coef = [
    (1/PPFD)*(1/CO2) , (1/PPFD) , (CO2/PPFD)   , (CO2**2/PPFD)     , (CO2**3/PPFD)     ,
    (1/CO2)          , 1        , CO2          , (CO2**2)          , (CO2**3)          ,
    PPFD*(1/CO2)     , PPFD     , PPFD*CO2     , PPFD*(CO2**2)     , PPFD*(CO2**3)     ,
    (PPFD**2)*(1/CO2), (PPFD**2), (PPFD**2)*CO2, (PPFD**2)*(CO2**2), (PPFD**2)*(CO2**3),
    (PPFD**3)*(1/CO2), (PPFD**3), (PPFD**3)*CO2, (PPFD**3)*(CO2**2), (PPFD**3)*(CO2**3),
] # Multipolynomial Regression Fits, Ewert Table 4-100

t_A_coef = [
    0     , 1.0289*(10**4), -3.7018, 0              , 3.6648*(10**-7),
    0     , 1.7571        , 0      , 2.3127*(10**-6), 0              ,
    1.8760, 0             , 0      , 0              , 0              ,
    0     , 0             , 0      , 0              , 0              ,
    0     , 0             , 0      , 0              , 0
] # Canopy Closure Time (t_A) coefficients, Ewert table 4-115 

""" """
CQY_max_coef = [
0, 0               , 0                , 0               , 0,
0, 4.4763*(10**-2) , 5.163*(10**-5)   , -2.075*(10**-8) , 0,
0, -1.1701*(10**-5), 0                , 0               , 0,
0, 0               , -1.9731*(10**-11), 8.9265*(10**-15), 0,
0, 0               , 0                , 0               , 0
] # Canopy Quantum Yield (CQY) Coefficients, Ewert table 4-102

""" Calculate each term of the polynomials. """
t_A_terms = [tac * gen_coef for tac, gen_coef in zip(t_A_coef, gen_coef)]
CQY_max_terms = [cqy * gen_coef for cqy, gen_coef in zip(CQY_max_coef, gen_coef)]

""" Calculate t_A and CQY_max by summing the terms. """
t_A = sum(t_A_terms)        # Canopy Closure Time, Ewert Eq 4-30
CQY_max = sum(CQY_max_terms)    # Maximum Canopy Quantum Yield, Ewert 4-22

##################################################
################# THE MODEL LOOP #################
##################################################
"""While time is less than timesteps to harvest. """
while t < ts_to_harvest:
    """ Before the canopy closes. """
    if t < t_A:
        A = A_max*(t/t_A)**n         # fraction of PPF absorbed by the plant canopy, Ewert eq 4-14
    """ After the canopy closes. """
    else:
        A = A_max                    # fraction of PPF absorbed by the plant canopy, Ewert eq 4-14
    """ Before the onset of senescense. """
    if t<= t_Q:
        CQY = CQY_max                # Canopy Quantum Yield, Ewert eq 4-15
        CUE_24 = CUE_max             # 24 hour Carbon Use Efficiency, Ewert eq 4-16
    """ When the crop is senescening """    
    else: 
        """For lettuce the values of CQY_min and CUE_min 
        are n/a due to the assumption that the canopy does
        not senesce before harvest. I coded them anyways, it
        makes it complete for all the other crops the MEC is 
        capable of utilizing. For crops other than lettuce 
        remove the break statement."""
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
    VP_SAT = 0.611*np.exp(1)**((17.4*T_LIGHT)/(T_LIGHT+239)) # assumes leaf tempp=air temp. Saturated Vapor Pressure. ewert eq 4-23 numbers likely from Monje 1998
    VP_AIR = VP_SAT*RH               # Atmo Vapor Pressure ewewrt eq 4-23
    VPD = VP_SAT - VP_AIR            # Vapor Pressure Deficit ewert eq 4-23
    P_GROSS = A*CQY*PPFD             # Gross photosynthesis ewert eq 4-24
    P_NET = (((D_PG-H)/D_PG)+((H*CUE_24)/D_PG))*P_GROSS     # Net Photosynthesis ewert eq 4-25
    g_S = (1.717*T_LIGHT-19.96-10.54*VPD)*(P_NET/CO2)        # stomatal conductance the numbers came from monje 1998, only for planophile canopies equation from ewert 4-27
    g_C = (g_A*g_S)/(g_A+g_S)                               # canopy conductance ewert 4-26
    DTR = 3600*H*(MW_W/p_W)*g_C*(VPD/P_ATM)                 # Daily transpiration rate Ewert eq 4-29
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
    t += res                         # advance timestep

# print(df_records)                    # prints a copy of output in the terminal
# df_records.to_csv('C:/Users/donal/Documents/Github/Modified-Energy-Cascade/Cavazzoni/MEC_CAV_OUT.csv') # exports final data frame to a CSV

##################################################
##################### VISUALIZATIONS #############
##################################################

# full_chart = df_records.plot(x='Timestep', marker='o')
# full_chart.set_ylabel('ALL THE UNITS!')
# plt.title('ALL THE DATA!')
# plt.show()

############### Canopy Development ########################
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

