import os
import naming_function

inputs = naming_function.mec_input_names()
outputs = naming_function.mec_output_names()
models = naming_function.model_names()

path = 'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure'

def empty__output_dirs():

    for model in models:
        model_short_name = model[0]
        model_long_name = model[1]
        data_path = f'{path}/GSUA_{model_short_name}_out/data'
        fig_path = f'{path}/GSUA_{model_short_name}_out/figures'
        EE_path =  f'{path}/GSUA_{model_short_name}_out/figures/EE'
        sobol_path =  f'{path}/GSUA_{model_short_name}_out/figures/sobol'
        
        ### These still need to be added
        # # sobol_multi_path = f'{path}/figures'
        # EE_multi_path = f'{path}/figures/Elementary_Effects'
        # hist_path = f'{path}/figures/histogram'
        # scatter_path = f'{path}/figures/scatter'
        # one specific to the constant outputs file!


        for filename in os.listdir(data_path): # this loop removes the data files
            file_path = os.path.join(data_path, filename)  
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)  
            except Exception as e:
                print(f'Error deleting {data_path}: {e}')

        for filename in os.listdir(fig_path): # this loop removes the general fig files
            file_path = os.path.join(fig_path, filename)  
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)  
            except Exception as e:
                print(f'Error deleting {fig_path}: {e}')

        for filename in os.listdir(EE_path): # this loop removes the general fig files
            file_path = os.path.join(EE_path, filename)  
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)  
            except Exception as e:
                print(f'Error deleting {EE_path}: {e}')

        for filename in os.listdir(sobol_path): # this loop removes the general fig files
            file_path = os.path.join(sobol_path, filename)  
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)  
            except Exception as e:
                print(f'Error deleting {sobol_path}: {e}')

    # # # print("Deletion done")

# Executes this program/function
if __name__ ==('__main__'):
    empty__output_dirs()

def clear_GSUA_sim_csv():
    if os.path.exists('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/GSUA_simulations.csv'):
        os.remove('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/GSUA_simulations.csv')

# Executes this program/function
if __name__ ==('__main__'):
    clear_GSUA_sim_csv

def clear_const_out():
    if os.path.exists('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/results/constant_outputs.txt'):
        os.remove('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/results/constant_outputs.txt')

# Executes this program/function
if __name__ ==('__main__'):
    clear_const_out

