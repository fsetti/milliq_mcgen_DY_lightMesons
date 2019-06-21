PACKAGE=package.tar.gz
OUTPUTDIR=$1
OUTPUTFILENAME=$2
INPUTFILENAMES=$3
INDEX=$4

# probably need a few other args, like nEvents and xSec (or maybe not?)

echo "[wrapper] OUTPUTDIR	= " ${OUTPUTDIR}
echo "[wrapper] OUTPUTFILENAME	= " ${OUTPUTFILENAME}
echo "[wrapper] INPUTFILENAMES	= " ${INPUTFILENAMES}
echo "[wrapper] INDEX		= " ${INDEX}

echo "[wrapper] hostname  = " `hostname`
echo "[wrapper] date      = " `date`
echo "[wrapper] linux timestamp = " `date +%s`

######################
# Set up environment #
######################

export SCRAM_ARCH=slc6_amd64_gcc630
source /cvmfs/cms.cern.ch/cmsset_default.sh

# Untar
tar -xJf ${PACKAGE}

# Build
cd CMSSW_9_4_14/src/looper
echo "[wrapper] in directory: " ${PWD}
echo "[wrapper] attempting to build"
eval `scramv1 runtime -sh`
scramv1 b ProjectRename
scram b
eval `scramv1 runtime -sh`
cd $CMSSW_BASE/src/looper/looper

echo "process.source = cms.Source(\"PoolSource\",
fileNames=cms.untracked.vstring(\"${INPUTFILENAMES}\".split(\",\"))
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32( -1 ) )
" >> python/ConfFile_cfg.py


# Create tag file
echo "[wrapper `date +\"%Y%m%d %k:%M:%S\"`] running: cmsRun -n 4 python/ConfFile_cfg.py"
cmsRun -n 4 python/ConfFile_cfg.py

echo "[wrapper] output root files are currently: "
ls -lh *.root

# Copy output
gfal-copy -p -f -t 4200 --verbose file://`pwd`/${OUTPUTFILENAME}.root gsiftp://gftp.t2.ucsd.edu/${OUTPUTDIR}/${OUTPUTFILENAME}_${INDEX}.root --checksum ADLER32
