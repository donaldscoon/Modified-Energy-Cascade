"""
##################################################################################
This is an important function that defines the problem statement, the model names,
input names, and output names for consistency throughout the code.
##################################################################################
"""

from SALib import ProblemSpec

def prob_spec(GSUA_type):
    if GSUA_type == 'Individual': # Sampling procedure for the Structure GSUA
        sp = ProblemSpec({
        'names': ['TEMP', 'RH', 'CO2', 'PPFD', 'H'],
        'num_vars': 5,
        # NORMAL Notation [Average, Standard Deviation]
        # TRIANGLE Notation [min, max, peak as % of that range]
        # for example, with  Temp the range is 35. 54.286% of that would equal 19, 
        # which would actually give a peak at 24 since the range starts at 5.
        'bounds': [[21.20, 0.30],    # Temperature Average, SD 
                [72.14, 8.13],    # Relative Humidity Average, SD 
                [767.74, 90.98],  # Atmo CO2 Concentration Average, SD 
                [236.95, 13.47],  # PPFD Level Average, SD 
                [10,22, 0.5]],    # Photoperiod Peak at 16 +- 6 hours
        'dists': ['norm',             # Temperature
                'norm',             # Relative Humidity
                'norm',             # Atmo CO2
                'norm',             # PPFD
                'triang'],          # Photoperiod
        'outputs': ['Y']
        })

    elif GSUA_type == 'Structure': # Sampling procedure for the Structure GSUA
        sp = ProblemSpec({
            'names': ['TEMP', 'RH', 'CO2', 'PPFD', 'H', 'STRU'],
            'num_vars': 6,
            'bounds': [[21.20, 0.30],    # Temperature Average, SD 
                    [72.14, 8.13],    # Relative Humidity Average, SD 
                    [767.74, 90.98],  # Atmo CO2 Concentration Average, SD 
                    [236.95, 13.47],  # PPFD Level Average, SD 
                    [10,22, 0.5],     # Photoperiod Peak at 16 +- 6 hours
                    [0.5,3.5]],           # Model structure, AMI, BOS, CAV, uniform distri
            'dists': ['norm',             # Temperature
                    'norm',             # Relative Humidity
                    'norm',             # Atmo CO2
                    'norm',             # PPFD
                    'triang',             # Photoperiod
                    'unif'],              # Model Structure
            'outputs': ['Y']
            })

    return sp


def path_names():
    ##### HOME PATHS
    gen_path = 'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/2^12-GSUA-3/'
    indiv_path = 'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/2^12-GSUA-3/Final-Indiv/'
    structure_path = 'C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/GSUA/2^12-GSUA-3/Final-Structure/'


    # # ###### SCHOOL PATHS
    # gen_path = 'C:/Users/dcoon/Documents/GitHub/Modified-Energy-Cascade/GSUA/2^12-GSUA-3/'
    # indiv_path = 'C:/Users/dcoon/Documents/GitHub/Modified-Energy-Cascade/GSUA/2^12-GSUA-3/Final-Indiv/'
    # structure_path = 'C:/Users/dcoon/Documents/GitHub/Modified-Energy-Cascade/GSUA/2^12-GSUA-3/Final-Structure/'


    return gen_path, indiv_path, structure_path


def model_names():          # Iterates through the model names
    models = [
            ["AMI", "Amitrano"], 
            ["BOS", "Boscheri"], 
            ["CAV", "Cavazzoni"]
            ]
    return models

def mec_input_names(GSUA_type):      # Iterates through the input names
    u = "\u00B5"        # unicode for the micro symbol
    if GSUA_type == 'Individual':
        mec_inputs = [
                    ["T_LIGHT", "Light Cycle Temperature", "Degrees Celsius"],
                    ["T_DARK", "Dark Cycle Temperature", "Degrees Celsius"],
                    ["RH", "Relative Humidity", "%"],
                    ["CO2", "CO$_{2}$ Concentration", u+"mol$_{carbon}$ mol$_{air}$"],
                    ["PPFD", "Photosynthetic Photon Flux", u+"mol$_{photons}$ m$^{-2}$ second$^{-1}$"],
                    ["H", "Photoperiod", "hours day$^{-1}$"]
                    ]

    elif GSUA_type == 'Structure':
        mec_inputs = [
                ["TEMP", "Light Cycle Temperature", "Degrees Celsius"],
                ["RH", "Relative Humidity", "%"],
                ["CO2", "CO$_{2}$ Concentration", u+"mol$_{carbon}$ mol$_{air}$"],
                ["PPFD", "Photosynthetic Photon Flux", u+"mol$_{photons}$ m$^{-2}$ second$^{-1}$"],
                ["H", "Photoperiod", "hours day$^{-1}$"],
                ["STRU", "Structure", ""]
                ]

    return mec_inputs

