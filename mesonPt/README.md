Code to obtain cross sections and pT distributions for pi0, rho, omega, phi, eta, etaprime production.
The distributions are stored in `pt_dists.root`. y-axis units are "particles per minbias event per 50 MeV bin".
So, the total cross section for a given particle is the sum of all bin contents ("particles per minbias event")
times the MinBias cross section (CMS recommends 69.2 mb @ 13 TeV).

This was originally done using CMS MC samples (Summer16, with TuneCUETP8M1).
To avoid using CMS samples for non-CMS work, this was duplicated in standalone pythia
using the public tune. The two methods were verified to give identical results.
Instructions for running both are below:

To run over CMS MC samples using a CMSSW analyzer:
```
cmsrel CMSSW_9_4_14
cp -r looper CMSSW_9_4_14/src
cd CMSSW_9_4_14/src
eval `scramv1 runtime -sh`
scram b -j12
cd looper/looper/python
cmsRun test_cfg.py
```

To run with a standalone pythia program:
```
cd pythia
. setup.sh  # this will download and compile pythia if it hasn't been done yet
make
./main <mode> <n_events>  # mode = 0 (minbias), 1, 2, 3 (qcd pT-binned 15to30, 30to50, 50to80)
```

Tools for batch submission are in `looper/looper/batchsubmit` or `pythia/batchsubmit`.

Once done with either method, `hadd` all output files somewhere. 
The script `stitch.py` makes stitched histograms for all particles, in `pt_dists.root`.
