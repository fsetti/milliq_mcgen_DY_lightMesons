import os
import ROOT as r
from math import *
from tqdm import tqdm
from patterns import *

# TAG = "v5_v6_dens1p00_1cm"
TAG = "v5_v6_kuhn_nodisp_1cm"
HIT_THRESH = 0.01
# f = r.TFile("/nfs-7/userdata/bemarsh/milliqan/milliq_mcgen/merged_sim/muons_v5_v6_dens1p00/skim_fourSlab/muons_all.root")
f = r.TFile("/nfs-7/userdata/bemarsh/milliqan/milliq_mcgen/merged_sim/muons_v5_v6_kuhn_nodisp/skim_fourSlab/muons_all.root")
t = f.Get("Events")

def pass_pattern(pattern, hits):
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            if pattern[i][j]==1 and not hits[i][j]:
                return False
            if pattern[i][j]==-1 and hits[i][j]:
                return False
    return True

h_top = r.TH1D("h_top","",len(patts_top), 0, len(patts_top))
h_side = r.TH1D("h_side","",len(patts_side), 0, len(patts_side))
hs_angles_top = [r.TH1D("h_top_angles_"+str(i),"",100,-10,10) for i in range(len(patts_top))]
hs_angles_side = [r.TH1D("h_side_angles_"+str(i),"",100,-10,10) for i in range(len(patts_side))]
Nevt = t.GetEntries()
for ievt in tqdm(range(Nevt)):
# for ievt in tqdm(range(100)):
    t.GetEntry(ievt)

    if t.hit_p_slabs != 15:
        continue
    if t.hit_p_nbars < 2:
        continue

    idxs = list(t.hit_p_bar_idxs)
    dists = list(t.hit_p_bar_dists)
    weight = t.xsec*t.filter_eff/t.n_events_total * 35000
    thetaX = atan(t.hit_p_p4.Px() / t.hit_p_p4.Pz()) * 180/pi
    thetaY = atan(t.hit_p_p4.Py() / t.hit_p_p4.Pz()) * 180/pi
    
    hit = [(idx in idxs and dists[idxs.index(idx)]>HIT_THRESH) for idx in range(18)]
    
    hits_top = [
        [hit[12] or hit[14] or hit[16], hit[13] or hit[15] or hit[17]],
        [hit[6]  or hit[8]  or hit[10], hit[7]  or hit[9]  or hit[11]],
        [hit[0]  or hit[2]  or hit[4],  hit[1]  or hit[3]  or hit[5]],
    ]

    hits_side = [
        [hit[16] or hit[17], hit[14] or hit[15], hit[12] or hit[13]],
        [hit[10] or hit[11], hit[8]  or hit[9],  hit[6]  or hit[7]],
        [hit[4]  or hit[5],  hit[2]  or hit[3],  hit[0]  or hit[1]],
        ]

    for ipatt,patt in enumerate(patts_top):
        if pass_pattern(patt, hits_top):
            h_top.Fill(ipatt, weight)
            hs_angles_top[ipatt].Fill(thetaY, weight)

    for ipatt,patt in enumerate(patts_side):
        if pass_pattern(patt, hits_side):
            h_side.Fill(ipatt, weight)
            hs_angles_side[ipatt].Fill(thetaX, weight)

os.system("mkdir -p outputs")
fout = r.TFile(os.path.join("outputs",TAG+".root"), "RECREATE")
h_top.Write()
h_side.Write()
for h in hs_angles_top:
    h.Write()
for h in hs_angles_side:
    h.Write()
fout.Close()