def mec_output_names():     # Iterates through the output names
    u = "\u00B5"        # unicode for the micro symbol
    outputs = [  
        ["A", "Absorption", ""],
        ["CQY", "Canopy Quantum Yield", u+"mol$_{fixed}$ "+u+"mol$_{aborbed}$"],
        ["CUE_24", "Carbon Use Efficiency", ""],
        ["ALPHA", "A*CQY*CUE_24", ""],
        ["BETA", "A*CQY", ""],
        ["DCG", "Daily Carbon Gain", "mol$_{carbon}$ m$^{-2}$ day$^{-1}$"],
        ["CGR", "Crop Growth Rate", "grams m$^{-2}$ day$^{-1}$"],
        ["TCB", "Total Crop Biomass", "grams m$^{-2}$"],
        ["TEB", "Total Edible Biomass", "grams m$^{-2}$"],
        ["VP_SAT", "Saturated Moisture Vapor Pressure", "kPa"],
        ["VP_AIR", "Actual Moisture Vapor Pressure", "kPa"],
        ["VPD", "Vapor Pressure Deficit", "kPa"],
        ["P_GROSS", "Gross Canopy Photosynthesis", u+"mol$_{carbon}$ m$^{-2}$ second$^{-1}$"],
        ["P_NET", "Net Canopy Photosynthesis", u+"mol$_{carbon}$ m$^{-2}$ second$^{-1}$"],
        ["g_S", "Stomatal Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$"],
        ["g_A", "Atmospheric Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$"],
        ["g_C", "Canopy Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$"],
        ["DTR", "Daily Transpiration Rate", "L$_{water}$ m$^{-2}$ day$^{-1}$"]
        ]
    return outputs

def colors(): # combines all these functions into one!
    # Model, dark color, light color, med/bright color, marker
    colors = [['AMI', '#2A119B', '#A798EC', '#5E46C6', 'o'],     # blues
              ['BOS', '#067300', '#96F391', '#09B600', 's'],     # greens
              ['CAV', '#8C0004', '#FE989A', '#DF0006', '^']]    # reds

def df_labels(GSUA_type):
    if GSUA_type =='Individual':
        df_AMI_sims_label = ['SIM_NUM','Timestep','skip?', 'H','A','ALPHA','BETA','CQY','CUE_24',
                            'DCG','CGR','TCB','TEB','DOP','VP_SAT','VP_AIR','VPD','P_GROSS',
                            'P_NET','g_S','g_A','g_C','DTR','T_LIGHT','T_DARK','RH','CO2','PPFD', 'STRU']

        df_BOS_sims_label = ['SIM_NUM','Timestep','H','Diurnal', 'A','ALPHA','BETA','CQY',
                            'CUE_24','DCG','CGR','DWCGR','TCB','TEB',
                            'VP_SAT','VP_AIR','VPD','P_NET','P_GROSS',
                            'DOP','DOC','g_S','g_A','g_C','DTR',
                            'DCO2C','DCO2P','DNC', 'DWC','T_LIGHT',
                            'T_DARK','RH','CO2','PPFD', 'STRU']

        df_CAV_sims_label = ['SIM_NUM','Timestep','H','A','ALPHA','BETA','CQY','CUE_24','DCG',
                            'CGR','TCB','TEB','DOP','VP_SAT','VP_AIR','VPD','P_GROSS',
                            'P_NET','g_S','g_A','g_C','DTR','T_LIGHT','T_DARK','RH','CO2','PPFD', 'STRU']

    elif GSUA_type == 'Structure':
        df_AMI_sims_label = ['Timestep','skip?','SIM_NUM', 'H','A','ALPHA','BETA','CQY','CUE_24',
                            'DCG','CGR','TCB','TEB','DOP','VP_SAT','VP_AIR','VPD','P_GROSS',
                            'P_NET','g_S','g_A','g_C','DTR','TEMP','T_DARK','RH','CO2','PPFD', 'STRU']

        df_BOS_sims_label = ['SIM_NUM','Timestep','H','Diurnal', 'A','ALPHA','BETA','CQY',
                            'CUE_24','DCG','CGR','DWCGR','TCB','TEB',
                            'VP_SAT','VP_AIR','VPD','P_NET','P_GROSS',
                            'DOP','DOC','g_S','g_A','g_C','DTR',
                            'DCO2C','DCO2P','DNC', 'DWC','TEMP',
                            'T_DARK','RH','CO2','PPFD', 'STRU']

        df_CAV_sims_label = ['SIM_NUM','Timestep','H','A','ALPHA','BETA','CQY','CUE_24','DCG',
                            'CGR','TCB','TEB','DOP','VP_SAT','VP_AIR','VPD','P_GROSS',
                            'P_NET','g_S','g_A','g_C','DTR','TEMP','T_DARK','RH','CO2','PPFD', 'STRU']

    return df_AMI_sims_label, df_BOS_sims_label, df_CAV_sims_label

def conf_bars():
    elinewidth = .75
    capsize = 2
    capthick = .75

    return elinewidth, capsize, capthick