#!/usr/bin/env python3

# Input: file XXXX.txt from the theorist
# which is a table of cross section as a function of pt
#
# Output: XXXX.root 
#
# Usage theory2Root XXXX
#
# Claudio June 20, 2019
#  no underscores, no dots in file names  June 26, 2019
#
from ROOT import TH1F, TFile
import math
import numpy as np
import matplotlib.pyplot as plt
import argparse

# The ArgumentParser object will hold the information
# necessary to parse the command line into python data types
parser =  argparse.ArgumentParser(description="Theory to Root",
                                           add_help=True)

# this is the definition of the positional arguments
parser.add_argument('file',nargs="+",help="name of text file (no extension)")

# this is a dictionary contining the optional arguments
args = vars(parser.parse_args())

# Extract the optional arguments into variables
name = args['file'][0]

# text and root files
# (remove dots and underscores from rootfile and pdf files)
betterName = name.replace("_","-")
betterName = betterName.replace(".","")
txtFile   = name + ".txt"
rootFile  = betterName + ".root"
figFile   = betterName + ".pdf" 

# Need to strip off the leading and trailing curly bracket
# Also in some cases "*^" is there instead of "e" for an exponent
# Store in a temporary file
outFile = open("temp.txt","w")
with open(txtFile, 'r') as f:
    for line in f:
        l = line.replace("{","")
        l = l.replace("}","")
        l = l.replace("*^","e")
        outFile.write(l)
outFile.close()

# Now load it
data = np.loadtxt("temp.txt", delimiter=',')

# Extract the columns
pt      = data[:,0]
down    = data[:,1]
central = data[:,2]
up      = data[:,3]

# Make sure that the size of the pt bins is constant
b  = pt[1] - pt[0]
qt = pt[1:] - pt[:-1] - b
if (np.abs(qt)).sum() > 0.001:
    print("Careful, uneven binning, I quit")
    exit()

# open the output root file
hfile = TFile(rootFile, 'RECREATE')

# parameters of the histograms
nbins   = len(pt)
binsize = pt[1] - pt[0]
ptmin   = pt[0]  - 0.5*binsize
ptmax   = pt[-1] + 0.5*binsize

# book the histograms
hCentral = TH1F("central", "central", nbins, ptmin, ptmax)
hUp      = TH1F("up",      "up",      nbins, ptmin, ptmax)
hDown    = TH1F("down",    "down",    nbins, ptmin, ptmax)

# fill the histograms
for p, c, d, u in zip(pt, central, down, up):
    hCentral.Fill(p, c)
    hUp.Fill(p, u)
    hDown.Fill(p, d)

# Get rid of annoying error bars
zero = np.zeros(nbins)
hCentral.SetError(zero)
hUp.SetError(zero)
hDown.SetError(zero)

# Write the root file
hfile.Write()


# As a bonus, plot it as well
fig, ax = plt.subplots()
ax.plot(pt, up,      linestyle='dashed', color='black',  label='up')
ax.plot(pt, central, linestyle='solid',  color='black', label='central')
ax.plot(pt, down,    linestyle='dashed',  color='black', label='down')
ax.fill_between(pt, down, up, color="lightblue")


ax.set_xlim(0, 40.)
ax.set_ylim(2e-4*up.max(), 5*up.max())
ax.set_title(name)
ax.set_yscale('log')
ax.set_xlabel('Pt (Gev)')
if "Y" in name:
    ax.set_ylabel('dsigma/dpt * BR(mumu) (nb/GeV) eta<1.2')
else:
    ax.set_ylabel('dsigma/dpt (nb/GeV) eta<1.2')
ax.legend(loc='upper right')
# plt.xticks(np.arange(min(pt), max(pt)+1, 2.0))
ax.tick_params("both", direction='in', length=10, right=True, top=True)
# ax.tick_params("both", direction='in', length=7, right=True, which='minor')

fig.show()
blah = input("Enter y if you want to save the plot to a pdf  ")
if blah == 'y':
    print("Saving plot in ", figFile)
    fig.savefig(figFile)
else:
    print("Plot not saved as pdf file")
