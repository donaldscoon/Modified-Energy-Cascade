
# # -*- coding: utf-8 -*-
# #! c:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/OO-MEC/

# """
# Created on Mon May 8 2023
# @author: donal
# End goal is global sensitivity and uncertainty analysis
# """

# import os
# import re
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd


# # -----------------------------------------------
# PPFD = 560          # umol/m^2/sec, needs to accept inputs
# CO2 = 419.5         # umol CO2 / mol air,needs to accept  inputs
# H = 16              # photoperiod defined as 16 in Cavazonni 2001
# T_LIGHT = 23        # Light Cycle Average Temperature ewert table 4-111
# T_DARK = 23         # Dark Cycle Average Temperature ewert table 4-111
# RH = .675           # relative humidty as a fraction bounded between 0 and 1. The 0.675 is a number pulled from a Dr. GH VPD table as ideal for lettuce

# t = 0               # time in days
# res = 1             # model resolution (in days)
# i = 0               # matrix/loop counter
# df_records = pd.DataFrame({})      # the empty dataframe ofor entire simultation


# # --------------------------------------------------
# for i in range(5):
#     P_NET = 5 # just a constant for testing
#     VP_SAT = 0.611*np.exp(1)**((17.4*T_LIGHT)/(T_LIGHT+239)) # assumes leaf tempp=air temp. Saturated Vapor Pressure. ewert eq 4-23 numbers likely from Monje 1998
#     VP_AIR = VP_SAT*RH                                       # Atmo Vapor Pressure ewewrt eq 4-23
#     VPD = VP_SAT - VP_AIR                                    # Vapor Pressure Deficit ewert eq 4-23
#     g_S = (1.717*T_LIGHT-19.96-10.54*VPD)*(P_NET/CO2)        # stomatal conductance the numbers came from monje 1998, only for planophile canopies equation from ewert 4-27
#     df_timestep = pd.DataFrame({
#     'Timestep': [t],
#     'VP_SAT': [VP_SAT],
#     'VP_AIR': [VP_AIR],
#     'VPD': [VPD],
#     'P_NET': [P_NET],
#     'g_S': [g_S],
#     'T_LIGHT': [T_LIGHT],
#     'T_DARK': [T_DARK],
#     'RH': [RH],
#     'CO2': [CO2]})
#     df_records = df_records.append(df_timestep, ignore_index= True)      
#     i += res
#     t += 1
# print(df_records)

"""--------------------------------------------------
--- Above is the code I provided to Chat GPT with the 
--- Prompt to convert it to an OOP design. Below is the
--- output it provided.
--------------------------------------------------"""

import pandas as pd
import numpy as np

class MECSimulation:
    def __init__(self, PPFD, CO2, H, T_LIGHT, T_DARK, RH):
        self.PPFD = PPFD
        self.CO2 = CO2
        self.H = H
        self.T_LIGHT = T_LIGHT
        self.T_DARK = T_DARK
        self.RH = RH
        self.t = 0
        self.res = 1
        self.df_records = pd.DataFrame({})
    
    def calculate_values(self):
        for i in range(5):
            P_NET = 5  # just a constant for testing
            VP_SAT = 0.611 * np.exp(1) ** ((17.4 * self.T_LIGHT) / (self.T_LIGHT + 239))
            VP_AIR = VP_SAT * self.RH
            VPD = VP_SAT - VP_AIR
            g_S = (1.717 * self.T_LIGHT - 19.96 - 10.54 * VPD) * (P_NET / self.CO2)
            
            df_timestep = pd.DataFrame({
                'Timestep': [self.t],
                'VP_SAT': [VP_SAT],
                'VP_AIR': [VP_AIR],
                'VPD': [VPD],
                'P_NET': [P_NET],
                'g_S': [g_S],
                'T_LIGHT': [self.T_LIGHT],
                'T_DARK': [self.T_DARK],
                'RH': [self.RH],
                'CO2': [self.CO2]
            })
            
            self.df_records = self.df_records.append(df_timestep, ignore_index=True)
            i += self.res
            self.t += 1
    
    def run_simulation(self):
        self.calculate_values()
        print(self.df_records)

# Create an instance of MECSimulation and run the simulation
simulation = MECSimulation(PPFD=560, CO2=419.5, H=16, T_LIGHT=23, T_DARK=23, RH=0.675)
simulation.run_simulation()