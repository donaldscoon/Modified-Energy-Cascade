# -*- coding: utf-8 -*-
"""
Created on Mon May 1 2023

@author: donal

Written to recreate the MEC authored by Boscheri using Object Oriented Programming. 

End goal is global sensitivity and uncertainty analysis of this version and comparison against others. 

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

t = 10
res = 1

class Timestep:
    def __init__(self, TS, t, res):
        self.TS = TS                # timestep trackers
        self.t = t                  # number of days to run the model
        self.res = res              # the division of 1 day to run the model
        self.pretty_print_name()
  
    def pretty_print_name(self):
        print("This Timestep is {}.".format(self.TS))

my_objects = {}
for i in range(1,11):
    TS = 'TS_{}'.format(i)
    my_objects[TS] = my_objects.get(TS, Timestep(TS = TS))






# class Environment:
#     def __init__(TS, T_LIGHT, T_DARK) -> None:
#         TS.T_LIGHT = T_LIGHT        # Light Cycle Average Temperature ewert table 4-111 or user input
#         TS.T_DARK  = T_DARK         # Dark Cycle Average Temperature ewert table 4-111 or user input

#     def Show_Temp(self, T_LIGHT, T_DARK) -> None:
#         print(f"When lights are on it is {self.T_Light}, when lights are off it is {self.T_Dark}")
#         pass
# TS = 0
# T_LIGHT = 30
# T_DARK = 25
#     # add environment methods here
# TS1 = Environment(T_LIGHT, T_DARK)
# print(Environment.