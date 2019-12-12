import os
import numpy as np
import ROOT as r
r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)

def mkdir(p):
    os.system("mkdir -p "+p)
    os.system("cp ~bemarsh/scripts/index.php "+p)

TAG = "v7_v1_save2m_skim0p25m_simmcp_v1_v1"
# TAG = "v7ext1_v1_save2m_skim0p25m_mcpData_v2_v1"
outdir = "/home/users/bemarsh/public_html/milliqan/geant_sim/signal_plots/"+TAG

ffast = r.TFile("../rate_files/v7_v1_save2m.root")
ffull = r.TFile("rate_files/{0}.root".format(TAG))

## fast/full rate comparisons
qs = [0.1, 0.05, 0.02, 0.01, 0.005]
mkdir(os.path.join(outdir, "fastfull"))

c = r.TCanvas("c","c",800,600)
c.SetTopMargin(0.07)
c.SetBottomMargin(0.13)
c.SetLeftMargin(0.11)
c.SetRightMargin(0.03)
c.SetLogx()
c.SetLogy()
c.SetTicky()
c.SetGridx()
c.SetGridy()

hdummy = r.TH1F("hdummy","",100,5e-3,16)
hdummy.SetLineColor(r.kWhite)
hdummy.GetXaxis().SetRangeUser(5e-3,16)
hdummy.GetYaxis().SetRangeUser(1e-5*35, 2e5*35)
hdummy.GetYaxis().SetTitle("Three bar line yield")
hdummy.GetXaxis().SetTitle("m_{mCP} [GeV]")
hdummy.GetXaxis().SetTitleSize(0.045)
hdummy.GetXaxis().SetTitleOffset(1.20)
hdummy.GetYaxis().SetTitleSize(0.045)
hdummy.GetYaxis().SetTitleOffset(1.16)
    
hdummy.Draw()

x = 0.74
y = 0.90
leg = r.TLegend(x,y-0.05*(len(qs)+1),x+0.20,y)

cs = [r.kBlack, r.kAzure-2, r.kOrange-3, r.kGreen+2, r.kRed+1][::-1]
for iq,q in enumerate(qs):
    sq = str(q).replace(".","p")
    gfast = ffast.Get("line_rate_q{0}_total".format(sq))
    gfull = ffull.Get("rate_mcTruth_threeBarLine_q{0}".format(sq))

    gfast.SetLineWidth(2)
    gfast.SetLineStyle(1)
    gfast.SetLineColor(r.kGray+2)
    gfast.SetMarkerStyle(20)
    gfast.SetMarkerColor(r.kBlack)
    gfast.Draw("SAME LP")
    if iq==0:
        leg.AddEntry(gfast, "Fast sim", 'pl')

    gfull.SetLineWidth(3)
    gfull.SetLineStyle(2)
    gfull.SetLineColor(cs[iq])
    gfull.SetMarkerStyle(20)
    gfull.SetMarkerColor(cs[iq])
    gfull.Draw("SAME LP")
    leg.AddEntry(gfull, "Full, Q = "+str(q), 'pl')

leg.Draw()

text = r.TLatex()
text.SetNDC(1)
text.SetTextSize(0.04)
text.SetTextFont(42)
text.SetTextAlign(31)
text.DrawLatex(0.96, 0.94, "35 fb^{-1} (13 TeV)")
text.SetTextFont(62)
text.SetTextAlign(11)
text.DrawLatex(0.12, 0.94, "milliQan simulation")

c.SaveAs(os.path.join(outdir, "fastfull","mcTruth_threeBarLine.png"))
c.SaveAs(os.path.join(outdir, "fastfull","mcTruth_threeBarLine.pdf"))


## mcTruth_threeBarLine vs >=1PE
qs = [0.1, 0.05, 0.02, 0.01, 0.005]
# qs = [0.02, 0.014, 0.01, 0.007, 0.005]
# qs = [0.3, 0.2, 0.14]
mkdir(os.path.join(outdir, "rate_comps"))

