import os
import time
import json
import subprocess
import numpy as np
import ROOT as r

outdir = "/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/ntuples_v4"

# masses = [0.010, 0.050, 0.100, 0.200, 0.300, 0.400, 0.500, 0.700, 1.000, 1.400, 1.600, 1.800, 2.000, 3.000, 4.000, 5.000]
masses = [1.0] 
N_target_events = 4e7
min_events = 10000
round_to = 10000
nevts_per_job = 10000  
assert round_to % nevts_per_job == 0

MAXLOCALJOBS = 20;

xsec_file = r.TFile("../scripts/plot-xsecs/xsecs.root")

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
        Nevt = max(Nevt, min_events)
        Nevt = int(round(Nevt / round_to) * round_to)
        subdir = os.path.join(outdir, "m_{0}".format(str(m).replace(".","p")), samp_names[dm])
        os.system("mkdir -p "+subdir)
        print "  {0:2d} {1:.3e} {2:.4f} {3:8d}".format(dm, xs, cum_xs[i], Nevt)
        points.append({"decay_mode":dm, "mass":m, "n_events":Nevt, "outdir":subdir})
        with open("blah.json", 'w') as fid:
            json.dump(points[-1], fid, indent=4, ensure_ascii=True)
        # os.system("hdfs dfs -copyFromLocal -f blah.json "+os.path.join(subdir,"metadata.json"))
        os.system("cp blah.json "+os.path.join(subdir,"metadata.json"))
        os.system("rm blah.json")
        

print "# SAMPLES:", len(points)
cmds = []
for p in points:
    njobs = p["n_events"] / nevts_per_job
    for j in range(njobs):
        localname = "output_{0}_{1}_{2}.root".format(p["decay_mode"],p["mass"],j+1)
        final_name = os.path.join(p["outdir"], "output_{0}.root".format(j+1))
        cmd = "nice -n 19 ./runDecays -d {0} -o {1} -m {2} -n {3} -N {4} -e {5} &> /dev/null; hdfs dfs -copyFromLocal -f {1} {6} &> /dev/null; rm {1};".format(
            p["decay_mode"],
            localname,
            p["mass"],
            nevts_per_job,
            p["n_events"],
            nevts_per_job * j,
            final_name.replace("/hadoop","")
            )
        cmds.append(cmd)

print "# JOBS:", len(cmds)

ps = []
done = 0
current = 0
lasttime = 0
while done < len(cmds):
    done = 0
    running = len(ps)
    for i in range(len(ps)):
        res = ps[i].poll()
        if res is not None:
            done += 1
            running -= 1
    for cmd in cmds[current:current+MAXLOCALJOBS-running]:
        ps.append(subprocess.Popen(cmd, shell=True))
        running += 1
        current += 1
    if done < len(cmds):
        thistime = time.time()
        if thistime > lasttime + 20:
            lasttime = thistime
            print "{0}/{1} jobs done. {2} currently running. Checking again in 20 seconds...".format(done, len(cmds), running)
        time.sleep(1)

