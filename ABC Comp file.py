import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

##################################################
################## MODEL INPUTS ##################
##################################################
PPFD = 314.54       # found at Amitrano 2020 table 2 but used decimal value in GN excel
CO2 = 370           # value used in Amitranos excel
H = 12              # Amitrano 2020 table 2
T_LIGHT = 24.35105263 # AVG from amitranos GN exp
RH = 0.810470947      # AVG from amitranos GN exp
t = 1               # time in days
res = 1             # model resolution (in days)  boscheri was hourly and totaled or averaged for the day
i = 0               # matrix/loop counter

BCF = 0.40          # Biomass carbon fraction ewert table 4-113
XFRT = 0.95         # edible biomass fraction ewert table 4-112
WBF = XFRT          # Boscheri doesn't define this, I'm assuming that its the same as XFRT
DRY_FR = 6.57/131.35# dry over wet biomass fraction Hanford 2004 Table 4.2.7, with part from wheeler 2003
NC_FR = 0.034       # Hanford 2004 table 4.2.10, ugh boscheri just state the number
OPF = 1.08          # Oxygen production fraction ewert table 4-113
g_A = 2.5           # atmospheric aerodynamic conductance boscheri "for horizontal canopies"
t_D = 1             # 1 for green, 8 for red initial time of development(days) Amirtrano 2020 CQY experiments
t_Mi = 16           # initial time of maturity (days) Amitrano 2020 table 2
t_M = 30            # time at harvest/maturity ewert table 4-112
t_E = 1             # time at onset of organ formation ewert table 4-112
t_Q = 50            # days onset of senescence placeholder value ewert table 4-112
D_PG = 24           # the plants diurnal cycle length assumed 24 in cavazzoni 2001
MW_O2 = 31.9988     # molecular weight of O2 boscheri table 4
MW_CO2 = 44.010     # molecular weight of CO2 boscheri table 4
MWC = 12.0107       # molecular weight of carbon boscheri table 4
MW_W = 18.0153      # Molecular weight of water, boscheri table 4
p_W = 998.23        # density of water at 20 C, ewert table 4-110
n = 2.5             # Ewert table 4-97 crop specific
P_ATM = 101         # atmospheric pressure Number from Amitrano excel
a = 0.0036          # boscheri table 4 similar to others but in 'a'
b = 3600            # boscheri table 4

A_max = 0.93        # maximum fraction of PPF Absorbtion ewert pg 180
CQY_min = 0         # N/A minimum canopy quantum yield ewert table 4-99
CUE_max = 0.625     # maximum carbon use efficiency ewert table 4-99
CUE_min = 0         # N/A minimum carbon use efficiency ewert table 4-99

#################################################
############ SUPPLEMENTAL EQUATIONS #############
#################################################
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


'''#############################################################################
   ############################# AMITRANO MODEL CODE ###########################
   #############################################################################'''
print('Beginning Amitrano Model')

amin_GN = 0.00691867456539118    # amitrano 2020 calibrated with growth chamber experiment exact value from excel
amin_RN = 0.0069915227965273     # amitrano 2020 calibrated with growth chamber experiment exact value from excel
amin_GON = 0.00342717997911672   # amitrano 2020 calibrated with growth chamber experiment exact value from excel
amin_RON = 0.0027368743949879    # amitrano 2020 calibrated with growth chamber experiment exact value from excel

amax_GN = 0.017148682744336      # amitrano 2020 calibrated with growth chamber experiment exact value from excel
amax_RN = 0.0210442078518921     # amitrano 2020 calibrated with growth chamber experiment exact value from excel    
amax_GON = 0.00952341360955465   # amitrano 2020 calibrated with growth chamber experiment exact value from excel
amax_RON = 0.0108277387986636    # amitrano 2020 calibrated with growth chamber experiment exact value from excel

bmin_GN = 0                      # amitrano 2020 calibrated with growth chamber experiment exact value from excel
bmin_RN = 0.0220120589922702     # amitrano 2020 calibrated with growth chamber experiment exact value from excel
bmin_GON = 0.0486455477321762    # amitrano 2020 calibrated with growth chamber experiment exact value from excel
bmin_RON = 0.0361034591767831    # amitrano 2020 calibrated with growth chamber experiment exact value from excel

