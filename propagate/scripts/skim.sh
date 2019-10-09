#! /bin/bash

TAG=$1
STAG=$2

SKIM="skim0p25m"
SEL="(does_hit_p && abs(hit_p_xyz.X())<0.125 && abs(hit_p_xyz.Y())<0.125) || (does_hit_m && abs(hit_m_xyz.X())<0.125 && abs(hit_m_xyz.Y())<0.125)"

INDIR=/nfs-7/userdata/bemarsh/milliqan/milliq_mcgen/merged_sim/${TAG}_${STAG}
mkdir -p logs

if [ ! -d $INDIR ]; then
    echo "ERROR: directory ${INDIR} does not exist"
    exit 1
fi

for MDIR in `ls -d $INDIR/m_*`; do
    M=`basename $MDIR`
    for QDIR in `ls -d ${MDIR}/q_*`; do
        Q=`basename $QDIR`
        for FILE in `ls -d $QDIR/*.root`; do
            S=`basename $FILE`
            OUTDIR=${QDIR}/${SKIM}
            mkdir -p ${OUTDIR}
            if [ -e ${OUTDIR}/${S} ]; then
                continue
            fi
            echo nohup nice -n19 copyTree.py "\"$QDIR/$S\" $OUTDIR/$S -1 0 Events \"$SEL\"&> logs/log_skim_${M}_${Q}_${S}.txt"
            # nohup nice -n19 copyTree.py "$QDIR/*.root" $OUTDIR/$S.root &> logs/log_${M}_${Q}_${S}.txt &
        done
    done
    # wait
done