c = r.TCanvas("c2","c2",800,600)
c.SetTopMargin(0.07)
c.SetBottomMargin(0.13)
c.SetLeftMargin(0.11)
c.SetRightMargin(0.03)
c.SetLogx()
c.SetLogy()
c.SetTicky()
c.SetGridx()
c.SetGridy()

hdummy = r.TH1F("hdummy2","",100,5e-3,16)
hdummy.SetLineColor(r.kWhite)
hdummy.GetXaxis().SetRangeUser(5e-3,16)
hdummy.GetYaxis().SetRangeUser(1e-5*35, 2e5*35)
hdummy.GetYaxis().SetTitle("Three bar line yield")
hdummy.GetXaxis().SetTitle("m_{mCP} [GeV]")
hdummy.GetXaxis().SetTitleSize(0.045)
hdummy.GetXaxis().SetTitleOffset(1.20)
hdummy.GetYaxis().SetTitleSize(0.045)
hdummy.GetYaxis().SetTitleOffset(1.16)
    
hdummy.Draw()

x = 0.73
y = 0.90
leg = r.TLegend(x,y-0.05*(len(qs)+1),x+0.21,y)

cs = [r.kBlack, r.kAzure-2, r.kOrange-3, r.kGreen+2, r.kRed+1][::-1]
for iq,q in enumerate(qs):
    sq = str(q).replace(".","p")
    g1 = ffull.Get("rate_mcTruth_threeBarLine_q{0}".format(sq))
    g2 = ffull.Get("rate_atLeast1PE_threeBarLine_q{0}".format(sq))

    # x,y = r.Double(), r.Double()
    # g1.GetPoint(0, x, y)
    # if float(x)==0.01:
    #     g1.RemovePoint(0)
    # g2.GetPoint(0, x, y)
    # if float(x)==0.01:
    #     g2.RemovePoint(0)

    g1.SetLineWidth(2)
    g1.SetLineStyle(1)
    g1.SetLineColor(r.kGray+2)
    g1.SetMarkerStyle(20)
    g1.SetMarkerColor(r.kBlack)
    g1.Draw("SAME LP")
    if iq==0:
        leg.AddEntry(g1, "Geometric", 'pl')

    g2.SetLineWidth(3)
    g2.SetLineStyle(2)
    g2.SetLineColor(cs[iq])
    g2.SetMarkerStyle(20)
    g2.SetMarkerColor(cs[iq])
    g2.Draw("SAME LP")
    leg.AddEntry(g2, "#geq1 PE, Q = "+str(q), 'pl')

leg.Draw()

text = r.TLatex()
text.SetNDC(1)
text.SetTextSize(0.04)
text.SetTextFont(42)
text.SetTextAlign(31)
text.DrawLatex(0.96, 0.94, "35 fb^{-1} (13 TeV)")
text.SetTextFont(62)
text.SetTextAlign(11)
text.DrawLatex(0.12, 0.94, "milliQan simulation")

c.SaveAs(os.path.join(outdir, "rate_comps","mcTruth_atLeast1PE_geom.png"))
c.SaveAs(os.path.join(outdir, "rate_comps","mcTruth_atLeast1PE_geom.pdf"))


## nPE histograms
mkdir(os.path.join(outdir, "nPE"))
mqs = [(1.0,0.01),(1.0,0.03),(1.0,0.05),(1.0,0.07),(1.0,0.1)]

c = r.TCanvas("c3","c3",600,600)
c.SetTopMargin(0.07)
c.SetBottomMargin(0.13)
c.SetLeftMargin(0.11)
c.SetRightMargin(0.05)
# c.SetLogy()
c.SetTicky()
c.SetGridx()
c.SetGridy()

