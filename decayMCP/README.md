### Generate mCP decays

Usage: 
```
./runDecays -d decay_mode -o outfile [-m m_mCP=0.001 (GeV)] [-n n_events=1000] \
               [-N n_events_total=n_events] [-e evtnum_offset=0] [-2 (if Run2)]
```

`decay_mode` is an integer specifiying which mode you want to generate. Currently supported:
1. B &rarr; J/&psi; X, J/&psi; &rarr; &chi;<sup>+</sup>&chi;<sup>&ndash;</sup>
2. B &rarr; &psi;(2S) X, &psi;(2S) &rarr; &chi;<sup>+</sup>&chi;<sup>&ndash;</sup>
3. &rho; &rarr; &chi;<sup>+</sup>&chi;<sup>&ndash;</sup>
4. &omega; &rarr; &chi;<sup>+</sup>&chi;<sup>&ndash;</sup>
5. &phi; &rarr; &chi;<sup>+</sup>&chi;<sup>&ndash;</sup>
6. &pi;<sup>0</sup> &rarr; &chi;<sup>+</sup>&chi;<sup>&ndash;</sup>&gamma;
7. &eta; &rarr; &chi;<sup>+</sup>&chi;<sup>&ndash;</sup>&gamma;
8. &eta;' &rarr; &chi;<sup>+</sup>&chi;<sup>&ndash;</sup>&gamma;
9. &omega; &rarr; &chi;<sup>+</sup>&chi;<sup>&ndash;</sup>&pi;<sup>0</sup>
10. &eta;' &rarr; &chi;<sup>+</sup>&chi;<sup>&ndash;</sup>&omega;
11. J/&psi; &rarr; &chi;<sup>+</sup>&chi;<sup>&ndash;</sup>
12. &psi;(2S) &rarr; &chi;<sup>+</sup>&chi;<sup>&ndash;</sup>
13. &Upsilon;(1S) &rarr; &chi;<sup>+</sup>&chi;<sup>&ndash;</sup>
14. &Upsilon;(2S) &rarr; &chi;<sup>+</sup>&chi;<sup>&ndash;</sup>
15. &Upsilon;(3S) &rarr; &chi;<sup>+</sup>&chi;<sup>&ndash;</sup>

`outfile` is the name of the ROOT file to output to.

`m_mCP` is the mass of the milli-charged particle, in GeV.

`n_events` is the number of events to generate.

`n_events_total` is a constant copied into the tree directly, and is meant to represent the total number of events generated in a given sample
(for the case where one sample is split over many files). This makes it easier to compute the per-event weight when looping over events later.

`evtnum_offset` is the value at which to start numbering events (so if you're making multiple files, event numbers don't overlap).

**Note:** the milliQan demonstrator eta/phi location is hardcoded into runDecays.cc. If this changes, you need to edit this.

### File format
Output root tree has the following branches:
* `event`: integer event number, starting from 0
* `n_events_total`: total number of events in the sample. Defaults to the number of events in the given file, but can be overridden
in the case that the sample is split over many files (see above)
* `decay_mode`: copy of the `decay_mode` argument to the program, defined above
* `parent_p4`: four-momentum of parent of mCP's (e.g. the J/&psi; for B &rarr; J/&psi; X, J/&psi; &rarr; &chi;<sup>+</sup>&chi;<sup>&ndash;</sup>)
* `parent_pdgId`: PDG ID of parent of mCP's
* `p4_p`: four-momentum of positively-charged mCP (in GeV)
* `p4_m`: four-momentum of negatively-charged mCP (in GeV)
* `xsec`: the cross-section of the process, before mCP BR, inclusively in pT/eta (in pb)
* `BR_q1`: the BR to mCPs for q(mCP)=1.
* `filter_eff`: efficiency of any eta/phi cuts applied to the mCP's
* `weight`: event weight, currently just equal to 1.0 for all events
* `weight_up` the up-variation weight. Computed as `pdf_up(pt) / pdf_central(pt)`, where pt is pt of mCP parent, when these functions are available
* `weight_dn` the down-variation weight. Computed as `pdf_down(pt) / pdf_central(pt)`, where pt is pt of mCP parent, when these functions are available

**note:** the proper per-event weight is given by:
```
Q^2 * xsec * BR_q1 * filter_eff * weight[_up/dn] * LUMI(pb^-1) / n_events_total
```

**units:** throughout this program, all masses/momenta are in GeV, and cross sections in pb.
