## Master milliQan MC generation tutorial
The full milliQan simulation pipeline involves numerous steps, pulling from multiple repositories written by multiple people. The initial event generation is handled by this repository, the propagation engine is in [MilliqanSim](https://github.com/bjmarsh/MilliqanSim), Geant4 simulation and ntuplization is in [milliQanDemoSim](https://github.com/milliQan-sw/milliQanDemoSim), and pulse injection is handled by macros in [milliqanOffline](https://github.com/milliQan-sw/milliqanOffline). Various scripts for analysis, plotting, and deriving calibrations/systematics are scattered across these repositories.

Here I've tried to organize everything into a single place, to provide some kind of instruction for anyone in the future trying to run through this whole process.

### Event Generation
Generation of initial events (mCPs or beam muons) is handled by this [milliq_mcgen](https://github.com/bjmarsh/milliq_mcgen) repository. First, we consider mCPs. Cross sections and p<sub>T</sub> distributions for all of the various production modes come from different places. All of these should already be in place in a fresh clone of the repository, and you can proceed straight to the generation, but I list them here for reference.
* Light meson production is done with pythia. All use the pythia8 Monash2013 tune, except for &phi;s which use the pythia6 DW tune. Instructions/scripts for running pythia and generating the p<sub>T</sub> distributions can be found in the [mesonPt](../mesonPt) directory. The output is a set of histograms with units of "particles per minbias event per 50 MeV bin" (for the eta range |&eta;|<2). So, the total cross section for a given particle is the sum of all bin contents ("particles per minbias event") times the MinBias cross section. The histograms used in the demonstrator paper are in [pt_dists.root](../mesonPt/pt_dists.root).
* J/&psi; and &psi;' production come from theory. We have merged together separate low-p<sub>T</sub> and high-p<sub>T</sub> files; see [oniaDirect/CMS-13-TeV/theory/psiLowPt](../oniaDirect/CMS-13-TeV/theory/psiLowPt) for the scripts and merged files (merged_*.root). These files contain d&sigma;/dp<sub>T</sub> histograms, for |&eta;|<1.2.
* Upsilon production comes from experiment (high-p<sub>T</sub> from 13 TeV ATLAS data, low-p<sub>T</sub> from 7 TeV CMS data). See [oniaDirect/upsilon](../oniaDirect/upsilon) for scripts and merged files (ups*_combined.root). The histograms again contain d&sigma;/dp<sub>T</sub> for |&eta;|<1.2, but this time the branching ratios to &mu;&mu; are folded in; this is divided out in the generation stage).
* Drell-Yan is taken from MadGraph. See the [madgraphDY](../madgraphDY) directory for instructions. For the purposes of the demonstrator paper, since DY is subdominant everywhere important, it was sufficient to run jobs locally overnight with the `parallel` utility. For higher stats/more mass points, grid submission will probably need implemented.

For all non-DY modes, we need to convert the differential cross section distributions into ntuples of generated mCPs. This is done with the tools in the [decayMCP](../decayMCP) directory. `DecayGen` is a class that interfaces with the various histograms described above, extracts total cross sections/BRs, and performs the decays. It shouldn't need to be touched unless you change the format of cross section histograms (or want to change hardcoded MinBias xsec at the top). The ntuples are generated with `runDecays`, following the instructions in [decayMCP](../decayMCP). It produces an `MCPTree`, with branches described in the README.

For a full production, it is easiest to submit jobs to the grid. Scripts and instructions are in [decayMCP/localbatch](../decayMCP/localbatch). These scripts automatically adjust the number of events in each production mode so that event weights are ~constant (i.e. # of events is proportional to xsec*BR). If this is done correctly, you should have a hadoop directory structured as `<mass_dir>/<mode_dir>/output_*.root` with MCPTrees in the ROOT files.

**Misc:** C++ files containing the functions used to compute branching ratios and do the four-vector decay math are in [utils](../utils). Python versions (not really used for anything any more) are in [scripts](../scripts). These shouldn't need to be touched unless you find a bug (hopefully not, since we will have published with that bug....). Scripts to generate a ROOT file with mCP cross sections and turn these into the [xsec plot used in the paper](http://uaf-8.t2.ucsd.edu/~bemarsh/milliqan/mcp-xsec.pdf) are in [scripts/plot-xsecs](../scripts/plot-xsecs).

### Propagation

### Geant4 simulation

### Geant ntuplization

### Pulse injection