hdummy = r.TH1F("hdummy3","",100,0,30)
hdummy.SetLineColor(r.kWhite)
hdummy.GetXaxis().SetRangeUser(0,30)
# hdummy.GetYaxis().SetRangeUser(1e-4, 1e1)
hdummy.GetYaxis().SetRangeUser(0, 1.0)
hdummy.GetYaxis().SetTitle("Fraction events")
hdummy.GetXaxis().SetTitle("nPE")
hdummy.GetXaxis().SetTitleSize(0.045)
hdummy.GetXaxis().SetTitleOffset(1.20)
hdummy.GetYaxis().SetTitleSize(0.045)
hdummy.GetYaxis().SetTitleOffset(1.16)
hdummy.Draw()

leg = r.TLegend(0.45, 0.62, 0.90, 0.92)
for i,(m,q) in enumerate(mqs):
    sm = str(m).replace(".","p")
    sq = str(q).replace(".","p")
    h = ffull.Get("h_slabNPE_m{0}_q{1}".format(sm,sq))
    h.Scale(1.0 / h.Integral(0,-1,"width"))
    h.SetLineWidth(2)
    h.SetLineColor(cs[i])
    h.Draw("HIST SAME")
    leg.AddEntry(h, "m = {0} GeV, Q = {1}".format(m,q), "l")
leg.Draw()

text.SetTextSize(0.04)
text.SetTextFont(62)
text.SetTextAlign(11)
text.DrawLatex(0.12, 0.94, "milliQan simulation")

c.SaveAs(os.path.join(outdir, "nPE", "slab_nPE_dists.png"))
c.SaveAs(os.path.join(outdir, "nPE", "slab_nPE_dists.pdf"))


c.Clear()
hdummy = r.TH1F("hdummy4","",100,0,2500)
hdummy.SetLineColor(r.kWhite)
hdummy.GetXaxis().SetRangeUser(0,2500)
# hdummy.GetYaxis().SetRangeUser(1e-4, 1e1)
hdummy.GetYaxis().SetRangeUser(0, 1.7)
hdummy.GetYaxis().SetTitle("A.U.")
hdummy.GetXaxis().SetTitle("nPE")
hdummy.GetXaxis().SetTitleSize(0.045)
hdummy.GetXaxis().SetTitleOffset(1.20)
hdummy.GetYaxis().SetTitleSize(0.045)
hdummy.GetYaxis().SetTitleOffset(1.16)
hdummy.Draw()

leg = r.TLegend(0.45, 0.62, 0.90, 0.92)
for i,(m,q) in enumerate(mqs):
    sm = str(m).replace(".","p")
    sq = str(q).replace(".","p")
    h = ffull.Get("h_barNPE_m{0}_q{1}".format(sm,sq))
    if 0.01 < q < 0.07:
        h.Rebin(10)
    if q >= 0.07:
        h.Rebin(2)
    h.Scale(1.0 / h.GetMaximum())
    h.SetLineWidth(2)
    h.SetLineColor(cs[i])
    h.Draw("HIST SAME")
    leg.AddEntry(h, "m = {0} GeV, Q = {1}".format(m,q), "l")
leg.Draw()

text.SetTextSize(0.04)
text.SetTextFont(62)
text.SetTextAlign(11)
text.DrawLatex(0.12, 0.94, "milliQan simulation")

c.SaveAs(os.path.join(outdir, "nPE", "bar_nPE_dists.png"))
c.SaveAs(os.path.join(outdir, "nPE", "bar_nPE_dists.pdf"))

## mean nPE curves
ms = [0.2, 0.5, 1.0, 2.0, 5.0]
qs = [0.005, 0.01, 0.02, 0.03, 0.05, 0.07, 0.1, 0.14, 0.2]

c = r.TCanvas("c4","c4",600,600)
c.SetTopMargin(0.07)
c.SetBottomMargin(0.13)
c.SetLeftMargin(0.13)
c.SetRightMargin(0.05)
c.SetLogy()
c.SetLogx()
c.SetTicky()
c.SetGridx()
c.SetGridy()

