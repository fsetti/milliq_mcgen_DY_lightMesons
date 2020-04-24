import glob
import os

ntuple_tag = "v8"
sim_tag = "v1_save2m"
config = "MQ"
dens_mult = 1.00 # scale all material densities by this number (used for deriving a systematic)
save_dist = 2.00 # save mCP trajectories this many meters before the milliqan detector face

charges = [0.005, 0.007, 0.01, 0.014, 0.02, 0.03, 0.05, 0.07, 0.1, 0.14, 0.2, 0.3]
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
    mass = float(mname.split("_")[1].replace("p","."))
    for sampdir in glob.glob(os.path.join(massdir, "*")):
        sampname = os.path.split(sampdir)[1]
        for q in charges:
            # if (mass <= 0.5 and q >= 0.021) or (mass >= 2.0 and q<0.11):
            #     continue
            # if mass>0.4 or (mass==0.35 and q<0.2) or (mass==0.3 and q<0.14) or (mass==0.2 and q<0.1) or (mass==0.1 and q<0.105) or (mass in [0.01,0.02,0.03,0.05] and q<0.03):
            #     continue
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
                fout.write("\narguments={0} {1} {2} {3} {4} {5} {6}\n".format(idx, fin, config, q, dens_mult, save_dist, outdir))
                fout.write("queue\n")
            fout.close()

