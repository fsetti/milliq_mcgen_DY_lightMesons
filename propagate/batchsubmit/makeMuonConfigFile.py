import glob
import os

ntuple_tag = "v5"
sim_tag = "v6_save2m"
config = "MQ"
dens_mult = 1.00
save_dist = 2.0
tarfile = "input.tar.xz"
# tarfile = "input_fixrock.tar.xz"

indir = "/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/muons_{0}".format(ntuple_tag)

os.system("mkdir -p "+"/data/tmp/bemarsh/condor_submit_logs/milliq_mcgen_muons_{0}_{1}".format(ntuple_tag,sim_tag))
os.system("mkdir -p "+"/data/tmp/bemarsh/condor_job_logs/milliq_mcgen_muons_{0}_{1}".format(ntuple_tag,sim_tag))

def write_header(fid):
    fid.write("""
universe=Vanilla
when_to_transfer_output = ON_EXIT
#the actual executable to run is not transfered by its name.
#In fact, some sites may do weird things like renaming it and such.
transfer_input_files=wrapper.sh, {0}
+DESIRED_Sites="T2_US_UCSD,T2_US_Caltech,T3_US_UCR,T2_US_MIT,T2_US_Vanderbilt,T2_US_Wisconsin,T3_US_Baylor,T3_US_Colorado,T3_US_NotreDame,T3_US_Rice,T3_US_Rutgers,T3_US_UMD,T3_US_Vanderbilt_EC2,T3_US_OSU"
#+remote_DESIRED_Sites="T2_US_UCSD"
+Owner = undefined
log=/data/tmp/bemarsh/condor_submit_logs/milliq_mcgen_muons_{1}_{2}/condor_12_01_16.log
output=/data/tmp/bemarsh/condor_job_logs/milliq_mcgen_muons_{1}_{2}/1e.$(Cluster).$(Process).out
error =/data/tmp/bemarsh/condor_job_logs/milliq_mcgen_muons_{1}_{2}/1e.$(Cluster).$(Process).err
notification=Never
x509userproxy=/tmp/x509up_u31592

executable=wrapper.sh
transfer_executable=True
""".format(tarfile,ntuple_tag,sim_tag))


for sdir in glob.glob(os.path.join(indir, "*")):
    sname = os.path.split(sdir)[1]
    cfgdir = "configs/muons_{0}_{1}".format(ntuple_tag, sim_tag)
    outdir = os.path.join(indir, sname, "postsim_"+sim_tag)
    print cfgdir
    os.system("mkdir -p "+cfgdir)
    fout = open(os.path.join(cfgdir, "cfg_{0}.cmd".format(sname)), 'w')
    write_header(fout)
    for fin in glob.glob(os.path.join(sdir, "*.root")):
        idx = fin.split("_")[-1].split(".")[0]
        fin = fin.replace("/hadoop/cms","root://redirector.t2.ucsd.edu/")
        fout.write("\narguments={0} {1} {2} {3} {4} {5} {6}\n".format(idx, fin, config, "mu", dens_mult, save_dist, outdir))
        fout.write("queue\n")
    fout.close()

