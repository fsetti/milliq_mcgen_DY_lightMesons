import os
import sys
import glob
import gzip
import time
import multiprocessing as mp
from tqdm import tqdm

MAXLOCALJOBS = 20

def simple_parse(fin, fout):
    fout = open(fout, 'w')
    nevents = 0
    with gzip.open(fin) as fid:
        within_event = False
        xsec = -1
        for line in fid:
            if not within_event and "Integrated weight" in line:
                xsec = float(line.split()[-1])
                fout.write(str(xsec)+'\n')
            if line.startswith("<event>"):
                if xsec < 0:
                    raise Exception("Didn't find xsec before first event!")
                within_event = True
            if line.startswith("</event>"):
                fout.write(" ".join(map(lambda s:"{0:22.15f}".format(s), p4_p + p4_m)) + '\n')
                nevents += 1
                within_event = False
            if not within_event:
                continue
            sp = line.strip().split()
            if sp[0] == "11":
                p4_p = map(float, sp[6:10])
            if sp[0] == "-11":
                p4_m = map(float, sp[6:10])
    fout.close()
    return nevents

if __name__=="__main__":
    indir = sys.argv[1]
    fs = glob.glob(os.path.join(indir,"*/Events/*/*.lhe.gz"))
    # fs = ["runs/out_mq5_13tev_xsecscan/mq5_1p002_1p0_chunk0/Events/run_01/unweighted_events.lhe.gz"]

    nchunks = 1 + max([int(f.split("chunk")[1].split("/")[0]) for f in fs])

    ps = []
    fouts = []
    pool = mp.Pool(MAXLOCALJOBS)
    for f in fs:                
        fout = os.path.join(os.path.split(f)[0], "mcp_p4s.txt")
        fouts.append(fout)
        if os.path.exists(fout):
            continue
        ps.append(pool.apply_async(simple_parse, (f,fout)))
        
    done = 0
    lasttime = 0
    while done < len(ps):
        done = sum([p.ready() for p in ps])
        if done < len(ps):
            thistime = time.time()
            if thistime > lasttime + 10:
                lasttime = thistime
                print "{0}/{1} done. Checking again in 10 seconds".format(done, len(ps))
            time.sleep(1)
            
    if len(ps) > 0:
        nevt = [p.get() for p in ps]
        minevt = reduce(min, nevt)
        maxevt = reduce(max, nevt)
        if minevt != maxevt:
            raise Exception("nevents doesn't appear to be consistent between jobs!")
    else:
        with open(fouts[0]) as fid:
            minevt = len(fid.readlines())-1

    fcmd = open("commands.txt", 'w')
    for fout in fouts:
        chunk = int(fout.split("chunk")[1].split("/")[0])
        mass = fout.split("/mq5_")[1].split("_")[0]
        nchunks = 1 + max([int(f.split("chunk")[1].split("/")[0]) for f in fs if "mq5_"+mass in f])
        outdir = "/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/ntuples_v8/m_{0}/dy/".format(mass)
        # outdir = "/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/ntuples_mapp_theta5_v1/m_{0}/dy/".format(mass)
        outfile = os.path.join(outdir,"output_{0}.root".format(chunk+1))
        if os.path.exists(outfile):
            continue
        os.system("mkdir -p "+outdir)
        cmd = "nice -n19 ./ntupler/run -i {0} -o {1} -N {2} -e {3} &> {4}; hdfs dfs -copyFromLocal -f {1} {5}; rm {1}".format(
        # cmd = "nice -n19 ./ntupler/run -i {0} -o {1} -N {2} -e {3} &> {4};".format(
            fout,
            fout.replace(".txt", ".root"),
            nchunks * minevt,
            chunk * minevt,
            fout.replace(".txt", ".log"),
            # outfile.replace("/hadoop",""),
            outfile,
            )
        fcmd.write(cmd + '\n')
    fcmd.close()
