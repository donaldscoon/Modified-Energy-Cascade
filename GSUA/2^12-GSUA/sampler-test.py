from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib import ProblemSpec

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import warnings
import naming_function

GSUA_type = 'Structure'


sp = naming_function.prob_spec(GSUA_type)
multiplier = 2**12
if GSUA_type == 'Structure': # Sampling procedure for the Structure GSUA
    param_values = sp.sample_sobol(multiplier, calc_second_order=True) # sobol sampling 2**6 generates 768 samples
    np.savetxt(f'C:/Users/dcoon/Documents/GitHub/Modified-Energy-Cascade/GSUA/2^12-GSUA/sampler/STRUCTURE_SOBOL_parameters.txt', sp.samples)
elif GSUA_type == 'Individual': # Sampling procedure for the individual GSUA's
    param_values = sp.sample_sobol(multiplier, calc_second_order=True) # sobol sampling 2**6 generates 768 samples
#     np.savetxt(f'C:/Users/dcoon/Documents/GitHub/Modified-Energy-Cascade/GSUA/2^12-GSUA/sampler/INDIV_SOBOL_parameters.txt', sp.samples)


samples = np.loadtxt(f'C:/Users/dcoon/Documents/GitHub/Modified-Energy-Cascade/GSUA/2^12-GSUA/sampler/STRUCTURE_SOBOL_parameters.txt')

ami_count = 0
bos_count = 0
cav_count = 0

for i, X in enumerate(samples):
    """ the structure of this for loop sets the model inputs equal to a
        row from the sampled parameters for each simulation iteration.
    """
    # Columns are Temp, Humidity, CO2, PPFD, H, Model Structure
    SIM_TEMP = X[0]
    SIM_RH   = X[1]
    SIM_CO2  = X[2]
    SIM_PPFD = X[3]
    SIM_H    = X[4]
    SIM_STRU = X[5]
    SIM_NUM = i


    if 0.5 <= SIM_STRU < 1.5:
        print(f'{SIM_STRU} AMI')
        ami_count += 1
    elif 1.5 <= SIM_STRU < 2.5:
        print(f'{SIM_STRU} BOS')
        bos_count += 1
    elif 2.5<= SIM_STRU < 3.5:
        print(f'{SIM_STRU} CAV')
        cav_count += 1

print(f'AMI SIMS {ami_count}')
print(f'BOS SIMS {bos_count}')
print(f'CAV SIMS {cav_count}')