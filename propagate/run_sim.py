import sys
from array import array
import numpy as np
import ROOT as r
from millisim.Environment import Environment
from millisim.Integrator import Integrator
from millisim.Detector import *
try:
    from tqdm import tqdm
    loaded_tqdm = True
except ImportError:
    tqdm = lambda x:x
    loaded_tqdm = False
 
if len(sys.argv) < 3:
    print "usage: {0} <Q> <input_file>".format(sys.argv[0])
    exit(1)

DO_DRAW = False
   
## CONFIGURABLE PARAMS ##

q = float(sys.argv[1])
dist_to_detector = 33.
eta = 0.16
det_width = 1.0  # in m
det_height = 1.0 # in m
# det_width = None
# det_height = None
rock_begins = dist_to_detector - 17.0

dt = 0.1
max_nsteps = 3700

# if outside of these bounds, don't bother simulating
# the phi bounds are negated for negatively charged mCP's
etamin = eta - 0.12
etamax = eta + 0.12
phimin = -0.03
phimax = 2.05

# pt cuts (if pt is less than pt_cut for a given mass, don't bother propagating)
m_vals  = [0.01, 0.05, 0.1,  0.2, 0.3, 0.4, 0.5,  0.7, 1.0, 1.4, 1.4, 1.8, 2.0,  3.0, 4.0, 5.0]
pt_cuts = [0.15, 0.20, 0.25, 0.3, 0.4, 0.5, 0.55, 0.7, 0.9, 1.1, 1.2, 1.3, 1.45, 1.9, 2.3, 2.7]

#########################

env = Environment(
    mat_setup = 'cms',
    bfield = 'cms',
    bfield_file = "MilliqanSim/bfield/bfield_coarse.pkl",
    rock_begins = rock_begins
)

itg = Integrator(
    environ = env,
    Q = q,
    m = 1, # overwritten later
    dt = dt,
    nsteps = max_nsteps,
    cutoff_dist = dist_to_detector + 5,
    cutoff_axis = 'R',
    use_var_dt = True,
    lowv_dx = 0.03,
    multiple_scatter = 'pdg',
    do_energy_loss = True,
    randomize_charge_sign = False,
    )

det = PlaneDetector(
    dist_to_origin = dist_to_detector,
    eta = eta,
    phi = 0.0,
    width = det_width,
    height = det_height,
)

mdet = MilliqanDetector(
    dist_to_origin = dist_to_detector,
    eta = eta,
    phi = 0.0,
    nrows = 3,
    ncols = 2,
    nlayers = 3,
    # bar_width = 1.0,
    # bar_height = 1.0,
    # bar_length = 2.0,
    # bar_gap = 0.50,
    # layer_gap = 1.0,
    bar_width = 0.05,
    bar_height = 0.05,
    bar_length = 0.86,
    bar_gap = 0.01,
    layer_gap = 0.20,
)

fin = r.TFile.Open(sys.argv[2])
tin = fin.Get("Events")

fout = r.TFile("output.root", "RECREATE")

# copy tree and initialize new branches
tout = tin.CopyTree("")
sim_q = np.array([itg.Q], dtype=float)
does_hit_p = np.zeros(1, dtype=bool)
hit_p_xyz = r.TVector3()
hit_p_p4 = r.TLorentzVector()
does_hit_m = np.zeros(1, dtype=bool)
hit_m_xyz = r.TVector3()
hit_m_p4 = r.TLorentzVector()
hit_p_nbars = np.zeros(1, dtype=int)
hit_p_nlayers = np.zeros(1, dtype=int)
hit_p_line = np.zeros(1, dtype=bool)
hit_m_nbars = np.zeros(1, dtype=int)
hit_m_nlayers = np.zeros(1, dtype=int)
hit_m_line = np.zeros(1, dtype=bool)
b_sim_q = tout.Branch("sim_q", sim_q, "sim_q/D")
b_does_hit_p = tout.Branch("does_hit_p", does_hit_p, "does_hit_p/O")
b_hit_p_xyz = tout.Branch("hit_p_xyz", hit_p_xyz)
b_hit_p_p4 = tout.Branch("hit_p_p4", hit_p_p4)
b_does_hit_m = tout.Branch("does_hit_m", does_hit_m, "does_hit_m/O")
b_hit_m_xyz = tout.Branch("hit_m_xyz", hit_m_xyz)
b_hit_m_p4 = tout.Branch("hit_m_p4", hit_m_p4)
b_hit_p_nbars = tout.Branch("hit_p_nbars", hit_p_nbars, "hit_p_nbars/I")
b_hit_p_nlayers = tout.Branch("hit_p_nlayers", hit_p_nlayers, "hit_p_nlayers/I")
b_hit_p_line = tout.Branch("hit_p_line", hit_p_line, "hit_p_line/O")
b_hit_m_nbars = tout.Branch("hit_m_nbars", hit_m_nbars, "hit_m_nbars/I")
b_hit_m_nlayers = tout.Branch("hit_m_nlayers", hit_m_nlayers, "hit_m_nlayers/I")
b_hit_m_line = tout.Branch("hit_m_line", hit_m_line, "hit_m_line/O")

