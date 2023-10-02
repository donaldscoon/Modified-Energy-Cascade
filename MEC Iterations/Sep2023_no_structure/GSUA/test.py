from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib import ProblemSpec

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
import naming_function

inputs = naming_function.mec_input_names()
outputs = naming_function.mec_output_names()
models = naming_function.model_names()
sp = naming_function.prob_spec()


sobol_tests = [
         ["ST", "Total Order"], 
         ["S1", "1st Order"], 
         ["S2", "2nd Order"]
         ]

# print(outputs)
for item in models:                 # loop for model names
    model_short_name = item[0]
    model_long_name = item[1]
    for item in outputs:   # loop for outputs
        output_short_name = item[0]
        output_long_name = item[1]
        output_unit = item[2]
        for item in sobol_tests:
            sobol_short_name = item [0]
            sobol_long_name = item [1]

import naming_function

##########################################################
############## Defining the Model Inputs #################
##########################################################

inputs = naming_function.mec_input_names()
outputs = naming_function.mec_output_names()
models = naming_function.model_names()
sp = naming_function.prob_spec()