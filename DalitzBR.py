#!/usr/bin/env python3
#
# Calculate BR for PS-> e+ e- X using the
# Vector Dominance Model (VDM) by brute force integration
# of the distribution of Mee^2 from the formula in
# http://cds.cern.ch/record/683210/files/soft-96-032.pdf
#
# Here PS is pi0 or eta or etaprime or omega.
# X is usually a gamma, but not always.
#
# The (pseudo)electron mass is a parameter.
#
# Usage:
# ./dalitzBR.py mass
# where mass is the (pseudo)electron mass in MeV
#
# Not sure that the VDM can be trusted too much
# for pseudo-electron masses approaching the rho.
# Get answers consistent with PDG when tested with both
# electron and muon masses.
# But the muon mass is stil << rho mass, so who knows.
#
# Written in python3 should work also in python2
#
# Claudio            31 May 2019
# Prettified          7 June 2019
# Fixed small bugs   13 June 2019
# Even better formula whan X is not a gamma
#                                   13 June 2019
#
from __future__ import print_function  # python2 compatibility (hopefully?)
import argparse
import numpy as np
import math

# http://cds.cern.ch/record/683210/files/soft-96-032.pdf
def DgammaDs(emass, mesonMass, daughterMesonMass, s):
    alpha    = 1./137.036
    rhoMass  = 775.5
    rhoWidth = 145.
    if daughterMesonMass < 1e-4:
        c1 = 2*alpha/(3*math.pi*s)
        c2 = 1 - s/mesonMass**2
    else:
        c1  = alpha/(3*math.pi*s)
        dm2 = mesonMass**2 - daughterMesonMass**2
        c2  = (1 + s/dm2)**2 - 4*s*mesonMass**2/(dm2*dm2)
        c2  = np.sqrt(c2)
    c3 = 1 + 2*emass**2/s
    c4 = np.sqrt(1 - 4*emass**2/s)
    c5 = (rhoMass**2 - s)**2 + (rhoMass*rhoWidth)**2 
    return c1 * c2**3 * c3 * c4 * (rhoMass**4 + (rhoMass*rhoWidth)**2 ) / c5
   
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

# particle masses
mpi0 = 134.97
meta = 547.862
metaprime = 957.78
momega = 782.65

# the decays that we calculate are
# scalarName -> X e+ e-
# and they are normalized to the BR of
# scalar -> X gamma
scalarName = ["pi0",    "eta",   "etaprime", "etaprime", "omega"]
XName      = ["gamma", "gamma",  "gamma",    "omega",    "pi0"]
scalarMass = [mpi0,     meta,     metaprime, metaprime,  momega]
Xmass      = [0,        0,       0,          momega,     mpi0]
scalarBR   = [0.98823,  0.3941,  0.0222,     0.0262,     0.0840]

# Loop over mesons
for thisMass,   thisBR,   thisName,   thisX, thisXmass in zip(
    scalarMass, scalarBR, scalarName, XName, Xmass):

    # Check that the mass is OK
    if 2*mass+thisXmass > thisMass:
        print("pseudo-electron mass too large for ", thisName, "-> ee", thisX)
        continue

    # Max and min inv mass of ee pair
    diMassMax = thisMass - thisXmass
    diMassMin = 2*mass 
        
    # Brute force integral.
    # Because the function varies very fast near 0,
    # need very fine binning. (the 1e-5 is to avoid numerical trouble)
    sarray   = np.linspace( diMassMin**2, (diMassMax**2- 1e-5), 20000000)
    ds       = sarray[1]-sarray[0]
    dgds     = DgammaDs(mass, thisMass, thisXmass, sarray)
    br       = 0.5 * np.sum( (dgds[1:]+dgds[:-1])) * ds * thisBR

    # Output the results
    print("Branching ratio for ",thisName,"-> ee", thisX, " = ", br)

