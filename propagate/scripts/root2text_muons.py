import ROOT as r
import numpy as np
import sys, os
import subprocess

TAG = "v5_v6_save2m"
NEVT_PER_JOB = 1000

indir = "/nfs-7/userdata/bemarsh/milliqan/milliq_mcgen/merged_sim/muons_{0}/skim_0p5m".format(TAG)
outdir = "/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/muons_txt/{0}".format(TAG)
proc_types = ["qcd","qcd_nonbc","w","dy"]

for proc in proc_types:
    os.system("mkdir -p "+os.path.join(outdir, proc))
    fname = os.path.join(indir,proc+".root")
    if not os.path.exists(fname):
        raise Exception("File {0} does not exist!".format(fname))
    fin = r.TFile(fname)
    t = fin.Get("Events")
    nevt = t.GetEntries()
    for jobid, startevt in enumerate(range(0, nevt, NEVT_PER_JOB)):
        print proc, jobid, startevt
        output = open("blah.txt",'w')
        for ievt in range(startevt, min(startevt+NEVT_PER_JOB, nevt)):
            t.GetEntry(ievt)
            output.write("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}\n".format(t.event, t.decay_mode, t.sim_q, t.p4_p.M(), 
                                                                        t.hit_p_xyz.Z(), t.hit_p_xyz.X(), t.hit_p_xyz.Y(), 
                                                                        t.hit_p_p4.Pz(), t.hit_p_p4.Px(), t.hit_p_p4.Py(), 
                                                                        t.xsec * t.filter_eff / t.n_events_total))
        output.close()
        subprocess.call("cp blah.txt {0}".format(os.path.join(outdir, proc, "output_{0}.txt".format(jobid+1))), shell=True)
        subprocess.call("rm blah.txt", shell=True)


