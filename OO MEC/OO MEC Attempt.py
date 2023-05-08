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
def get_env_data():
   """This is specifically for GSUA data"""
   # Convert text file to a dataframe
   data = pd.read_csv('c:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/OO MEC/ENV-data.txt', sep= ' ')
   env_df = pd.DataFrame(data)
   
   # Assign column names to the DataFrame
   column_names = ['Temperature', 'Humidity', 'CO2']
   env_df.columns = column_names
   
   # print(env_df)

   # hmm, would it be worth writing this to pull single columns at a time? Probably.
   # I know there is no class statement for this one, but I am not sure how to write
   # optional arguments yet. I'll move on and hopefully that isn't too difficult to 
   # add later. :)

# --------------------------------------------------
def main():
   get_env_data()
   for
   print('Give me something')
   
# --------------------------------------------------
main()