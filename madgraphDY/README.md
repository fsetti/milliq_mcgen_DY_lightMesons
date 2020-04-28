This directory contains scripts necessary to generate DY production of mCPs from MadGraph 5.
Follow these steps:
1. Run `. setup.sh`. This will download MadGraph if not done already, and setup the environment.
2. Edit `carddir`, `nevents`, `njobs_per_mass`, and `masses` at the top of `write_cards.py`. `nevents` is the number of events
to generate per job. `njobs_per_mass` is the number of jobs per mass point. So the total number of events per mass
point is `nevents * njobs_per_mass`.
3. Run `python write_cards.py`. This will dump MG cards into `carddir`.
4. Run `. make_commands.sh <carddir> > commands.txt`. This will dump a list of commands that need to be run into `commands.txt`.
5. You need to run all of these commands one way or another. It will take a very long time if run one at a time. The GNU [parallel](https://www.gnu.org/software/parallel/)
utility can help, by running the jobs in parallel. e.g. `parallel --nice 10 --jobs 15 --bar --shuf --joblog joblog.txt < commands.tx` will run all commands, up to 15 at a time.
6. This will generate events in gzipped LHE files. Now we need to extract the mCP kinematics and dump into root files. Run `python extract_kinematics.py <carddir>` 
(probably after editting `outdir` near the bottom). This will dump a list of commands into `commands.txt` that can be run with `parallel` again. These commands
dump the kinematics into text files, then feed these into a C++ program `ntupler/run.cc` that converts them into ROOT files.
7. These root files are placed into wherever you set `outdir` in the previous step. These should be in the same format as those from
`decayMCP/runDecays.cc`, and can be fed into the propagator in the same way.

### Grid submission

I've now added scripts to `batchsubmit` to do all of the above with a single condor submission, allowing for larger samples and far less babysiting. See instructions there.
