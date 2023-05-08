"""
This is a test of the library SALib as outlined in the
documentation. It will perform a Sobol sensitivity analysis
on the Ishigami function because it " exhibits strong 
nonlinearity and nonmonotonicity"

Follows documentation
https://salib.readthedocs.io/en/latest/user_guide/basics.html

"""

from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami
import numpy as np



##########################################################
############## Defining the Model Inputs #################
##########################################################

problem = {
    'num_vars': 3,                                  # number of variable        
    'names:': ['x1','x2','x3'],                     # names of the variables
    'bounds': [[-3.14159265359, 3.14159265359],     # bounds of x1
               [-3.14159265359, 3.14159265359],     # bounds of x2
               [-3.14159265359, 3.14159265359]]     # bounds of x3
}

##########################################################
############## Generate the Samples ######################
##########################################################

param_values = saltelli.sample(problem, 1024)      # 1024 = N = number of samples
# print(param_values.shape)                        # The samples generates N*((2*D)+2) samples

##########################################################
######################### Run Model ######################
##########################################################
"""SALib is not involved in the evaluation of the 
mathematical or computational model. If the model is 
written in Python, then generally you will loop over each 
sample input and evaluate the model:"""

"""I think the structure of this example is wonk. This Y= 
seems to be whats running the model, the loop is simply 
assembling the data files."""
Y = np.zeros([param_values.shape[0]])
Y = Ishigami.evaluate(param_values)
print(Y)

# goodness gracious. I can't get this to work. :(

for i, X in enumerate(param_values):
    # print(i, X, Y[i])
    # this saves each of the 8192 model outputs for that sample. If its working correctly.
    np.savetxt("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/outputs.txt", Y)

    # this saves each of the 8192 samples of the parameters to a text file
    # np.savetxt("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/param_values.txt", param_values)
    
    #idk if this is useful.
    # Y = np.loadtxt("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/outputs.txt", float)
    
    
    # Y[i] = evaluate_model(X) #this blasted thing better not be important!!



##########################################################
#################### Perform Analysis ####################
##########################################################

Si = sobol.analyze(problem, Y)
print(Si['S1'])