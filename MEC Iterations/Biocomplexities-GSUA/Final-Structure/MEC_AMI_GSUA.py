'''
This version of the Amitrano Model is meant to run GSUA 
and has been altered for...
    *being called from another program
    *keeping track of the simulation number
    *exporting data for GSUA as .txt files
    *creating every possible version of charts needed
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import naming_function

##########################################################
############## Defining the Model Inputs #################
##########################################################

inputs = naming_function.mec_input_names()
outputs = naming_function.mec_output_names()
models = naming_function.model_names()
sp = naming_function.prob_spec()

#########################################################
################### OTHER MODEL CONSTANTS ###############
#########################################################

amin_GN = 0.00691867456539118    # amitrano 2020 calibrated with growth chamber experiment exact value from excel
amin_GON = 0.00342717997911672   # amitrano 2020 calibrated with growth chamber experiment exact value from excel

amax_GN = 0.017148682744336      # amitrano 2020 calibrated with growth chamber experiment exact value from excel
amax_GON = 0.00952341360955465   # amitrano 2020 calibrated with growth chamber experiment exact value from excel

bmin_GN = 0                      # amitrano 2020 calibrated with growth chamber experiment exact value from excel
bmin_GON = 0.0486455477321762    # amitrano 2020 calibrated with growth chamber experiment exact value from excel

bmax_GN = 0.0451765692503675     # amitrano 2020 calibrated with growth chamber experiment exact value from excel
bmax_GON = 0.0564626043274799    # amitrano 2020 calibrated with growth chamber experiment exact value from excel

def RUN_SIM(SIM_TEMP, SIM_RH, SIM_CO2, SIM_PPFD, SIM_H, SIM_NUM, SIM_LENGTH, SIM_STRU):     # used to package this version of the MEC as a function callable by other programs

    # start=datetime.now()
    # print("Begining Amitrano Simulations")
    ##########################################################
    ############## Defining the Model Inputs #################
    ##########################################################

    df_sims = pd.DataFrame({})

    ####################################################
    ################## RUN MODEL #######################
    ####################################################

    PPFD = SIM_PPFD       # umol/m^2/sec, Amitrano 2020 Table 2
    CO2 = SIM_CO2         # umol CO2 / mol air
    H = SIM_H             # photoperiod defined as 16 in Cavazonni 2001
    T_LIGHT = SIM_TEMP    # Light Cycle Average Temperature ewert table 4-111 or user input
    T_DARK = T_LIGHT -  5  # Dark Cycle Average. Instead of creating a range for this I simply subtract from T_LIGHT
    RH = SIM_RH           # relative humidty as a fraction bounded between 0 and 1. The 0.675 is a number pulled from a Dr. GH VPD table as ideal for lettuce
    t_M = SIM_LENGTH            # time at harvest/maturity ewert table 4-112
    P_ATM = 101           # atmospheric pressure placeholder is gainesville FL value
    T_T = 10            # days to transplant, based on experimental design


    ##################################################
    ################# INTIALIZATION  #################
    ##################################################

    t = 0               # time in days
    res = 1             # model resolution (in days)
    day = 0             # used in the seedling stage loop
    df_records = pd.DataFrame({})            # simulation record dataframe
    ts_to_harvest = int(t_M/res)             # calcs the timesteps needed to set up the matrix for each ts
    TEB = 8.53                               # The value of TEB at 10 DAE

    ##################################################
    #################### CONSTANTS ###################
    ##################################################
    BCF = 0.4           # Amitrano 2020 table 2 -> Adeyemi 2018
    XFRT = 0.95         # Amitrano 2020 table 2 -> Adeyemi 2018
    OPF = 1.08          # Amitrano 2020 table 2 -> Adeyemi 2018
    g_A = 2.5           # Amitrano 2020 table 2 -> Amitrano 2019
    t_D = 1             # 1 for green, 8 for red initial time of development(days) Amirtrano 2020 CQY experiments
    t_Mi = 16           # initial time of maturity (days) Amitrano 2020 table 2
    t_E = 1             # time at onset of organ formation Amitrano 2020 same as ewert table 4-112
    MWC = 12.01            # molecular weight of carbon amitrano 2020
    MW_W = 18.015       # molecular weight of water ewert table 4-110
    d_W = 998.23        # water density ewert table 4-110
    P_ATM = 100         # atmospheric pressure Number from Amitrano excel
    T_LEAF = 20.2       # experimental data from  amitrano        

    # This first loop is needed to align dataframe across models.
    # It is the first 10 days from seedling to transplant. 
    while t < T_T:
        dfts = pd.DataFrame({
            'Timestep': [t],
            'Day': [day]})
        df_records = pd.concat([df_records, dfts], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
        t += res
        day += 1
    t=0
    

    # This second loop continues from transplant to harvest.
    while t <= ts_to_harvest:                  # while time is less than harvest time
        if t<= t_D:                            # if timestep is before formation of edible organs
            ALPHA = amin_GN                    # amitrano 2020 eq 15
            BETA = bmin_GN                     # amitrano 2020 eq 15
        elif t <= t_Mi:                        # if timestep is after organ formation but before maturity
            ALPHA = amin_GN+(amax_GN-amin_GN)*(t-t_D)/(t_Mi-t_D)        # amitrano 2020 eq 15
            BETA = bmin_GN+(bmax_GN-bmin_GN)*(t-t_D)/(t_Mi-t_D)         # amitrano 2020 eq 15
        else:                                  # all other timesteps
            ALPHA = amax_GN                    # amitrano 2020 eq 15
            BETA = bmax_GN                     # amitrano 2020 eq 15
        DCG = 0.0036*H*ALPHA*PPFD              # amitrano 2020 eq 4
        DOP = OPF*DCG                          # amitrano 2020 eq 5
        CGR = MWC*(DCG/BCF)                      # amitrano 2020 eq 6
        if t > t_E:                            # if edible organ formation has begun
            TEB = CGR+TEB                      # Amitrano 2020 GN excel column I
        P_GROSS = BETA*PPFD                    # amitrano 2020 eq 8
        VP_SAT = 0.611*np.exp(1)**(17.4*T_LIGHT/(T_LIGHT+239)) # Same as ewert and cavazzoni, though likely from Monje 1998
        VP_AIR = VP_SAT*RH                     # Same as ewert and cavazzoni, though likely from Monje 1998
        VPD = VP_SAT*(1-RH)                    # Same as ewert and cavazzoni, though likely from Monje 1998
        P_NET = (H*ALPHA/24+BETA*(24-H)/24)*PPFD    # Amitrano 2020 eq 9
        g_S = ((1.717*T_LIGHT)-19.96-(10.54*VPD))*(P_NET/CO2) # Amitrano 2020 eq 10 (with some nice parenthesis that don't change anything)
        g_C = g_A*g_S/(g_A+g_S)                # Amitrano 2020 eq 10
        DTR = 3600*H*(MW_W/d_W)*g_C*(VPD/P_ATM)
        dfts = pd.DataFrame({
            'SIM_NUM': [SIM_NUM],
            'Timestep': [t],
            'H': [H],
            'A': [0],       # Not included in Amitranos Model
            'ALPHA':[ALPHA],
            'BETA':[BETA],
            'CQY': [0],       # Not included in Amitranos Model
            'CUE_24': [0],       # Not included in Amitranos Model
            'DCG': [DCG],
            'CGR': [CGR],
            'TCB': [0],       # Not included in Amitranos Model
            'TEB': [TEB],
            'DOP': [DOP],
            'VP_SAT': [VP_SAT],
            'VP_AIR': [VP_AIR],
            'VPD': [VPD],
            'P_GROSS': [P_GROSS],
            'P_NET': [P_NET],
            'g_S': [g_S],
            'g_A': [g_A],
            'g_C': [g_C],
            'DTR': [DTR],
            'T_LIGHT': [T_LIGHT],
            'T_DARK': [T_DARK],
            'RH': [RH],
            'CO2': [CO2],
            'PPFD': [PPFD],
            'STRU': [SIM_STRU],
        }) # creates a dataframe of all variables/outputs for each timestep. 
        df_records = pd.concat([df_records, dfts], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
        t += res                          # advance timestep
    # print(df_records)                    # prints a copy of output in the terminal
    df_sims = pd.concat([df_sims, df_records.iloc[-1:]], ignore_index=True) # should save the last row of each version of df_records
    df_sims.to_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/GSUA_AMI_out/data/GSUA_AMI_Simulations.csv', mode='a', index=False, header=False)
    for output in outputs:      # This loop runs create text files for each /inputoutput of the MEC!
        with open(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/GSUA_AMI_out/data/GSUA_AMI_data_{output[0]}.txt', 'a') as file: # opens each output file in append mode
            np.savetxt(file, df_sims[[f'{output[0]}']]) # saves the output to the proper txt file


# print("Amitrano Simulations Complete")
# time = datetime.now()-start
# print(f"Simulations took {time}")

# Executes this program/function
if __name__ ==('__main__'):
    RUN_SIM()


##########################################################
############### VISUALIZATIONS ###########################
##########################################################

def RUN_CHART(models, inputs, outputs):
    mec_inputs = inputs
    outputs = outputs
    df_sims_label = ['SIM_NUM','Timestep','skip?', 'H','A','ALPHA','BETA','CQY','CUE_24',
                     'DCG','CGR','TCB','TEB','DOP','VP_SAT','VP_AIR','VPD','P_GROSS',
                     'P_NET','g_S','g_A','g_C','DTR','TEMP','T_DARK','RH','CO2','PPFD', 'STRU']

    start=datetime.now()
    print("Begining Amitrano Visulizations")

    df_AMI_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/GSUA_AMI_out/data/GSUA_AMI_Simulations.csv', names = df_sims_label)

    for item in mec_inputs:        # this allows easy injection of labels into chart elements
        input_short_name = item[0]
        input_long_name = item[1]
        input_unit = item[2]
        for item in outputs:
            output_short_name = item[0]
            output_long_name = item[1]
            output_unit = item[2]

            """This chart bulding stuff works!"""
            VIS_GSUA = df_AMI_sims[[output_short_name, input_short_name]]
            VIS_GSUA = VIS_GSUA.sort_values(input_short_name, ascending=True)
            x = VIS_GSUA[[input_short_name]].values.flatten()       # the flatten converts the df to a 1D array, needed for trendline
            y = VIS_GSUA[[output_short_name]].values.flatten()      # the flatten converts the df to a 1D array, needed for trendline
            fig, ax = plt.subplots()
            ax.scatter(x, y)
            ax.set_ylabel(f'{output_long_name} ({output_unit})')
            ax.set_xlabel(f'{input_long_name} ({input_unit})')
            plt.title(f'AMI {input_short_name} x {output_short_name}')
            # plt.axhline(y=np.nanmean(y), color='red', linestyle='--', linewidth=3, label='Avg')     # just the straight average of the DTR for all simulations

            # calc the trendline
            z = np.polyfit(x, y, 2) # 1 is linear, 2 is quadratic!
            p = np.poly1d(z)
            plt.plot(x,p(x),"red")

            plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/Final-Structure/GSUA_AMI_out/figures/AMI {input_short_name} x {output_short_name}.png', bbox_inches='tight') #there are many options for savefig
            # in the likely rare event all of these need to be viewed...
            # plt.show()

    print("Amitrano Visulizations Complete")
    time = datetime.now()-start
    print(f"Charting took {time}")

# Executes this program/function
if __name__ ==('__main__'):
    RUN_CHART()

def RUN_FULL():
    print("Running Amitrano Simulations and Charting Functions")
    start=datetime.now()
    RUN_SIM()
    RUN_CHART()
    time = datetime.now()-start
    print(f"Full Amitrano run completed. It took {time}")

# Executes this program/function
if __name__ ==('__main__'):
    RUN_FULL()