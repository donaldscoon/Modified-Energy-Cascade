'''
Going to try and run a small scale version of the MEC through GSUA before doing the whole thing.
'''

from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami


##########################################################
############## Defining the Model Inputs #################
##########################################################

MEC = {
    'num_vars': 3,
    'names': ['Temp','Humi','CO2'],
    'bounds': [[20,40],       # Temperature variable
               [60, 90],      # Humidity variable
               [300, 500]]    # CO2 variable
}

##########################################################
############## Generate the Samples ######################
##########################################################

param_values = saltelli.sample(MEC, 32)      # 2**5 = 32 for 256 samples
# print(param_values.shape)                    # The samples generates N*((2*D)+2) samples

##########################################################
######################### Run Model ######################
##########################################################
'''Now I need to find a way to make the MEC run... 
   from this program, with the param_values inputs
   and capture the outputs. '''

'''This is where the OOP will come in handy I believe.'''