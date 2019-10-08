import ROOT as r
import numpy as np
import sys
import os
import glob
import subprocess

TAG = "v7_v1_save2m"
SKIM = "skim0p25m"
NEVT_PER_JOB = 10000

indir = "/nfs-7/userdata/bemarsh/milliqan/milliq_mcgen/merged_sim/{0}".format(TAG)
outdir = "/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/mcp_txt/{0}_{1}".format(TAG,SKIM)

particles = ["b_jpsi", "jpsi", "etaprime_omega", "etaprime_photon", "eta", "omega", "omega_pi0", "pi0", "phi", "rho", "b_psiprime", "psiprime", "dy"]
masses = [0.010, 0.02, 0.03, 0.05, 0.1, 0.2, 0.3, 0.35, 0.4, 0.5, 0.7, 1.0, 1.4, 1.6, 1.8, 2.0, 3.0, 3.5, 4.0, 4.5, 5.0, 7.0, 10.0]
charges = [0.005, 0.01, 0.02, 0.03, 0.05, 0.07, 0.1, 0.14, 0.2, 0.3]

for mdir in glob.glob(os.path.join(indir, "m_*")):
    m = mdir.split("/")[-1]
    for qdir in glob.glob(os.path.join(mdir, "q_*")):
        q = qdir.split("/")[-1]
        for f in glob.glob(os.path.join(qdir, SKIM, "*.root")):
            s = f.split("/")[-1].split(".")[0]
            odir = os.path.join(outdir, m, q, s)
            if os.path.exists(odir):
                continue
            os.system("mkdir -p "+odir)
            fin = r.TFile(f)
            t = fin.Get("Events")
            nevt = t.GetEntries()
            for jobid, startevt in enumerate(range(0, nevt, NEVT_PER_JOB)):
                print m, q, s, jobid, startevt
                output = open("blah.txt", 'w')
                for ievt in range(startevt, min(startevt+NEVT_PER_JOB, nevt)):
                    t.GetEntry(ievt)
                    if t.hit_p_xyz.Z() != 0:
                        output.write("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}\n".format(
                                t.event, t.decay_mode, t.sim_q, t.p4_m.M(), 
                                t.hit_p_xyz.Z(), t.hit_p_xyz.X(), t.hit_p_xyz.Y(), 
                                t.hit_p_p4.Pz(), t.hit_p_p4.Px(), t.hit_p_p4.Py(), 
                                t.sim_q**2 * t.xsec * t.BR_q1 * t.filter_eff * 1000 / t.n_events_total))
                    if t.hit_m_xyz.Z() != 0:
                        output.write("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}\n".format(
                                t.event, t.decay_mode, t.sim_q, t.p4_m.M(), 
                                t.hit_m_xyz.Z(), t.hit_m_xyz.X(), t.hit_m_xyz.Y(), 
                                t.hit_m_p4.Pz(), t.hit_m_p4.Px(), t.hit_m_p4.Py(), 
                                t.sim_q**2 * t.xsec * t.BR_q1 * t.filter_eff * 1000 / t.n_events_total))
                output.close()
                subprocess.call("cp blah.txt {0}".format(os.path.join(odir, "output_{0}.txt".format(jobid+1))), shell=True)
                subprocess.call("rm blah.txt", shell=True)

            fin.Close()




