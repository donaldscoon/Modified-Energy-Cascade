import numpy as np
from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami

# Define the problem dictionary
problem = {
    'num_vars': 1,  # Number of model inputs
    'names': [['X1']],  # Names of the inputs
    'bounds': [[1, 3]],  # Discrete uniform distribution with levels 1, 2, 3
    'dists': 'unif',  # Specify 'discrete' distribution type
    # 'levels': [3]  # Number of levels for each input
}

# Generate samples using the Sobol sampler
param_values = saltelli.sample(problem, 2**3, calc_second_order=False)

# The param_values array now contains samples from the discrete uniform distribution

# You can convert these values to integers if needed
param_values = param_values.astype(int)

# Print the generated samples
print(param_values)
