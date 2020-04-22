## Master milliQan MC generation tutorial
The full milliQan simulation pipeline involves numerous steps, pulling from multiple repositories written by multiple people. The initial event generation is handled by this repository, the propagation engine is in [MilliqanSim](https://github.com/bjmarsh/MilliqanSim), Geant4 simulation and ntuplization is in [milliQanDemoSim](https://github.com/milliQan-sw/milliQanDemoSim), and pulse injection is handled by macros in [milliqanOffline](https://github.com/milliQan-sw/milliqanOffline). Various scripts for analysis, plotting, and deriving calibrations/systematics are scattered across these repositories.

Here I've tried to organize everything into a single place, to provide some kind of instruction for anyone in the future trying to run through this whole process.

#### Event Generation
Generation of initial events (mCPs or beam muons) is handled by this [milliq_mcgen](https://github.com/bjmarsh/milliq_mcgen) repository. First, we consider mCPs. Cross sections and p<sub>T</sub> distributions for all of the various production modes come from different places:
* Light meson production is done with pythia. All use the pythia8 Monash2013 tune, except for &phi;s which use the pythia6 DW tune. Instructions for running pythia and generating the pT distributions can be [found here](../mesonPt). The output are histograms with units of "particles per minbias event per 50 MeV bin". So, the total cross section for a given particle is the sum of all bin contents ("particles per minbias event") times the MinBias cross section. The histograms used in the demonstrator paper are in [pt_dists.root](../mesonPt/pt_dists.root).

#### Propagation

#### Geant4 simulation

#### Geant ntuplization

#### Pulse injection
