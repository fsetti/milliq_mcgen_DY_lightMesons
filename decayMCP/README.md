### Generate mCP decays

Usage: `./runDecays <decayMode> <mMCP> <nEvents> <outfile>`

`decayMode` is an integer specifiying which mode you want to generate. Currently supported:
1. B &rarr; &psi; X, &psi; &rarr; &zeta;<sup>+</sup>&zeta;<sup>&ndash;</sup>
2. B &rarr; &psi;' X, &psi;' &rarr; &zeta;<sup>+</sup>&zeta;<sup>&ndash;</sup>
3. &rho; &rarr; &zeta;<sup>+</sup>&zeta;<sup>&ndash;</sup>
4. &omega; &rarr; &zeta;<sup>+</sup>&zeta;<sup>&ndash;</sup>
5. &phi; &rarr; &zeta;<sup>+</sup>&zeta;<sup>&ndash;</sup>
6. &pi;<sup>0</sup> &rarr; &zeta;<sup>+</sup>&zeta;<sup>&ndash;</sup>&gamma;
7. &eta; &rarr; &zeta;<sup>+</sup>&zeta;<sup>&ndash;</sup>&gamma;
8. &eta;' &rarr; &zeta;<sup>+</sup>&zeta;<sup>&ndash;</sup>&gamma;
9. &omega; &rarr; &zeta;<sup>+</sup>&zeta;<sup>&ndash;</sup>&pi;<sup>0</sup>
10. &eta;' &rarr; &zeta;<sup>+</sup>&zeta;<sup>&ndash;</sup>&omega;

`mMCP` is the mass of the milli-charged particle.

`nEvents` is the number of events to generate.

`outfile` is the name of the ROOT file to output to.

### File format
Output root tree has the following branches:
* `event`: integer event number, starting from 0
* `decay_flag`: copy of the `decayMode` argument to the program, defined above
* `parent_p4`: four-momentum of parent of mCP's (e.g. the J/&psi; for B &rarr; J/&psi; X, J/&psi; &rarr; &zeta;<sup>+</sup>&zeta;<sup>&ndash;</sup>)
* `parent_pdgId`: PDG ID of parent of mCP's
* `p4_1`: four-momentum of first mCP
* `p4_2`: four-momentum of second mCP
* `xsec`: the cross-section of the process, before mCP BR, inclusively in pT/eta
* `BR_q1`: the BR to mCPs for q(mCP)=1.
* `filter_eff`: efficiency of any eta/phi cuts applied
* `weight`: event weight, currently just equal to 1.0 for all events
* `weight_up` the up-variation weight. Computed as `pdf_up(pt) / pdf_central(pt)`, where pt is pt of mCP parent, when these functions are available
* `weight_dn` the down-variation weight. Computed as `pdf_down(pt) / pdf_central(pt)`, where pt is pt of mCP parent, when these functions are available

**note:** the proper per-event weight is given by `xsec * BR_q1 * filter_eff * weight[_up/dn] / Nevents`
