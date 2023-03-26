import os

tag = "A2-MSTW2008LO"

base_dir="/ceph/cms/store/user/fsetti/milliQan_generation/pionPt/"

names = ["minbias","qcd_pt15to30","qcd_pt30to50","qcd_pt50to80","qcd_pt80to120"]
#names = ["minbias"]

for mode in range(len(names)):
    outdir = os.path.join(base_dir,tag,names[mode])
    os.system("rm -rf %s/logs"%(outdir))
