import glob
import os

ntuple_tag = "v7"
sim_tag = "v1"
config = "MQ"

charges = [0.01, 0.02, 0.05, 0.07, 0.1, 0.14, 0.2, 0.3]
# charges = [0.01,0.05,0.07,0.1]

indir = "/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/ntuples_{0}".format(ntuple_tag)

os.system("mkdir -p "+"/data/tmp/bemarsh/condor_submit_logs/milliq_mcgen_{0}_{1}".format(ntuple_tag,sim_tag))
os.system("mkdir -p "+"/data/tmp/bemarsh/condor_job_logs/milliq_mcgen_{0}_{1}".format(ntuple_tag,sim_tag))

def write_header(fid):
    fid.write("""
universe=Vanilla
when_to_transfer_output = ON_EXIT
#the actual executable to run is not transfered by its name.
#In fact, some sites may do weird things like renaming it and such.
transfer_input_files=wrapper.sh, input.tar.xz
+DESIRED_Sites="T2_US_UCSD,T2_US_Caltech,T3_US_UCR,T2_US_MIT,T2_US_Vanderbilt,T2_US_Wisconsin,T3_US_Baylor,T3_US_Colorado,T3_US_NotreDame,T3_US_Rice,T3_US_Rutgers,T3_US_UMD,T3_US_Vanderbilt_EC2,T3_US_OSU"
#+remote_DESIRED_Sites="T2_US_UCSD"
+Owner = undefined
log=/data/tmp/bemarsh/condor_submit_logs/milliq_mcgen_{0}_{1}/condor_12_01_16.log
output=/data/tmp/bemarsh/condor_job_logs/milliq_mcgen_{0}_{1}/1e.$(Cluster).$(Process).out
error =/data/tmp/bemarsh/condor_job_logs/milliq_mcgen_{0}_{1}/1e.$(Cluster).$(Process).err
notification=Never
x509userproxy=/tmp/x509up_u31592

executable=wrapper.sh
transfer_executable=True
""".format(ntuple_tag,sim_tag))


for massdir in glob.glob(os.path.join(indir, "m_*")):
    mname = os.path.split(massdir)[1]
    for sampdir in glob.glob(os.path.join(massdir, "*")):
        sampname = os.path.split(sampdir)[1]
        for q in charges:
            qname = "q_"+str(q).replace(".","p")
            cfgdir = "configs/{0}_{1}/{2}/{3}".format(ntuple_tag, sim_tag, mname, qname)
            outdir = os.path.join(indir, mname, sampname, "postsim_"+sim_tag, qname)
            print cfgdir
            os.system("mkdir -p "+cfgdir)
            fout = open(os.path.join(cfgdir, "cfg_{0}.cmd".format(sampname)), 'w')

            write_header(fout)
            for fin in glob.glob(os.path.join(sampdir, "*.root")):
                idx = fin.split("_")[-1].split(".")[0]
                fin = fin.replace("/hadoop/cms","root://redirector.t2.ucsd.edu/")
                fout.write("\narguments={0} {1} {2} {3} {4}\n".format(idx, fin, config, q, outdir))
                fout.write("queue\n")
            fout.close()

