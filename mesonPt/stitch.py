import os
import ROOT as r
from math import log, exp
r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(1)

plotdir = "/home/users/bemarsh/public_html/milliqan/milliq_mcgen/pionPt/fromPythia_v2_monash2013/stitch"
os.system("mkdir -p "+plotdir)

dname = "hadded/fromPythia_v2_monash2013"

doPlot = True

fm = r.TFile(os.path.join(dname, "minbias.root"))
fq1 = r.TFile(os.path.join(dname, "qcd_pt15to30.root"))
fq2 = r.TFile(os.path.join(dname, "qcd_pt30to50.root"))
fq3 = r.TFile(os.path.join(dname, "qcd_pt50to80.root"))
fq4 = r.TFile(os.path.join(dname, "qcd_pt80to120.root"))

# special file to get phis from pythia6 DW tune
fphi = r.TFile("hadded/pythia6_DW_minbias_franny.root")

fout = r.TFile("pt_dists.root", "RECREATE")

nev_m = fm.Get("h_nevents").GetBinContent(1)
nev_q1 = fq1.Get("h_nevents").GetBinContent(1)
nev_q2 = fq2.Get("h_nevents").GetBinContent(1)
nev_q3 = fq3.Get("h_nevents").GetBinContent(1)
nev_q4 = fq4.Get("h_nevents").GetBinContent(1)

cuts = [10.0, 18.5, 30.0, 50.0]

