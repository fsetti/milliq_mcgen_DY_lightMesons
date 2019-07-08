import glob
import os
import numpy as np
import ROOT as r
r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(1)

ntuple_tag = "v3"
qs = [0.1,0.01]
     
fin = r.TFile("rates.root")

samp_names = {
    1:  "b_jpsi",
    2:  "b_psiprime",
    3:  "rho",
    4:  "omega",
    5:  "phi",
    6:  "pi0",
    7:  "eta",
    8:  "etaprime_photon",
    9:  "omega_pi0",
    10: "etaprime_omega",
    11: "jpsi",
    12: "psiprime",
    13: "ups1S",
    14: "ups2S",
    15: "ups3S",
    }

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

def make_plots(type_):
    if type_ not in ["rate","acc"]:
        raise Exception()

    for q in qs:

        c = r.TCanvas("c"+str(q),"c",800,600)
        c.SetTopMargin(0.05)
        c.SetBottomMargin(0.13)
        c.SetLeftMargin(0.11)
        c.SetRightMargin(0.03)
        c.SetLogx()
        if type_=="rate":
            c.SetLogy()
        c.SetTicky()

        hdummy = r.TH1F("hdummy"+str(q),"",100,5e-3,10)
        hdummy.SetLineColor(r.kWhite)
        hdummy.GetXaxis().SetRangeUser(5e-3,10)
        if type_=="rate":
            hdummy.GetYaxis().SetRangeUser(1e-1*q**2,1e12*q**2)
            hdummy.GetYaxis().SetTitle("Incidence rate [hits / m^{2} / fb^{-1}]")
        elif type_=="acc":
            # hdummy.GetYaxis().SetRangeUser(1e-6, 1e-2)
            hdummy.GetYaxis().SetRangeUser(0, 2.7e-4)
            hdummy.GetYaxis().SetTitle("Acceptance (per m^{2})")
        hdummy.GetXaxis().SetTitle("m_{mCP} [GeV]")
        hdummy.GetXaxis().SetTitleSize(0.045)
        hdummy.GetXaxis().SetTitleOffset(1.20)
        hdummy.GetYaxis().SetTitleSize(0.045)
        hdummy.GetYaxis().SetTitleOffset(1.16)

        hdummy.Draw()

        gs = {}
        for i in range(1,16):
            gs[i] = fin.Get("{0}_q{1}_{2}".format(type_, str(q).replace(".","p"), samp_names[i]))
            gs[i].SetLineWidth(1 if type_=="acc" else 2)
            gs[i].SetLineColor(colors[i])
            gs[i].SetMarkerStyle(1 if type_=="acc" else 20)
            gs[i].SetMarkerColor(colors[i])
            gs[i].Draw("SAME LP")

        gt = fin.Get("{0}_q{1}_{2}".format(type_, str(q).replace(".","p"), "total"))
        gt.SetLineWidth(3)
        gt.SetLineStyle(2)
        gt.SetLineColor(r.kBlack)
        gt.SetMarkerStyle(20)
        gt.SetMarkerColor(r.kBlack)
        gt.Draw("SAME LP")

        line = r.TLine()
        line.SetLineWidth(gt.GetLineWidth())
        line.SetLineStyle(gt.GetLineStyle())
        line.SetLineColor(gt.GetLineColor())
        text = r.TLatex()
        text.SetNDC(1)
        text.SetTextFont(42)
        text.SetTextAlign(12)
        text.SetTextSize(0.032)
        line.DrawLineNDC(0.327, 0.916, 0.365, 0.916)
        text.DrawLatex(0.375, 0.919, "Total non-Drell-Yan #zeta^{+}#zeta^{#kern[0.3]{#minus}} "+("acceptance" if type_=="acc" else type_))

        text.SetTextAlign(32)
        text.DrawLatex(0.92, 0.65, "#bf{pp} (13 TeV)")
        text.DrawLatex(0.92, 0.61, "#eta(parent) #in [-2, 2]")

        leg = r.TLegend(0.32,0.7,0.93,0.892)
        leg.SetFillStyle(0)
        leg.SetLineWidth(0)
        leg.SetNColumns(4)

        leg.AddEntry(gs[6], "#pi^{0}#rightarrow#zeta#zeta#gamma", 'l')
        leg.AddEntry(gs[3], "#rho#rightarrow#zeta#zeta", 'l')
        leg.AddEntry(gs[11], "J/#psi#rightarrow#zeta#zeta", 'l')
        leg.AddEntry(gs[13], "#varUpsilon#scale[0.7]{(1S)}#rightarrow#zeta#zeta", 'l')

        leg.AddEntry(gs[7], "#eta#rightarrow#zeta#zeta#gamma", 'l')
        leg.AddEntry(gs[8], "#eta'#rightarrow#zeta#zeta#gamma", 'l')
        leg.AddEntry(gs[12], "#psi#scale[0.7]{(2S)}#rightarrow#zeta#zeta", 'l')
        leg.AddEntry(gs[14], "#varUpsilon#scale[0.7]{(2S)}#rightarrow#zeta#zeta", 'l')

        leg.AddEntry(gs[9], "#omega#rightarrow#zeta#zeta#pi^{0}", 'l')
        leg.AddEntry(gs[5], "#phi#rightarrow#zeta#zeta", 'l')
        leg.AddEntry(gs[1], "B#rightarrowJ/#psiX, J/#psi#rightarrow#zeta#zeta", 'l')
        leg.AddEntry(gs[15], "#varUpsilon#scale[0.7]{(3S)}#rightarrow#zeta#zeta", 'l')

        leg.AddEntry(gs[4], "#omega#rightarrow#zeta#zeta", 'l')
        leg.AddEntry(gs[10], "#eta'#rightarrow#zeta#zeta#omega", 'l')
        leg.AddEntry(gs[2], "B#rightarrow#psi#scale[0.7]{(2S)}X, #psi#scale[0.7]{(2S)}#rightarrow#zeta#zeta", 'l')
        leg.AddEntry(hdummy, "", 'l')
        leg.Draw()

        outdir = os.path.join("~/public_html/milliqan/milliq_mcgen/",type_,ntuple_tag)
        os.system("mkdir -p "+outdir)
        os.system("cp ~/scripts/index.php "+outdir)
        c.SaveAs(os.path.join(outdir, "q_"+str(q).replace(".","p")+".png"))
        c.SaveAs(os.path.join(outdir, "q_"+str(q).replace(".","p")+".pdf"))



make_plots("rate")
make_plots("acc")