hdummy = r.TH1F("hdummy5","", 100, 1e-3, 1e0)
hdummy.SetLineColor(r.kWhite)
hdummy.GetXaxis().SetRangeUser(1e-3,1e0)
# hdummy.GetYaxis().SetRangeUser(1e-4, 1e1)
hdummy.GetYaxis().SetRangeUser(1e-2, 3e3)
hdummy.GetYaxis().SetTitle("Mean slab nPE")
hdummy.GetXaxis().SetTitle("Q/e")
hdummy.GetXaxis().SetTitleSize(0.045)
hdummy.GetXaxis().SetTitleOffset(1.20)
hdummy.GetYaxis().SetTitleSize(0.045)
hdummy.GetYaxis().SetTitleOffset(1.3)
hdummy.Draw()

gs = []
leg = r.TLegend(0.17, 0.65, 0.56, 0.91)
for i,m in enumerate(ms):
    sm = str(m).replace(".","p")
    g = r.TGraphErrors()
    g.SetLineWidth(2)
    g.SetLineColor(cs[i])
    g.SetMarkerStyle(20)
    g.SetMarkerColor(cs[i])
    xs, ys = [], []
    for q in qs:
        sq = str(q).replace(".","p")
        h = ffull.Get("h_slabNPE_m{0}_q{1}".format(sm,sq))
        if h.GetMean()==0:
            continue
        N = g.GetN()
        xs.append(np.log(q))
        ys.append(np.log(h.GetMean()))
        g.SetPoint(N, q, h.GetMean())
        g.SetPointError(N, 0, h.GetRMS()/h.GetEntries()**0.5)
    g.Draw("SAME LP")
    gs.append(g)
    p = np.polyfit(xs,ys,1)
    leg.AddEntry(g, "m = {0} GeV (pow={1:.1f})".format(m,p[0]), 'lp')
leg.Draw()

text.SetTextSize(0.04)
text.SetTextFont(62)
text.SetTextAlign(11)
text.DrawLatex(0.14, 0.94, "milliQan simulation")

c.SaveAs(os.path.join(outdir, "nPE", "slab_nPE_means.png"))
c.SaveAs(os.path.join(outdir, "nPE", "slab_nPE_means.pdf"))

c.Clear()

hdummy = r.TH1F("hdummy6","", 100, 1e-3, 1e0)
hdummy.SetLineColor(r.kWhite)
hdummy.GetXaxis().SetRangeUser(1e-3,1e0)
# hdummy.GetYaxis().SetRangeUser(1e-4, 1e1)
hdummy.GetYaxis().SetRangeUser(1e0, 3e5)
hdummy.GetYaxis().SetTitle("Mean bar nPE")
hdummy.GetXaxis().SetTitle("Q/e")
hdummy.GetXaxis().SetTitleSize(0.045)
hdummy.GetXaxis().SetTitleOffset(1.20)
hdummy.GetYaxis().SetTitleSize(0.045)
hdummy.GetYaxis().SetTitleOffset(1.3)
hdummy.Draw()

gs = []
leg = r.TLegend(0.17, 0.65, 0.56, 0.91)
for i,m in enumerate(ms):
    sm = str(m).replace(".","p")
    g = r.TGraphErrors()
    g.SetLineWidth(2)
    g.SetLineColor(cs[i])
    g.SetMarkerStyle(20)
    g.SetMarkerColor(cs[i])
    xs, ys = [], []
    for q in qs:
        sq = str(q).replace(".","p")
        h = ffull.Get("h_barNPE_m{0}_q{1}".format(sm,sq))
        if h.GetMean()==0:
            continue
        N = g.GetN()
        xs.append(np.log(q))
        ys.append(np.log(h.GetMean()))
        g.SetPoint(N, q, h.GetMean())
        g.SetPointError(N, 0, h.GetRMS()/h.GetEntries()**0.5)
    g.Draw("SAME LP")
    gs.append(g)
    p = np.polyfit(xs,ys,1)
    leg.AddEntry(g, "m = {0} GeV (pow={1:.1f})".format(m,p[0]), 'lp')
