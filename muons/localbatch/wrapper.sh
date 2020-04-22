#!/bin/bash

#
# args
#

FILEID=$1
DECAYMODE=$2
NEVENTS=$3
NEVENTSTOTAL=$4
COPYDIR=$5

echo "[wrapper] FILEID    = " ${FILEID}
echo "[wrapper] DECAYMODE = " ${DECAYMODE}
echo "[wrapper] NEVENTS   = " ${NEVENTS}
echo "[wrapper] NEVENTSTOTAL = " ${NEVENTSTOTAL}
echo "[wrapper] COPYDIR   = " ${COPYDIR}

echo
echo "[wrapper] uname -a:" `uname -a`

if [ -r "$OSGVO_CMSSW_Path"/cmsset_default.sh ]; then
    echo "sourcing environment: source $OSGVO_CMSSW_Path/cmsset_default.sh"
    source "$OSGVO_CMSSW_Path"/cmsset_default.sh
elif [ -r "$OSG_APP"/cmssoft/cms/cmsset_default.sh ]; then
    echo "sourcing environment: source $OSG_APP/cmssoft/cms/cmsset_default.sh"
    source "$OSG_APP"/cmssoft/cms/cmsset_default.sh
elif [ -r /cvmfs/cms.cern.ch/cmsset_default.sh ]; then
    echo "sourcing environment: source /cvmfs/cms.cern.ch/cmsset_default.sh"
    source /cvmfs/cms.cern.ch/cmsset_default.sh
else
    echo "ERROR! Couldn't find $OSGVO_CMSSW_Path/cmsset_default.sh or /cvmfs/cms.cern.ch/cmsset_default.sh or $OSG_APP/cmssoft/cms/cmsset_default.sh"
    exit 1
fi

#
# set up environment
#
# if [[ `uname -a` = *"el6"* ]]; then
#     export SCRAM_ARCH=slc6_amd64_gcc630
#     CMSSW_VERSION=CMSSW_9_4_14
# fi
# if [[ `uname -a` = *"el7"* ]]; then
#     export SCRAM_ARCH=slc6_amd64_gcc700
#     CMSSW_VERSION=CMSSW_10_2_15
# fi
export SCRAM_ARCH=slc6_amd64_gcc630
CMSSW_VERSION=CMSSW_9_4_14

echo "[wrapper] SCRAM_ARCH" $SCRAM_ARCH
echo "[wrapper] CMSSW_VERSION" $CMSSW_VERSION

###version using cvmfs install of CMSSW
echo "[wrapper] setting env"
# source /cvmfs/cms.cern.ch/cmsset_default.sh
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

TMPDIR=output_${DECAYMODE}${FILEID}
mkdir $TMPDIR
cp input.tar.xz $TMPDIR
cd $TMPDIR

echo "[wrapper] extracting input sandbox"
tar -xJf input.tar.xz

echo "[wrapper] input contents are"
ls -a

cd muons

#
# run it
#
EVT=$((($FILEID-1)*$NEVENTS))
OUTFILE=output_${DECAYMODE}_${FILEID}.root
echo "[wrapper] running: ./runMuons -d $DECAYMODE -n $NEVENTS -e $EVT -o $OUTFILE"

./runMuons -d $DECAYMODE -n $NEVENTS -N $NEVENTSTOTAL -e $EVT -o $OUTFILE

#
# do something with output
#

echo "[wrapper] output is"
ls -lrth

#
# clean up
#

echo "[wrapper] copying file"

if [ ! -d "${COPYDIR}" ]; then
    echo "creating output directory " ${COPYDIR}
    mkdir ${COPYDIR}
fi

env -i X509_USER_PROXY=${X509_USER_PROXY} gfal-copy -p -f -t 4200 --verbose file://`pwd`/$OUTFILE gsiftp://gftp.t2.ucsd.edu${COPYDIR}/output_${FILEID}.root

echo "[wrapper] cleaning up"
cd ../..
rm -r $TMPDIR
echo "[wrapper] cleaned up"
ls
