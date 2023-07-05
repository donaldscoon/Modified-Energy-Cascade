'''
This version of the Amitrano Model is meant to run GSUA 
and has been altered for...
    *being called from another program
    *keeping track of the simulation number
    *exporting data for GSUA as .txt files
    *creating every possible version of charts needed
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

#########################################################
############### Some Data Structuring ###################
#########################################################
u = "\u00B5"        # unicode for the micro symbol
# These list of lists defines the short name, full name and units 
# for the model inputs/outputs to limit the places they need to be 
# changed should they need to be.

mec_outputs = [  
            ["A", "Absorption", ""],
            ["CQY", "Canopy Quantum Yield", u+"mol$_{fixed}$ "+u+"mol$_{aborbed}$"],
            ["CUE_24", "Carbon Use Efficiency", ""],
            ["ALPHA", "A*CQY*CUE_24", ""],
            ["BETA", "A*CQY", ""],
            ["DCG", "Daily Carbon Gain", "mol$_{carbon}$ m$^{-2}$ day$^{-1}$"],
            ["CGR", "Crop Growth Rate", "grams m$^{-2}$ day$^{-1}$"],
            ["TCB", "Total Crop Biomass", "grams m$^{-2}$"],
            ["TEB", "Total Edible Biomass", "grams m$^{-2}$"],
            ["VP_SAT", "Saturated Moisture Vapor Pressure", "kPa"],
            ["VP_AIR", "Actual Moisture Vapor Pressure", "kPa"],
            ["VPD", "Vapor Pressure Deficit", "kPa"],
            ["P_GROSS", "Gross Canopy Photosynthesis", u+"mol$_{carbon}$ m$^{-2}$ second$^{-1}$"],
            ["P_NET", "Net Canopy Photosynthesis", u+"mol$_{carbon}$ m$^{-2}$ second$^{-1}$"],
            ["g_S", "Stomatal Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$"],
            ["g_A", "Atmospheric Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$"],
            ["g_C", "Canopy Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$"],
            ["DTR", "Daily Tranpiration Rate", "L$_{water}$ m$^{-2}$ day$^{-1}$"]
]

mec_inputs = [
            ["T_LIGHT", "Light Cycle Temperature", "Degrees Celsius"],
            ["T_DARK", "Dark Cycle Temperature", "Degrees Celsius"],
            ["RH", "Relative Humidity", "%"],
            ["CO2", "CO$_{2}$ Concentration", u+"mol$_{carbon}$ mol$_{air}$"],
            ["PPFD", "Photosynthetic Photon Flux", u+"mol$_{fixed}$ m$^{-2}$ second$^{-1}$"],
            ["H", "Photoperiod", "hours day$^{-1}$"]
]
#########################################################
########################## 
amin_GN = 0.00691867456539118    # amitrano 2020 calibrated with growth chamber experiment exact value from excel
amin_GON = 0.00342717997911672   # amitrano 2020 calibrated with growth chamber experiment exact value from excel

amax_GN = 0.017148682744336      # amitrano 2020 calibrated with growth chamber experiment exact value from excel
amax_GON = 0.00952341360955465   # amitrano 2020 calibrated with growth chamber experiment exact value from excel

bmin_GN = 0                      # amitrano 2020 calibrated with growth chamber experiment exact value from excel
bmin_GON = 0.0486455477321762    # amitrano 2020 calibrated with growth chamber experiment exact value from excel

bmax_GN = 0.0451765692503675     # amitrano 2020 calibrated with growth chamber experiment exact value from excel
bmax_GON = 0.0564626043274799    # amitrano 2020 calibrated with growth chamber experiment exact value from excel

