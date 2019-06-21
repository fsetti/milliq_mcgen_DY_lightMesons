#!/usr/bin/env python3
#
# Reads HEPDATA root files from Atlas 7 GeV paper
# and outputs root files with histograms of
# central, upper, and lower 
#
# The output histograms are of
# dsigma/dpt in nb/GeV * BR(ups->mu mu)
# integrated over abs(eta)<1.2 and rescaled
# to 13 TeV using the parametrizations from LHCB data
#
# Since I was lazy, you need to set the upsilon flag by hand
#
# Claudio 21 June 2019
#
from ROOT import TH1F, TFile, gROOT, gDirectory
import math
import numpy as np
import matplotlib.pyplot as plt
import argparse

# SET THIS FLAG BY HAND!!!!!!!!
#upsilonFlag = "1S"
#upsilonFlag = "2S"
upsilonFlag = "3S"

# 1S, 2S, or 3S ???
if upsilonFlag == "1S":
    HEPDatafile = "HEPData-ins1204994-v1-Table_6.root"
    folder      = "Table 6"
    outfile     = "Atlas_1S.root"
    LHCBFlag     = 1
elif upsilonFlag == "2S":
    HEPDatafile = "HEPData-ins1204994-v1-Table_7.root"
    folder      = "Table 7"
    outfile     = "Atlas_2S.root"
    LHCBFlag     = 2
elif upsilonFlag == "3S":
    HEPDatafile = "HEPData-ins1204994-v1-Table_8.root"
    folder      = "Table 8"
    outfile     = "Atlas_3S.root"
    LHCBFlag     = 3
else:
    print("Illegal upsilonFlag..quitting")
    exit()
print("processing data for upsilon ", upsilonFlag)

# Function to rescale the cross-section from 7 TeV to 13 TeV
def LHCBRescale(flag, ptrans):
    qt = ptrans
    if ptrans > 25:
        qt = 25

    if flag == 1:
        return 1.152 + 0.05074*qt - 0.0007649*qt*qt
    elif flag == 2:
        return 1.07 + 0.05387*qt - 0.001126*qt*qt
    elif flag == 3:
        return 1.192 + 0.0516*qt - 0.001176*qt*qt

    print("Illegal call to LHCBRescale")
    return 1.0
        
# Open the file
hfile = TFile(HEPDatafile, "READ")
hfile.cd(folder)

# Get the histograms
y1 = gROOT.FindObject("Hist1D_y1")   # Contents
e1 = gROOT.FindObject("Hist1D_y1_e1")   # First Error
e2 = gROOT.FindObject("Hist1D_y1_e2")   # Second Error
e3plus  = gROOT.FindObject("Hist1D_y1_e3plus")   # Third Error
e3minus = gROOT.FindObject("Hist1D_y1_e3minus")   # Third Error

# store histogram contents into arrays.
# Note first and last entries are underflow/overflow
Ay1      = np.array(y1)
Ae1      = np.array(e1)
Ae2      = np.array(e2)
Ae3plus  = np.array(e3plus)
Ae3minus = np.array(e3minus)

# error propagation
erUp     = np.sqrt(Ae1*Ae1+Ae2*Ae2+Ae3plus*Ae3plus)
errDown  = np.sqrt(Ae1*Ae1+Ae2*Ae2+Ae3minus*Ae3minus)

# Contents of up and down variations
AyUp   = Ay1 + erUp
AyDown = Ay1 - errDown

# open a new file
newfile = TFile(outfile, "RECREATE")

# The central, up, and down output histograms
cen  = y1.Clone()
up   = y1.Clone()
down = y1.Clone()
cen.SetName("central")
cen.SetTitle("central")
up.SetName("up")
up.SetTitle("up")
down.SetName("down")
down.SetTitle("down")
cen.SetYTitle("BR(mumu) * dsigma/dpt (nb/GeV) for abs(y)<1.2")
up.SetYTitle("BR(mumu) * dsigma/dpt (nb/GeV) for abs(y)<1.2")
down.SetYTitle("BR(mumu) * dsigma/dpt (nb/GeV) for abs(y)<1.2")

# Go from femtobarn to nanobarn
# Go from dsigma/(dPt dY) to dsigma/dPt over |Y|<1.2
Ay1    = 2 * 1.2 * Ay1 / 1e6
AyUp   = 2 * 1.2 * AyUp / 1e6
AyDown = 2 * 1.2 * AyDown / 1e6

# Rescale to 13 TeV
for i in range(len(AyUp)):
    thisPt = cen.GetBinCenter(i)
    scale  = LHCBRescale(LHCBFlag, thisPt)
    # print(thisPt, scale)
    Ay1[i]     = scale * Ay1[i]
    AyUp[i]    = scale * AyUp[i]
    AyDown[i]  = scale * AyDown[i]

# zero everything out
cen.Reset("ICESM")
up.Reset("ICESM")
down.Reset("ICESM")

# fill the histograms
for i in range(len(AyUp)):
    cen.SetBinContent(i, Ay1[i])
    up.SetBinContent(i, AyUp[i])
    down.SetBinContent(i, AyDown[i])
    cen.SetBinError(i, 0)
    up.SetBinError(i, 0)
    down.SetBinError(i, 0)

# Write and close files
newfile.Write()
newfile.Close()
hfile.Close()









