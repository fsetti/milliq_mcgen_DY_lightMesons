import numpy as np
import ROOT as r
r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)

DO_DY = True
DY_ERR = 0.20
# If this is a number >0, then only display the portion of the graphs
# where the contribution from the given mode is at least DISP_THRESH of total xsec
DISP_THRESH = 0.00

f = r.TFile("xsecs.root")

c = r.TCanvas("c","c",800,600)
c.SetTopMargin(0.04)
c.SetBottomMargin(0.13)
c.SetLeftMargin(0.12)
c.SetRightMargin(0.02)
c.SetLogx()
c.SetLogy()
c.SetTicky()

xmax = 20 if DO_DY else 10
ymin = 2.0e2 if DO_DY else 2.0e2
hdummy = r.TH1F("hdummy","",100,1e-2,xmax)
hdummy.SetLineColor(r.kWhite)
hdummy.GetXaxis().SetRangeUser(1e-2,xmax)
hdummy.GetYaxis().SetRangeUser(ymin,3.0e10)

hdummy.GetXaxis().SetTitle("m_{#kern[0.2]{#chi}} [GeV]")
hdummy.GetXaxis().SetLabelSize(0.040)
hdummy.GetXaxis().SetLabelOffset(-0.005)
hdummy.GetXaxis().SetTitleSize(0.050)
hdummy.GetXaxis().SetTitleOffset(1.15)
hdummy.GetYaxis().SetTitle("#sigma #times #bf{#it{#Beta}} / (Q/e)^{2} [pb]")
hdummy.GetYaxis().SetLabelSize(0.040)
hdummy.GetYaxis().SetTitleSize(0.047)
hdummy.GetYaxis().SetTitleOffset(1.25)

hdummy.Draw("AXIS")

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
    # gs[i].Draw("SAME LX")

##### Handle DY curve #####

if DO_DY:

    xvals_interp = []
    x, y = r.Double(), r.Double()
    for i in range(gs[15].GetN()):
        gs[15].GetPoint(i, x, y)
        xvals_interp.append(float(x))
    xvals_interp = np.array(xvals_interp)

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
    x = np.loadtxt("dy_xsecs_eta1.txt")
    m_dy = x[:,0]
    xs = x[:,1]
    eff = x[:,2]
    smoothed = np.exp(ma(np.log(xs*eff), n=15))
    xvals_interp = np.append(xvals_interp, m_dy[np.argmax(m_dy>xvals_interp[-1]):])
    smoothed_interp = np.interp(xvals_interp, m_dy, smoothed)
    np2graph(gdy, xvals_interp, smoothed_interp)
    gdy.SetLineWidth(3)
    gdy.SetLineStyle(1)
    gdy.SetLineColor(r.kYellow+1)
    # gdy.Draw("SAME LX")

###########################

gt = f.Get("xsecs_total")
if DO_DY:
    x, y = r.Double(), r.Double()
    for i in range(gt.GetN()):
        gt.GetPoint(i, x, y)
        err_up = gt.GetErrorYhigh(i)
        err_dn = gt.GetErrorYlow(i)
        dy = np.interp(float(x), m_dy, smoothed)
        gt.SetPoint(i, x, y+dy)
        dy_err = DY_ERR*dy
        gt.SetPointError(i, 0, 0, np.sqrt(err_dn**2 + dy_err**2), np.sqrt(err_up**2 + dy_err**2))
    idx = np.argmax(m_dy > float(x))
    N = gt.GetN()
    for i in range(m_dy.size - idx):
        gt.SetPoint(N+i, m_dy[idx+i], smoothed[idx+i])
        gt.SetPointError(N+i, 0, 0, smoothed[idx+i]*DY_ERR, smoothed[idx+i]*DY_ERR)
gt.SetLineWidth(3)
gt.SetLineStyle(2)
gt.SetLineColor(r.kBlack)
gray = r.TColor.GetFreeColorIndex()
gray_c = r.TColor(gray, *([0.85]*3))
gt.SetFillColor(gray)
gt.Draw("SAME 3")

# now draw the individual modes, clipping out the portions
# of the graphs where the contribution to the total xsec is less than DISP_THRESH
all_gs = [gs[i] for i in range(1,16)]
if DO_DY:
    all_gs.append(gdy)
