import os
import time
import json
import subprocess
import numpy as np
import ROOT as r

outdir = "/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/ntuples_v9/m_{sm}/dy"
masses = [1.0, 1.4, 1.6, 1.8, 2.0, 3.0, 3.5, 4.0, 4.5, 5.0, 7.0, 10.0, 14.0, 20.0, 28.0, 34.0, 
          40.0, 44.0, 48.0, 52.0, 58.0, 68.0, 80.0, 100.0]
nevts_per_job = 1000000
njobs = 500


fout = open("config.cmd",'w')
fout.write("""
universe=Vanilla
when_to_transfer_output = ON_EXIT
#the actual executable to run is not transfered by its name.
#In fact, some sites may do weird things like renaming it and such.
transfer_input_files=input.tar.xz
+DESIRED_Sites="T2_US_UCSD"
+Owner = undefined
log=logs/submit_logs/submit.log
output=logs/job_logs/1e.$(Cluster).$(Process).out
error =logs/job_logs/1e.$(Cluster).$(Process).err
notification=Never
x509userproxy=/tmp/x509up_u31592
+SingularityImage="/cvmfs/singularity.opensciencegrid.org/bbockelm/cms:rhel7"

executable=condor_exe.sh
transfer_executable=True

""")

for m in masses:
    sm = str(m).replace(".","p")
    for j in range(njobs):
        fout.write("arguments={0} {1} {2} {3} {4}\n".format(m, j+1, nevts_per_job, nevts_per_job*njobs, outdir.format(sm=sm)))
        fout.write("queue\n\n")
fout.close()
