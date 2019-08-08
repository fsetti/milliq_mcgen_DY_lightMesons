import numpy as np
import matplotlib.pyplot as plt
import ROOT as r

def parse_file(fid):
    vals = []
    for line in fid:
        if line.startswith("#"):
            continue
        vals.append(map(float, line.strip().strip("{}").split(",")))
    vals = np.array(vals)
    return vals


def merge(fine_file, coarse_file, eta_scale=1.2, merge_point=8.0, do_scale=True):
    fc = open(coarse_file)
    ff = open(fine_file)
    valsc = parse_file(fc)
    valsf = parse_file(ff)
    # if it is in the (pt, up, down) format, add a column for "central"
    if valsf.shape[1] == 3:
        valsf = np.append(valsf, valsf[:,2].reshape(valsf.shape[0],1), axis=1)
        valsf[:,2] = 0.5*(valsf[:,1] + valsf[:,3])
    # since they are given in eta [-1,1], and the coarse is [-1.2,1.2]
    valsf[:,1:] *= eta_scale
    new_row = valsf[-1,:] + (valsf[-1,:] - valsf[-2,:])
    valsf = np.append(valsf, new_row.reshape(1,4), axis=0)
    
    idxc = np.argmax(np.abs(valsc[:,0] - merge_point) < 1e-5)
    idxf = np.argmax(np.abs(valsf[:,0] - merge_point) < 1e-5)
    if valsc[idxc,0] < merge_point-1e-5 or valsf[idxf,0] > merge_point+1e-5:
        raise Exception()

    if do_scale:
        scale = valsc[idxc,2] / valsf[idxf,2]
        print "Scale fine:", scale
        valsf[:,1:] *= scale

    vals = np.append(valsf[:idxf,:], valsc[idxc:,:], axis=0)

    # extend down to 0
    new_row = vals[0,:] - (vals[1,:] - vals[0,:])
    vals = np.append(new_row.reshape(1,4), vals, axis=0)

    return vals[:,0], vals[:,1], vals[:,2], vals[:,3]

type_ = "jpsi"
# type_ = "psiprime"
if type_ == "jpsi":
    merge_point = 8.0
    pt, dn, cn, up = merge("Jpsi_fine-0-10.txt", "../CMS_Jpsi_tot_0_1.2_Tev_13_CMS_1.txt", eta_scale=1.2, merge_point=merge_point, do_scale=True)
if type_ == "psiprime":
    merge_point = 5.0
    pt, dn, cn, up = merge("cc_Psi2S_fine-0-10.txt", "../CMS_Psi2S_tot_0_1.2_Tev_13_CMS_1.txt", eta_scale=1.0, merge_point=merge_point, do_scale=False)

dpt = 0.05
fine_pt = np.arange(0.0, pt[-1]+1e-6, dpt)
fine_dn = np.interp(fine_pt, pt, dn)
fine_cn = np.interp(fine_pt, pt, cn)
fine_up = np.interp(fine_pt, pt, up)
i = np.argmax(fine_pt >= merge_point)
fine_dn[i:] = np.exp(np.interp(fine_pt[i:], pt, np.log(dn)))
fine_cn[i:] = np.exp(np.interp(fine_pt[i:], pt, np.log(cn)))
fine_up[i:] = np.exp(np.interp(fine_pt[i:], pt, np.log(up)))

fout = r.TFile("merged_jpsi.root" if type_=="jpsi" else "merged_psiprime.root", "RECREATE")
minpt = 0.0
maxpt = fine_pt[-1]
nbins = int((maxpt - minpt) / (2*dpt))
h_dn = r.TH1D("down",    ";p_{T} [GeV];dsigma / dpt [nb/GeV]", nbins, minpt, maxpt)
h_cn = r.TH1D("central", ";p_{T} [GeV];dsigma / dpt [nb/GeV]", nbins, minpt, maxpt)
h_up = r.TH1D("up",      ";p_{T} [GeV];dsigma / dpt [nb/GeV]", nbins, minpt, maxpt)
for i in range(nbins):
    h_dn.SetBinContent(i+1, fine_dn[2*i+1])
    h_cn.SetBinContent(i+1, fine_cn[2*i+1])
    h_up.SetBinContent(i+1, fine_up[2*i+1])
h_dn.Write()
h_cn.Write()
h_up.Write()
fout.Close()

plt.plot(pt, cn, 'b-o', lw=2)
plt.plot(fine_pt, fine_cn, 'r-o', ms=3.0)

plt.gca().set_xlim(0, 20)
# plt.gca().set_yscale('log')

plt.show()

