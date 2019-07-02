Takes the output of `decayMCP/runDecays` and propagates mCP's through CMS environment,
using the [MilliqanSim](https://github.com/bjmarsh/MilliqanSim/tree/master) package.
Adds branches to the tree indicating position and momentum upon intersection with the detector face.

Run `. setup.sh` to download the MilliqanSim repository (if this hasn't been done yet)
and set the correct PYTHONPATH environment variable.

There are configurable parameters at the top of `run_sim.py` that control the location
and size of the detector, as well as various simulation parameters.

After setting up, run with `python run_sim.py <Q> <input_file>`, where `Q` is the charge
of the mCP's you want to simulate. This will propagate all of the mCP's, add branches
to the tree, throw away events where there were no hits, and output to `output.root`.

This is slow! (tested at 1.5 Hz). To run over more than a few thousand events will 
need to submit jobs to the grid.

**Coordinates:** coordinates used for the position/momentum of hit are *not* in CMS coordinates.
x and y are parallel to the Milliqan detector face (x horizontal, y vertical), and z is perpendicular
(positive z points *into* the detector, in the same direction as traveling particles).

Below is a list of branches added to the tree (note that `*` can be either `p` or `m`, indicating
whether the branch is for the positively or negatively charged mCP).
* `sim_q`: the charge of the simulated mCP's
* `does_hit_*`: boolean indicating whether or not mCP hits detector
* `hit_*_xyz`: a TVector3 of hit position, in coordinates described above
* `hit_*_p4`: a TLorentzVector of momentum upon hit (also in above coordinate system)
* `hit_eff`: the fraction of events with at least 1 mCP hit (*not* the fraction of mCP's that hit).

