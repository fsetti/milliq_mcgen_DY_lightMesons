1. Edit `outdir`, the list of `masses`, `nevts_per_job`, and `njobs` (i.e. # of jobs per mass point) at the top of `make_config.py`.
2. Run `python make_config.py`. This should create a `config.cmd` with `nevts_per_job * njobs * len(masses)` individual jobs/.
3. `condor_submit config.cmd`.
4. Let these finish running, then do `python checkConfig.py`. This will check all of the outputs and create a `resubmit.cmd` with any failed
jobs.
5. If there were any failures, do `condor_submit resubmit.cmd` and repeat these last two steps until 100% completion.
