# -*- coding: utf-8 -*-
#! c:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/OO-MEC/

"""
Created on Mon May 8 2023
@author: donal
End goal is global sensitivity and uncertainty analysis
"""

import os
import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# -----------------------------------------------
PPFD = 560          # umol/m^2/sec, needs to accept inputs
CO2 = 419.5         # umol CO2 / mol air,needs to accept  inputs
H = 16              # photoperiod defined as 16 in Cavazonni 2001
T_LIGHT = 23        # Light Cycle Average Temperature ewert table 4-111
T_DARK = 23         # Dark Cycle Average Temperature ewert table 4-111
RH = .675           # relative humidty as a fraction bounded between 0 and 1. The 0.675 is a number pulled from a Dr. GH VPD table as ideal for lettuce

t = 0               # time in days
res = 1             # model resolution (in days)
i = 0               # matrix/loop counter
df_records = pd.DataFrame({})      # the empty dataframe ofor entire simultation


# --------------------------------------------------
for i in range(5):
    P_NET = 5 # just a constant for testing
    VP_SAT = 0.611*np.exp(1)**((17.4*T_LIGHT)/(T_LIGHT+239)) # assumes leaf tempp=air temp. Saturated Vapor Pressure. ewert eq 4-23 numbers likely from Monje 1998
    VP_AIR = VP_SAT*RH                                       # Atmo Vapor Pressure ewewrt eq 4-23
    VPD = VP_SAT - VP_AIR                                    # Vapor Pressure Deficit ewert eq 4-23
    g_S = (1.717*T_LIGHT-19.96-10.54*VPD)*(P_NET/CO2)        # stomatal conductance the numbers came from monje 1998, only for planophile canopies equation from ewert 4-27
    df_timestep = pd.DataFrame({
    'Timestep': [t],
    'VP_SAT': [VP_SAT],
    'VP_AIR': [VP_AIR],
    'VPD': [VPD],
    'P_NET': [P_NET],
    'g_S': [g_S],
    'T_LIGHT': [T_LIGHT],
    'T_DARK': [T_DARK],
    'RH': [RH],
    'CO2': [CO2]})
    df_records = df_records.append(df_timestep, ignore_index= True)      
    i += res
    t += 1
print(df_records)
