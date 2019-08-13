import numpy as np
import ROOT as r
r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)

DO_DY = True

f = r.TFile("xsecs.root")

c = r.TCanvas("c","c",800,600)
c.SetTopMargin(0.05)
c.SetBottomMargin(0.13)
c.SetLeftMargin(0.11)
c.SetRightMargin(0.03)
c.SetLogx()
c.SetLogy()

xmax = 15 if DO_DY else 10
hdummy = r.TH1F("hdummy","",100,1e-2,xmax)
hdummy.SetLineColor(r.kWhite)
hdummy.GetXaxis().SetRangeUser(1e-2,xmax)
hdummy.GetYaxis().SetRangeUser(1.0e2,5.0e10)

hdummy.GetXaxis().SetTitle("m_{mCP} [GeV]")
hdummy.GetXaxis().SetTitleSize(0.045)
hdummy.GetXaxis().SetTitleOffset(1.20)
hdummy.GetYaxis().SetTitle("#sigma #times #bf{#it{#Beta}} / Q^{2} [pb]")
hdummy.GetYaxis().SetTitleSize(0.045)
hdummy.GetYaxis().SetTitleOffset(1.16)

hdummy.Draw()

colors = {
    1:  r.kBlue+2,
    2:  r.kAzure-4,
    3:  r.kRed,
    4:  r.kRed+2,
    5:  r.kOrange-3,
    6:  r.kGray+1,
    7:  r.kGreen+1,
    8:  r.kGreen+3,
    9:  r.kPink+1,
    10: r.kTeal-1,
    11: r.kBlue-4,
    12: r.kAzure+6,
    13: r.kMagenta,
    14: r.kMagenta+2,
    15: r.kMagenta+3,
}
gs = {}
for i in range(1,16):
    gs[i] = f.Get("xsecs_"+str(i))
    gs[i].SetLineWidth(2)
    gs[i].SetLineColor(colors[i])
    gs[i].Draw("SAME L")

##### Handle DY curve #####

if DO_DY:
    def np2graph(g, m, xs):
        g.Set(0)
        for i in range(m.size):
            g.SetPoint(i, m[i], xs[i])

    def ma(a, n=3):
        ones = np.ones(2*n+1)
        avg = np.convolve(a, ones, mode='same')
        n = np.convolve(np.ones(a.size), ones, mode='same')
        return avg / n

    gdy = r.TGraph()
    x = np.loadtxt("dy/dy_xsecs_eta1.txt")
    m_dy = x[:,0]
    xs = x[:,1]
    eff = x[:,2]
    smoothed = np.exp(ma(np.log(xs*eff), n=15))
    np2graph(gdy, m_dy, smoothed)
    gdy.SetLineWidth(3)
    gdy.SetLineStyle(1)
    gdy.SetLineColor(r.kYellow+1)
    gdy.Draw("SAME L")

###########################

gt = f.Get("xsecs_total")
if DO_DY:
    x, y = r.Double(), r.Double()
    for i in range(gt.GetN()):
        gt.GetPoint(i, x, y)
        dy = np.interp(float(x), m_dy, smoothed)
        gt.SetPoint(i, x, y+dy)
    idx = np.argmax(m_dy > float(x))
    N = gt.GetN()
    for i in range(m_dy.size - idx):
        gt.SetPoint(N+i, m_dy[idx+i], smoothed[idx+i])
gt.SetLineWidth(3)
gt.SetLineStyle(2)
gt.SetLineColor(r.kBlack)
gt.Draw("SAME L")

line = r.TLine()
line.SetLineWidth(gt.GetLineWidth())
line.SetLineStyle(gt.GetLineStyle())
line.SetLineColor(gt.GetLineColor())
text = r.TLatex()
text.SetNDC(1)
text.SetTextFont(42)
text.SetTextAlign(12)
text.SetTextSize(0.032)
line.DrawLineNDC(0.357, 0.916, 0.395, 0.916)
if DO_DY:
    text.DrawLatex(0.405, 0.919, "Total #zeta^{+}#zeta^{#kern[0.3]{#minus}} cross section")
else:
    text.DrawLatex(0.405, 0.919, "Total non-Drell-Yan #zeta^{+}#zeta^{#kern[0.3]{#minus}} cross section")

text.SetTextAlign(32)
text.DrawLatex(0.95, 0.65, "#bf{pp} (13 TeV)")
text.DrawLatex(0.95, 0.60, "#eta(parent) #in [-2, 2]")

leg = r.TLegend(0.35,0.7,0.96,0.892)
leg.SetFillStyle(0)
leg.SetLineWidth(0)
leg.SetNColumns(4)

leg.AddEntry(gs[6], "#pi^{0}#rightarrow#zeta#zeta#gamma", 'l')
leg.AddEntry(gs[3], "#rho#rightarrow#zeta#zeta", 'l')
leg.AddEntry(gs[11], "J/#psi#rightarrow#zeta#zeta", 'l')
leg.AddEntry(gs[13], "#varUpsilon#scale[0.7]{(1S)}#rightarrow#zeta#zeta", 'l')

leg.AddEntry(gs[7], "#eta#rightarrow#zeta#zeta#gamma", 'l')
leg.AddEntry(gs[8], "#eta'#rightarrow#zeta#zeta#gamma", 'l')
leg.AddEntry(gs[1], "B#rightarrowJ/#psiX, J/#psi#rightarrow#zeta#zeta", 'l')
leg.AddEntry(gs[14], "#varUpsilon#scale[0.7]{(2S)}#rightarrow#zeta#zeta", 'l')

leg.AddEntry(gs[9], "#omega#rightarrow#zeta#zeta#pi^{0}", 'l')
leg.AddEntry(gs[5], "#phi#rightarrow#zeta#zeta", 'l')
leg.AddEntry(gs[12], "#psi#scale[0.7]{(2S)}#rightarrow#zeta#zeta", 'l')
leg.AddEntry(gs[15], "#varUpsilon#scale[0.7]{(3S)}#rightarrow#zeta#zeta", 'l')

leg.AddEntry(gs[4], "#omega#rightarrow#zeta#zeta", 'l')
leg.AddEntry(gs[10], "#eta'#rightarrow#zeta#zeta#omega", 'l')
leg.AddEntry(gs[2], "B#rightarrow#psi#scale[0.7]{(2S)}X, #psi#scale[0.7]{(2S)}#rightarrow#zeta#zeta ", 'l')
if DO_DY:
    leg.AddEntry(gdy, "Drell-Yan*", 'l')
else:
    leg.AddEntry(hdummy, "", 'l')
leg.Draw()

c.SaveAs("~/public_html/milliqan/mcp-xsec.pdf")
c.SaveAs("~/public_html/milliqan/mcp-xsec.png")

