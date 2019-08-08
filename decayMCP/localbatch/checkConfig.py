import os

header = []
jobs = []
found_job = False
f = open("config.cmd")
for line in f:

    if line.startswith("arguments"):
        found_job = True
        outdir = line.strip().split()[-1]
        idx = int(line.split()[0].split("=")[-1])
        outfile = os.path.join(outdir, "output_{0}.root".format(idx))
        if not os.path.exists(outfile):
            jobs.append(line)
            print outfile

    if not found_job:
        header.append(line)

fout = open("resubmit.cmd",'w')
for line in header:
    fout.write(line)
for job in jobs:
    fout.write(job)
    fout.write("queue\n\n")
fout.close()