for g in all_gs:
    to_remove = []
    x, y = r.Double(), r.Double()
    yt = r.Double()
    for j in range(gt.GetN()):
        gt.GetPoint(j, x, yt)
        g.GetPoint(j, x, y)
        if y < DISP_THRESH*yt:
            to_remove.append(j)
    for ip in to_remove[::-1]:
        g.RemovePoint(ip)
    g.Draw("SAME LX")
gt.Draw("SAME LX")
hdummy.Draw("SAME AXIS")

line = r.TLine()
line.SetLineWidth(gt.GetLineWidth())
line.SetLineStyle(gt.GetLineStyle())
line.SetLineColor(gt.GetLineColor())
text = r.TLatex()
text.SetNDC(1)
text.SetTextFont(42)
text.SetTextAlign(12)
text.SetTextSize(0.032)
x1, x2, y = 0.332, 0.370, 0.927
box = r.TLegend(x1, y-0.013, x2, y+0.013)
box.SetFillColor(gray)
box.SetLineWidth(0)
box.Draw()
line.DrawLineNDC(x1, y, x2, y)
if DO_DY:
    # text.DrawLatex(x2+0.01, y+0.000, "Total #chi^{+}#chi^{#kern[0.3]{#minus}} cross section (#kern[0.25]{#pm}1 s.d._{#lower[-0.15]{#kern[0.8]{t}heory}}#kern[0.25]{)}")
    text.DrawLatex(x2+0.01, y+0.000, "Total #chi^{+}#chi^{#kern[0.3]{#minus}} cross section (#kern[0.25]{#pm}1 st. dev.)")
else:
    text.DrawLatex(x2+0.01, y+0.000, "Total non-Drell-Yan #chi^{+}#chi^{#kern[0.3]{#minus}} cross section (#kern[0.25]{#pm}1 s.d._{#lower[-0.15]{#kern[0.8]{t}heory}}#kern[0.25]{)}")

text.SetTextAlign(32)
text.DrawLatex(x1+0.600, y-0.267, "#bf{pp} (13 TeV)")
text.DrawLatex(x1+0.600, y-0.317, "#eta(parent) #in [-2, 2]")
text.SetTextAlign(11)
text.SetTextFont(62)
text.SetTextSize(0.047)
text.DrawLatex(0.16, 0.91, "milliQan")

leg = r.TLegend(x1-0.007,y-0.217,x1+0.610,y-0.025)
leg.SetFillStyle(0)
leg.SetLineWidth(0)
leg.SetNColumns(4)

leg.AddEntry(gs[6], "#pi^{0}#rightarrow#chi#chi#gamma", 'l')
leg.AddEntry(gs[3], "#rho#rightarrow#chi#chi", 'l')
leg.AddEntry(gs[11], "J/#psi#rightarrow#chi#chi", 'l')
leg.AddEntry(gs[13], "#varUpsilon#scale[0.7]{(1S)}#rightarrow#chi#chi", 'l')

leg.AddEntry(gs[7], "#eta#rightarrow#chi#chi#gamma", 'l')
leg.AddEntry(gs[8], "#eta'#rightarrow#chi#chi#gamma", 'l')
leg.AddEntry(gs[1], "B#rightarrowJ/#psiX, J/#psi#rightarrow#chi#chi", 'l')
leg.AddEntry(gs[14], "#varUpsilon#scale[0.7]{(2S)}#rightarrow#chi#chi", 'l')

leg.AddEntry(gs[9], "#omega#rightarrow#chi#chi#pi^{0}", 'l')
leg.AddEntry(gs[5], "#phi#rightarrow#chi#chi", 'l')
leg.AddEntry(gs[12], "#psi#scale[0.7]{(2S)}#rightarrow#chi#chi", 'l')
leg.AddEntry(gs[15], "#varUpsilon#scale[0.7]{(3S)}#rightarrow#chi#chi", 'l')

leg.AddEntry(gs[4], "#omega#rightarrow#chi#chi", 'l')
leg.AddEntry(gs[10], "#eta'#rightarrow#chi#chi#omega", 'l')
leg.AddEntry(gs[2], "B#rightarrow#psi#scale[0.7]{(2S)}X, #psi#scale[0.7]{(2S)}#rightarrow#chi#chi ", 'l')
if DO_DY:
    leg.AddEntry(gdy, "Drell-Yan*", 'l')
else:
    leg.AddEntry(hdummy, "", 'l')
leg.Draw()

c.SaveAs("~/public_html/milliqan/mcp-xsec.pdf")
c.SaveAs("~/public_html/milliqan/mcp-xsec.png")

