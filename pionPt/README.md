To run looper to extract pT distributions:

```
cmsrel CMSSW_9_4_14
cd CMSSW_9_4_14/src
scram b -j12
cd looper/looper/python
cmsRun ConfFile_cfg.py
```

tools for batch submission are in looper/looper batchsubmit