bs = [b_sim_q, b_does_hit_p, b_hit_p_xyz, b_hit_p_p4, b_does_hit_m, b_hit_m_xyz, b_hit_m_p4,
      b_hit_p_nbars,b_hit_p_nlayers,b_hit_p_line,b_hit_m_nbars,b_hit_m_nlayers,b_hit_m_line]

Nevt = tin.GetEntries()
evt_start = 0
# Nevt = 10
# evt_start = 5528
print "Simulating {0} events, 2 trajectories per event".format(Nevt)

trajs = []
n_hits = 0
for i in tqdm(range(evt_start, evt_start+Nevt)):
    
    if not loaded_tqdm and i%100 == 0:
        print "{0} / {1}".format(i, Nevt)

    tin.GetEntry(i)
    for b in bs:
        b.GetEntry(i)

    # set the seeds to 1 so results are reproducible
    r.gRandom.SetSeed(tin.event)
    np.random.seed(tin.event)

    def do_propagate(p4, q, traj_array=None):
        itg.m = p4.M() * 1000.0
        itg.Q = q
        
        within_bounds = True
        if p4.Eta() < etamin or p4.Eta() > etamax:
            within_bounds = False
        if q>0 and (p4.Phi() < phimin or p4.Phi() > phimax):
            within_bounds = False
        if q<0 and (p4.Phi() < -phimax or p4.Phi() > -phimin):
            within_bounds = False
        pt_cut = np.interp(p4.M(), m_vals, pt_cuts) * (q/0.1)**2
        if p4.Pt() < pt_cut:
            within_bounds = False

        if within_bounds:
            x0 = 1000.*np.array([0., 0., 0., p4.Px(), p4.Py(), p4.Pz()])
            traj,_ = itg.propagate(x0)
            idict = det.FindIntersection(traj)
            bars_intersects = mdet.FindEntriesExits(traj)
            # if traj_array is not None and idict is not None:
            if traj_array is not None:
                traj_array.append(traj)
            return idict, bars_intersects
        else:
            return None, None

    idict_p, bars_p = do_propagate(tin.p4_p, q, trajs if DO_DRAW else None)
    idict_m, bars_m = do_propagate(tin.p4_m, -q, trajs if DO_DRAW else None)    
    
    if idict_p is not None:
        does_hit_p[0] = True
        hit_p_xyz.SetXYZ(idict_p["v"], idict_p["w"], det.dist_to_origin)
        px = np.dot(idict_p["p_int"], det.unit_v) / 1000.
        py = np.dot(idict_p["p_int"], det.unit_w) / 1000.
        pz = np.dot(idict_p["p_int"], det.norm) / 1000.
        E = np.sqrt(np.linalg.norm(idict_p["p_int"])**2 + itg.m**2) / 1000.
        hit_p_p4.SetPxPyPzE(px,py,pz,E)
        hit_p_nbars[0] = len(bars_p)
        hit_p_nlayers[0] = len(set([i[0][0] for i in bars_p]))
        hit_p_line[0] = mdet.hits_straight_line(bars_p)
    else:
        does_hit_p[0] = False
        hit_p_xyz.SetXYZ(0,0,0)
        hit_p_p4.SetPxPyPzE(0,0,0,0)
        hit_p_nbars[0] = 0
        hit_p_nlayers[0] = 0
        hit_p_line[0] = False

    if idict_m is not None:
        does_hit_m[0] = True
        hit_m_xyz.SetXYZ(idict_m["v"], idict_m["w"], det.dist_to_origin)
        px = np.dot(idict_m["p_int"], det.unit_v) / 1000.
        py = np.dot(idict_m["p_int"], det.unit_w) / 1000.
        pz = np.dot(idict_m["p_int"], det.norm) / 1000.
        E = np.sqrt(np.linalg.norm(idict_m["p_int"])**2 + itg.m**2) / 1000.
        hit_m_p4.SetPxPyPzE(px,py,pz,E)
        hit_m_nbars[0] = len(bars_m)
        hit_m_nlayers[0] = len(set([i[0][0] for i in bars_m]))
        hit_m_line[0] = mdet.hits_straight_line(bars_m)
    else:
        does_hit_m[0] = False
        hit_m_xyz.SetXYZ(0,0,0)
        hit_m_p4.SetPxPyPzE(0,0,0,0)
        hit_m_nbars[0] = 0
        hit_m_nlayers[0] = 0
        hit_m_line[0] = False

    for b in bs:
        ret = b.Fill()
        if ret < 0:
            print "BAD BRANCH WRITE:", i, b.GetName()
            print "    does_hit_m:", does_hit_m[0]
            print "    does_hit_p:", does_hit_p[0]
            print "      hit_m_p4:", hit_m_p4.Px(), hit_m_p4.Py(), hit_m_p4.Pz()
            print "      hit_p_p4:", hit_p_p4.Px(), hit_p_p4.Py(), hit_p_p4.Pz()
            # print "    trying to write again..."
            # b.GetEntry(i)
            # ret = b.Fill()
            # if ret < 0:
            #     print "   FAILED"
            # else:
            #     print "   SUCCESS"

