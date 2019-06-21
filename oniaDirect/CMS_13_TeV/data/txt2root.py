#!/usr/bin/env python3
#
# Input: file XXXX.txt from the results of BPH-15-005
# which is a table of cross section as a function of pt
#
# Output: XXXX.root
#
# The output histograms are
# dsigma/dpt * BR(mu mu) in nb/GeV
# integrated over abs(eta) < 1.2
#
# A luminosity uncertainty of 4% is added by hand
#
# Usage ./txt2root.py XXXX
#
# Claudio June 21, 2019
#
#
from ROOT import TH1D, TFile, gROOT, gDirectory
import math
import numpy as np
import matplotlib.pyplot as plt
import argparse

# The ArgumentParser object will hold the information
# necessary to parse the command line into python data types
parser =  argparse.ArgumentParser(description="Text file to Root",
                                           add_help=True)

# this is the definition of the positional arguments
parser.add_argument('file',nargs="+",help="name of text file (no extension)")

# this is a dictionary contining the optional arguments
args = vars(parser.parse_args())

# Extract the optional arguments into variables
name = args['file'][0]

# text and root files
txtFile   = name + ".txt"
rootFile  = name + ".root"
print(txtFile, "--->", rootFile)


# Read the data in
data = np.loadtxt(txtFile, skiprows=1)

# Extract the columns
ptlo      = data[:,0]
pthi      = data[:,1]
central   = data[:,2]
stat      = data[:,3]
sys       = data[:,4]

# total error in percent including 4% luminosity
err = np.sqrt(stat*stat + sys*sys + 4*4)

# up and down
up   = (1. + 0.01*err) * central
down = (1. - 0.01*err) * central

# Go from picobarn to nanobarn
# Go from dsigma/(dPt dY) to dsigma/dPt over |Y|<1.2
central    = 2 * 1.2 * central / 1e3
down       = 2 * 1.2 * down / 1e3
up         = 2 * 1.2 * up / 1e3

# Open the output file
hfile = TFile(rootFile, 'RECREATE')
    
# bin edges
bin = np.append( ptlo, pthi[-1] ) 

# Book histograms
hCentral = TH1D("central", "central", len(bin)-1, bin)
hUp      = TH1D("up",      "up",      len(bin)-1, bin)
hDown    = TH1D("down",    "down",    len(bin)-1, bin)

# fill the histograms
for p, c, d, u in zip(ptlo, central, down, up):
    hCentral.Fill(p+0.1, c)
    hUp.Fill(p+0.1, u)
    hDown.Fill(p+0.1, d)

# Get rid of annoying error bars
zero = np.zeros(len(bin)-1)
hCentral.SetError(zero)
hUp.SetError(zero)
hDown.SetError(zero)

# Y-axis title
hCentral.SetYTitle("BR(mumu) * dsigma/dpt (nb/GeV) for abs(y)<1.2")
hUp.SetYTitle("BR(mumu) * dsigma/dpt (nb/GeV) for abs(y)<1.2")
hDown.SetYTitle("BR(mumu) * dsigma/dpt (nb/GeV) for abs(y)<1.2")

# Write the root file
hfile.Write()


