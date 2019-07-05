#!/usr/bin/env python3
#
# Input: file XXXX.txt from
# http://www.lpthe.jussieu.fr/~cacciari/fonll/fonllform.html
# which is a table of cross section as a function of pt
#
# Output: XXXX.root 
#
# Usage fonll2Root XXXX
#
# Claudio June 16, 2019
# Hacked it to label the plot vs pseudorapidity
# if the file name contains the word "eta"
# or rapidity if the file contains "y"
#   4 July 2019
#
from ROOT import TH1D, TFile
import math
import numpy as np
import matplotlib.pyplot as plt
import argparse

# The ArgumentParser object will hold the information
# necessary to parse the command line into python data types
parser =  argparse.ArgumentParser(description="FONLL to Root",
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

# load the data
data = np.loadtxt(txtFile)

# open the output root file
hfile = TFile(rootFile, 'RECREATE')

# Extract the columns we want
pt_coarse = data[:,0]
central   = data[:,1]
down      = data[:,2]
up        = data[:,3]

pt = np.linspace(pt_coarse[0], pt_coarse[-1], 500)
central = np.interp(pt, pt_coarse, central)
down = np.interp(pt, pt_coarse, down)
up = np.interp(pt, pt_coarse, up)

# parameters of the histograms
nbins   = len(pt)
binsize = pt[1] - pt[0]
ptmin   = pt[0]  - 0.5*binsize
ptmax   = pt[-1] + 0.5*binsize

# book the histograms
hCentral = TH1D("central", "central", nbins, ptmin, ptmax)
hUp      = TH1D("up",      "up",      nbins, ptmin, ptmax)
hDown    = TH1D("down",    "down",    nbins, ptmin, ptmax)

# fill the histograms
for p, c, d, u in zip(pt, central, down, up):
    hCentral.Fill(p, c)
    hUp.Fill(p, u)
    hDown.Fill(p, d)

# Write the root file
hfile.Write()

# As a bonus, plot it as well
fig, ax = plt.subplots()
ax.plot(pt, up,      linestyle='dashed', color='black',  label='up')
ax.plot(pt, central, linestyle='solid',  color='black', label='central')
ax.plot(pt, down,    linestyle='dashed',  color='black', label='down')
ax.fill_between(pt, down, up, color="lightblue")


ax.set_xlim(pt[0], pt[-1])
ax.set_title(name)
if "eta" in name:
    ax.set_xlabel('eta')
    ax.set_ylabel('dsigma/deta (pb)')
    ax.set_ylim(0, 1.2*np.max(up))
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
elif "y" in name:
    ax.set_xlabel('rapidity')
    ax.set_ylabel('dsigma/dy (pb)')
    ax.set_ylim(0, 1.2*np.max(up))
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
else:
    ax.set_yscale('log')
    ax.set_xlabel('Pt (Gev)')
    ax.set_ylabel('dsigma/dpt (pb/GeV)')
# ax.legend(loc='upper right')
plt.xticks(np.arange(min(pt), max(pt)+1, 2.0))
ax.tick_params("both", direction='in', length=10, right=True, top=True)
ax.tick_params("both", direction='in', length=7, right=True, which='minor')

fig.show()
blah = input("Enter y if you want to save the plot to a pdf  ")
if blah == 'y':
    figFile = name + ".pdf" 
    print("Saving plot in ", figFile)
    fig.savefig(figFile)
else:
    print("Plot not saved as pdf file")
