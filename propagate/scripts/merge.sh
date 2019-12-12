#! /bin/bash

TAG=$1
STAG=$2

INDIR=/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/ntuples_${TAG}
mkdir -p logs

if [ ! -d $INDIR ]; then
    echo "ERROR: directory ${INDIR} does not exist"
    exit 1
fi

for MDIR in `ls -d $INDIR/m_*`; do
    M=`basename $MDIR`
    # if [ $M != m_0p02 ] && [ $M != m_0p03 ]; then
    #     continue
    # fi
    for SDIR in `ls -d $MDIR/*`; do
        S=`basename $SDIR`
        # if [ $S != dy ]; then
        #     continue
        # fi
        if [ ! -d $SDIR/postsim_$STAG ]; then
            continue
        fi
        for QDIR in `ls -d ${SDIR}/postsim_${STAG}/q_*`; do
            Q=`basename $QDIR`
            # if [ $Q != q_0p014 ]; then
            #     continue
            # fi
            OUTDIR=/nfs-7/userdata/bemarsh/milliqan/milliq_mcgen/merged_sim/${TAG}_${STAG}/$M/$Q
            if [ -e ${OUTDIR}/${S}.root ]; then
                continue
            fi
            mkdir -p $OUTDIR
            echo nohup nice -n19 copyTree.py "\"$QDIR/*.root\" $OUTDIR/$S.root &> logs/log_${M}_${Q}_${S}.txt"
            # nohup nice -n19 copyTree.py "$QDIR/*.root" $OUTDIR/$S.root &> logs/log_${M}_${Q}_${S}.txt &
        done
    done
    # wait
done
