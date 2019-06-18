### Generate mCP decays

Usage: `./runDecays <decayMode> <mMCP> <nEvents> <outfile>`

`decayMode` is an integer specifiying which mode you want to generate. Currently supported:
1. B -> psi X, psi -> mCP mCP
2. B -> psi' X, psi' -> mCP mCP

`mMCP` is the mass of the milli-charged particle.

`nEvents` is the number of events to generate.

`outfile` is the name of the ROOT file to output to.

### File format
Output root tree has the following branches:
* `event`: integer event number, starting from 0
* `decay_flag`: copy of the `decayMode` argument to the program, defined above
* `parent_p4`: four-momentum of parent of mCP's (e.g. the J/psi for B -> J/psi X, J/psi -> mCP mCP)
* `parent_pdgId`: PDG ID of parent of mCP's
* `p4_1`: four-momentum of first mCP
* `p4_2`: four-momentum of second mCP
* `xsec`: the cross-section of the process, before mCP BR, inclusively in pT/eta
* `BR_q1`: the BR to mCPs for q(mCP)=1.
* `weight`: event weight, currently just equal to 1.0 for all events
* `weight_up` the up-variation weight. Currently, computed as `pdf_up(pt) / pdf_central(pt)`, where pt is pt of mCP parent
* `weight_dn` the down-variation weight. Currently, computed as `pdf_down(pt) / pdf_central(pt)`, where pt is pt of mCP parent
