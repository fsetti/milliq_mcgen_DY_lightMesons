import cPickle as pickle
import numpy as np
from scipy.misc import factorial
import matplotlib.pyplot as plt
import ROOT as r

charges = [0.005, 0.007, 0.01, 0.014, 0.02, 0.03, 0.05, 0.07, 0.1, 0.14, 0.2, 0.3]
extra_charges = [0.001, 0.0014, 0.002, 0.0025, 0.003, 0.0035, 0.004, 0.0045]
DO_NPE1 = True
DO_RECOGEN = DO_NPE1 and True
NLAYERS=4
CONTOURS = [5,10,20,50]
DRAW_LOI_CURVES = True

fin = r.TFile("rate_files/v8_v1_save2m_FULLMQ.root")
if DO_NPE1:
    fnpe = r.TFile("geant_analysis/rate_files/v8_v1_save2m_skim0p25m_mcpData_v4_v2calib.root")
    if DO_RECOGEN:
        frecogen = r.TFile("mixed_analysis/recogen_templates/recogen_templates.root")

def get_p0(m, q, use_poisson=None):
    if not DO_NPE1:
        return 0
    if use_poisson:
        p0 = np.exp(-use_poisson)
    else:
        hgeant = fnpe.Get("h_barNPE_m{0}_q{1}".format(str(m).replace(".","p"), str(q).replace(".","p")))
        p0 = hgeant.GetBinContent(1) / hgeant.Integral(1,-1)
    if not DO_RECOGEN:
        return p0
    hrg = frecogen.Get("recogen_ch25")
    for i in range(1,10):
        if use_poisson:
            p0 += use_poisson**i*np.exp(-use_poisson)/factorial(i) * hrg.Integral(i+1, i+1, 1, 1) / hrg.Integral(i+1,i+1,1,-1)
        else:
            p0 += hgeant.GetBinContent(i+1) / hgeant.Integral(1,-1) * hrg.Integral(i+1, i+1, 1, 1) / hrg.Integral(i+1,i+1,1,-1)
    return p0

# print get_p0(0.35,0.005)
# h = fnpe.Get("h_barNPE_m0p35_q0p005")
# p0 = h.GetBinContent(1)/h.Integral(1,-1)
# print p0
# print get_p0(0.35, 0.005, use_poisson=p0)
# print get_p0(0.35, 0.005, use_poisson=p0*(.002/.005)**2)

gs = {}
for q in charges:
    gs[q] = fin.Get("line_rate_q{0}_total".format(str(q).replace(".","p")))
    
masses = []
yields = {}

npoints = gs[charges[0]].GetN()
for i in range(npoints):
    x, y = r.Double(), r.Double()
    gs[charges[0]].GetPoint(i, x, y)
    m = x
    if m in [0.01,0.04,0.07,0.14]:
        continue
    masses.append(m)
    yields[m] = []
    capped_m = min(m, 10.0)
    for q in charges:
        gs[q].GetPoint(i, x, y)
        p0 = 0
        if DO_NPE1:
            h = fnpe.Get("h_barNPE_m{0}_q{1}".format(str(capped_m).replace(".","p"), str(q).replace(".","p")))
            p0 = h.GetBinContent(1) / h.Integral(1,-1)
            p0 = get_p0(capped_m, q, use_poisson=-np.log(p0)*0.75 if p0>0 else 100)
        yields[m].append(float(y) * (1-p0)**NLAYERS)

    y0 = yields[m][0]
    p0 = 0
    if DO_NPE1:
        h = fnpe.Get("h_barNPE_m{0}_q{1}".format(str(capped_m).replace(".","p"), str(charges[0]).replace(".","p")))
        p0geant = h.GetBinContent(1) / h.Integral(1,-1)
        meannpe = -np.log(p0geant)*0.75 if p0geant>0 else 100
        p0 = get_p0(capped_m, charges[0], use_poisson=meannpe)
    for q in extra_charges[::-1]:
        newp0 = 0
        if DO_NPE1:
            newp0 = get_p0(capped_m, charges[0], use_poisson=meannpe*(q/charges[0])**2)
        y = y0*(q/charges[0])**2 * (1-newp0)**NLAYERS/(1-p0)**NLAYERS
        # if m==0.35:
        #     print q, p0geant, meannpe, p0, newp0
        yields[m].insert(0, y)        

    yields[x] = np.array(yields[x])

charges = extra_charges + charges

print charges
print yields[1.0]

def get_charge_for_yield(charges, yields, N, verbose=False):
    if N < yields[0]:
        return np.sqrt(N/yields[0]) * charges[0]
    if N > yields[-1]:
        return np.sqrt(N/yields[-1]) * charges[-1]
    i = np.argmax(yields > N)
    q1 = min(charges[i], np.sqrt(N/yields[i-1]) * charges[i-1])
    q2 = max(charges[i-1], np.sqrt(N/yields[i]) * charges[i])
    frac1 = 1 - np.log(N/yields[i-1]) / np.log(yields[i]/yields[i-1])
    # if i==1:
    #     frac1 = 0
    # if verbose:
    #     print i, q1, q2, frac1, yields[i], charges[i]
    return frac1*q1 + (1-frac1)*q2

lims = {}
for N in CONTOURS:
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

if DRAW_LOI_CURVES:
    mq300 = np.loadtxt("matthew_csv_inputs/milliqan300.csv", delimiter=',')
    mq3000 = np.loadtxt("matthew_csv_inputs/milliqan3000.csv", delimiter=',')
    plt.plot(mq300[:,0], mq300[:,1], '-k', lw=2)
    plt.plot(mq3000[:,0], mq3000[:,1], '-k', lw=-2)

cols = ['r','b','g','c']
for i,N in enumerate(CONTOURS):
    plt.plot(masses, lims[N], '-o'+cols[i], label="N = {}".format(N))

print masses
pickle.dump(lims, open("yield_contours.pkl", 'wb'))

# plt.plot([1e-2,1e2], [0.3,0.3], 'k--')

plt.gca().set_xscale('log')
plt.gca().set_yscale('log')
plt.gca().set_xlim(1e-2, 2e2)
plt.gca().set_ylim(1e-3, 1e0)
plt.xlabel("mCP mass [GeV]")
plt.ylabel("mCP Q/e")
plt.legend(loc='upper left')



plt.savefig("/home/users/bemarsh/public_html/milliqan/milliq_mcgen/curves_const_yield.png", transparent=True)

# plt.show()
