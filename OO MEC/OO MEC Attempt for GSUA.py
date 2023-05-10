# -*- coding: utf-8 -*-
#! c:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/OO-MEC/

"""
Created on Mon May 8 2023
@author: donal
Written to recreate the MEC authored by Boscheri using Object Oriented Programming. 
End goal is global sensitivity and uncertainty analysis of this version and comparison against others. 
"""

import os
import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# --------------------------------------------------
class env:
   def __init__(self, baseline):
      self.baseline = baseline
      self.GSUA_data = GSUA_data

   def baseline():
      PPFD = 560          # umol/m^2/sec, needs to accept inputs
      CO2 = 419.5         # umol CO2 / mol air,needs to accept  inputs
      H = 16              # photoperiod defined as 16 in Cavazonni 2001
      T_LIGHT = 23        # Light Cycle Average Temperature ewert table 4-111
      T_DARK = 23         # Dark Cycle Average Temperature ewert table 4-111
      RH = .675           # relative humidty as a fraction bounded between 0 and 1. The 0.675 is a number pulled from a Dr. GH VPD table as ideal for lettuce
      P_ATM = 101         # atmospheric pressure placeholder is gainesville FL value
      return PPFD, CO2, H, T_LIGHT, T_DARK, RH, P_ATM

   def GSUA_data():
      """This is specifically for GSUA data"""
      # Convert text file to a dataframe
      data = pd.read_csv('c:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/OO MEC/ENV-data.txt', sep= ' ')
      env_df = pd.DataFrame(data)
      
      # Assign column names to the DataFrame
      column_names = ['Temp', 'RH', 'CO2']
      env_df.columns = column_names
      return env_df
      
   # hmm, would it be worth writing this to pull single columns at a time? Probably.
   # I know there is no class statement for this one, but I am not sure how to write
   # optional arguments yet. I'll move on and hopefully that isn't too difficult to 
   # add later. :)

# --------------------------------------------------
class data:
   def __init__(self, init_df, update_df, GSUA_out):
      self.init_df = init_df
      self.update_df = update_df
      self.GSUA_out = GSUA_out

   def init_df():
      t = 0               # time in days
      res = 1             # model resolution (in days)
      i = 0               # matrix/loop counter
      df_records = pd.DataFrame({})       # the empty dataframe ofor entire simultation
      return df_records, t, res, i

# --------------------------------------------------
def main():
   #there needs to be a way to specify baseline or input data or sensor data when running the program
   PPFD, CO2, H, T_LIGHT, T_DARK, RH, P_ATM = env.baseline()      # sets the environmental baselines for the entire simultaion
   env_df = env.GSUA_data()                                         # pulls in the GSUA sample data frame
   df_records, t, res, i = data.init_df()
   print(df_records)
   # P_NET = 5 # just a constant for testing
   # VP_SAT = 0.611*np.exp(1)**((17.4*T_LIGHT)/(T_LIGHT+239)) # assumes leaf tempp=air temp. Saturated Vapor Pressure. ewert eq 4-23 numbers likely from Monje 1998
   # VP_AIR = VP_SAT*RH                                       # Atmo Vapor Pressure ewewrt eq 4-23
   # VPD = VP_SAT - VP_AIR                                    # Vapor Pressure Deficit ewert eq 4-23
   # g_S = (1.717*T_LIGHT-19.96-10.54*VPD)*(P_NET/CO2)        # stomatal conductance the numbers came from monje 1998, only for planophile canopies equation from ewert 4-27
   # print(g_S)
   print(df_records)

   print(df_rec)
# --------------------------------------------------
main()