leg.Draw()

text.SetTextSize(0.04)
text.SetTextFont(62)
text.SetTextAlign(11)
text.DrawLatex(0.14, 0.94, "milliQan simulation")

c.SaveAs(os.path.join(outdir, "nPE", "bar_nPE_means.png"))
c.SaveAs(os.path.join(outdir, "nPE", "bar_nPE_means.pdf"))



## slab nPE probs
m, sm = 1.0, "1p0"
c = r.TCanvas("c5","c5",600,600)
c.SetTopMargin(0.07)
c.SetBottomMargin(0.13)
c.SetLeftMargin(0.13)
c.SetRightMargin(0.05)
c.SetLogy()
c.SetLogx()
c.SetTicky()
c.SetGridx()
c.SetGridy()

hdummy = r.TH1F("hdummy5","", 100, 3e-3, 5e-1)
hdummy.SetLineColor(r.kWhite)
hdummy.GetXaxis().SetRangeUser(3e-3,5e-1)
# hdummy.GetYaxis().SetRangeUser(1e-4, 1e1)
hdummy.GetYaxis().SetRangeUser(1e-2, 1.2e1)
hdummy.GetYaxis().SetTitle("Probability")
hdummy.GetXaxis().SetTitle("Q/e")
hdummy.GetXaxis().SetTitleSize(0.045)
hdummy.GetXaxis().SetTitleOffset(1.20)
hdummy.GetYaxis().SetTitleSize(0.045)
hdummy.GetYaxis().SetTitleOffset(1.3)

gs = []
cfgs = [["single","geone","all","none"], ["none","one","two","three","all"],["none","geone","getwo","gethree","all"]]
outnames = ["slab_nPE_probs", "slab_nPE_probs2", "slab_nPE_probs3"]
names = {
    "single" : "p(#geq1 PE in given slab)",
    "geone" : "p(#geq1 PE in at least 1 slab)",
    "getwo" : "p(#geq1 PE in at least 2 slabs)",
    "gethree" : "p(#geq1 PE in at least 3 slabs)",
    "all" : "p(#geq1 PE in all slabs)",
    "none" : "p(0 PE in all slabs)",
    "one" : "p(#geq1 PE in exactly 1 slab)",
    "two" : "p(#geq1 PE in exactly 2 slabs)",
    "three" : "p(#geq1 PE in exactly 3 slabs)",
}
for ic,cfg_set in enumerate(cfgs):
    c.Clear()
    hdummy.Draw()
    leg = r.TLegend(0.45, 0.68, 0.90, 0.91)
    for i,cfg in enumerate(cfg_set):
        g = r.TGraphErrors()
        g.SetLineWidth(2)
        g.SetLineColor(cs[i])
        g.SetMarkerStyle(20)
        g.SetMarkerColor(cs[i])
        for q in qs:
            sq = str(q).replace(".","p")
            h = ffull.Get("h_slabNPE_m{0}_q{1}".format(sm,sq))
            p = 1 - h.GetBinContent(1) / h.Integral(1,-1)
            if cfg=="all":
                p = p**4
            if cfg=="none":
                p = (1-p)**4
            if cfg=="one":
                p = 4*p*(1-p)**3
            if cfg=="two":
                p = 6*p**2*(1-p)**2
            if cfg=="three":
                p = 4*p**3*(1-p)
            if cfg=="geone":
                p = 1-(1-p)**4
            if cfg=="getwo":
                p = 6*p**2*(1-p)**2 + 4*p**3*(1-p) + p**4
            if cfg=="gethree":
                p = 4*p**3*(1-p) + p**4
        
            N = g.GetN()        
            g.SetPoint(N, q, p)
            g.SetPointError(N, 0, np.sqrt(p*(1-p)/h.GetEntries()))
        g.Draw("SAME LP")
        gs.append(g)
        leg.AddEntry(g, names[cfg], 'lp')
    leg.Draw()

    text.SetTextSize(0.04)
    text.SetTextFont(62)
    text.SetTextAlign(11)
    text.DrawLatex(0.14, 0.94, "milliQan simulation")
    
    c.SaveAs(os.path.join(outdir, "nPE", "{0}.png".format(outnames[ic])))
    c.SaveAs(os.path.join(outdir, "nPE", "{0}.pdf".format(outnames[ic])))

