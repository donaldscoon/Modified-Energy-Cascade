# -*- coding: utf-8 -*-

# reproducing the modified energy cascasde model for SIMoN lettuce production
# as detailed by Cavazzoni (2001), Volk (1995), Monje (1998), and presented in Anderson (2015).

# we're primarily interested in crop growth weight (CGR), total crop biomass, dry (TCB), and total edible biomass (TEB)


# inputs
H = 16 # photoperiod
CO2 = 419.5 # CO_2 level 419.5 ppm
PPF = 200
# define parameters

A_MAX = 0.93 # Eq. 4.15
n = 2.5 
# nominal temperature regimes, planting densities, and photoperiods for the plant growth and transpiration models
H0 = 16 # nominal photoperiod, hours/day
pd = 19.2 # planting density, plants/m^2
T_l = 23 # light cycle temperature, ˚C
T_d = 23 # dark cycle temperature, ˚C
MW_C = 12.01 # molecular weight of carbon, 12.01 g/mol
BCF = 0.40 # biomass carbon fraction


# biomass production model time constants for nominal temperature regime and photoperiod
# from table 4.119

XFRT = 0.95
t_E = 1
#t_Q = n/a
t_M = 30

# canopy closure time, ta, coefficients, lettuce

t_A_c1 = 0;
t_A_c2 = 1.0289*pow(10, 4)
t_A_c3 = -3.7018
t_A_c4 = 0
t_A_c5 = 3.6648 * pow(10, -7)
t_A_c6 = 0
t_A_c7 = 1.7571
t_A_c8 = 0
t_A_c9 = 2.3127 * pow(10, -6)
t_A_c10 = 0
t_A_c11 = 1.8760


PPF_E = PPF*(H/H0) # effective photosynthetic photon flux (umol/(m^2/s))

t_A = t_A_c1*1/PPF_E*1/CO2

# all other coefficients, through ta_c25, are zero.

# Biomass Production Model Constants (Table 4.106)
# Waldmann's Green
CUE_MAX = 0.625
CUE_24 = CUE_MAX
# CUE_MIN = n/a

# CQY_MAX coefficients (Table 4.109) [=] umol C fixed/umol PPF_abs
CQY_c1 = 0
CQY_c2 = 0
CQY_c3 = 0
CQY_c4 = 0
CQY_c5 = 0
CQY_c6 = 0
CQY_c7 = 4.4763*pow(10, -2)
CQY_c8 = 5.163*pow(10, -5)
CQY_c9 = -2.075*pow(10, -8)
CQY_c10 = 0
CQY_c11 = 0
CQY_c12 = -1.1701*pow(10, -5)
CQY_c13 = 0
CQY_c14 = 0
CQY_c15 = 0
CQY_c16 = 0
CQY_c17 = 0
CQY_c18 = -1.9731*pow(10, -11)
CQY_c19 = 8.9265*pow(10, -15)

CQY_MAX = CQY_c7+CQY_c8*CO2+CQY_c9*(CO2**2)+CQY_c12*PPF+CQY_c18*(PPF**2)*CO2+CQY_c19*(PPF**2)*(CO2**2)

CQY = CQY_MAX # no canopy senescence onset, so this is just a constant

# time-dependent equations (Eq. 4.15 and 4.16)
# lettuce doesn't get to "maturity", so CQY = CQY_max

# for each timestep
days = 30
for day in range(days):
    t = day + 1
    A = A_MAX*(t/t_A)**n
    DCG = 0.0036*H*CUE_24*A*CQY*PPF # 
    CGR = MW_C*DCG/BCF # g/(m^2*d)

    print(DCG)
    print(CGR)
# total crop biomass integrates CGR over the full grow
