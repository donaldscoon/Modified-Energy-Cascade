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
import winsound
from datetime import datetime
from clear_contents import confirm_and_erase
from clear_contents import clear_GSUA_sim_csv

import MEC_AMI_GSUA
import MEC_BOS_GSUA
import MEC_CAV_GSUA
import EE
import SOBOL_ANALYSIS
import GSUA_visulization
import naming_function


########################################################
############ Helper Code #################
########################################################


outputs = naming_function.mec_output_names()
models = naming_function.model_names()
# GSUA_types = ['Individual', 'Structure']
GSUA_types = ['Structure']
gen_path, indiv_path, structure_path = naming_function.path_names()

confirm_and_erase(structure_path)
# confirm_and_erase(indiv_path)


########################################################
############ Generate the Samples ######################
########################################################
"""
    If needed this step of generating parameters may be skipped
    once generated and the simulations performed. The output
    files will be able to be used for the analysis and charting
"""


if __name__ == '__main__':

    time_start = datetime.now()
    for item in GSUA_types:
        GSUA_type = item
        inputs = naming_function.mec_input_names(GSUA_type)

        # type_start = datetime.now()

        # print(f"Generating the {GSUA_type} samples")
        # SOBOL_ANALYSIS.SAMPLE(GSUA_type)
        
        # time_sampling = datetime.now() - type_start
        # print(f'{GSUA_type} samples generated it took {time_sampling}')

        time_sim_start = datetime.now()
        if GSUA_type == 'Individual':
            type_start = datetime.now()

            time_indiv_start = datetime.now()
            SIM_STRU = 0 # Here to successfully run the MEC scripts
            print(f'Proceeding to the {GSUA_type} simulations')
            param_values = np.loadtxt(f'{gen_path}INDIV_SOBOL_parameters.txt')
            total_sims = len(param_values)

            for i, X in enumerate(param_values):
                """ the structure of this for loop sets the model inputs equal to a
                    row from the sampled parameters for each simulation iteration.
                """
                # Columns are Temp, Humidity, CO2, PPFD, H,
                SIM_TEMP = X[0]
                SIM_RH   = X[1]
                SIM_CO2  = X[2]
                SIM_PPFD = X[3]
                SIM_H    = X[4]
                SIM_NUM = i
                # print(SIM_NUM,SIM_TEMP,SIM_RH,SIM_CO2,SIM_PPFD,SIM_H)
                SIM_LENGTH = 30
                if SIM_NUM % 50 == 0:
                    print(f"{SIM_NUM} / {total_sims} simulations completed")
                MEC_AMI_GSUA.RUN_SIM(SIM_TEMP, SIM_RH, SIM_CO2, SIM_PPFD, SIM_H, SIM_NUM, SIM_LENGTH, SIM_STRU, 
                                    GSUA_type, inputs, outputs, models)      # Runs just the simulations for the Amitrano Model

                MEC_BOS_GSUA.RUN_SIM(SIM_TEMP, SIM_RH, SIM_CO2, SIM_PPFD, SIM_H, SIM_NUM, SIM_LENGTH, SIM_STRU, 
                                    GSUA_type, inputs, outputs, models)      # Runs just the simulations for the Boscheri Model

                MEC_CAV_GSUA.RUN_SIM(SIM_TEMP, SIM_RH, SIM_CO2, SIM_PPFD, SIM_H, SIM_NUM, SIM_LENGTH, SIM_STRU, 
                                    GSUA_type, inputs, outputs, models)      # Runs just the simulations for the Cavazzoni Model
            time_indiv_dun = datetime.now() - time_indiv_start
            print(f'{total_sims} simulations complete, it took {time_indiv_dun}')

        elif GSUA_type == 'Structure':
            time_stru_start = datetime.now()
            print(f'Proceeding to the {GSUA_type} simulations')
            param_values = np.loadtxt(f'{gen_path}STRUCTURE_SOBOL_parameters.txt')
            total_sims = len(param_values)

            ami_count = 0
            bos_count = 0
            cav_count = 0
            for i, X in enumerate(param_values):
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
                # print(SIM_NUM,SIM_TEMP,SIM_RH,SIM_CO2,SIM_PPFD,SIM_H, SIM_STRU)
                SIM_LENGTH = 30
                if SIM_NUM % 100 == 0:
                    print(f"{SIM_NUM} / {total_sims} simulations completed")
                if SIM_STRU == 1:
                    ami_count += 1
                    MEC_AMI_GSUA.RUN_SIM(SIM_TEMP, SIM_RH, SIM_CO2, SIM_PPFD, SIM_H, SIM_NUM, SIM_LENGTH, SIM_STRU, 
                                         GSUA_type, inputs, outputs, models)      # Runs just the simulations for the Amitrano Model
                elif SIM_STRU == 2:
                    bos_count += 1
                    MEC_BOS_GSUA.RUN_SIM(SIM_TEMP, SIM_RH, SIM_CO2, SIM_PPFD, SIM_H, SIM_NUM, SIM_LENGTH, SIM_STRU, 
                                         GSUA_type, inputs, outputs, models)      # Runs just the simulations for the Boscheri Model
                else:
                    cav_count += 1
                    MEC_CAV_GSUA.RUN_SIM(SIM_TEMP, SIM_RH, SIM_CO2, SIM_PPFD, SIM_H, SIM_NUM, SIM_LENGTH, SIM_STRU, 
                                         GSUA_type, inputs, outputs, models)      # Runs just the simulations for the Cavazzoni Model
            # print(f'AMI={ami_count} BOS={bos_count} CAV={cav_count}')

            # # Combining all the seperate datafiles into one for the anaylsis portion
            AMI_df = pd.read_csv(f'{structure_path}/GSUA_AMI_out/data/GSUA_AMI_Simulations.csv', header=None)
            AMI_df_label = ['Timestep','skip?','SIM_NUM', 'H','A','ALPHA','BETA','CQY','CUE_24',
                            'DCG','CGR','TCB','TEB','DOP','VP_SAT','VP_AIR','VPD','P_GROSS',
                            'P_NET','g_S','g_A','g_C','DTR','T_LIGHT','T_DARK','RH','CO2','PPFD', 'SIM_STRU']
            AMI_df.columns = AMI_df_label

            BOS_df = pd.read_csv(f'{structure_path}/GSUA_BOS_out/data/GSUA_BOS_Simulations.csv', header=None)
            BOS_df_label = ['SIM_NUM','Timestep','H','Diurnal', 'A','ALPHA','BETA','CQY', 'CUE_24','DCG','CGR','DWCGR','TCB','TEB',
                            'VP_SAT','VP_AIR','VPD','P_NET','P_GROSS', 'DOP','DOC','g_S','g_A','g_C','DTR', 'DCO2C','DCO2P','DNC', 
                            'DWC','T_LIGHT', 'T_DARK','RH','CO2','PPFD', 'SIM_STRU']
            BOS_df.columns = BOS_df_label

            CAV_df = pd.read_csv(f'{structure_path}/GSUA_CAV_out/data/GSUA_CAV_Simulations.csv', header=None)
            CAV_df_label = ['SIM_NUM','Timestep','H','A','ALPHA','BETA','CQY','CUE_24','DCG', 'CGR','TCB','TEB','DOP',
                            'VP_SAT','VP_AIR','VPD','P_GROSS', 'P_NET','g_S','g_A','g_C','DTR','T_LIGHT','T_DARK','RH','CO2',
                            'PPFD', 'SIM_STRU']
            CAV_df.columns = CAV_df_label

            GSUA_df = pd.concat([AMI_df, BOS_df, CAV_df])
            GSUA_df = GSUA_df.sort_values(by='SIM_NUM')
            clear_GSUA_sim_csv()
            GSUA_df.to_csv(f'{structure_path}GSUA_simulations.csv', mode='a', index=False, header=True)
            time_stru_dun = datetime.now() - time_stru_start
            print(f'{total_sims} simulations complete, it took {time_stru_dun}')

        time_sim_dun = datetime.now() - time_sim_start
        print(f'All simulations complete. It took {time_sim_dun}')

        #########################################################
        ################## Analysis #############################
        #########################################################
        time_ana_start = datetime.now()
        print(f'Beginning analysis of {GSUA_type} simulations')

        SOBOL_ANALYSIS.ANALYZE(GSUA_type, models, inputs, outputs)
        EE.ANALYZE(GSUA_type, models, inputs, outputs)

        time_ana_dun = datetime.now() - time_ana_start
        print(f'Analysis complete. It took {time_ana_dun}')

        ##########################################################
        ################### VISUALIZATIONS #######################
        ##########################################################
        print(f'Creating charts for the results of {GSUA_type} simulations and analysis')
        time_viz_start = datetime.now() 
        MEC_AMI_GSUA.RUN_CHART(GSUA_type, models, inputs, outputs)    # Runs just the charting for the Amitrano Model
        MEC_BOS_GSUA.RUN_CHART(GSUA_type, models, inputs, outputs)    # Runs just the charting for the Boscheri Model
        MEC_CAV_GSUA.RUN_CHART(GSUA_type, models, inputs, outputs)    # Runs just the charting for the Cavazzoni Model
        GSUA_visulization.GSUA_CHARTS(GSUA_type, models, inputs, outputs)
        EE.CHART(GSUA_type, models, inputs, outputs)
        SOBOL_ANALYSIS.CHART(GSUA_type, models, inputs, outputs)
        time_viz_dun = datetime.now() - time_viz_start
        print(f'Visulizations took {time_viz_dun}')


time_dun = datetime.now() - time_start
print(f'BOOOP! GSUA Complete. It took {time_dun}')

duration = 1000  # milliseconds
freq = 440  # Hz
winsound.Beep(freq, duration)


###########################################
############ To Do ########################
###########################################


            ##################################################################
            #### Does EE analysis need to iterate through the input columns?
            ##################################################################
            #### Maybe try to condense the EE and sobol charting functions?
            ##################################################################
            #### Add monotonicity to the EE Plots