# skim tree, keeping only events with >=1 hit
tout = tout.CopyTree("(does_hit_m || does_hit_p) && Entry$ < {0}".format(Nevt))

# compute hit efficiency and add to tree
hit_eff = np.array([float(tout.GetEntries())/Nevt], dtype=float)
print "Hit efficiency:", hit_eff[0]
b = tout.Branch("hit_eff", hit_eff, "hit_eff/D")
for i in range(tout.GetEntries()):
    b.GetEntry(i)
    b.Fill()

tout.Write("Events", r.TObject.kWriteDelete)
fout.Close()


if DO_DRAW:
    import matplotlib.pyplot as plt
    from millisim.Drawing import *
    plt.figure(num=1, figsize=(15,7))
    Draw3Dtrajs(trajs, subplot=121)
    # the four corners
    if det.width is not None and det.height is not None:
        c1,c2,c3,c4 = det.GetCorners()
        DrawLine(c1,c2,is3d=True,c='k')
        DrawLine(c2,c3,is3d=True,c='k')
        DrawLine(c3,c4,is3d=True,c='k')
        DrawLine(c4,c1,is3d=True,c='k')

    mdet.draw(plt.gca(), c='0.75', draw_containing_box=False)
    plt.gca().set_xlim(mdet.center_3d[0]-8, mdet.center_3d[0]+8)
    plt.gca().set_ylim(mdet.center_3d[1]-8, mdet.center_3d[1]+8)
    plt.gca().set_zlim(mdet.center_3d[2]-8, mdet.center_3d[2]+8)

    colors = ['r','g','b','c','m','y']
    hit_boxes = set()
    for i,traj in enumerate(trajs):
        # idict = det.FindIntersection(traj)
        # if idict is not None:
        #     DrawLine(idict["x_int"], idict["x_int"], is3d=True, linestyle="None", marker='o', color='r')
        isects = mdet.FindEntriesExits(traj)
        for isect in isects:
            hit_boxes.add(isect[0])
            c = colors[i % len(colors)]
            DrawLine(isect[1], isect[1], is3d=True, linestyle='None', marker='o', mfc=c, mec='k')
            DrawLine(isect[2], isect[2], is3d=True, linestyle='None', marker='o', mfc='w', mec=c)

    for ilayer,irow,icol in hit_boxes:
        mdet.bars[ilayer][irow][icol].draw(plt.gca(), c='k')

    DrawXYslice(trajs, subplot=122)
    plt.show()

