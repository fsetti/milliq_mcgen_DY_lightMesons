### Generate mCP decays

Usage: `./runDecays <decayMode> <mMCP> <BR> <nEvents> <outfile>`

`decayMode` is an integer specifiying which mode you want to generate. Currently supported:
1. B -> psi X, psi -> mCP mCP
2. B -> psi' X, psi' -> mCP mCP

`mMCP` is the mass of the milli-charged particle.

`BR` is the branching ratio into mCP's for q(mCP)=1.

`nEvents` is the number of events to generate.

`outfile` is the name of the ROOT file to output to.
