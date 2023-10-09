import os
import naming_function

inputs = naming_function.mec_input_names()
outputs = naming_function.mec_output_names()
models = naming_function.model_names()

path = 'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA'

def empty__output_dirs():

    for model in models:
        model_short_name = model[0]
        model_long_name = model[1]
        data_path = f'{path}/GSUA_{model_short_name}_out/data'
        fig_path = f'{path}/GSUA_{model_short_name}_out/figures'
        EE_path =  f'{path}/GSUA_{model_short_name}_out/figures/EE'
        sobol_path =  f'{path}/GSUA_{model_short_name}_out/figures/sobol'

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