import os
import numpy as np
import ROOT as r
from patterns import *
r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)

# TAG1 = "v5_v6_kuhn_nodisp_1cm"
TAG1 = "geantsim_run3"
# TAG2 = "v5_v6_kuhn_nodisp_1cm"
TAG2 = "franny_data"
NORM = True
outdir = os.path.join("/home/users/bemarsh/public_html/milliqan/geant_sim/muangles/test",TAG1+"_"+TAG2)
os.system("mkdir -p "+outdir)

# f1 = r.TFile("outputs/{0}.root".format(TAG1))
# h_top1 = f1.Get("h_top")
# h_side1 = f1.Get("h_side")
f1 = r.TFile("~/analysis/milliqan/geantDemoSim/slim_ntupler/looper/test_beam.root")
h_top1 = f1.Get("reco_fourSlab/muangles_top_2500")
h_side1 = f1.Get("reco_fourSlab/muangles_side_2500")

if TAG2.startswith("franny"):
    h_top2 = r.TH1D("h_top2","",8,0,8)
    h_top2.SetBinContent(1, 25)
    h_top2.SetBinContent(2, 47)
    h_top2.SetBinContent(3, 217)
    h_top2.SetBinContent(4, 523)
    h_top2.SetBinContent(5, 539)
    h_top2.SetBinContent(6, 240)
    h_top2.SetBinContent(7, 61)
    h_top2.SetBinContent(8, 40)
    for i in range(h_top2.GetNbinsX()):
        h_top2.SetBinError(i+1, np.sqrt(h_top2.GetBinContent(i+1)))
    # h_side2 = h_side1.Clone("h_side2")
    h_side2 = r.TH1D("h_side2","",11,0,11)
    h_side2.SetBinContent(1, 19)
    h_side2.SetBinContent(2, 57)
    h_side2.SetBinContent(3, 102)
    h_side2.SetBinContent(4, 91)
    h_side2.SetBinContent(5, 330)
    h_side2.SetBinContent(6, 228)
    h_side2.SetBinContent(7, 288)
    h_side2.SetBinContent(8, 133)
    h_side2.SetBinContent(9, 166)
    h_side2.SetBinContent(10, 80)
    h_side2.SetBinContent(11, 27)
    for i in range(h_side2.GetNbinsX()):
        h_side2.SetBinError(i+1, np.sqrt(h_side2.GetBinContent(i+1)))
else:
    f2 = r.TFile("outputs/{0}.root".format(TAG2))
    h_top2 = f2.Get("h_top")
    h_side2 = f2.Get("h_side")

