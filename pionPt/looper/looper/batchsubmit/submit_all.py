import sys, os
import time
import itertools
import numpy
import json

from metis.Sample import DBSSample
from metis.CondorTask import CondorTask
from metis.StatsParser import StatsParser

job_tag = "v2"
exec_path = "condor_exe.sh"
tar_path = "package.tar.xz"
hadoop_path = "milliqan/milliq_mcgen/pionPt"

DOSKIM = True

datasets = [ 
    ("/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80-NoPU_80X_mcRun2_asymptotic_v14-v1/AODSIM", 2),
    ("/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRStdmix-94X_mc2017_realistic_v4_ext1-v1/AODSIM", 2),
    ("/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRStdmix-NoPU_92X_upgrade2017_realistic_v10-v1/AODSIM", 2),
    ("/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM", 10),
    ("/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM", 5),
    ("/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM", 5),
    ("/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM", 5),
    ("/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM", 5),
]

total_summary = {}
while True:
    allcomplete = True
    for ds,fpo in datasets:
        sample = DBSSample( dataset=ds )
        task = CondorTask(
                sample = sample,
                open_dataset = False,
                files_per_output = fpo,
                output_name = "output.root",
                tag = job_tag,
                executable = exec_path,
                tarfile = tar_path,
                # condor_submit_params = {"sites" : "T2_US_UCSD"},
                special_dir = hadoop_path,
                )
        task.process()
        allcomplete = allcomplete and task.complete()
        # save some information for the dashboard
        total_summary[ds] = task.get_task_summary()
    # parse the total summary and write out the dashboard
    StatsParser(data=total_summary, webdir="~/public_html/dump/metis/").do()
    os.system("chmod -R 755 ~/public_html/dump/metis")
    if allcomplete:
        print ""
        print "Job={} finished".format(job_tag)
        print ""
        break
    print "Sleeping 300 seconds ..."
    time.sleep(300)
