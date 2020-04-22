Tools for batch submission of event generation jobs.
1. After compiling with `make` in the parent directory, run `. createTar.sh`.
2. Run `python make_config.py`. Note you will have to edit `outdir`, 
and maybe `masses`, `N_target_events`, `n_evts_per_job` at the top of the file.
For reference, the demonstrator paper used 5e7 and 5e5 for `N_target_events` and `n_evts_per_job`.
The high-stats extension samples used 5e8 and 1e6.
3. This should produce `config.cmd`, which can be submitted with condor. Unless you
set `n_evts_per_job` too high, this should be pretty quick.
4. Run `python checkConfig.py` to check for any missing files. If there are any,
you can just submit `condor_submit resubmit.cmd`.
