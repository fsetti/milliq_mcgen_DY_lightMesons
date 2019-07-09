import os
import ROOT as r
from math import log
r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(1)

plotdir = "/home/users/bemarsh/public_html/milliqan/milliq_mcgen/pionPt/v3_eta2/stitch"
os.system("mkdir -p "+plotdir)

dname = "hadded/v3_eta2"

doPlot = True

fm = r.TFile(os.path.join(dname, "minbias.root"))
fq1 = r.TFile(os.path.join(dname, "qcd_pt15to30.root"))
fq2 = r.TFile(os.path.join(dname, "qcd_pt30to50.root"))
fq3 = r.TFile(os.path.join(dname, "qcd_pt50to80.root"))

fout = r.TFile("pt_dists.root", "RECREATE")

nev_m = fm.Get("h_nevents").GetBinContent(1)
nev_q1 = fq1.Get("h_nevents").GetBinContent(1)
nev_q2 = fq2.Get("h_nevents").GetBinContent(1)
nev_q3 = fq3.Get("h_nevents").GetBinContent(1)

cuts = [8.0, 18.5, 30.0]

ps = ["pi","pi0","rho","omega","phi","eta","etap"]
for p in ps:
    hm = fm.Get("h_"+p)
    hq1 = fq1.Get("h_"+p)
    hq2 = fq2.Get("h_"+p)
    hq3 = fq3.Get("h_"+p)

    # scale by # events
    hm.Scale(1.0 / nev_m)
    hq1.Scale(1.0 / nev_q1)
    hq2.Scale(1.0 / nev_q2)
    hq3.Scale(1.0 / nev_q3)

    # scale by xsec ratios
    hq1.Scale(1837410. / 78418400)
    hq2.Scale( 140932. / 78418400)
    hq3.Scale(  19204. / 78418400)

    int_range = (8.0, 14.0)
    c = r.TCanvas()
    ratio_n = hm.Clone("ratio_n")
    ratio_d = hq1.Clone("ratio_d")
    ratio_n.Rebin(8)
    ratio_d.Rebin(8)
    ratio_n.Divide(ratio_d)
    ratio_n.GetYaxis().SetRangeUser(0,10)
    ratio_n.GetXaxis().SetRangeUser(0,30)
    ratio_n.Draw()
    line = r.TLine()
    line.DrawLine(int_range[0], 0, int_range[0], 7)
    line.DrawLine(int_range[1], 0, int_range[1], 7)
    if doPlot:
        c.SaveAs(os.path.join(plotdir, "ratio_mb_qcd_{0}.png".format(p)))
        c.SaveAs(os.path.join(plotdir, "ratio_mb_qcd_{0}.pdf".format(p)))
        
    int_q1 = hq1.Integral(hm.FindBin(int_range[0]), hm.FindBin(int_range[1])-1)
    int_m  =  hm.Integral(hm.FindBin(int_range[0]), hm.FindBin(int_range[1])-1)
    qcd_mb_sf = int_m / int_q1

    hq1.Scale(qcd_mb_sf)
    hq2.Scale(qcd_mb_sf)
    hq3.Scale(qcd_mb_sf)

    # f = r.TF1("fit","[0]*exp([1]*(x-10))",10,40)
    # f.SetParameter(1, hq1.GetBinContent(hm.FindBin(10)))
    # hq1.Fit(f, "QR", "goff")
    # aq1 = f.GetParameter(0)
    # bq1 = f.GetParameter(1)
    # f.SetParameter(1, hq2.GetBinContent(hm.FindBin(10)))
    # hq2.Fit(f, "QR", "goff")
    # aq2 = f.GetParameter(0)
    # bq2 = f.GetParameter(1)
    # f.SetParameter(1, hq3.GetBinContent(hm.FindBin(10)))
    # hq3.Fit(f, "QR", "goff")
    # aq3 = f.GetParameter(0)
    # bq3 = f.GetParameter(1)
    
    # cuts[1] = log(aq2 / aq1) / (bq1 - bq2) + 10
    # cuts[2] = log(aq3 / aq2) / (bq2 - bq3) + 10
    # print cuts[1], cuts[2]

    b1 = hq1.FindBin(cuts[0])
    b2 = hq1.FindBin(cuts[1])
    b3 = hq1.FindBin(cuts[2])
    for i in range(b1, hm.GetNbinsX()+1):
        hm.SetBinContent(i,0)
        hm.SetBinError(i,0)
    for i in range(b2, hm.GetNbinsX()+1):
        hq1.SetBinContent(i,0)
        hq1.SetBinError(i,0)
    for i in range(b3, hm.GetNbinsX()+1):
        hq2.SetBinContent(i,0)
        hq2.SetBinError(i,0)

    hm.SetLineColor(r.kBlack)
    hq1.SetLineColor(r.kRed)
    hq2.SetLineColor(r.kGreen+2)
    hq3.SetLineColor(r.kBlue)
    hm.SetMarkerColor(r.kBlack)
    hq1.SetMarkerColor(r.kRed)
    hq2.SetMarkerColor(r.kGreen+2)
    hq3.SetMarkerColor(r.kBlue)

    hm.Rebin(1)
    hq1.Rebin(1)
    hq2.Rebin(1)
    hq3.Rebin(1)

    c = r.TCanvas()
    c.SetLogy()
    
    hm.GetXaxis().SetRangeUser(0,40)
    hm.GetYaxis().SetRangeUser(1e-10, 2e0)
    hm.GetYaxis().SetTitle("particles / event / {0} MeV".format(int(hm.GetBinWidth(1) * 1000)))

    hm.Draw("L")
    hq1.Draw("L SAME")
    hq2.Draw("L SAME")
    hq3.Draw("L SAME")

    leg = r.TLegend(0.55,0.65,0.88,0.88)
    leg.AddEntry(hm, "MinBias", 'l')
    leg.AddEntry(hq1, "QCD pT 15to30", 'l')
    leg.AddEntry(hq2, "QCD pT 30to50", 'l')
    leg.AddEntry(hq3, "QCD pT 50to80", 'l')
    leg.Draw()

    if doPlot:
        c.SaveAs(os.path.join(plotdir, "h_{0}.png".format(p)))
        c.SaveAs(os.path.join(plotdir, "h_{0}.pdf".format(p)))

    hout = r.TH1D("h_"+p,";p_{T} [GeV]", hm.GetNbinsX(), hm.GetBinLowEdge(1), hm.GetXaxis().GetBinUpEdge(hm.GetNbinsX()))
    for i in range(1, hm.GetNbinsX()+1):
        h = hm
        if i >= b1:
            h = hq1
        if i >= b2:
            h = hq2
        if i >= b3:
            h = hq3
        hout.SetBinContent(i, h.GetBinContent(i))
        hout.SetBinError(i, h.GetBinError(i))
    hout.Write()

fout.Close()

