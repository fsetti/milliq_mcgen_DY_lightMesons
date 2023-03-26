#!/bin/bash

#
# args
#

FILEID=$1
MODE=$2
TUNE=$3
NEVT=$4
COPYDIR=$5

echo "[wrapper] FILEID    = " ${FILEID}
echo "[wrapper] MODE      = " ${MODE}
echo "[wrapper] TUNE      = " ${TUNE}
echo "[wrapper] NEVT      = " ${NEVT}
echo "[wrapper] COPYDIR   = " ${COPYDIR}

echo
echo "[wrapper] uname -a:" `uname -a`

#if [ -r "$OSGVO_CMSSW_Path"/cmsset_default.sh ]; then
#    echo "sourcing environment: source $OSGVO_CMSSW_Path/cmsset_default.sh"
#    source "$OSGVO_CMSSW_Path"/cmsset_default.sh
#elif [ -r "$OSG_APP"/cmssoft/cms/cmsset_default.sh ]; then
#    echo "sourcing environment: source $OSG_APP/cmssoft/cms/cmsset_default.sh"
#    source "$OSG_APP"/cmssoft/cms/cmsset_default.sh
#elif [ -r /cvmfs/cms.cern.ch/cmsset_default.sh ]; then
#    echo "sourcing environment: source /cvmfs/cms.cern.ch/cmsset_default.sh"
#    source /cvmfs/cms.cern.ch/cmsset_default.sh
#else
#    echo "ERROR! Couldn't find $OSGVO_CMSSW_Path/cmsset_default.sh or /cvmfs/cms.cern.ch/cmsset_default.sh or $OSG_APP/cmssoft/cms/cmsset_default.sh"
#    exit 1
#fi
source /cvmfs/cms.cern.ch/cmsset_default.sh  > /dev/null 2>&1


export SCRAM_ARCH=slc6_amd64_gcc630
CMSSW_VERSION=CMSSW_9_4_14

echo "[wrapper] SCRAM_ARCH" $SCRAM_ARCH
echo "[wrapper] CMSSW_VERSION" $CMSSW_VERSION

###version using cvmfs install of CMSSW
echo "[wrapper] setting env"
cd /cvmfs/cms.cern.ch/$SCRAM_ARCH/cms/cmssw/$CMSSW_VERSION/ 
cmsenv 
cd -

echo

echo "[wrapper] hostname  = " `hostname`
echo "[wrapper] date      = " `date`
echo "[wrapper] linux timestamp = " `date +%s`

#
# untar input sandbox
#

mkdir tmp
mv input.tar.xz tmp
mv pythia8245.tgz tmp
cd tmp

echo "[wrapper] extracting input sandbox"
tar -xJf input.tar.xz

echo "[wrapper] input contents are"
ls -a

. setup.sh

#XMLDIR=`ls -d */share/Pythia8/xmldoc`
#export PYTHIA8DATA=$XMLDIR

#
# run it
#
echo "[wrapper] running: ./main $MODE $TUNE $NEVT $FILEID"

./main $MODE $TUNE $NEVT $FILEID

#
# do something with output
#

echo "[wrapper] output is"
ls -lrth

#
# clean up
#

echo "[wrapper] copying file"

OUTFILE=output.root
if [ ! -d "${COPYDIR}" ]; then
    echo "creating output directory " ${COPYDIR}
    mkdir ${COPYDIR}
fi

substr="/ceph/cms"
COPYDIR_CEPH=${COPYDIR#$substr}
env -i X509_USER_PROXY=${X509_USER_PROXY} gfal-copy -p -f -t 4200 --verbose  --checksum ADLER32 file://`pwd`/$OUTFILE davs://redirector.t2.ucsd.edu:1095/${COPYDIR_CEPH}/output_${FILEID}.root
