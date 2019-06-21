#!/usr/bin/env python3
#
# Reads the usilon ROOT files for Atlas and CMS from
# ../CMS_13_TeV/data and ../Atlas_7_Tev
# and combines them into an output ROOT file
#
# Since I was lazy, you need to set the upsilon flag by hand
#
# Claudio 21 June 2019
#
from ROOT import TH1F, TH1D, TFile, gROOT, gDirectory
import math
import numpy as np
import matplotlib.pyplot as plt
import argparse

# SET THIS FLAG BY HAND!!!!!!!!
# upsilonFlag = "1S"
# upsilonFlag = "2S"
upsilonFlag = "3S"

# 1S, 2S, or 3S ???
if upsilonFlag == "1S":
    cmsIn    = "../CMS_13_TeV/data/ups1S.root"
    atlasIn  = "../Atlas_7_TeV/Atlas_1S.root"
    fileOut  = "ups1S_combined.root"
elif upsilonFlag == "2S":
    cmsIn    = "../CMS_13_TeV/data/ups2S.root"
    atlasIn  = "../Atlas_7_TeV/Atlas_2S.root"
    fileOut  = "ups2S_combined.root"
elif upsilonFlag == "3S":
    cmsIn    = "../CMS_13_TeV/data/ups3S.root"
    atlasIn  = "../Atlas_7_TeV/Atlas_3S.root"
    fileOut  = "ups3S_combined.root"
else:
    print("Illegal upsilonFlag..quitting")
    exit()
print("Making ", fileOut)

# Open the CMS file
cmsFile = TFile(cmsIn)

# Get the contents of the CMS histograms and the bin edges
# Remove underflow
cmsCentral = np.array(gROOT.FindObject("central"))[1:]
cmsUp      = np.array(gROOT.FindObject("up"))[1:]
cmsDown    = np.array(gROOT.FindObject("down"))[1:]
cmsBins    = np.array(gROOT.FindObject("central").GetXaxis().GetXbins())

# Close the CMS file
cmsFile.Close()

# Open the Atlas file
atlasFile =  TFile(atlasIn)

# Get the contents of the Atlas histograms and the bin edges
# Remove underflow
atlasCentral = np.array(gROOT.FindObject("central"))[1:]
atlasUp      = np.array(gROOT.FindObject("up"))[1:]
atlasDown    = np.array(gROOT.FindObject("down"))[1:]
atlasBins    = np.array(gROOT.FindObject("central").GetXaxis().GetXbins())

# Close the Atlas file
atlasFile.Close()

# Debug
debug = False
if debug:
    print(len(atlasCentral))
    print(atlasCentral)
    print(len(atlasBins))
    print(atlasBins)
    print(" ")
    print(len(cmsCentral))
    print(cmsCentral)
    print(len(cmsBins))
    print(cmsBins)

# Find the last bin of Atlas to use
boundary = cmsBins[0]
iBin     = 0
for x in atlasBins:
    if abs(x-boundary) < 0.01:
        break
    iBin = iBin + 1
if iBin == len(atlasBins):
    print("Could not find good bin edges...quitting")
    exit()

# Truncate the Atlas information
atlasCentral = atlasCentral[:iBin]
atlasUp      = atlasUp[:iBin]
atlasDown    = atlasDown[:iBin]
atlasBins    = atlasBins[:iBin]

# Debug
if debug:
    print(" ")
    print("bin ", iBin)
    print(len(atlasCentral))
    print(atlasCentral)
    print(len(atlasBins))
    print(atlasBins)
    print(" ")

# Concatenate atlas and cms bins
bins    = np.concatenate( (atlasBins,    cmsBins   ) )
central = np.concatenate( (atlasCentral, cmsCentral) )
up      = np.concatenate( (atlasUp,      cmsUp     ) )
down    = np.concatenate( (atlasDown,    cmsDown   ) )

# Debug
if debug:
    print(" ")
    print(len(central))
    print(central)
    print(len(bins))
    print(bins)
    print(" ")

# write output file
rootFile = TFile(fileOut, "RECREATE")

# Book histograms
hCentral = TH1D("central", "central", len(bins)-1, bins)
hUp      = TH1D("up",      "up",      len(bins)-1, bins)
hDown    = TH1D("down",    "down",    len(bins)-1, bins)

# fill the histograms
for p, c, d, u in zip(bins, central, down, up):
    hCentral.Fill(p+0.01, c)
    hUp.Fill(p+0.01, u)
    hDown.Fill(p+0.01, d)

# Get rid of annoying error bars
zero = np.zeros(len(bins)-1)
hCentral.SetError(zero)
hUp.SetError(zero)
hDown.SetError(zero)

# Y-axis title
hCentral.SetYTitle("BR(mumu) * dsigma/dpt (nb/GeV) for abs(y)<1.2")
hUp.SetYTitle("BR(mumu) * dsigma/dpt (nb/GeV) for abs(y)<1.2")
hDown.SetYTitle("BR(mumu) * dsigma/dpt (nb/GeV) for abs(y)<1.2")

# Write the root file
rootFile.Write()


