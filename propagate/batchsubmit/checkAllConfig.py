import sys, os
import time
import glob
import socket
import subprocess

indir = sys.argv[1]

found_header = False
header = []
jobs = []

for f in glob.glob(os.path.join(indir,"*","*","*.cmd")):
    with open(f) as fid:
        within_job = False
        for line in fid:
            if line.startswith("arguments"):
                job = []
                within_job = True
                found_header = True            
                outdir = line.split()[4]
                i = line.split()[0].split("=")[1]
                fout = os.path.realpath(os.path.join(outdir, "output_{0}.root".format(i)))

            if not found_header:
                header.append(line)
            elif within_job:
                job.append(line)

            if line.startswith("queue"):
                jobs.append((job,fout))

while True:
    cmd = "condor_q {0} -nobatch -wide".format("bemarsh")
    # if "uaf-1." in socket.gethostname():
    #     cmd = cmd.replace("-nobatch","")
    p = subprocess.Popen(cmd.format("bemarsh").split(), stdout=subprocess.PIPE)
    out,err = p.communicate()
    condor_out = out.split("\n")
    running_files = []
    for line in condor_out:
        if "bemarsh" not in line:
            continue
        if "wrapper" not in line:
            continue
        if "milliqan/milliq_mcgen" not in line:
            continue
        idx = int(line.strip().split()[9])
        outdir = line.strip().split()[-1]
        running_files.append(os.path.realpath(os.path.join(outdir,"output_{0}.root".format(idx))))
    print "Found {0} jobs currently running".format(len(running_files))

    fout = open(os.path.join(indir,"resubmit.cfg"), 'w')
    for line in header:
        fout.write(line)
    n_resubmit = 0
    n_redundant = 0
    for job,f in jobs:
        # if "/dy" not in f:
        #     continue
        if os.path.exists(f):            
            if f in running_files:
                n_redundant += 1
            continue
        if f in running_files:
            continue
        n_resubmit += 1
        for line in job:
            fout.write(line)
    fout.close()

    print "Found {0} jobs to resubmit".format(n_resubmit)
    if n_resubmit >0:
        os.system("condor_submit "+os.path.join(indir,"resubmit.cfg"))

    print "Found {0} redundant jobs".format(n_redundant)

    towait = 30*60
    print "Waiting {0} minutes".format(towait/60.0)
    time.sleep(towait)