cs = []
boxes = []
for typ in ["top","side"]:

    patts = patts_side if typ=="side" else patts_top
    h1 = h_side1 if typ=="side" else h_top1
    h2 = h_side2 if typ=="side" else h_top2
    if NORM:
        SF = h2.Integral()/h1.Integral()
        h1.Scale(SF)
    h1err = h1.Clone("h1err")
    hratio = h2.Clone("hratio")
    hratio.Divide(h1)

    c = r.TCanvas("c"+typ,"c"+typ, 700, 700)
    p0 = r.TPad("p0","p0",0.0,0.3,1.0,1.0)
    p0.SetTickx()
    p0.SetTicky()
    p0.SetTopMargin(0.10)
    p0.SetBottomMargin(0)
    p0.SetRightMargin(0.05)
    p0.SetLeftMargin(0.13)    
    p1 = r.TPad("p1","p1",0.0,0.0,1.0,0.3)
    p1.SetTickx()
    p1.SetTicky()
    p1.SetTopMargin(0)
    p1.SetBottomMargin(0.5)
    p1.SetRightMargin(0.05)
    p1.SetLeftMargin(0.13)    
    
    p1.Draw()
    p0.Draw()
    p0.cd()

    top = p0.GetTopMargin()
    bot = p1.GetBottomMargin()
    left = p0.GetLeftMargin()
    right = p0.GetRightMargin()
    h1.SetLineColor(r.kBlack)
    h1.SetFillColor(r.kAzure-9)
    h2.SetLineColor(r.kBlack)
    h2.SetMarkerColor(r.kBlack)
    h2.SetMarkerStyle(20)
    h2.SetLineWidth(2)
    h1err.SetFillStyle(3344)
    h1err.SetFillColor(r.kGray+3)    
    h1.SetTitle("")
    h1.GetXaxis().SetNdivisions(len(patts))
    h1.GetXaxis().SetLabelSize(0)
    h1.GetYaxis().SetTitle("Events")
    h1.GetYaxis().SetTitleOffset(1.5)
    h1.GetYaxis().SetTitleSize(0.04)
    h1.GetYaxis().SetLabelSize(0.04)
    h1.GetYaxis().SetRangeUser(1e-2, (1.10*max(h1.GetMaximum(), h2.GetMaximum())))
    h1.Draw("HIST")
    h1err.Draw("SAME E2")
    h2.Draw("SAME PE")

    text = r.TLatex()
    text.SetNDC(1)
    text.SetTextFont(42)
    text.SetTextAlign(31)
    text.SetTextSize(0.045)
    text.DrawLatex(1.0-right-0.01, 1.0-top+0.015, "35 fb^{-1} (13 TeV)")
    text.SetTextFont(62)
    text.SetTextAlign(11)
    text.DrawLatex(left+0.01, 1.0-top+0.015, "milliQan")
    if NORM:
        text.SetTextFont(62)
        text.SetTextAlign(11)
        text.DrawLatex(left+0.04, 1.0-top-0.08, "SF = {0:.2f}".format(SF))

    h1.Draw("SAME AXIS")

    leg = r.TLegend(0.69, 0.65, 0.91, 0.85)
    # leg.SetLineWidth(0)
    leg.AddEntry(h2, "Data", 'ple')
    leg.AddEntry(h1, "Simulation", 'f')
    leg.Draw()

    p0.Update()

    p1.cd()
    hratio.SetLineColor(r.kBlack)
    hratio.SetMarkerColor(r.kBlack)
    hratio.SetMarkerStyle(20)
    hratio.GetYaxis().SetRangeUser(0.0, 1.99)
    hratio.GetYaxis().SetNdivisions(504)
    hratio.GetYaxis().SetLabelSize(0.09)
    hratio.GetYaxis().SetLabelOffset(0.01)
    hratio.GetXaxis().SetLabelSize(0)
    hratio.GetXaxis().SetNdivisions(len(patts))
    hratio.GetXaxis().SetTickSize(0.04)
    hratio.Draw("PE")

    bin_width = (1.0 - left - right) / len(patts)
    bar_width = (1.0 - left - right) / 80.0
    bar_height = bot/4
    y_center = bot/2
    for ipatt,patt in enumerate(patts):
        x_center = left + (ipatt+0.5)*bin_width
        for i in range(len(patt)):
            ic = -(i - (len(patt)-1)/2.0)
            yc = y_center + ic*(1.1*bar_height)
            for j in range(len(patt[i])):
                ic = j - (len(patt[i])-1)/2.0
                xc = x_center + ic*(1.4*bar_width)
            
                box = r.TLegend(xc-bar_width/2, yc-bar_height/2, xc+bar_width/2, yc+bar_height/2)
                if patt[i][j] == 1:
                    box.SetFillColor(r.kBlack)
                if patt[i][j] == 0:
                    box.SetFillColor(r.kBlack)
                    r.gStyle.SetHatchesSpacing(0.7)
                    box.SetFillStyle(3354)
                if patt[i][j] == -1:
                    box.SetLineColor(r.kBlack)
                box.Draw()
                boxes.append(box)

    line = r.TLine()
    line.SetLineStyle(2)
    line.DrawLine(0, 1, len(patts), 1)

    cs.append(c)
    c.SaveAs(os.path.join(outdir, typ+".png"))
    c.SaveAs(os.path.join(outdir, typ+".pdf"))

# raw_input()
