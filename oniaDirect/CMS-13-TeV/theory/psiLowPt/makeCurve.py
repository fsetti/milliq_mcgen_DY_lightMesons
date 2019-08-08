#!/usr/bin/env python3
#
# Make the pretty picture for the documentation
# of the j/psi or psiprime curve
# 
# Usage: makeCurve XX
# where XX = "psi" or "psiprime"
#
import math
import numpy as np
import matplotlib.pyplot as plt
import argparse

# The ArgumentParser object will hold the information
# necessary to parse the command line into python data types
parser =  argparse.ArgumentParser(description="jpsi or psiprime curve",
                                           add_help=True)

# this is the definition of the positional arguments
parser.add_argument('which_ccbar',nargs="+",help="psi or psiprime?")

# this is a dictionary contining the optional arguments
args = vars(parser.parse_args())

# Extract the optional arguments into variables
which_ccbar = args['which_ccbar'][0]

if which_ccbar == "psi":
    txtFile  = "../CMS_Jpsi_tot_0_1.2_Tev_13_CMS_1.txt"
    fineFile = "Jpsi_fine-0-10.txt"
    figFile  = "psiDirect_fullRange.pdf"
elif which_ccbar == "psiprime":
    txtFile  = "../CMS_Psi2S_tot_0_1.2_Tev_13_CMS_1.txt"
    fineFile = "Psi2S_fine-0-10.txt"
    figFile  = "psiprimeDirect_fullRange.pdf"
else:
    print("Input should be psi or psiprime")

    
# Need to strip off the leading and trailing curly bracket
# Also in some cases "*^" is there instead of "e" for an exponent
# Also skip lines starting with "#'
# Store in a temporary file
def cleanupFile(fileToClean):
    outFile = open("temp.txt","w")
    with open(fileToClean, 'r') as f:
        for line in f:
            if "#" != line[0]:
                l = line.replace("{","")
                l = l.replace("}","")
                l = l.replace("*^","e")
                outFile.write(l)
    outFile.close()

# Now load the coarse file and extract the columns
cleanupFile(txtFile)
data = np.loadtxt("temp.txt", delimiter=',')
pt      = data[:,0]
down    = data[:,1]
central = data[:,2]
up      = data[:,3]
binsize = pt[1] - pt[0]

# Now load the fine file and extract the columns
cleanupFile(fineFile)
Ldata = np.loadtxt("temp.txt", delimiter=',')
Lpt      = Ldata[:,0]
Ldown    = 1.2*Ldata[:,1]
Lup      = 1.2*Ldata[:,2]
Lcentral = 0.5*(Lup+Ldown)
n        = (Lpt<pt[0]).sum()   # number of points to keep
# a little fudge to make it "smooth"
fudge    = central[0]/Lcentral[n]
pt       = np.concatenate( (Lpt[:n],            pt) )
up       = np.concatenate( (fudge*Lup[:n],      up) )
down     = np.concatenate( (fudge*Ldown[:n],    down) )
central  = np.concatenate( (fudge*Lcentral[:n], central) )

# The fudge factor
print("The fudge factor for the finescan is", 1.2*fudge)

# Curve drawing for the documentation
fig, ax = plt.subplots()
ax.plot(pt, up,      linestyle='dashed', color='black',  label='up')
ax.plot(pt, central, linestyle='solid',  color='black', label='central')
ax.plot(pt, down,    linestyle='dashed',  color='black', label='down')
ax.fill_between(pt, down, up, color="lightblue")
ax.set_xlim(0, 40.)
ax.set_ylim(2e-4*up.max(), 5*up.max())
ax.set_title(which_ccbar)
ax.set_yscale('log')
ax.set_xlabel('Pt (Gev)')
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

# Now output a file for the low pt data with the
# right format to then
# be able to make a root file that can be merged
# with the file made from the high pt information
#
# This file differs from the original file as follows
# (a) it includes a central value
# (b) the values are "fudges" for abs(eta) to be consistent with high pt
# (c) stops at 5 GeV where the high pt stuff takes over
#
blah = input("Enter y if you want to make a text file  ")
if blah == 'y':
    outfile = "cc_" + fineFile
    print("Writing out ", outfile)
    f = open(outfile, "w+")
    for p,d,u,c in zip(pt, down, up, central):
        if p>4.999: break
        f.write("{%f, %f, %f, %f}\n" % (p,d,c,u))
        f.close()
