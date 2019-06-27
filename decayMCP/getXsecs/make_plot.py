import ROOT as r
r.gStyle.SetOptStat(0)

f = r.TFile("xsecs.root")

c = r.TCanvas("c","c",800,600)
c.SetTopMargin(0.07)
c.SetBottomMargin(0.13)
c.SetRightMargin(0.05)
c.SetLogx()
c.SetLogy()

hdummy = r.TH1F("hdummy","",100,1e-2,10)
hdummy.GetXaxis().SetRangeUser(1e-2,10)
hdummy.GetYaxis().SetRangeUser(1,1e10)

hdummy.GetXaxis().SetTitle("m_{mCP} [GeV]")
hdummy.GetXaxis().SetTitleSize(0.045)
hdummy.GetXaxis().SetTitleOffset(1.20)
hdummy.GetYaxis().SetTitle("#sigma #times BR [pb]")
hdummy.GetYaxis().SetTitleSize(0.045)
hdummy.GetYaxis().SetTitleOffset(1.10)

hdummy.Draw()

colors = {
    1:  r.kBlue+2,
    2:  r.kAzure-3,
    3:  r.kRed,
    4:  r.kRed+2,
    5:  r.kOrange-3,
    6:  r.kGray+1,
    7:  r.kGreen+1,
    8:  r.kGreen+3,
    9:  r.kPink+9,
    10: r.kTeal-1,
    11: r.kBlue,
    12: r.kAzure-4,
    13: r.kMagenta,
    14: r.kMagenta+2,
    15: r.kMagenta+3,
}
gs = []
for i in range(1,16):
    gs.append(f.Get("xsecs_"+str(i)))
    gs[-1].SetLineWidth(2)
    gs[-1].SetLineColor(colors[i])
    gs[-1].Draw("SAME L")

gt = f.Get("xsecs_total")
gt.SetLineWidth(3)
gt.SetLineStyle(7)
gt.SetLineColor(r.kBlack)
gt.Draw("SAME L")

c.SaveAs("~/public_html/milliqan/mcp_xsec.pdf")

raw_input()
