import os
import time
import json
import subprocess
import numpy as np
import ROOT as r

# outdir = "/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/ntuples_mapp_theta5_v1"
outdir = "/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/ntuples_v8"

masses = [0.010, 0.020, 0.030, 0.050, 0.100, 0.200, 0.300, 0.350, 0.400, 0.500, 0.700, 1.000, 1.400, 1.600, 1.800, 2.000, 3.000, 3.500, 4.000, 4.500, 5.000]
# masses = [0.010, 0.020, 0.030, 0.050, 0.100, 0.200, 0.300, 0.350, 0.400, 0.500]
# masses = [2.000, 3.000, 3.500, 4.000, 4.500, 5.000]

# we target this amount of events per mass point, in practice it will be a bit higher since we
# put a floor on the number of events in each mode
N_target_events = 5e7

# the number of events in each job (i.e. each output file).
# Since every mode must have at least 1 job, this is effectively the minimum number of events per mode
nevts_per_job = 500000  


xsec_file = r.TFile("../../scripts/plot-xsecs/xsecs.root")

def get_xsec(decay_mode, m):
    if decay_mode == 0:
        decay_mode = "total"

    g = xsec_file.Get("xsecs_"+str(decay_mode))
    x = r.Double(-1)
    y = r.Double(0)
    n = -1
    while n < g.GetN()-1 and x < m:
        n += 1
        g.GetPoint(n, x, y)

    if n == 0:
        return y

    if x < m:
        return 0.0

    xprev, yprev = r.Double(), r.Double()
    g.GetPoint(n-1, xprev, yprev)
    
    return yprev + (y - yprev) / (x - xprev) * (m - xprev)

samp_names = {
    1:  "b_jpsi",
    2:  "b_psiprime",
    3:  "rho",
    4:  "omega",
    5:  "phi",
    6:  "pi0",
    7:  "eta",
    8:  "etaprime_photon",
    9:  "omega_pi0",
    10: "etaprime_omega",
    11: "jpsi",
    12: "psiprime",
    13: "ups1S",
    14: "ups2S",
    15: "ups3S",
}

points = []
for m in masses:
    xs = [get_xsec(i, m) for i in range(16)]

    total_xsec = xs[0]
    sorted_xs = sorted(zip(range(1,16),xs[1:]), key=lambda x:x[1], reverse=True)
    
    cum_xs = np.cumsum(zip(*sorted_xs)[1]) / total_xsec
    max_idx = max(0, np.argmax(cum_xs > 0.9999))

    print "\nmass =", m
    for i, (dm, xs) in enumerate(sorted_xs[:max_idx+1]):
        Nevt = xs / total_xsec * N_target_events
        Nevt = max(Nevt, nevts_per_job)
        Nevt = int(round(Nevt / nevts_per_job) * nevts_per_job)
        subdir = os.path.join(outdir, "m_{0}".format(str(m).replace(".","p")), samp_names[dm])
        os.system("mkdir -p "+subdir)
        print "  {0:2d} {1:.3e} {2:.4f} {3:8d}".format(dm, xs, cum_xs[i], Nevt)
        points.append({"decay_mode":dm, "mass":m, "n_events":Nevt, "outdir":subdir})
        with open("blah.json", 'w') as fid:
            json.dump(points[-1], fid, indent=4, ensure_ascii=True)
        # os.system("hdfs dfs -copyFromLocal -f blah.json "+os.path.join(subdir,"metadata.json"))
        os.system("cp blah.json "+os.path.join(subdir,"metadata.json"))
        os.system("rm blah.json")
        

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

executable=wrapper.sh
transfer_executable=True

""")

print "# SAMPLES:", len(points)
cmds = []
for p in points:
    njobs = p["n_events"] / nevts_per_job
    for j in range(njobs):
        localname = "output_{0}_{1}_{2}.root".format(p["decay_mode"],p["mass"],j+1)
        final_name = os.path.join(p["outdir"], "output_{0}.root".format(j+1))
        fout.write("arguments={0} {1} {2} {3} {4} {5}\n".format(j+1, p["decay_mode"], p["mass"], nevts_per_job, p["n_events"], p["outdir"]))
        fout.write("queue\n\n")
fout.close()
