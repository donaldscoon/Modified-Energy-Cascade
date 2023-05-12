
PPFD = 314.54          # umol/m^2/sec, Amitrano 2020 Table 2
CO2 = 419.5         # umol CO2 / mol air, no reference value given 


gen_coef = [
    (1/PPFD)*(1/CO2) , (1/PPFD) , (CO2/PPFD)   , (CO2**2/PPFD)     , (CO2**3/PPFD)     ,
    (1/CO2)          , 1        , CO2          , (CO2**2)          , (CO2**3)          ,
    PPFD*(1/CO2)     , PPFD     , PPFD*CO2     , PPFD*(CO2**2)     , PPFD*(CO2**3)     ,
    (PPFD**2)*(1/CO2), (PPFD**2), (PPFD**2)*CO2, (PPFD**2)*(CO2**2), (PPFD**2)*(CO2**3),
    (PPFD**3)*(1/CO2), (PPFD**3), (PPFD**3)*CO2, (PPFD**3)*(CO2**2), (PPFD**3)*(CO2**3),
]

t_A_coef = [
    0     , 1.0289*(10**4), -3.7018, 0              , 3.6648*(10**-7),
    0     , 1.7571        , 0      , 2.3127*(10**-6), 0              ,
    1.8760, 0             , 0      , 0              , 0              ,
    0     , 0             , 0      , 0              , 0              ,
    0     , 0             , 0      , 0              , 0
]

""" Canopy Quantum Yield Equation """
# CQY_max Coefficients ewert table 4-102
CQY_max_coef = [
0, 0               , 0                , 0               , 0,
0, 4.4763*(10**-2) , 5.163*(10**-5)   , -2.075*(10**-8) , 0,
0, -1.1701*(10**-5), 0                , 0               , 0,
0, 0               , -1.9731*(10**-11), 8.9265*(10**-15), 0,
0, 0               , 0                , 0               , 0
]

# Calculate t_A coefficients
t_A_terms = [tac * gen_coef for tac, gen_coef in zip(t_A_coef, gen_coef)]

# Calculate t_A using the t_A coefficients
t_A = sum(t_A_terms)

# Calculate t_A coefficients
CQY_max_terms = [cqy * gen_coef for cqy, gen_coef in zip(CQY_max_coef, gen_coef)]

# Calculate t_A using the t_A coefficients
CQY_max = sum(CQY_max_terms)        # Ewert Eq 4-22
