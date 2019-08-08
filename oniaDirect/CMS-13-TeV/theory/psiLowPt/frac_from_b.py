import numpy as np
import matplotlib.pyplot as plt
import ROOT as r

fs = []
fs.append(r.TFile("merged_jpsi.root"))
fs.append(r.TFile("../../../../oniaFromB/psi.root"))
fs.append(r.TFile("merged_psiprime.root"))
fs.append(r.TFile("../../../../oniaFromB/psiprime.root"))

hs = [f.Get("central") for f in fs]

pts = []
xss = []
for h in hs:
    pts.append([])
    xss.append([])
    for i in range(h.GetNbinsX()):
        pts[-1].append(h.GetBinCenter(i+1))
        xss[-1].append(h.GetBinContent(i+1))
    pts[-1] = np.array(pts[-1])
    xss[-1] = np.array(xss[-1])

new_x = np.arange(0.1, 50.01, 0.1)
new_xss = []
for i in range(len(pts)):
    new_xss.append(np.interp(new_x, pts[i], xss[i]))

# correct for different eta bounds
new_xss[0] /= 1.2
new_xss[2] /= 1.2

# b's are in pb, direct in nb
new_xss[1] /= 1000
new_xss[3] /= 1000

ratio_psi = new_xss[1] / (new_xss[0] + new_xss[1])
ratio_psip = new_xss[3] / (new_xss[2] + new_xss[3])
# ratio_psi = new_xss[1] / (new_xss[0])
# ratio_psip = new_xss[3] / (new_xss[2])

plt.plot(new_x, ratio_psi, 'r-', lw=2, label=r"$\mathrm{J/\psi}$")
plt.plot(new_x, ratio_psip, 'b-', lw=2, label=r"$\mathrm{\psi(2S)}$")
plt.legend(loc='upper left', fontsize='x-large')
plt.xlabel("$p_T$ [GeV]")
plt.ylabel("Fraction from b hadrons")
plt.grid()
plt.gca().set_xlim(0,40)
# plt.savefig("/home/users/bemarsh/public_html/milliqan/milliq_mcgen/psi-b-ratio.png")
# plt.savefig("/home/users/bemarsh/public_html/milliqan/milliq_mcgen/psi-b-ratio.pdf")
plt.savefig("psi-b-ratio.png")
plt.savefig("psi-b-ratio.pdf")

plt.show()
