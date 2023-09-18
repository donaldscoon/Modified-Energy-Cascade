"""

This is the main GSUA script. It contains calls the master definition list of the inputs/outputs. and the problem. Runs the sampler,
runs each of the models, stores the outputs, analyzes the outputs, and charts them throught the use of functions.

"""


from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib import ProblemSpec
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

import MEC_AMI_GSUA
import MEC_BOS_GSUA
import MEC_CAV_GSUA
import SOBOL_ANALYSIS
import GSUA_visulization


##########################################################
############## Defining the Model Inputs #################
##########################################################
# -------------------------------------------------------------------------------------
""" YO YO YO YO YO YO BIG CODING GENIUS
I Think you should make the models/inputs/ouputs defining and lists a function...
go for it buddy! """
# -------------------------------------------------------------------------------------

models = [
         ["AMI", "Amitrano"], 
         ["BOS", "Boscheri"], 
         ["CAV", "Cavazzoni"]
         ]

# this is leftover from before I figured out the better method
# problem = {
#     'num_vars': 5,
#     'names': ['Temp','RH','CO2', 'PPFD', 'H'],
#     'bounds': [[5,40],       # Temperature
#                [35,100],      # Relative Humidity
#                [330,1300],    # Atmo CO2 Concentration
#                [0,1100],     # PPFD Level
#                [0,24]]        # Photoperiod
#                }

u = "\u00B5"        # unicode for the micro symbol

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
            ["PPFD", "Photosynthetic Photon Flux", u+"mol$_{photons}$ m$^{-2}$ second$^{-1}$"],
            ["H", "Photoperiod", "hours day$^{-1}$"]
]

sp = ProblemSpec({
    'names': ['TEMP', 'RH', 'CO2', 'PPFD', 'H'],
    # Notation [min, max, peak as % of that range]
    # for example, with  Temp the range is 35. 54.286% of that would equal 19, 
    # which would actually give a peak at 24 since the range starts at 5.
    'bounds': [[5,40,0.54286],      # Temperature Peak at 24 
               [35,100,0.38461],    # Relative Humidity Peak at 60
               [330,1300,0.48453],  # Atmo CO2 Concentration Peak at 800
               [0,1100,0.27273],    # PPFD Level Peak at 300
               [0,24, 0.66667]],    # Photoperiod Peak at 16
    'dists': ['triang',             # Temperature
              'triang',             # Relative Humidity
              'triang',             # Atmo CO2
              'triang',             # PPFD
              'triang'],            # Photoperiod
    'outputs': ['Y']
})


##########################################################
############## Generate the Samples ######################
##########################################################
""" 
    If needed this step of generating parameters may be skipped
    once generated and the simulations performed. The output 
    files will be able to be used for the analysis and charting
"""
if __name__ == '__main__':

    # sim_start=datetime.now()
    # print("Generating the samples")

    # SOBOL_ANALYSIS.SAMPLE()
    # # Morris_EE.SAMPLE()

    # print('sobol sampling completed, proceeding to the simulations')



##########################################################
######################### Run Models #####################
##########################################################


    MEC_AMI_GSUA.RUN_SIM('morris')      # Runs just the simulations for the Amitrano Model
    # MEC_BOS_GSUA.RUN_SIM()      # Runs just the simulations for the Boscheri Model
    # MEC_CAV_GSUA.RUN_SIM()      # Runs just the simulations for the Cavazzoni Model

    # MEC_AMI_GSUA.RUN_CHART()    # Runs just the charting for the Amitrano Model
    # MEC_BOS_GSUA.RUN_CHART()    # Runs just the charting for the Boscheri Model
    # MEC_CAV_GSUA.RUN_CHART()    # Runs just the charting for the Cavazzoni Model

    # MEC_AMI_GSUA.RUN_FULL()     # Runs both the simulations and charting for the Amitrano Model
    # MEC_BOS_GSUA.RUN_FULL()     # Runs both the simulations and charting for the Boscheri Model
    # MEC_CAV_GSUA.RUN_FULL()     # Runs both the simulations and charting for the Cavazzoni Model
    # sim_time = datetime.now()-sim_start
    # print(f"All three models have run. It took {sim_time}")

###########################################################
#################### Analysis #############################
###########################################################
#     print("Beginning Analysis of simulations")
#     analysis_start=datetime.now()

#     SOBOL_ANALYSIS.ANALYZE()
#     # Morris_EE.ANALYZE()

# ################################# Morris Elementary Effects Anlaysis ##################################


#     analysis_time = datetime.now()-analysis_start



    # print(f"All three models analyzed. It took {analysis_time}")


###########################################################
#################### VISUALIZATIONS #######################
###########################################################

# GSUA_visulization.GSUA_CHARTS()

###########################################
############ To Do ########################
###########################################

# line 21