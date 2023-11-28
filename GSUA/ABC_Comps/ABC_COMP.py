import pandas as pd

path = 'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/ABC_Comps/'


def RUN_COMP():     # used to package this version of the MEC as a function callable by other programs
    # start=datetime.now()
    # print("Begining Amitrano Simulations")
    # ##########################################################
    # ############## Defining the Model Inputs #################
    # ##########################################################

    param_values = pd.read_csv(f'{path}AM_data_input.csv') # loads the parameters of AMI's experimental data
    df_sims = pd.DataFrame({})


    for i, row in param_values.iterrows():     
        print(row)
        # df_AMI_records = MEC_AMI_COMP.timestep(i, row, timestep)
        # df_sims = pd.concat([df_sims, df_records], ignore_index=True)
        # print(df_sims)

# Executes this program/function
if __name__ ==('__main__'):
    RUN_COMP()
