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
import naming_function

##########################################################
############## Defining the Model Inputs #################
##########################################################

inputs = naming_function.mec_input_names()
outputs = naming_function.mec_output_names()
models = naming_function.model_names()
sp = naming_function.prob_spec()


##########################################################
############## Generate the Samples ######################
##########################################################
""" 
    If needed this step of generating parameters may be skipped
    once generated and the simulations performed. The output 
    files will be able to be used for the analysis and charting
"""
if __name__ == '__main__':

    sim_start=datetime.now()
    print("Generating the samples")

    SOBOL_ANALYSIS.SAMPLE()
    
    print('sobol sampling completed, proceeding to the simulations')



##########################################################
######################### Run Models #####################
##########################################################


    # MEC_AMI_GSUA.RUN_SIM()      # Runs just the simulations for the Amitrano Model
    # MEC_BOS_GSUA.RUN_SIM()      # Runs just the simulations for the Boscheri Model
    # MEC_CAV_GSUA.RUN_SIM()      # Runs just the simulations for the Cavazzoni Model

    # MEC_AMI_GSUA.RUN_CHART()    # Runs just the charting for the Amitrano Model
    # MEC_BOS_GSUA.RUN_CHART()    # Runs just the charting for the Boscheri Model
    # MEC_CAV_GSUA.RUN_CHART()    # Runs just the charting for the Cavazzoni Model

    MEC_AMI_GSUA.RUN_FULL()     # Runs both the simulations and charting for the Amitrano Model
    MEC_BOS_GSUA.RUN_FULL()     # Runs both the simulations and charting for the Boscheri Model
    MEC_CAV_GSUA.RUN_FULL()     # Runs both the simulations and charting for the Cavazzoni Model
    sim_time = datetime.now()-sim_start
    print(f"All three models have run. It took {sim_time}")

###########################################################
#################### Analysis #############################
###########################################################
    print("Beginning Analysis of simulations")
    analysis_start=datetime.now()

    SOBOL_ANALYSIS.ANALYZE()
    EE.ANALYZE()

###########################################################
#################### VISUALIZATIONS #######################
###########################################################

    GSUA_visulization.GSUA_CHARTS()
    EE.CHARTS()
    SOBOL_ANALYSIS.CHART()


    analysis_time = datetime.now()-analysis_start
    print(f"All three models analyzed. It took {analysis_time}")

total_time = datetime.now()-sim_start
print(f"Individual Model GSUA Complete: {total_time}")

###########################################
############ To Do ########################
###########################################

# line 21