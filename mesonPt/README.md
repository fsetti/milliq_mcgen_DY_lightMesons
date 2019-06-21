For now, we extract pT distributions from CMS samples. Will implement in pythia later.
To run looper to extract pT distributions:

```
cmsrel CMSSW_9_4_14
cp -r looper CMSSW_9_4_14/src
cd CMSSW_9_4_14/src
scram b -j12
cd looper/looper/python
cmsRun test_cfg.py
```

Tools for batch submission are in looper/looper/batchsubmit

Once done, `hadd` them all somewhere. The script `stitch.py` makes stitched histograms for all particles, in `pt_dists.root`.
