import os,sys
import numpy as np
import ROOT as r
import matplotlib.pyplot as plt

ch = sys.argv[1]

f = r.TFile("recogen_templates.root")

h = f.Get("recogen_ch{0}".format(ch))
fit = r.TF1("fit","gaus", 0, 200)
fit.SetNpx(500)

npes = list(range(10,80,5))
means = []
stds = []
for i in npes:
    hproj = h.ProjectionY("h_"+str(i), i+1, i+1)
    fit.SetParameter(0, hproj.GetMaximum())
    fit.SetParameter(1, i)
    fit.SetParameter(2, np.sqrt(i))
    hproj.Fit(fit, "QNR", "goff")
    
    means.append(fit.GetParameter(1))
    stds.append(fit.GetParameter(2))

# p = np.polyfit(np.sqrt(npes), stds, 1)
p = np.sum(np.sqrt(npes)*stds)/np.sum(npes)
print "{0},{1:.3f},".format(ch,p)

plt.figure()
plt.plot(npes, means, 'o-')
plt.plot([0,100],[0,100],'k--')

plt.figure()
plt.plot(npes, stds, 'o-')
xs = np.linspace(0,100,201)
ys = p*np.sqrt(xs)
plt.plot(xs, ys, 'k--')

plt.show()
