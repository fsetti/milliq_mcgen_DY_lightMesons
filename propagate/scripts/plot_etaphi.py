import glob
import os
import numpy as np
import ROOT as r
r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(1)

    # pt cuts (if pt is less than pt_cut for a given mass, don't bother propagating)
m_vals  = [0.01, 0.05, 0.1,  0.2, 0.3, 0.4, 0.5, 0.7, 1.0, 1.4, 1.6, 1.8, 2.0, 3.0, 4.0, 5.0, 7.0, 10.0]
pt_cuts = [0.10, 0.15, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.2, 1.4, 1.8, 2.2, 2.5, 3.0, 3.5]

def plot_etaphi(ch, m, q, outname=None):

    c = r.TCanvas("c","c",1600,500)
    p0 = r.TPad("1","1",0.0,   0.0, 0.333,1.0)
    p1 = r.TPad("2","2",0.333, 0.0, 0.666,1.0)
    p2 = r.TPad("3","3",0.666, 0.0, 1.0,  1.0)
    p0.Draw()
    p1.Draw()
    p2.Draw()

    ch.GetEntry(0)
    phimin = ch.mCP_phimin
    phimax = ch.mCP_phimax
    etamin = ch.mCP_etamin
    etamax = ch.mCP_etamax

    h_etap = r.TH1D("h_etap",";eta", 60, etamin-0.15, etamax+0.15)
    h_phip = r.TH1D("h_phip",";phi", 60, phimin-0.2, phimax+0.2)
    h_ptp = r.TH1D("h_ptp",";pt", 100, 0, 2)
    h_etam = r.TH1D("h_etam",";eta", 60, etamin-0.15, etamax+0.15)
    h_phim = r.TH1D("h_phim",";phi", 60, phimin-0.2, phimax+0.2)
    h_ptm = r.TH1D("h_ptm",";pt", 100, 0, 2)

    ch.Draw("p4_p.phi()>>h_phip","does_hit_p","goff")
    ch.Draw("-p4_m.phi()>>h_phim","does_hit_m","goff")
    ch.Draw("p4_p.eta()>>h_etap","does_hit_p","goff")
    ch.Draw("p4_m.eta()>>h_etam","does_hit_m","goff")
    ch.Draw("p4_p.pt()>>h_ptp","does_hit_p","goff")
    ch.Draw("p4_m.pt()>>h_ptm","does_hit_m","goff")

    p0.cd()

    h_etap.SetLineColor(r.kBlue)
    h_etam.SetLineColor(r.kRed)

    h_etap.SetMaximum(1.2*max(h_etap.GetMaximum(),h_etam.GetMaximum()))
    h_etap.Draw("HIST")
    h_etam.Draw("HIST SAME")
    line = r.TLine()
    line.SetLineWidth(2)
    line.SetLineStyle(2)
    line.DrawLine(etamin, 0, etamin, h_etap.GetMaximum() / 1.2)
    line.DrawLine(etamax, 0, etamax, h_etap.GetMaximum() / 1.2)

    p1.cd()

    h_phip.SetMaximum(1.2*max(h_phip.GetMaximum(),h_phim.GetMaximum()))
    h_phip.SetLineColor(r.kBlue)
    h_phim.SetLineColor(r.kRed)

    h_phip.Draw("HIST")
    h_phim.Draw("HIST SAME")
    line.DrawLine(phimin, 0, phimin, h_phip.GetMaximum() / 1.2)
    line.DrawLine(phimax, 0, phimax, h_phip.GetMaximum() / 1.2)

    p2.cd()

    h_ptp.SetMaximum(1.2*max(h_ptp.GetMaximum(),h_ptm.GetMaximum()))
    h_ptp.SetLineColor(r.kBlue)
    h_ptm.SetLineColor(r.kRed)

    h_ptp.Draw("HIST")
    h_ptm.Draw("HIST SAME")
    pt_cut = np.interp(m, m_vals, pt_cuts) * min(q/0.1,1.0)**2
    line.DrawLine(pt_cut, 0, pt_cut, h_ptp.GetMaximum() / 1.2)

    if outname:
        c.SaveAs(outname+".pdf")
        c.SaveAs(outname+".png")

def plot_etaparent(ch, outname=None):

    c = r.TCanvas("c","c",800,600)
    h_etap = r.TH1D("h_etap",";eta", 60 , -3.2, 3.2)
    ch.Draw("parent_p4.eta()>>h_etap","does_hit_p || does_hit_m","goff")
    h_etap.SetLineColor(r.kBlue)
    h_etap.Draw("HIST")
    line = r.TLine()
    line.SetLineWidth(2)
    line.SetLineStyle(2)
    line.DrawLine(-3, 0, -3, h_etap.GetMaximum() / 1.2)
    line.DrawLine(3, 0, 3, h_etap.GetMaximum() / 1.2)
    if outname:
        c.SaveAs(outname+".pdf")
        c.SaveAs(outname+".png")

ntuple_tag = "v8"
sim_tag = "v1_save2m"

basedir = "/nfs-7/userdata/bemarsh/milliqan/milliq_mcgen/merged_sim/{0}_{1}/".format(ntuple_tag, sim_tag)
for mdir in glob.glob(os.path.join(basedir, "*")):
    mname = os.path.split(mdir)[1]
    m = float(mname.split("_")[1].replace("p","."))
    for qdir in glob.glob(os.path.join(mdir, "q*")):
        qname = os.path.split(qdir)[1]
        q = float(qname.split("_")[1].replace("p","."))
        for sfile in glob.glob(os.path.join(qdir, "*.root")):
            samp = os.path.split(sfile)[1].split(".")[0]

            # if samp != "dy":
            #     continue

            print mname, qname, samp

            ch = r.TChain("Events")
            ch.Add(sfile)

            if ch.GetEntries()==0:
                continue

            outdir = os.path.join("~/public_html/milliqan/milliq_mcgen/plots/etaphi",ntuple_tag,mname,qname)
            os.system("mkdir -p "+outdir)
            os.system("cp ~/scripts/index.php "+outdir)
            plot_etaphi(ch, m=m, q=q, outname=os.path.join(outdir,samp))
    
            outdir = os.path.join("~/public_html/milliqan/milliq_mcgen/plots/etaparent",ntuple_tag,mname,qname)
            os.system("mkdir -p "+outdir)
            os.system("cp ~/scripts/index.php "+outdir)
            plot_etaparent(ch, outname=os.path.join(outdir,samp))
    
