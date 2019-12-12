#! /bin/bash

TAG=$1
STAG=$2

INDIR=/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/muons_${TAG}
mkdir -p logs

if [ ! -d $INDIR ]; then
    echo "ERROR: directory ${INDIR} does not exist"
    exit 1
fi

OUTDIR=/nfs-7/userdata/bemarsh/milliqan/milliq_mcgen/merged_sim/muons_${TAG}_${STAG}
mkdir -p $OUTDIR

for proc in qcd qcd_nonbc w dy; do
    echo nohup nice -n19 copyTree.py "\"$INDIR/$proc/postsim_$STAG/*.root\" $OUTDIR/$proc.root &> logs/log_mu_$proc.txt"
    nohup nice -n19 copyTree.py "$INDIR/$proc/postsim_$STAG/*.root" $OUTDIR/$proc.root &> logs/log_mu_$proc.txt &
done
