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
CO2 = 400           # umol CO2 / mol air,needs to accept  inputs

##################################################
############## INTIALIZING VARIABLES  ############
##################################################
t = 0               # time in days
n = 2.5             # Ewert table 4-97 crop specific


##################################################
############# SUPPLEMENTAL EQUATIONS #############
##################################################
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
t_A_1 = tac1*(1/PPFD)*(1/CO2)
t_A_2 = tac2*(1/PPFD)
t_A_3 = tac3*(CO2/PPFD)
t_A_4 = tac4*(CO2**2/PPFD)
t_A_5 = tac5*(CO2**3/PPFD)
t_A_6 = tac6*(1/CO2)
t_A_7 = tac7
t_A_8 = tac8*CO2
t_A_9 = tac9*(CO2**2)
t_A_10 = tac10*(CO2**3)
t_A_11 = tac11*(PPFD/CO2)
t_A_12 = tac12*PPFD
t_A_13 = tac13*PPFD*CO2
t_A_14 = tac14*PPFD*(CO2**2)
t_A_15 = tac15*PPFD*(CO2**3)
t_A_16 = tac16*(PPFD**2/CO2)
t_A_17 = tac17*(PPFD**2)
t_A_18 = tac18*(PPFD**2)*CO2
t_A_19 = tac19*(PPFD**2)*(CO2**2)
t_A_20 = tac20*(PPFD**2)*(CO2**3)
t_A_21 = tac21*(PPFD**3/CO2)
t_A_22 = tac22*(PPFD**3)
t_A_23 = tac23*(PPFD**3)*CO2
t_A_24 = tac24*(PPFD**3)*(CO2**2)
t_A_25 = tac25*(PPFD**3)*(CO2**3)

t_A = (t_A_1 + t_A_2 + t_A_3 + t_A_4 + t_A_5 + 
       t_A_6 + t_A_7 + t_A_8 + t_A_9 + t_A_10 + 
       t_A_11 + t_A_12 + t_A_13 + t_A_14 + t_A_15 + 
       t_A_16 + t_A_17 + t_A_18 + t_A_19 + t_A_20 + 
       t_A_21 + t_A_22 + t_A_23 + t_A_24 + t_A_25)

print("Time to Canopy Closure (t_A) =",t_A)

##################################################
################# THE MODEL LOOP #################
##################################################
while t <= 100:     
    
    t += 1
    
print(t)