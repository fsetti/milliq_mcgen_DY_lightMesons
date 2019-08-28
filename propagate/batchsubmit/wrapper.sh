#!/bin/bash

#
# args
#

FILEID=$1
INPUT=$2
CONFIG=$3
CHARGE=$4
COPYDIR=$5

echo "[wrapper] FILEID    = " ${FILEID}
echo "[wrapper] INPUT     = " ${INPUT}
echo "[wrapper] CONFIG    = " ${CONFIG}
echo "[wrapper] CHARGE    = " ${CHARGE}
echo "[wrapper] COPYDIR   = " ${COPYDIR}

#
# set up environment
#
CMSSW_VERSION=CMSSW_9_4_14

###version using cvmfs install of CMSSW
echo "[wrapper] setting env"
export SCRAM_ARCH=slc6_amd64_gcc630
source /cvmfs/cms.cern.ch/cmsset_default.sh
OLDDIR=`pwd`
cd /cvmfs/cms.cern.ch/$SCRAM_ARCH/cms/cmssw/$CMSSW_VERSION/src
#cmsenv
eval `scramv1 runtime -sh`
cd $OLDDIR

echo

echo "[wrapper] hostname  = " `hostname`
echo "[wrapper] date      = " `date`
echo "[wrapper] linux timestamp = " `date +%s`

#
# untar input sandbox
#

echo "[wrapper] extracting input sandbox"
tar -xJf input.tar.xz

#source job_input/setupenv.sh
#printenv

echo "[wrapper] input contents are"
ls -a

PYTHONPATH=./MilliqanSim:${PYTHONPATH}

#
# run it
#
echo "[wrapper] running: python -u run_sim.py ${CONFIG} ${CHARGE} ${INPUT}"

python -u run_sim.py ${CONFIG} ${CHARGE} ${INPUT}

#
# do something with output
#

echo "[wrapper] output is"
ls -lrth

#
# clean up
#

# Rigorous sweeproot which checks ALL branches for ALL events.
# If GetEntry() returns -1, then there was an I/O problem, so we will delete it
cat > rigorousSweepRoot.py << EOL
import ROOT as r
import os, sys

f1 = r.TFile("output.root")
if not f1 or not f1.IsOpen() or f1.IsZombie():
    print "[RSR] removing zombie output.root because it does not deserve to live"
    os.system("rm output.root")
    sys.exit()

t = f1.Get("Events")
if type(t)==type(r.TObject()):
    print "[RSR] no tree named 'Events' in file! Deleting."
    os.system("rm output.root")
    sys.exit()

print "[RSR] ntuple has %i events" % t.GetEntries()

foundBad = False
for i in range(0,t.GetEntries(),1):
    if t.GetEntry(i) < 0:
        foundBad = True
        print "[RSR] found bad event %i" % i
        break

if foundBad:
    print "[RSR] removing output.root because it does not deserve to live"
    os.system("rm output.root")
else:
    print "[RSR] passed the rigorous sweeproot"
EOL

date +%s
echo "[wrapper] running rigorousSweepRoot.py"
python rigorousSweepRoot.py
date +%s


echo "[wrapper] copying file"

if [ ! -d "${COPYDIR}" ]; then
    echo "creating output directory " ${COPYDIR}
    mkdir ${COPYDIR}
fi

gfal-copy -p -f -t 4200 --verbose file://`pwd`/output.root gsiftp://gftp.t2.ucsd.edu${COPYDIR}/output_${FILEID}.root

echo "[wrapper] cleaning up"
for FILE in `find . -not -name "*stderr" -not -name "*stdout"`; do rm -rf $FILE; done
echo "[wrapper] cleaned up"
ls