## max/min npe plots
mqs = [(1.0,0.01),(1.0,0.03),(1.0,0.05),(1.0,0.07),(1.0,0.1)]

c = r.TCanvas("c6","c6",600,600)
c.SetTopMargin(0.07)
c.SetBottomMargin(0.13)
c.SetLeftMargin(0.11)
c.SetRightMargin(0.05)
# c.SetLogy()
c.SetTicky()
c.SetGridx()
c.SetGridy()

hdummy = r.TH1F("hdummy6","",100,0,30)
hdummy.SetLineColor(r.kWhite)
hdummy.GetXaxis().SetRangeUser(0,20)
hdummy.GetYaxis().SetRangeUser(0, 0.5)
# hdummy.GetYaxis().SetRangeUser(1e-4, 1e-1)
hdummy.GetYaxis().SetTitle("Fraction events")
hdummy.GetXaxis().SetTitle("maxNPE / minNPE")
hdummy.GetXaxis().SetTitleSize(0.045)
hdummy.GetXaxis().SetTitleOffset(1.20)
hdummy.GetYaxis().SetTitleSize(0.045)
hdummy.GetYaxis().SetTitleOffset(1.16)
hdummy.Draw()

leg = r.TLegend(0.45, 0.62, 0.90, 0.92)
for i,(m,q) in enumerate(mqs):
    sm = str(m).replace(".","p")
    sq = str(q).replace(".","p")
    h = ffull.Get("h_barMaxMin_m{0}_q{1}".format(sm,sq))
    h.Scale(1.0 / h.Integral(1,-1))
    h.SetLineWidth(2)
    h.SetLineColor(cs[i])
    h.Draw("HIST SAME")
    leg.AddEntry(h, "m = {0} GeV, Q = {1}".format(m,q), "l")
leg.Draw()

text.SetTextSize(0.04)
text.SetTextFont(62)
text.SetTextAlign(11)
text.DrawLatex(0.12, 0.94, "milliQan simulation")

c.SaveAs(os.path.join(outdir, "nPE", "bar_MaxMin_dists.png"))
c.SaveAs(os.path.join(outdir, "nPE", "bar_MaxMin_dists.pdf"))

## max/min npe eff contours
m, sm = 1.0, "1p0"
qs = [0.005, 0.01, 0.02, 0.03, 0.05, 0.07, 0.1, 0.14, 0.2, 0.3]
effs = [0.90, 0.93, 0.95, 0.97, 0.98]

c = r.TCanvas("c7","c7",600,600)
c.SetTopMargin(0.07)
c.SetBottomMargin(0.13)
c.SetLeftMargin(0.11)
c.SetRightMargin(0.05)
c.SetLogx()
c.SetLogy()
c.SetTicky()
c.SetGridx()
c.SetGridy()

hdummy = r.TH1F("hdummy7","", 100, 3e-3, 5e-1)
hdummy.SetLineColor(r.kWhite)
hdummy.GetXaxis().SetRangeUser(3e-3,5e-1)
# hdummy.GetYaxis().SetRangeUser(0, 50)
hdummy.GetYaxis().SetRangeUser(1, 1000)
hdummy.GetYaxis().SetTitle("Max/Min cut")
hdummy.GetXaxis().SetTitle("Q/e")
hdummy.GetXaxis().SetTitleSize(0.045)
hdummy.GetXaxis().SetTitleOffset(1.20)
hdummy.GetYaxis().SetTitleSize(0.045)
hdummy.GetYaxis().SetTitleOffset(1.2)
hdummy.Draw()

