import os

nevts_per_job = 100000
njobs = 500
outdir = "/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/muons_v5"        

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

names = ["qcd","w","dy","qcd_nonbc"]
for mode in range(len(names)):
    for j in range(njobs):
        fout.write("arguments={0} {1} {2} {3} {4}\n".format(j+1, mode+1, nevts_per_job, nevts_per_job*njobs, os.path.join(outdir,names[mode])))
        fout.write("queue\n\n")
fout.close()
