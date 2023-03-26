import os

tag = "Monash2013"
nevts_per_job = 100000
njobs = 2500
offset = 0
tune = 0

base_dir="/ceph/cms/store/user/fsetti/milliQan_generation/pionPt/"
os.system("mkdir -p %s"%(base_dir))

#names = {"minbias": 0 ,"qcd_pt15to30": 1 ,"qcd_pt30to50": 2 ,"qcd_pt50to80": 3, "qcd_pt80to120": 4}
#names = {"minbias": 0 ,"qcd_pt50to80": 3, "qcd_pt80to120": 4}
names = {"qcd_pt15to30": 1 ,"qcd_pt30to50": 2}

for process in names.keys() :
    mode = int(names[process])
    outdir = os.path.join(base_dir,tag,process)
    os.system("mkdir -p %s"%(outdir))
    os.system("mkdir -p %s/logs"%(outdir))

    fout = open("config.cmd",'w')
    fout.write("""
    universe=Vanilla
    when_to_transfer_output = ON_EXIT
    transfer_input_files=input.tar.xz,../pythia8245.tgz
    
    +DESIRED_Sites="T2_US_UCSD,T2_US_CALTECH,T2_US_WISCONSIN,T2_US_Purdue,T2_US_Vanderbilt,T2_US_Florida"
    
    +Owner = undefined
    
    log=/%s/logs/submit_$(Cluster)_$(Process).log
    output=/%s/logs/1e.$(Cluster).$(Process).out
    error =/%s/logs/1e.$(Cluster).$(Process).err
    
    +project_Name = "cmssurfandturf"
    use_x509userproxy = True
    Requirements = (HAS_SINGULARITY=?=True) && (TARGET.K8SNamespace =!= "abc")
    +SingularityImage="/cvmfs/singularity.opensciencegrid.org/cmssw/cms:rhel7-m202006"
    +RequestK8SNamespace="cms-ucsd-t2"
    
    x509userproxy=/tmp/x509up_u31704
    
    executable=wrapper.sh
    transfer_executable=True
    
    
    RequestMemory = 2048
    RequestDisk = 5000
    RequestCpus = 1
    
    """%(outdir,outdir,outdir)
    )
    
    run = False	
    for ijob in range(njobs):
        if not os.path.isfile("%s/output_%s.root"%(outdir,str(ijob+1+offset))):
          fout.write("arguments={0} {1} {2} {3} {4}\nqueue\n\n".format(ijob+1+offset, mode, tune, nevts_per_job, outdir))
          if not run:
            run = True

    fout.close()
    if run:
      print("Now processing: " + process + "." )
      os.system("condor_submit config.cmd")
