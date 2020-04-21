import json
import numpy as np
import matplotlib.pyplot as plt
import ROOT as r

systs = json.load(open("systs/v8_v1_save2m.json"))
toplot = "omega_xs"

qs = []
ms = []

for sq in systs:
    q = float(sq.split("_")[1].replace("p","."))
    if q not in qs:
        qs.append(q)
    for sm in systs[sq]:
        m = float(sm.split("_")[1].replace("p","."))
        if m not in ms:
            ms.append(m)

qs = sorted(qs)
ms = sorted(ms)

logq = np.log10(qs)
logm = np.log10(ms)

binsq = 0.5*(logq[:-1] + logq[1:])
binsm = 0.5*(logm[:-1] + logm[1:])

binsq = np.insert(binsq, 0, binsq[0] - (binsq[1]-binsq[0]))
binsq = np.insert(binsq, binsq.size, binsq[-1] + (binsq[-1]-binsq[-2]))
binsm = np.insert(binsm, 0, binsm[0] - (binsm[1]-binsm[0]))
binsm = np.insert(binsm, binsm.size, binsm[-1] + (binsm[-1]-binsm[-2]))

binsq = 10**binsq
binsm = 10**binsm

# for m in binsm:
#     plt.plot([m]*2, [binsq[0],binsq[-1]], 'k--')
# for q in binsq:
#     plt.plot([binsm[0],binsm[-1]], [q]*2, 'k--')
# plt.gca().set_xscale("log")
# plt.gca().set_yscale("log")
# plt.show()

r.gStyle.SetOptStat(0)
r.gStyle.SetNumberContours(255)
r.gStyle.SetPalette(r.kLightTemperature)
h = r.TH2D("h",";m [GeV];Q/e", binsm.size-1, binsm, binsq.size-1, binsq)

maxval = 0.0
for q in qs:
    for m in ms:
        sq = "q_"+str(q).replace(".","p")
        sm = "m_"+str(m).replace(".","p")
        val = systs[sq][sm].get(toplot, (0.,0.))[0]
        maxval = max(abs(val), maxval)
        h.Fill(m, q, val)
h.GetZaxis().SetRangeUser(-maxval, maxval)

c = r.TCanvas()
c.SetLogx()
c.SetLogy()
h.Draw("colz")

raw_input()
