#!/usr/bin/env python3
#
# Calculate BR for V -> e+ e- using the
# with user-specified (pseudo)electron mass.
#
# V = rho, phi, omega, Psi, Psi(2S), Uspilon(1S)
#     Upsilon(2S), Upsilon(3S), Upsilon(4S)
#
# Usage:
# ./OniaBR.py mass
# where mass is the (pseudo)electron mass in MeV
#
# Written in python3 should work also in python2
#
# Claudio 11 June 2019
#          3 July 2019  Fixed BR for Ups(1S)->ee 
#
#
#
from __future__ import print_function  # python2 compatibility (hopefully?)
import argparse
import numpy as np
import math

# The ArgumentParser object will hold the information
# necessary to parse the command line into python data types
parser =  argparse.ArgumentParser(description="Calculate pi0 Dalitz BR",
                                           add_help=True)

# this is the definition of the positional arguments
parser.add_argument('mass', nargs="+", help="pseudo-electron mass in MeV")

# this is a dictionary contining the optional arguments
args = vars(parser.parse_args())

# Extract the optional arguments into variables
# Careful, arguments are strings, need to cast as needed
theMass = args['mass']
mass = float(theMass[0])
print("pseudo-electron mass = ",mass, " MeV")
if mass < 0:
    print("pseudo-electron mass should be positive")
    exit()

# particle masses in MeV
mrho   =   775.3
mphi   =  1019.5
momega =   782.7
mpsi   =  3096.9
mpsi2S =  3686.1
mups1S =  9460.3
mups2S = 10023.3
mups3S = 10355.2
mups4S = 10579.4

# BR into ee
BRrho   = 4.72e-5
BRphi   = 2.97e-4
BRomega = 7.36e-5
BRpsi   = 5.96e-2
BRpsi2S = 7.93e-3
BRups1S = 2.38e-2
BRups2S = 1.91e-2
BRups3S = 2.18e-2
BRups4S = 1.57e-5

# lists to hold stuff
vName = ["rho", "phi", "omega", "psi", "psi2S", "ups1S", "ups2S", "ups3S", "ups4S"]
vMass = [mrho,  mphi,  momega,  mpsi,  mpsi2S,  mups1S,  mups2S,  mups3S,  mups4S]
vBR   = [BRrho, BRphi, BRomega, BRpsi, BRpsi2S, BRups1S, BRups2S, BRups3S, BRups4S]

# electron mass
emass = 0.511

# Loop over mesons
for thisMass,   thisBR,   thisName,  in zip(vMass, vBR, vName):

    # Check that the mass is OK
    if 2*mass > thisMass:
        print("pseudo-electron mass too large for ", thisName, "-> ee")
        continue

    # Calculate BR
    x1  =  mass/thisMass
    xe  = emass/thisMass
    num = math.sqrt(1-4*x1*x1) * (1+2*x1*x1) 
    den = math.sqrt(1-4*xe*xe) * (1+2*xe*xe) 
    br  = thisBR * num / den
    
    # Output the results
    print("Branching ratio for ",thisName,"-> ee"" = ", br)

