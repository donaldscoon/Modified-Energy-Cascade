import pandas as pd

##################################################
################## MODEL INPUTS ##################
##################################################
PPFD = 314.54       # found at Amitrano 2020 table 2 but used decimal value in GN excel
CO2 = 370           # value used in Amitranos excel
H = 12              # Amitrano 2020 table 2
T_LIGHT = 24.35105263 # AVG from amitranos GN exp
RH = 0.810470947      # AVG from amitranos GN exp


##################################################
################# INTIALIZATION  #################
##################################################

t = 1               # time in days
res = 1             # model resolution (in days)
i = 0               # matrix/loop counter

##################################################
################ Pull in the data ################
##################################################

ami = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/MEC_AMI_OUT_comp.csv")
bos_tot = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/BOS_CAV_OUT_comp.csv")
bos_avg = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/BOS_CAV_OUT_AVG_comp.csv")
cav = pd.read_csv("C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/MEC_CAV_OUT_comp.csv")

print(ami[['Timestep']])