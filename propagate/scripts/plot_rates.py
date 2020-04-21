import glob
import os
import numpy as np
import ROOT as r
r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(1)

# ntuple_tag = "mapp_theta5_v1"
ntuple_tag = "v8"
sim_tag = "v1_save2m"
extra_tag = ""
# extra_tag = "_upsFix"
# qs = [0.1,0.07,0.05,0.02,0.01]
qs = [0.006, 0.008, 0.012, 0.017]
# qs = [0.3,0.2,0.1,0.05,0.01]
# qs = [0.02,0.014,0.01,0.007,0.005]
# qs = [0.3,0.2,0.14]

Z_ZOOM = True
     
fin = r.TFile("rate_files/{0}_{1}.root".format(ntuple_tag,sim_tag))
# lumi = None
lumi = 35
area = None
# area = 0.0150

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
    16:  "dy",
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
    16:  r.kYellow+2,
    }

def make_plots(type_):
    if type_ not in ["rate","line_rate","acc","line_acc"]:
        raise Exception()

    for q in qs:

        c = r.TCanvas("c"+str(q),"c",800,600)
        c.SetTopMargin(0.05)
        c.SetBottomMargin(0.13)
        c.SetLeftMargin(0.11)
        c.SetRightMargin(0.03)
        c.SetLogx()
        if type_ in ["rate","line_rate"]:
            c.SetLogy()
        c.SetTicky()

        hdummy = r.TH1F("hdummy"+str(q),"",100,5e-3,160 if Z_ZOOM else 16)
        hdummy.SetLineColor(r.kWhite)
        hdummy.GetXaxis().SetRangeUser(5e-3,160 if Z_ZOOM else 16)
        if type_=="rate":
            mult = 1.0
            if lumi is not None:
                mult *= lumi
            if area is not None:
                mult *= area
            hdummy.GetYaxis().SetRangeUser((1e-3 if Z_ZOOM else 1e-1)*q**2*mult,1e12*q**2*mult)
            if lumi is None:
                if area is None:
                    hdummy.GetYaxis().SetTitle("Incidence rate [hits / m^{2} / fb^{-1}]")
                else:
                    hdummy.GetYaxis().SetTitle("Incidence rate [hits / fb^{-1}]")
            else:
                if area is None:
                    hdummy.GetYaxis().SetTitle("Yield (per m^{2})")
                else:
                    hdummy.GetYaxis().SetTitle("Yield")
        elif type_=="line_rate":
            mult = 1.0
            if lumi is not None:
                mult *= lumi
            hdummy.GetYaxis().SetRangeUser((1e-5 if Z_ZOOM else 1e-3)*q**2*mult, 1e10*q**2*mult)
            hdummy.GetYaxis().SetTitle("Yield")
        elif type_=="acc":
            # hdummy.GetYaxis().SetRangeUser(1e-6, 1e-2)
            hdummy.GetYaxis().SetRangeUser(0, 2.3e-4)
            hdummy.GetYaxis().SetTitle("Acceptance (per m^{2})")
        elif type_=="line_acc":
            hdummy.GetYaxis().SetRangeUser(0, 1.8)
            hdummy.GetYaxis().SetTitle("p(3 bars in line)")
        hdummy.GetXaxis().SetTitle("m_{mCP} [GeV]")
        hdummy.GetXaxis().SetTitleSize(0.045)
        hdummy.GetXaxis().SetTitleOffset(1.20)
        hdummy.GetYaxis().SetTitleSize(0.045)
        hdummy.GetYaxis().SetTitleOffset(1.16)

        hdummy.Draw()

        gs = {}
        for i in sorted(samp_names.keys()):
            gs[i] = fin.Get("{0}_q{1}_{2}".format(type_, str(q).replace(".","p"), samp_names[i]))
            if not gs[i]:
                continue
            gs[i].SetLineWidth(1 if "acc" in type_ else 2)
            gs[i].SetLineColor(colors[i])
            gs[i].SetMarkerStyle(1 if "acc" in type_ else 20)
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
        what = "acceptance" if "acc" in type_ else "rate" if lumi is None else "yield"
        text.DrawLatex(0.375, 0.919, "Total non-Drell-Yan #zeta^{+}#zeta^{#kern[0.3]{#minus}} "+what)

        text.SetTextAlign(32)
        text.DrawLatex(0.92, 0.65, "Q(mCP) = {0}#kern[0.3]{{#it{{e}}}}".format(q))
        # text.DrawLatex(0.92, 0.61, "#eta(parent) #in [-2, 2]")

        text.SetTextAlign(11)
        text.SetTextFont(62)
        text.DrawLatex(0.12,0.96,"milliQan simulation")

        if lumi is not None and "acc" not in type_:
            text.SetTextAlign(31)
            text.SetTextFont(42)
            text.DrawLatex(0.96,0.96, "{0} fb^{{-1}} (13 TeV)".format(lumi))

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
        leg.AddEntry(gs[16], "Drell-Yan", 'l')
        # leg.AddEntry(hdummy, "", 'l')
        leg.Draw()

        outdir = os.path.join("~/public_html/milliqan/milliq_mcgen/plots/",type_,ntuple_tag+"_"+sim_tag+extra_tag)
        os.system("mkdir -p "+outdir)
        os.system("cp ~/scripts/index.php "+outdir)
        c.SaveAs(os.path.join(outdir, "q_"+str(q).replace(".","p")+".png"))
        c.SaveAs(os.path.join(outdir, "q_"+str(q).replace(".","p")+".pdf"))