bmax_GN = 0.0451765692503675     # amitrano 2020 calibrated with growth chamber experiment exact value from excel
bmax_RN = 0.0284636898862895     # amitrano 2020 calibrated with growth chamber experiment exact value from excel
bmax_GON = 0.0564626043274799    # amitrano 2020 calibrated with growth chamber experiment exact value from excel
bmax_RON = 0.0598757705974144    # amitrano 2020 calibrated with growth chamber experiment exact value from excel

df_AMI_records = pd.DataFrame({})

ts_to_harvest = int(t_M/res)             # calcs the timesteps needed to set up the matrix for each ts
TEB = 8.53                               # this is the only way I could make it match excel WHERE IT FROM??
edible_mat = np.zeros(ts_to_harvest+1)   # matrix for TEB storage
day = 0

while t <= ts_to_harvest:                  # while time is less than harvest time
    if t<= t_D:                            # if timestep is before formation of edible organs
        alpha = amin_GN                    # amitrano 2020 eq 15
        beta = bmin_GN                     # amitrano 2020 eq 15
    elif t <= t_Mi:                        # if timestep is after organ formation but before maturity
        alpha = amin_GN+(amax_GN-amin_GN)*(t-t_D)/(t_Mi-t_D)        # amitrano 2020 eq 15
        beta = bmin_GN+(bmax_GN-bmin_GN)*(t-t_D)/(t_Mi-t_D)         # amitrano 2020 eq 15
    else:                                  # all other timesteps
        alpha = amax_GN                    # amitrano 2020 eq 15
        beta = bmax_GN                     # amitrano 2020 eq 15
    DCG = 0.0036*H*alpha*PPFD              # amitrano 2020 eq 4
    DOP = OPF*DCG                          # amitrano 2020 eq 5
    CGR = MWC*DCG/BCF                      # amitrano 2020 eq 6
    if t > t_E:                            # if edible organ formation has begun
        TEB = CGR+TEB                      # Amitrano 2020 GN excel column I
    edible_mat[i] = TEB                    # matrix that stores past values of TEB
    P_GROSS = beta*PPFD                    # amitrano 2020 eq 8
    VP_SAT = 0.611*np.exp(1)**(17.4*T_LIGHT/(T_LIGHT+239)) # Same as ewert and cavazzoni, though likely from Monje 1998
    VP_AIR = VP_SAT*RH                     # Same as ewert and cavazzoni, though likely from Monje 1998
    VPD = VP_SAT*(1-RH)                    # Same as ewert and cavazzoni, though likely from Monje 1998
    P_NET = (H*alpha/24+beta*(24-H)/24)*PPFD    # Amitrano 2020 eq 9
    g_S = ((1.717*T_LIGHT)-19.96-(10.54*VPD))*(P_NET/CO2) # Amitrano 2020 eq 10 (with some nice parenthesis that don't change anything)
    g_C = g_A*g_S/(g_A+g_S)                # Amitrano 2020 eq 10
    DTR = 3600*H*(MW_W/p_W)*g_C*(VPD/P_ATM)

    dfts = pd.DataFrame({
        'AMI_Timestep': [t],
        'Day': [day],
        'AMI_Photoperiod': [H],
        'AMI_PPFD': [PPFD],
        'AMI_alpha': [alpha],
        'AMI_beta': [beta],
        'AMI_DCG': [DCG],
        'AMI_DOP': [DOP],
        'AMI_CGR': [CGR],
        'AMI_TEB': [TEB],
        'AMI_P_GROSS': [P_GROSS],
        'AMI_P_NET': [P_NET],
        'AMI_T_LIGHT': [T_LIGHT],
        'AMI_VP_SAT': [VP_SAT],
        'AMI_VP_AIR': [VP_AIR],
        'AMI_RH': [RH],
        'AMI_VPD': [VPD], 
        'AMI_g_S': [g_S],
        'AMI_g_C': [g_C],
        'AMI_DTR': [DTR],
        'AMI_g_A': [g_A]
    }) # creates a dataframe of all variables/outputs for each timestep. 
    df_AMI_records = pd.concat([df_AMI_records, dfts], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
    t += res                         # advance timestep
    day += 1
    i += 1                           # increase matrix index counter

df_AMI_records.to_csv('C:/Users/donal/Documents/Github/Modified-Energy-Cascade/MEC_AMI_OUT_comp.csv') # exports final data frame to a CSV
print('Exported Amitrano Data')

'''#############################################################################
   ############################ CAVAZZONI MODEL CODE ###########################
   ############################################################################'''

print('Beginning Cavazzoni Model')

##################################################
################# INTIALIZATION  #################
##################################################
t = 0               # time in days
res = 1             # model resolution (in days)
i = 0               # matrix/loop counter

##################################################
################ Data Management #################
##################################################
df_CAV_records = pd.DataFrame({})

"""These matrices may need to become obsolete with
   the new dataframes I'm about to introduce. :) """
ts_to_harvest = int(t_M/res)             # calcs the timesteps needed to set up the matrix for each ts
matrix = range(ts_to_harvest) + np.ones(ts_to_harvest)      # only works with whole numbers of ts_to_harvest
TCB = 0                                 # starting crop biomass
Biomass_mat = np.zeros(ts_to_harvest)             # matrix for TCB storage
TEB = 0                                 # starting total edible biomass
edible_mat = np.zeros(ts_to_harvest)              # matrix for TEB storage

#################################################
################ THE MODEL LOOP #################
#################################################
day = 0
while t < ts_to_harvest:                 # while time is less than harvest time
    if t < t_A:                  # before canopy closure
        A = A_max*(t/t_A)**n         # Ewert eq 4-14
    else:                        # after canopy closure
        A = A_max                    # Ewert eq 4-14
    if t<= t_Q:                  # before onset of senescence
        CQY = CQY_max                # ewert eq 4-15
        CUE_24 = CUE_max             # ewert eq 4-16
    else: 
        """For lettuce the values of CQY_min and CUE_min 
        are n/a due to the assumption that the canopy does
        not senesce before harvest. I coded them anyways, it
        makes it complete for all the other crops too. For 
        crops other than lettuce remove the break statement."""
        CQY = CQY_max - (CQY_max - CQY_min)*((t-t_Q)/(t_M-t_Q)) # ewert eq 4-15
        CUE_24 = CUE_max - (CUE_max - CUE_min)*((t-t_Q)/(t_M-t_Q)) #ewert eq 4-16
        print("Error: Utilizing CQY and CUE values without definitions")
        break
    ALPHA = A*CQY*CUE_24
    BETA = A*CQY
    DCG = 0.0036*H*CUE_24*A*CQY*PPFD # ewert eq 4-17 number is related to seconds in an hour
    DOP = OPF*DCG                    # ewert eq 4-18
    CGR = 12.01*(DCG/BCF)            # ewert eq 4-19 number is molecular weight of carbon
    TCB += CGR                       # ewert eq 4-20
    if t > t_E:                      # accumilate edible biomass when organ formation begins
        TEB += XFRT*CGR              # ewert eq 4-21
    Biomass_mat[i] = TCB             # matrix that stores past values of TCB
    '''^^^^this will probably be fixed by making t divisable by dt^^^^'''
    '''now it works more, but only if the it results in a whole number'''
    edible_mat[i] = TEB
    VP_SAT = 0.611*np.exp(1)**((17.4*T_LIGHT)/(T_LIGHT+239)) # assumes leaf tempp=air temp. Saturated Vapor Pressure. ewert eq 4-23 numbers likely from Monje 1998
    VP_AIR = VP_SAT*RH               # Atmo Vapor Pressure ewewrt eq 4-23
    VPD = VP_SAT - VP_AIR            # Vapor Pressure Deficit ewert eq 4-23
    P_GROSS = A*CQY*PPFD             # Gross photosynthesis ewert eq 4-24
    P_NET = (((D_PG-H)/D_PG)+((H*CUE_24)/D_PG))*P_GROSS     # Net Photosynthesis ewert eq 4-25
    g_S = (1.717*T_LIGHT-19.96-10.54*VPD)*(P_NET/CO2)        # stomatal conductance the numbers came from monje 1998, only for planophile canopies equation from ewert 4-27
    g_C = (g_A*g_S)/(g_A+g_S)                               # canopy conductance ewert 4-26
    DTR = 3600*H*(MW_W/p_W)*g_C*(VPD/P_ATM)
    dfts = pd.DataFrame({
        'CAV_Timestep': [t],
        'Day': [day],
        'CAV_ALPHA': [ALPHA],
        'CAV_BETA': [BETA],
        'CAV_A': [A],
        'CAV_CQY': [CQY],
        'CAV_CUE_24': [CUE_24],
        'CAV_DCG': [DCG],
        'CAV_CGR': [CGR],
        'CAV_TCB': [TCB],
        'CAV_TEB': [TEB],
        'CAV_VP_SAT': [VP_SAT],
        'CAV_VP_AIR': [VP_AIR],
        'CAV_VPD': [VPD],
        'CAV_P_GROSS': [P_GROSS],
        'CAV_P_NET': [P_NET],
        'CAV_g_S': [g_S],
        'CAV_g_A': [g_A],
        'CAV_g_C': [g_C],
        'CAV_DTR': [DTR],
        'CAV_T_LIGHT': [T_LIGHT],
        'CAV_RH': [RH],
        'CAV_CO2': [CO2]
    }) # creates a dataframe of all variables/outputs for each timestep. 
    df_CAV_records = pd.concat([df_CAV_records, dfts], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
    t += res                          # advance timestep
    day += 1
    i += 1                           # increase matrix index counter

df_CAV_records.to_csv('C:/Users/donal/Documents/Github/Modified-Energy-Cascade/MEC_CAV_OUT_comp.csv') # exports final data frame to a CSV
print('Exported Cavazzoni Data')

'''#############################################################################
   ############################# BOSCHERI MODEL CODE ###########################
   #############################################################################'''

print('Beginning Boscheri Model')

##################################################
################# INTIALIZATION  #################
##################################################
t = 0                       # time in days
res = 1                     # model resolution 1 hour
i = 0                       # matrix/loop counter
I = 0                       # boscheri "I is equal to 1 and 0 during the photoperiod (day) and dark period (night)"
night_len = 24 - H          # length of night
day_len = 24 - night_len    # length of day
pp_count = 0                # photoperiod counter
day = 0

##################################################
################ Data Management #################
##################################################
df_BOS_TOT_records = pd.DataFrame({})
df_BOS_AVG_records = pd.DataFrame({})

"""These matrices may need to become obsolete with
   the new dataframes I'm about to introduce. :) """
ts_to_harvest = int(t_M*24/res)             # calcs the timesteps needed to set up the matrix for each ts
matrix = range(ts_to_harvest) + np.ones(ts_to_harvest)      # only works with whole numbers of ts_to_harvest
TCB = 0                                 # starting crop biomass
Biomass_mat = np.zeros(ts_to_harvest)             # matrix for TCB storage
TEB = 0                                 # starting total edible biomass
edible_mat = np.zeros(ts_to_harvest)              # matrix for TEB storage

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
    HTR = b*MW_W*g_C*(VPD/P_ATM)    # boscheir eq 10
    HCO2C = HOP*MW_CO2*MW_O2**(-1)  # boscheri eq 14
    HCO2P = HOC*MW_CO2*MW_O2**(-1)  # boscheri eq 15 
    HNC = HCGR*DRY_FR*NC_FR         # boscheri eq unlabeled
    HWC = HTR+HOP+HCO2P+HWCGR-HOC-HCO2C-HNC # boscheri eq 16

    dfts_AVG = pd.DataFrame({
        'BOS_AVG_Timestep': [t],
        'Day': [day],
        'BOS_AVG_diurnal': [I],
        'BOS_AVG_ALPHA': [ALPHA],
        'BOS_AVG_BETA': [BETA],
        'BOS_AVG_A': [A],
        'BOS_AVG_CQY': [CQY],
        'BOS_AVG_CUE_24': [CUE_24],
        'BOS_AVG_DCG': [HCG],
        'BOS_AVG_g_S': [g_S],
        'BOS_AVG_g_C': [g_C],
        'BOS_AVG_P_NET': [P_NET],
        'BOS_AVG_DCGR': [HCGR],
        'BOS_AVG_DWCGR': [HWCGR],
        'BOS_AVG_DOP': [HOP],
        'BOS_AVG_DOC': [HOC],
        'BOS_AVG_DTR': [HTR],
        'BOS_AVG_DCO2C': [HCO2C],
        'BOS_AVG_DCO2P': [HCO2P],
        'BOS_AVG_DNC': [HNC], 
        'BOS_AVG_DWC': [HWC],
        }) # creates a dataframe of all variables/outputs for each timestep. 
    
    dfts_TOT = pd.DataFrame({
        'BOS_TOT_Timestep': [t],
        'Day': [day],
        'BOS_TOT_diurnal': [I],
        'BOS_TOT_ALPHA': [ALPHA],
        'BOS_TOT_BETA': [BETA],
        'BOS_TOT_A': [A],
        'BOS_TOT_CQY': [CQY],
        'BOS_TOT_CUE_24': [CUE_24],
        'BOS_TOT_DCG': [HCG],
        'BOS_TOT_g_S': [g_S],
        'BOS_TOT_g_C': [g_C],
        'BOS_TOT_P_NET': [P_NET],
        'BOS_TOT_DCGR': [HCGR],
        'BOS_TOT_DWCGR': [HWCGR],
        'BOS_TOT_DOP': [HOP],
        'BOS_TOT_DOC': [HOC],
        'BOS_TOT_DTR': [HTR],
        'BOS_TOT_DCO2C': [HCO2C],
        'BOS_TOT_DCO2P': [HCO2P],
        'BOS_TOT_DNC': [HNC], 
        'BOS_TOT_DWC': [HWC],
        }) # creates a dataframe of all variables/outputs for each timestep.
    df_BOS_TOT_records = pd.concat([df_BOS_TOT_records, dfts_TOT], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
    df_BOS_AVG_records = pd.concat([df_BOS_AVG_records, dfts_AVG], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
    df_day_TOT = df_BOS_TOT_records.groupby(['Day']).sum()
    df_day_AVG = df_BOS_AVG_records.groupby(['Day']).mean()
    t += res                          # advance timestep
    i += 1                           # increase matrix index counter
    pp_count += 1                    # photoperiod counter + 1
df_day_TOT.to_csv('C:/Users/donal/Documents/Github/Modified-Energy-Cascade/BOS_OUT_TOT_comp.csv') # exports final data frame to a CSV
df_day_AVG.to_csv('C:/Users/donal/Documents/Github/Modified-Energy-Cascade/BOS_OUT_AVG_comp.csv') # exports final data frame to a CSV
print('Exported Boscheri Data')

'''#############################################################################
   ############################# COMPARISON CODE ###############################
   #############################################################################'''

print('Beginning Comparisons')
##################################################
################ Pull in the data ################
##################################################

ami =     pd.read_csv("C:/Users/donal/Documents/Github/Modified-Energy-Cascade/MEC_AMI_OUT_comp.csv")
bos_tot = pd.read_csv("C:/Users/donal/Documents/Github/Modified-Energy-Cascade/BOS_OUT_TOT_comp.csv")
bos_avg = pd.read_csv("C:/Users/donal/Documents/Github/Modified-Energy-Cascade/BOS_OUT_AVG_comp.csv")
cav =     pd.read_csv("C:/Users/donal/Documents/Github/Modified-Energy-Cascade/MEC_CAV_OUT_comp.csv")
print('Data Imported')
bigdf =   pd.merge(pd.merge(pd.merge(bos_avg, bos_tot, on='Day'), ami, on='Day'), cav, on='Day')
bigdf.to_csv('C:/Users/donal/Documents/Github/Modified-Energy-Cascade/ABC_comp.csv') # exports final data frame to a CSV
# print(bigdf)
print('Dataframes Merged')

''' AMI= green colors or 'o'
     BOS= blue colors or 's'
     CAV= yelllow colors or '^'  '''
# ##################################################
# ###############   Start Charting  ################
# ##################################################

####### Alpha and Beta Comparison ##############
fig, ax = plt.subplots()
ax.plot(bigdf['Day'], bigdf['AMI_alpha'],       marker='o', color='lightgreen',     label='AMI α')
ax.plot(bigdf['Day'], bigdf['AMI_beta'],        marker='o', color='green',          label='AMI β')
ax.plot(bigdf['Day'], bigdf['BOS_AVG_ALPHA'],   marker='s', color='lightblue',      label='BOS α')
ax.plot(bigdf['Day'], bigdf['BOS_AVG_BETA'],    marker='s', color='blue',           label='BOS β')
ax.plot(bigdf['Day'], bigdf['CAV_ALPHA'],       marker='^', color='gold',           label='CAV α')
ax.plot(bigdf['Day'], bigdf['CAV_BETA'],        marker='^', color='goldenrod',      label='CAV β')
ax.set_ylabel('Unsure about units')
ax.set_xlabel('Days After Emergence')
plt.figlegend(bbox_to_anchor=(-0.21, 0.39, 0.5, 0.5))
plt.title('Alpha and Beta Comparison')
plt.savefig('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/Comparison Charts/Alpha_Beta_Comparison.png') #there are many options for savefig
plt.show()


###################### A, CQY, CUE, ###################################
fig, ax = plt.subplots()
ax.plot(bigdf['Day'], bigdf['BOS_AVG_A'],      marker='s', color='lightblue',  label='BOS A')
ax.plot(bigdf['Day'], bigdf['CAV_A'],          marker='^', color='gold',       label='CAV A')
ax.plot(bigdf['Day'], bigdf['BOS_AVG_CUE_24'], marker='s', color='blue',       label='BOS CUE')
ax.plot(bigdf['Day'], bigdf['CAV_CUE_24'],     marker='^', color='goldenrod',  label='CAV CUE')
ax.set_ylabel('Fractional')
ax2 = ax.twinx()
ax2.plot(bigdf['Day'], bigdf['BOS_AVG_CQY'],    marker='s', color='lightcoral',label='BOS CQY')
ax2.plot(bigdf['Day'], bigdf['CAV_CQY'],        marker='^', color='indianred',  label='CAV CQY')
ax2.set_facecolor('darkred')
ax2.set_ylabel('μmol$_{Carbon}$ μmol$_{Photon}^{-1}$', color='darkred')
ax2.tick_params(axis='y',labelcolor='darkred')
ax.set_xlabel('Days After Emergence')
plt.figlegend(bbox_to_anchor=(0.40, -0.1, 0.5, 0.5))
plt.title('A CUE CQY Comparison')
plt.savefig('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/Comparison Charts/A_CUE_CQY_Comparison.png', bbox_inches='tight') #there are many options for savefig
plt.show()

########## Conductances #########################
fig, ax = plt.subplots()
ax.plot(bigdf['Day'], bigdf['AMI_g_S'],     marker='o', color='green',      label='AMI g$_S$')
ax.plot(bigdf['Day'], bigdf['AMI_g_C'],     marker='o', color='lightgreen', label='AMI g$_C$')
ax.plot(bigdf['Day'], bigdf['BOS_AVG_g_S'], marker='s', color='blue',       label='BOS g$_S$')
ax.plot(bigdf['Day'], bigdf['BOS_AVG_g_C'], marker='s', color='lightblue',  label='BOS g$_C$')
ax.plot(bigdf['Day'], bigdf['CAV_g_S'],     marker='^', color='goldenrod',  label='CAV g$_S$')
ax.plot(bigdf['Day'], bigdf['CAV_g_C'],     marker='^', color='gold',       label='CAV g$_C$')
ax.set_ylabel('mol$_{water}$ m$^{-2}$ second $^{-1}$')
ax.set_xlabel('Days After Emergence')
plt.figlegend(bbox_to_anchor=(-0.185, 0.39, 0.5, 0.5))
plt.title('Conductances')
plt.savefig('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/Comparison Charts/Conductances_Comparison.png') #there are many options for savefig
plt.show()

################### Gas Exchanges ######################
fig, ax= plt.subplots()
ax.plot(bigdf['Day'], bigdf['AMI_DTR'],     marker='o', color='green',      label='AMI DTR')
ax.plot(bigdf['Day'], bigdf['BOS_TOT_DTR'], marker='s', color='blue',       label='BOS DTR')
ax.plot(bigdf['Day'], bigdf['CAV_DTR'],     marker='^', color='goldenrod',  label='CAV DTR')
ax.set_ylabel('L$_{water}$ m$^{-2}$ day$^{-1}$')
ax.set_xlabel('Days After Emergence')
plt.figlegend(bbox_to_anchor=(-0.185, 0.39, 0.5, 0.5))
plt.title('Gas Exchanges')
plt.savefig('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/Comparison Charts/Gas_Exchange_Comparison.png') #there are many options for savefig
plt.show()


################## Photosynthesis #####################
fig, ax = plt.subplots()
ax.plot(bigdf['Day'], bigdf['AMI_P_GROSS'],     marker='o', color='green',      label='AMI P$_{GROSS}$')
ax.plot(bigdf['Day'], bigdf['AMI_P_NET'],       marker='o', color='lightgreen', label='AMI P$_{NET}$')
ax.plot(bigdf['Day'], bigdf['BOS_AVG_P_NET'],   marker='s', color='lightblue',  label='BOS P$_{NET}$')
ax.plot(bigdf['Day'], bigdf['CAV_P_GROSS'],     marker='^', color='goldenrod',  label='CAV P$_{GROSS}$')
ax.plot(bigdf['Day'], bigdf['CAV_P_NET'],       marker='^', color='gold',       label='CAV P$_{NET}$')
ax.set_ylabel('μmol$_{Carbon}$ m$^{-2}$ second$^{-1}$')
ax.set_xlabel('Days After Emergence')
plt.figlegend(bbox_to_anchor=(-0.16, 0.39, 0.5, 0.5))
plt.title('Photosynthesis')
plt.savefig('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/Comparison Charts/Photosynthesis_Comparison.png') #there are many options for savefig
plt.show()

##################### Daily Carbon Gain ###################################
fig, ax = plt.subplots()
ax.plot(bigdf['Day'], bigdf['AMI_DCG'],      marker='o', color='green',      label='AMI DCG')
ax.plot(bigdf['Day'], bigdf['BOS_TOT_DCG'],  marker='s', color='blue',       label='BOS DCG')
ax.plot(bigdf['Day'], bigdf['CAV_DCG'],      marker='^', color='goldenrod',  label='CAV DCG')
ax.set_xlabel('Days After Emergence')
ax.set_ylabel('mol$_{Carbon}$ m$^{-2}$ day$^{-1}$')
plt.figlegend(bbox_to_anchor=(-0.18, 0.39, 0.5, 0.5))
plt.title('Daily Carbon Gain')
plt.savefig('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/Comparison Charts/DCG_Comparison.png') #there are many options for savefig
plt.show()

##################### Crop Productivity ###################################
fig, ax = plt.subplots()
ax.plot(bigdf['Day'], bigdf['AMI_TEB'],      marker='o', color='darkgreen',  label='AMI TEB')
ax.plot(bigdf['Day'], bigdf['CAV_TEB'],      marker='^', color='green',      label='CAV TEB')
ax.plot(bigdf['Day'], bigdf['CAV_TCB'],      marker='^', color='lightgreen', label='CAV TCB')
ax.set_ylabel('grams m$^{-2}$', color='green')
ax.tick_params(axis='y', labelcolor='green')
ax2 = ax.twinx()
ax2.plot(bigdf['Day'], bigdf['AMI_CGR'],      marker='o', color='lightcoral',     label='AMI CGR')
ax2.plot(bigdf['Day'], bigdf['BOS_TOT_DCGR'], marker='s', color='salmon',  label='BOS CGR')
ax2.plot(bigdf['Day'], bigdf['CAV_CGR'],      marker='^', color='indianred', label='CAV CGR')
ax2.set_ylabel('grams m$^{-2}$ day$^{-1}$', color='darkred')
ax2.tick_params(axis='y',labelcolor='darkred')
ax.set_xlabel('Days After Emergence')
plt.figlegend(bbox_to_anchor=(-0.18, 0.39, 0.5, 0.5))
plt.title('Crop Productivity')
plt.savefig('C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/Comparison Charts/Crop_Productivity_Comparison.png') #there are many options for savefig
plt.show()

