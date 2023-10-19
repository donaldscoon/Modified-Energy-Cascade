# -*- coding: utf-8 -*-
'''
This version of the Boscheri Model is meant to run GSUA 
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

def RUN_SIM(SIM_TEMP, SIM_RH, SIM_CO2, SIM_PPFD, SIM_H, SIM_NUM, SIM_LENGTH, SIM_STRU):     # used to package this version of the MEC as a function callable by other programs
    # start=datetime.now()
    # print("Begining Boscheri Simulations")
    ##########################################################
    ############## Defining the Model Inputs #################
    ##########################################################

    df_sims = pd.DataFrame({})

    ##################################################
    ################## MODEL INPUTS ##################
    ##################################################
    PPFD = SIM_PPFD       # umol/m^2/sec, needs to accept inputs
    CO2 = SIM_CO2         # umol CO2 / mol air,needs to accept  inputs
    H = SIM_H             # photoperiod defined as 16 in Cavazonni 2001
    T_LIGHT = SIM_TEMP    # Light Cycle Average Temperature ewert table 4-111 or user input
    T_DARK = T_LIGHT - 5  # Dark Cycle Average Temperature ewert table 4-111 or user input
    RH = SIM_RH           # relative humidty as a fraction bounded between 0 and 1. The 0.675 is a number pulled from a Dr. GH VPD table as ideal for lettuce
    t_M = SIM_LENGTH            # days  at harvest/maturity ewert table 4-112
    P_ATM = 101           # atmospheric pressure placeholder is gainesville FL value

    ##################################################
    ################# INTIALIZATION  #################
    ##################################################
    t = 0                       # time in days
    res = 1                     # model resolution 1 hour
    I = 0                       # boscheri "I is equal to 1 and 0 during the photoperiod (day) and dark period (night)"
    night_len = 24 - H.round()  # length of night (rounded so the decimals don't break my day/nigh cycle)
    day_len = 24 - night_len    # length of day
    pp_count = 0                # photoperiod counter
    day = 0

    ##################################################
    #################### CONSTANTS ###################
    ##################################################
    BCF = 0.40          # Biomass carbon fraction ewert table 4-113
    XFRT = 0.95         # edible biomass fraction ewert table 4-112
    OPF = 1.08          # Oxygen production fraction ewert table 4-113
    g_A = 2.5           # atmospheric aerodynamic conductance boscheri "for horizontal canopies"
    A_max = 0.93        # maximum fraction of PPF Absorbtion ewert pg 180
    t_Q = 50            # days onset of senescence placeholder value ewert table 4-112
    t_E = 1             # time at onset of organ formation ewert table 4-112
    MW_W = 18.0153      # Molecular weight of water, boscheri table 4
    MWC = 12.0107       # molecular weight of carbon boscheri table 4
    MW_O2 = 31.9988     # molecular weight of O2 boscheri table 4
    MW_CO2 = 44.010     # molecular weight of CO2 boscheri table 4
    CQY_min = 0         # N/A minimum canopy quantum yield ewert table 4-99
    CUE_max = 0.625     # maximum carbon use efficiency ewert table 4-99
    CUE_min = 0         # N/A minimum carbon use efficiency ewert table 4-99
    D_PG = 24           # the plants diurnal cycle length assumed 24 in cavazzoni 2001
    p_W = 998.23        # density of water at 20 C, ewert table 4-110
    n = 2.5             # Ewert table 4-97 crop specific
    a = 0.0036          # boscheri table 4 similar to others but in 'a'
    b = 3600            # boscheri table 4
    WBF = XFRT          # Boscheri doesn't define this, I'm assuming that its the same as XFRT
    DRY_FR = 6.57/131.35 # dry over wet biomass fraction Hanford 2004 Table 4.2.7, with part from wheeler 2003
    NC_FR = 0.034       # Hanford 2004 table 4.2.10, ugh boscheri just state the number

    ##################################################
    ################ Data Management #################
    ##################################################
    df_records = pd.DataFrame({})
    ts_to_harvest = int(t_M*24/res)             # calcs the timesteps needed to set up the matrix for each ts
    TCB = 0                                 # starting crop biomass
    TEB = 0                                 # starting total edible biomass

    ##################################################
    ############# SUPPLEMENTAL EQUATIONS #############
    ##################################################
    """ Multipolynomial Regression Fits Ewert Table 4-100 """
    # used in the calculation of A_max and CQY_max

    c1 = (1/PPFD)*(1/CO2)
    c2 = (1/PPFD)
    c3 = (CO2/PPFD)
    c4 = (CO2**2/PPFD)
    c5 = (CO2**3/PPFD)
    c6 = (1/CO2)
    c7 = 1
    c8 = CO2
    c9 = (CO2**2)
    c10 = (CO2**3)
    c11 = PPFD*(1/CO2)
    c12 = PPFD
    c13 = PPFD*CO2
    c14 = PPFD*(CO2**2)
    c15 = PPFD*(CO2**3)
    c16 = (PPFD**2)*(1/CO2)
    c17 = (PPFD**2)
    c18 = (PPFD**2)*CO2
    c19 = (PPFD**2)*(CO2**2)
    c20 = (PPFD**2)*(CO2**3)
    c21 = (PPFD**3)*(1/CO2)
    c22 = (PPFD**3)
    c23 = (PPFD**3)*CO2
    c24 = (PPFD**3)*(CO2**2)
    c25 = (PPFD**3)*(CO2**3)


    """ Canopy Closure t_A """
    # t_A coefficients (tac) values originate from EWert table 4-115 
    tac1 = 0
    tac2 = 1.0289*(10**4)
    tac3 = -3.7018
    tac4  = 0 
    tac5 = 3.6648*(10**-7)
    tac6 = 0
    tac7 = 1.7571
    tac8 = 0
    tac9 = 2.3127*(10**-6)
    tac10 = 0
    tac11 = 1.8760
    tac12 = 0
    tac13 = 0
    tac14 = 0
    tac15 = 0
    tac16 = 0
    tac17 = 0
    tac18 = 0
    tac19 = 0
    tac20 = 0
    tac21 = 0
    tac22 = 0
    tac23 = 0
    tac24 = 0
    tac25 = 0

    # each term in the t_A Ewert eq 4-30
    t_A_1 = tac1*c1
    t_A_2 = tac2*c2
    t_A_3 = tac3*c3
    t_A_4 = tac4*c4
    t_A_5 = tac5*c5
    t_A_6 = tac6*c6
    t_A_7 = tac7*c7
    t_A_8 = tac8*c8
    t_A_9 = tac9*c9
    t_A_10 = tac10*c10
    t_A_11 = tac11*c11
    t_A_12 = tac12*c12
    t_A_13 = tac13*c13
    t_A_14 = tac14*c14
    t_A_15 = tac15*c15
    t_A_16 = tac16*c16
    t_A_17 = tac17*c17
    t_A_18 = tac18*c18
    t_A_19 = tac19*c19
    t_A_20 = tac20*c20
    t_A_21 = tac21*c21
    t_A_22 = tac22*c22
    t_A_23 = tac23*c23
    t_A_24 = tac24*c24
    t_A_25 = tac25*c25

    # the calculation of canopy closure ewert eq 4-30
    t_A = (t_A_1 + t_A_2 + t_A_3 + t_A_4 + t_A_5 + 
        t_A_6 + t_A_7 + t_A_8 + t_A_9 + t_A_10 + 
        t_A_11 + t_A_12 + t_A_13 + t_A_14 + t_A_15 + 
        t_A_16 + t_A_17 + t_A_18 + t_A_19 + t_A_20 + 
        t_A_21 + t_A_22 + t_A_23 + t_A_24 + t_A_25)

    """ Canopy Quantum Yield Equation """
    # CQY_max Coefficients ewert table 4-102
    CQY_m_c_1 = 0
    CQY_m_c_2 = 0
    CQY_m_c_3 = 0
    CQY_m_c_4 = 0
    CQY_m_c_5 = 0
    CQY_m_c_6 = 0
    CQY_m_c_7 = 4.4763*(10**-2)
    CQY_m_c_8 = 5.163*(10**-5)
    CQY_m_c_9 = -2.075*(10**-8)
    CQY_m_c_10 = 0
    CQY_m_c_11 = 0
    CQY_m_c_12 = -1.1701*(10**-5)
    CQY_m_c_13 = 0
    CQY_m_c_14 = 0
    CQY_m_c_15 = 0
    CQY_m_c_16 = 0
    CQY_m_c_17 = 0
    CQY_m_c_18 = -1.9731*(10**-11)
    CQY_m_c_19 = 8.9265*(10**-15)
    CQY_m_c_20 = 0
    CQY_m_c_21 = 0
    CQY_m_c_22 = 0
    CQY_m_c_23 = 0
    CQY_m_c_24 = 0
    CQY_m_c_25 = 0

    # CQY_max Terms ewert eq 4-22
    CQY_m_t_1 = CQY_m_c_1*c1
    CQY_m_t_2 = CQY_m_c_2*c2
    CQY_m_t_3 = CQY_m_c_3*c3
    CQY_m_t_4 = CQY_m_c_4*c4
    CQY_m_t_5 = CQY_m_c_5*c5
    CQY_m_t_6 = CQY_m_c_6*c6
    CQY_m_t_7 = CQY_m_c_7*c7
    CQY_m_t_8 = CQY_m_c_8*c8
    CQY_m_t_9 = CQY_m_c_9*c9
    CQY_m_t_10 = CQY_m_c_10*c10
    CQY_m_t_11 = CQY_m_c_11*c11
    CQY_m_t_12 = CQY_m_c_12*c12
    CQY_m_t_13 = CQY_m_c_13*c13
    CQY_m_t_14 = CQY_m_c_14*c14
    CQY_m_t_15 = CQY_m_c_15*c15
    CQY_m_t_16 = CQY_m_c_16*c16
    CQY_m_t_17 = CQY_m_c_17*c17
    CQY_m_t_18 = CQY_m_c_18*c18
    CQY_m_t_19 = CQY_m_c_19*c19
    CQY_m_t_20 = CQY_m_c_20*c20
    CQY_m_t_21 = CQY_m_c_21*c21
    CQY_m_t_22 = CQY_m_c_22*c22
    CQY_m_t_23 = CQY_m_c_23*c23
    CQY_m_t_24 = CQY_m_c_24*c24
    CQY_m_t_25 = CQY_m_c_25*c25

    # CQY_max Calculation ewert eq 4-22
    CQY_max = (CQY_m_t_1 + CQY_m_t_2 + CQY_m_t_3 + CQY_m_t_4 + CQY_m_t_5 +
            CQY_m_t_6 + CQY_m_t_7 + CQY_m_t_8 + CQY_m_t_9 + CQY_m_t_10 + 
            CQY_m_t_11 + CQY_m_t_12 + CQY_m_t_13 + CQY_m_t_14 + CQY_m_t_15 + 
            CQY_m_t_16 + CQY_m_t_17 + CQY_m_t_18 + CQY_m_t_19 + CQY_m_t_20 + 
            CQY_m_t_21 + CQY_m_t_22 + CQY_m_t_23 + CQY_m_t_24 + CQY_m_t_25)

    ##################################################
    ################# THE MODEL LOOP #################
    ##################################################
    while t < ts_to_harvest:                 # while time is less than harvest time
        if I == 0 and pp_count == night_len:    # turns night to day
            I = 1
            pp_count = 0
        elif I == 1 and pp_count == day_len:    # turns day to night
            I = 0
            pp_count = 0
        if (t % 24) == 0:                       # this if statement counts the days by checking if the ts/24 is a whole number
            day += 1
            if t == 0:                          # need this because 0/24 = 0 triggering day counter
                day = 0
        if t < (t_A*24/res):                  # before canopy closure
            A = A_max*(t/(t_A*24/res))**n         # boscheri eq 5
        else:                        # after canopy closure
            A = A_max                    # boscheri eq 5
        if t<= t_Q:                  # before onset of senescence
            CQY = CQY_max                # boscheri eq 3
            CUE_24 = CUE_max             # boscheri eq 4
        elif (t_Q*24/res) < t: 
            """For lettuce the values of CQY_min and CUE_min 
            are n/a due to the assumption that the canopy does
            not senesce before harvest. I coded them anyways, it
            makes it complete for all the other crops too. For 
            crops other than lettuce remove the break statement."""
            CQY = CQY_max - (CQY_max - CQY_min)*((t-t_Q)/(t_M-t_Q)) # boscheri eq 3
            CUE_24 = CUE_max - (CUE_max - CUE_min)*((t-t_Q)/(t_M-t_Q)) # boscheri eq 4
            print(t, "Error: Utilizing CQY and CUE values without definitions")
            break
        ALPHA = A*CQY*CUE_24
        BETA = A*CQY
        HCG = a*CUE_24*A*CQY*PPFD*I      # boscheri eq 2  
        HCGR = HCG*MWC*(BCF)**(-1)       # boscheri eq 6
        ######## SEE WBF FOR ASSUMPTION #############
        HWCGR = HCGR*(1-WBF)**(-1)       # boscheri eq 7 
        HOP = HCG/CUE_24*OPF*MW_O2       # boscheri eq 8
        HOC = HCG/(1-CUE_24)/CUE_24*OPF*MW_O2*H/24 # paper includes "I" with a weird notation, but can't divide by I so I removed boscheri eq 9 
        VP_SAT = 0.611*np.exp(1)**((17.4*T_LIGHT)/(T_LIGHT+239)) # boscheri eq 12
        VPD = VP_SAT*(1-RH)             # boscheri eq 12
        P_NET = A*CQY*PPFD              # boscheri eq 13
        g_S = (1.717*T_LIGHT-19.96-10.54*VPD)*(P_NET/CO2) # boscheri unlabeled equation
        g_C = (g_A*g_S)*(g_A+g_S)**(-1) # boscheri unlabeled equation
        # HTR = b*MW_W*g_C*(VPD/P_ATM)    # boscheir eq 10
        HTR = 3600*H*(MW_W/p_W)*g_C*(VPD/P_ATM) # cavazzonis DTR equation
        HCO2C = HOP*MW_CO2*MW_O2**(-1)  # boscheri eq 14
        HCO2P = HOC*MW_CO2*MW_O2**(-1)  # boscheri eq 15 
        HNC = HCGR*DRY_FR*NC_FR         # boscheri eq unlabeled
        HWC = HTR+HOP+HCO2P+HWCGR-HOC-HCO2C-HNC # boscheri eq 16
        dfts = pd.DataFrame({
            'Timestep': [t],
            'H': [H],
            'Day': [day],
            'diurnal': [I],
            'A': [A],
            'ALPHA':[ALPHA],
            'BETA':[BETA],
            'CQY': [CQY],
            'CUE_24': [CUE_24],
            'DCG': [HCG],
            'CGR': [HCGR],
            'DWCGR': [HWCGR],
            'TCB': [0],
            'TEB': [0],
            'VP_SAT': [VP_SAT],
            'VP_AIR': [0],
            'VPD': [VPD],
            'P_NET': [P_NET],
            'P_GROSS': [0],
            'DOP': [HOP],
            'DOC': [HOC],
            'g_S': [g_S],
            'g_A': [g_A],
            'g_C': [g_C],
            'DTR': [HTR],
            'DCO2C': [HCO2C],
            'DCO2P': [HCO2P],
            'DNC': [HNC], 
            'DWC': [HWC],
            'T_LIGHT': [T_LIGHT],
            'T_DARK': [T_DARK],
            'RH': [RH],
            'CO2': [CO2],
            'PPFD': [PPFD],
            'SIM_STRU': [SIM_STRU],
            }) # creates a dataframe of all variables/outputs for each timestep. 
        df_records = pd.concat([df_records, dfts], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
        df_day_avg = df_records.groupby(['Day']).mean()
        df_day_sum = df_records.groupby(['Day']).sum()
        t += res                          # advance timestep
        pp_count += 1                     # photoperiod counter + 1
    df_avg_sims = pd.concat([df_sims, df_day_avg.iloc[-1:]], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
    df_sum_sims = pd.concat([df_sims, df_day_sum.iloc[-1:]], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
    df_sims = df_avg_sims
    df_sims['DCG'] = df_sum_sims['DCG']
    df_sims['CGR'] = df_sum_sims['CGR']
    df_sims.to_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_BOS_out/data/GSUA_BOS_Simulations.csv', mode='a', index=False, header=False) # exports entire final data frame to a CSV
    for output in outputs:      # This loop runs create text files for each /inputoutput of the MEC!
        with open(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_BOS_out/data/GSUA_BOS_data_{output[0]}.txt', 'a') as file: # opens each output file in append mode
            np.savetxt(file, df_sims[[f'{output[0]}']]) # saves the output to the proper txt file

# print("NOTE: Boscheri did not calculate P_GROSS, VP_AIR, TCB, TEB")
# print("Boscheri Simulations Complete")
# time = datetime.now()-start
# print(f"Simulations took {time}")

# Executes this program/function
if __name__ ==('__main__'):
    RUN_SIM()

###########################################################
#################### VISUALIZATIONS #######################
# ###########################################################
def RUN_CHART(models, inputs, outputs):
    mec_inputs = inputs
    outputs = outputs
    df_sims_label = ['Timestep','H','A','ALPHA','BETA','CQY',
                     'CUE_24','DCG','CGR','DWCGR','TCB','TEB',
                     'VP_SAT','VP_AIR','VPD','P_NET','P_GROSS',
                     'DOP','DOC','g_S','g_A','g_C','DTR',
                     'DCO2C','DCO2P','DNC', 'DWC','T_LIGHT',
                     'T_DARK','RH','CO2','PPFD']



    start=datetime.now()

    print("Begining Boscheri Visulizations")

    df_BOS_sims = pd.read_csv('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_BOS_out/data/GSUA_BOS_Simulations.csv', names= df_sims_label)

    for item in mec_inputs:        # this allows easy injection of labels into chart elements
        input_short_name = item[0]
        input_long_name = item[1]
        input_unit = item[2]
        for item in outputs:
            output_short_name = item[0]
            output_long_name = item[1]
            output_unit = item[2]
            # print(input_short_name, output_short_name)

            """This chart bulding stuff works!"""
            VIS_GSUA = df_BOS_sims[[output_short_name, input_short_name]]
            VIS_GSUA = VIS_GSUA.sort_values(input_short_name, ascending=True)
            x = VIS_GSUA[[input_short_name]].values.flatten()       # the flatten converts the df to a 1D array, needed for trendline
            y = VIS_GSUA[[output_short_name]].values.flatten()      # the flatten converts the df to a 1D array, needed for trendline
            fig, ax = plt.subplots()
            ax.scatter(x, y)
            ax.set_ylabel(f'{output_long_name} ({output_unit})')
            ax.set_xlabel(f'{input_long_name} ({input_unit})')
            plt.title(f'BOS {input_short_name} x {output_short_name}')
            # plt.axhline(y=np.nanmean(y), color='red', linestyle='--', linewidth=3, label='Avg')     # just the straight average of the DTR for all simulations

            # calc the trendline
            z = np.polyfit(x, y, 2) # 1 is linear, 2 is quadratic!
            p = np.poly1d(z)
            plt.plot(x,p(x),"red")

            plt.savefig(f'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/GSUA_BOS_out/figures/BOS {input_short_name} x {output_short_name}.png', bbox_inches='tight') #there are many options for savefig
            # in the likely rare event all of these need to be viewed...
            # plt.show()

    print("Boscheri Visulizations Complete")
    time = datetime.now()-start
    print(f"Charting took {time}")

# Executes this program/function
if __name__ ==('__main__'):
    RUN_CHART()

# def RUN_FULL():
#     print("Running Boscheri Simulations and Charting Functions")
#     start=datetime.now()
#     RUN_SIM()
#     RUN_CHART()
#     time = datetime.now()-start
#     print(f"Full Boscheri run completed. It took {time}")
# # Executes this program/function
# if __name__ ==('__main__'):
#     RUN_FULL()