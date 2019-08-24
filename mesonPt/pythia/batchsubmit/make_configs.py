import os

tag = "v2_with_mus"
nevts_per_job = 100000
njobs = 200

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

"""
)

names = ["minbias","qcd_pt15to30","qcd_pt30to50","qcd_pt50to80","qcd_pt80to120"]

for mode in range(len(names)):
    outdir = os.path.join("/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/pionPt/fromPythia/",tag,names[mode])
    for ijob in range(njobs):
        fout.write("arguments={0} {1} {2} {3}\nqueue\n\n".format(ijob+1, mode, nevts_per_job, outdir))

fout.close()
