"""
##################################################################################
This is an important function that defines the problem statement, the model names,
input names, and output names for consistency throughout the code.
##################################################################################
"""

from SALib import ProblemSpec

def prob_spec():
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
              'triang'],            # Photoperiod
    'outputs': ['Y']
    })
    return sp

# Executes this program/function
if __name__ ==('__main__'):
    prob_spec()


def model_names():          # Iterates through the model names
    models = [
            ["AMI", "Amitrano"], 
            ["BOS", "Boscheri"], 
            ["CAV", "Cavazzoni"]
            ]
    return models

# Executes this program/function
if __name__ ==('__main__'):
    model_names()

def mec_input_names():      # Iterates through the input names
    u = "\u00B5"        # unicode for the micro symbol
    mec_inputs = [
                ["T_LIGHT", "Light Cycle Temperature", "Degrees Celsius"],
                ["T_DARK", "Dark Cycle Temperature", "Degrees Celsius"],
                ["RH", "Relative Humidity", "%"],
                ["CO2", "CO$_{2}$ Concentration", u+"mol$_{carbon}$ mol$_{air}$"],
                ["PPFD", "Photosynthetic Photon Flux", u+"mol$_{photons}$ m$^{-2}$ second$^{-1}$"],
                ["H", "Photoperiod", "hours day$^{-1}$"]
    ]
    return mec_inputs

# Executes this program/function
if __name__ ==('__main__'):
    mec_input_names()


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
        ["DTR", "Daily Tranpiration Rate", "L$_{water}$ m$^{-2}$ day$^{-1}$"]
        ]
    return outputs

# Executes this program/function
if __name__ ==('__main__'):
    mec_output_names()


def colors(): # combines all these functions into one!
    # Model, dark color, light color, med/bright color, marker
    colors = [['AMI', '#2A119B', '#A798EC', '#5E46C6', 'o'],     # blues
              ['BOS', '#2A119B', '#96F391', '#09B600', 's'],     # greens
              ['CAV', '#2A119B', '#FE989A', '#DF0006', '^']]    # reds

# Executes this program/function
if __name__ ==('__main__'):
    all_names()