ps = ["pi","pi0","rho","omega","phi","eta","etap","mu","mu_nonbc"]
for p in ps:
    if p != "phi":
        hm = fm.Get("h_"+p)
    else:
        hm = fphi.Get("h_phi_pT")
    hq1 = fq1.Get("h_"+p)
    hq2 = fq2.Get("h_"+p)
    hq3 = fq3.Get("h_"+p)
    hq4 = fq4.Get("h_"+p)

    # scale by # events
    if p!= "phi":
        hm.Scale(1.0 / nev_m)
    hq1.Scale(1.0 / nev_q1)
    hq2.Scale(1.0 / nev_q2)
    hq3.Scale(1.0 / nev_q3)
    hq4.Scale(1.0 / nev_q4)

    # ad-hoc adjustments based on data comparisons
    linedef = None
    if p=="eta":
        linedef = ((3.0, 1.0), (0.5, 2.0))
    if p=="rho" or p=="omega":
        linedef = ((1.0, 1.0), (0.5, 2.0))
    if linedef:
        m = (linedef[0][1]-linedef[1][1])/(log(linedef[0][0])-log(linedef[1][0]))
        b = linedef[0][1]-m*log(linedef[0][0])
        f = lambda x: m*log(x)+b
        for i in range(1, hm.GetNbinsX()+1):
            x = hm.GetBinCenter(i)
            if x>linedef[0][0]:
                break
            scale = 1.0 / f(x)
            hm.SetBinContent(i, hm.GetBinContent(i)*scale)
            hm.SetBinError(i, hm.GetBinError(i)*scale)
            
            

    # scale by xsec ratios
    hq1.Scale(1837410. / 78418400)
    hq2.Scale( 140932. / 78418400)
    hq3.Scale(  19204. / 78418400)
    hq4.Scale(   2763. / 78418400)
    hqa = hq1.Clone("hqa")
    hqa.Add(hq2)
    hqa.Add(hq3)
    hqa.Add(hq4)

    int_range = (10.0, 16.0)
    c = r.TCanvas()
    ratio_n = hm.Clone("ratio_n")
    ratio_d = hqa.Clone("ratio_d")
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
        
    int_qa = hqa.Integral(hm.FindBin(int_range[0]), hm.FindBin(int_range[1])-1)
    int_m  =  hm.Integral(hm.FindBin(int_range[0]), hm.FindBin(int_range[1])-1)
    qcd_mb_sf = int_m / int_qa

    print "QCD-MinBias SF:", qcd_mb_sf
    hq1.Scale(qcd_mb_sf)
    hq2.Scale(qcd_mb_sf)
    hq3.Scale(qcd_mb_sf)
    hq4.Scale(qcd_mb_sf)
    hqa.Scale(qcd_mb_sf)

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
    b4 = hq1.FindBin(cuts[3])
    for i in range(b1, hm.GetNbinsX()+1):
        hm.SetBinContent(i,0)
        hm.SetBinError(i,0)
    # for i in range(b2, hm.GetNbinsX()+1):
    #     hq1.SetBinContent(i,0)
    #     hq1.SetBinError(i,0)
    # for i in range(b3, hm.GetNbinsX()+1):
    #     hq2.SetBinContent(i,0)
    #     hq2.SetBinError(i,0)
    # for i in range(b4, hm.GetNbinsX()+1):
    #     hq3.SetBinContent(i,0)
    #     hq3.SetBinError(i,0)

    hm.SetLineColor(r.kBlack)
    hm.SetMarkerColor(r.kBlack)
    hm.SetFillColor(r.kBlack)
    hq1.SetLineColor(r.kRed-7)
    hq1.SetMarkerColor(r.kRed-7)
    hq1.SetFillColor(r.kRed-7)
    hq2.SetLineColor(r.kSpring-5)
    hq2.SetMarkerColor(r.kSpring-5)
    hq2.SetFillColor(r.kSpring-5)
    hq3.SetLineColor(r.kOrange)
    hq3.SetMarkerColor(r.kOrange)
    hq3.SetFillColor(r.kOrange)
    hq4.SetLineColor(r.kAzure+7)
    hq4.SetMarkerColor(r.kAzure+7)
    hq4.SetFillColor(r.kAzure+7)

    hm.Rebin(1)
    hq1.Rebin(1)
    hq2.Rebin(1)
    hq3.Rebin(1)
    hq4.Rebin(1)

    stack = r.THStack()
    stack.Add(hq4)
    stack.Add(hq3)
    stack.Add(hq2)
    stack.Add(hq1)

    c = r.TCanvas()
    c.SetLogy()
    
    hm.GetXaxis().SetTitle("p_{T} [GeV]")
    hm.GetXaxis().SetRangeUser(0,40)
    if "mu" in p:
        hm.GetYaxis().SetRangeUser(1e-13, 2e0)
    else:
        hm.GetYaxis().SetRangeUser(1e-10, 2e0)
    hm.GetYaxis().SetTitle("particles / event / {0} MeV".format(int(hm.GetBinWidth(1) * 1000)))

    hm.Draw("L")
    # hq1.Draw("L SAME")
    # hq2.Draw("L SAME")
    # hq3.Draw("L SAME")
    # hq4.Draw("L SAME")
    stack.Draw("HIST SAME")
    hm.Draw("L SAME")

    leg = r.TLegend(0.55,0.59,0.88,0.88)
    leg.AddEntry(hm, "MinBias", 'l')
    leg.AddEntry(hq1, "QCD pT 15to30", 'f')
    leg.AddEntry(hq2, "QCD pT 30to50", 'f')
    leg.AddEntry(hq3, "QCD pT 50to80", 'f')
    leg.AddEntry(hq4, "QCD pT 80to120", 'f')
    leg.Draw()

    if doPlot:
        c.SaveAs(os.path.join(plotdir, "h_{0}.png".format(p)))
        c.SaveAs(os.path.join(plotdir, "h_{0}.pdf".format(p)))

    hout = r.TH1D("h_"+p,";p_{T} [GeV]", hm.GetNbinsX(), hm.GetBinLowEdge(1), hm.GetXaxis().GetBinUpEdge(hm.GetNbinsX()))
    for i in range(1, hm.GetNbinsX()+1):
        h = hm
        if i >= b1:
            h = hqa

        # if i >= b1:
        #     h = hq1
        # if i >= b2:
        #     h = hq2
        # if i >= b3:
        #     h = hq3
        # if i >= b4:
        #     h = hq4
        hout.SetBinContent(i, h.GetBinContent(i))
        hout.SetBinError(i, h.GetBinError(i))
    hout.Write()

fout.Close()