leg = r.TLegend(0.45, 0.72, 0.90, 0.92)
gs = {}
for i,eff in enumerate(effs):
    gs[eff] = r.TGraph()
    for j,q in enumerate(qs):
        sq = str(q).replace(".","p")
        h = ffull.Get("h_barMaxMin_m{0}_q{1}".format(sm,sq))
        ibin = 1
        while h.Integral(1,ibin)/h.Integral(1,-1) < eff:
            ibin += 1
        cut = h.GetXaxis().GetBinUpEdge(ibin)
        gs[eff].SetPoint(j, q, cut)
    gs[eff].SetLineWidth(2)
    gs[eff].SetLineColor(cs[i])
    gs[eff].SetMarkerStyle(20)
    gs[eff].SetMarkerColor(cs[i])
    gs[eff].Draw("SAME LP")
    leg.AddEntry(gs[eff], "eff = {0:.2f}".format(eff), "lp")
leg.Draw()

text.SetTextSize(0.04)
text.SetTextFont(62)
text.SetTextAlign(11)
text.DrawLatex(0.12, 0.94, "milliQan simulation")

c.SaveAs(os.path.join(outdir, "nPE", "bar_MaxMin_effs.png"))
c.SaveAs(os.path.join(outdir, "nPE", "bar_MaxMin_effs.pdf"))

## max/min npe eff curves
m, sm = 1.0, "1p0"
qs = [0.01, 0.03, 0.05, 0.1, 0.2]

c = r.TCanvas("c8","c8",600,600)
c.SetTopMargin(0.07)
c.SetBottomMargin(0.13)
c.SetLeftMargin(0.11)
c.SetRightMargin(0.05)
c.SetLogx()
# c.SetLogy()
c.SetTicky()
c.SetGridx()
c.SetGridy()

hdummy = r.TH1F("hdummy8","", 100, 1, 100)
hdummy.SetLineColor(r.kWhite)
hdummy.GetXaxis().SetRangeUser(1, 100)
# hdummy.GetYaxis().SetRangeUser(0, 50)
hdummy.GetYaxis().SetRangeUser(0.8, 1.1)
hdummy.GetYaxis().SetTitle("Efficiency")
hdummy.GetXaxis().SetTitle("Max/Min cut")
hdummy.GetXaxis().SetTitleSize(0.045)
hdummy.GetXaxis().SetTitleOffset(1.20)
hdummy.GetYaxis().SetTitleSize(0.045)
hdummy.GetYaxis().SetTitleOffset(1.2)
hdummy.Draw()

leg = r.TLegend(0.45, 0.72, 0.90, 0.92)
gs = {}
for j,q in enumerate(qs):
    sq = str(q).replace(".","p")
    h = ffull.Get("h_barMaxMin_m{0}_q{1}".format(sm,sq))
    gs[sq] = r.TGraph()
    for i in range(h.GetNbinsX()):
        eff = h.Integral(1,i+1) / h.Integral(1,-1)
        gs[sq].SetPoint(i, h.GetXaxis().GetBinUpEdge(i+1), eff)
    gs[sq].SetLineWidth(3)
    gs[sq].SetLineColor(cs[j])
    gs[sq].Draw("SAME L")
    leg.AddEntry(gs[sq], "Q = {0:.2f}".format(q), "lp")
leg.Draw()

text.SetTextSize(0.04)
text.SetTextFont(62)
text.SetTextAlign(11)
text.DrawLatex(0.12, 0.94, "milliQan simulation")

c.SaveAs(os.path.join(outdir, "nPE", "bar_MaxMin_effcurves.png"))
c.SaveAs(os.path.join(outdir, "nPE", "bar_MaxMin_effcurves.pdf"))
