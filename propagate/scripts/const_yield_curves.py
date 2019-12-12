import cPickle as pickle
import numpy as np
import matplotlib.pyplot as plt
import ROOT as r

charges = [0.005, 0.01, 0.02, 0.03, 0.05, 0.07, 0.1, 0.14, 0.2, 0.3]
extra_charges = [0.001, 0.002, 0.003]
DO_NPE1 = True

fin = r.TFile("rate_files/v7_v1.root")
if DO_NPE1:
    fnpe = r.TFile("geant_analysis/rate_files/v7_v1_save2m_skim0p25m_simmcp_v1_v1.root")

gs = {}
for q in charges:
    gs[q] = fin.Get("line_rate_q{0}_total".format(str(q).replace(".","p")))
    
masses = []
yields = {}

npoints = gs[charges[0]].GetN()
for i in range(npoints):
    x, y = r.Double(), r.Double()
    gs[charges[0]].GetPoint(i, x, y)
    if x > 10:
        continue
    m = x
    if m==0.01:
        continue
    masses.append(m)
    yields[m] = []
    for q in charges:
        gs[q].GetPoint(i, x, y)
        p0 = 0
        if DO_NPE1:
            h = fnpe.Get("h_barNPE_m{0}_q{1}".format(str(m).replace(".","p"), str(q).replace(".","p")))
            p0 = h.GetBinContent(1) / h.Integral(1,-1)
        yields[m].append(float(y) * (1-p0)**3)

    y0 = yields[m][0]
    p0 = 0
    if DO_NPE1:
        h = fnpe.Get("h_barNPE_m{0}_q{1}".format(str(m).replace(".","p"), str(charges[0]).replace(".","p")))
        p0 = h.GetBinContent(1) / h.Integral(1,-1)
        # meannpe = h.GetMean()
        meannpe = -np.log(p0) if p0>0 else 100
    for q in extra_charges[::-1]:
        newp0 = 0
        if DO_NPE1:
            newp0 = np.exp(-meannpe*(q/charges[0])**2)
        y = y0*(q/charges[0])**2 * (1-newp0)**3/(1-p0)**3
        yields[m].insert(0, y)        

    yields[x] = np.array(yields[x])

charges = extra_charges + charges

def get_charge_for_yield(charges, yields, N, mode=0):
    if N < yields[0]:
        return np.sqrt(N/yields[0]) * charges[0]
    if N > yields[-1]:
        return np.sqrt(N/yields[-1]) * charges[-1]
    i = np.argmax(yields > N)
    q1 = np.sqrt(N/yields[i-1]) * charges[i-1]
    q2 = np.sqrt(N/yields[i]) * charges[i]
    frac1 = 1 - np.log(N/yields[i-1]) / np.log(yields[i]/yields[i-1])
    return frac1*q1 + (1-frac1)*q2

lims = {}
for N in [5,10,20]:
    lims[N] = []
    for m in masses:    
        lims[N].append(get_charge_for_yield(charges, yields[m], N))


# for m in masses:
#     for q in charges:
#         plt.plot([m], [q], 'o', color="0.7", markersize=5.0, markeredgecolor="0.7")
for m in masses+[14.0, 20.0, 28.0, 34.0, 40.0, 44.0, 48.0, 52.0, 58.0, 68.0, 80.0, 100.0]:
    plt.plot([m,m], [0.001,1.0], ':', color="0.5")
for q in charges:
    plt.plot([0.01,100], [q,q], ':', color="0.5")

plt.plot(masses, lims[5], 'g-o', label="N = 5")
plt.plot(masses, lims[10], 'b-o', label="N = 10")
plt.plot(masses, lims[20], 'r-o', label="N = 20")
# plt.plot(masses, lims[40], 'm-o', label="N = 40")

print masses
pickle.dump(lims, open("yield_contours.pkl", 'wb'))

# plt.plot([1e-2,1e2], [0.3,0.3], 'k--')

plt.gca().set_xscale('log')
plt.gca().set_yscale('log')
plt.gca().set_xlim(1e-2, 2e2)
plt.gca().set_ylim(1e-3, 1e0)
plt.xlabel("mCP mass [GeV]")
plt.ylabel("mCP Q/e")
plt.legend()



plt.savefig("/home/users/bemarsh/public_html/milliqan/milliq_mcgen/curves_const_yield.png", transparent=True)

# plt.show()