def make_charge_comparisons(type_):
    if type_ not in ["rate","line_rate","threeLayer_rate","acc","line_acc"]:
        raise Exception()

    c = r.TCanvas("c","c",800,600)
    c.SetTopMargin(0.07)
    c.SetBottomMargin(0.13)
    c.SetLeftMargin(0.11)
    c.SetRightMargin(0.03)
    c.SetLogx()
    if type_ in ["rate","line_rate","threeLayer_rate"]:
        c.SetLogy()
    c.SetTicky()
    c.SetGridx()
    c.SetGridy()

    hdummy = r.TH1F("hdummy","",100,5e-3,160 if Z_ZOOM else 16)
    hdummy.SetLineColor(r.kWhite)
    hdummy.GetXaxis().SetRangeUser(5e-3,160 if Z_ZOOM else 16)
    if type_=="rate":
        mult = 1.0
        if lumi is not None:
            mult *= lumi
        if area is not None:
            mult *= area
        hdummy.GetYaxis().SetRangeUser((1e-6 if Z_ZOOM else 1e-3)*mult, 2e7*mult)
        if lumi is None:
            if area is None:
                hdummy.GetYaxis().SetTitle("Incidence rate [hits / m^{2} / fb^{-1}]")
            else:
                hdummy.GetYaxis().SetTitle("Incidence rate [hits / fb^{-1}]")
        else:
            if area is None:
                hdummy.GetYaxis().SetTitle("Yield (per m^{2})")
            else:
                hdummy.GetYaxis().SetTitle("Yield")
    elif type_=="line_rate" or type_=="threeLayer_rate":
        mult = 1.0
        if lumi is not None:
            mult *= lumi
        hdummy.GetYaxis().SetRangeUser((1e-7 if Z_ZOOM else 1e-5)*mult, 2e5*mult)
        hdummy.GetYaxis().SetTitle("Yield")
    elif type_=="acc":
        hdummy.GetYaxis().SetRangeUser(0, 1.5e-4)
        hdummy.GetYaxis().SetTitle("Acceptance (per m^{2})")
    elif type_=="line_acc":
        hdummy.GetYaxis().SetRangeUser(0, 1.0)
        hdummy.GetYaxis().SetTitle("p(3 bars in line)")
    hdummy.GetXaxis().SetTitle("m_{mCP} [GeV]")
    hdummy.GetXaxis().SetTitleSize(0.045)
    hdummy.GetXaxis().SetTitleOffset(1.20)
    hdummy.GetYaxis().SetTitleSize(0.045)
    hdummy.GetYaxis().SetTitleOffset(1.16)
    
    hdummy.Draw()
    
    x = 0.65 if "rate" in type_ else 0.25
    y = 0.90
    leg = r.TLegend(x,y-0.05*len(qs),x+0.21,y)
    # leg.SetFillStyle(0)
    # leg.SetLineWidth(0)

    cs = [r.kBlack, r.kAzure-2, r.kOrange-3, r.kGreen+2, r.kRed+1]
    # cs = [r.kBlack, r.kAzure-2, r.kViolet-2, r.kOrange-3, r.kGreen+2, r.kRed+1, r.kAzure-9]
    for i,q in enumerate(qs):
        gt = fin.Get("{0}_q{1}_{2}".format(type_, str(q).replace(".","p"), "total"))
        gt.SetLineWidth(3)
        gt.SetLineStyle(1)
        gt.SetLineColor(cs[i])
        gt.SetMarkerStyle(20)
        gt.SetMarkerColor(cs[i])
        gt.Draw("SAME LP")
        leg.AddEntry(gt, "Q /#it{e} = "+str(q), 'pl')

    leg.Draw()

    text = r.TLatex()
    text.SetNDC(1)
    text.SetTextFont(62)
    text.SetTextSize(0.040)
    text.SetTextAlign(11)
    text.DrawLatex(0.12,0.94,"milliQan simulation")

    if lumi is not None and "acc" not in type_:
        text.SetTextFont(42)
        text.SetTextAlign(31)
        text.DrawLatex(0.94,0.94, "{0} fb^{{-1}} (13 TeV)".format(lumi))

    outdir = os.path.join("~/public_html/milliqan/milliq_mcgen/plots/",type_,ntuple_tag+"_"+sim_tag+extra_tag)
    os.system("mkdir -p "+outdir)
    os.system("cp ~/scripts/index.php "+outdir)
    c.SaveAs(os.path.join(outdir, "qcomp.png"))
    c.SaveAs(os.path.join(outdir, "qcomp.pdf"))
        

make_plots("rate")
make_plots("line_rate")
make_plots("acc")
make_plots("line_acc")
make_charge_comparisons("rate")
make_charge_comparisons("line_rate")
make_charge_comparisons("threeLayer_rate")
make_charge_comparisons("acc")
make_charge_comparisons("line_acc")
