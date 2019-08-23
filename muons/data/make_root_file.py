import sys
import numpy as np
import ROOT as r

fin = sys.argv[1]

data = []
with open(fin) as fid:
    for line in fid:
        if line.strip().startswith("#"):
            continue
        data.append(map(float, line.strip().split()))

data = np.array(data)

pt = data[:,0]
cn = data[:,1]
up = data[:,3]
dn = data[:,2]

dpt = 0.1
new_pt = np.arange(dpt/2, 300-dpt/2+1e-12, dpt)
new_cn = np.exp(np.interp(new_pt, pt, np.log(cn)))
new_up = np.exp(np.interp(new_pt, pt, np.log(up)))
new_dn = np.exp(np.interp(new_pt, pt, np.log(dn)))

nbins = int(300/dpt)
h_cn = r.TH1D("central", ";p_{T}(#mu) [GeV]; dsigma / dpt [pb/GeV]", nbins, 0, 300)
h_up = r.TH1D("up", ";p_{T}(#mu) [GeV]; dsigma / dpt [pb/GeV]", nbins, 0, 300)
h_dn = r.TH1D("down", ";p_{T}(#mu) [GeV]; dsigma / dpt [pb/GeV]", nbins, 0, 300)

for i in range(new_cn.size):
    h_cn.SetBinContent(i+1, new_cn[i])
    h_up.SetBinContent(i+1, new_up[i])
    h_dn.SetBinContent(i+1, new_dn[i])

fout = r.TFile(fin.replace(".txt",".root"), "RECREATE")
h_cn.Write()
h_up.Write()
h_dn.Write()
fout.Close()




