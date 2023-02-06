# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 12:33:34 2023

@author: donal

Written to recreate the MEC authored by Jones and Cavazzoni. Created using the 
Life Support Baseline Values and Assumptions Document by Ewert 2020

End goal is global sensitivity and uncertainty analysis of this version and comparison against others. 

"""

##################################################
################## MODEL INPUTS ##################
##################################################
PPFD = 800          # umol/m^2/sec, needs to accept inputs
CO2 = 450           # umol CO2 / mol air,needs to accept  inputs

##################################################
############## INTIALIZING VARIABLES  ############
##################################################
t = 0               # time in days
n = 2.5             # Ewert table 4-97 crop specific


##################################################
############# SUPPLEMENTAL EQUATIONS #############
##################################################
""" Canopy Closure t_A """
# tac values originate from EWert table 4-115 
tac1 = 0
tac2 = 1.0289*10**4
tac3 = -3.7018
tac4 = 0























print(tac2)
t_A_1 = 2
t_A_2 = 4

t_A = t_A_1 + t_A_2

##################################################
################# THE MODEL LOOP #################
##################################################
while t <= 100:     
    
    t += 1
    
print(t)