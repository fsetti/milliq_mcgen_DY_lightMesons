import glob
import os
import ROOT as r
r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(1)

def plot_etaphi(ch, outname=None):

    c = r.TCanvas("c","c",1000,400)
    p0 = r.TPad("1","1",0.0,0.0,0.5,1.0)
    p1 = r.TPad("2","2",0.5,0.0,1.0,1.0)
    p0.Draw()
    p1.Draw()

    ch.GetEntry(0)
    phimin = ch.mCP_phimin
    phimax = ch.mCP_phimax
    etamin = ch.mCP_etamin
    etamax = ch.mCP_etamax

    h_etap = r.TH1D("h_etap",";eta", 60, 0.02, 0.30)
    h_phip = r.TH1D("h_phip",";phi", 60, phimin-0.1, phimax+0.1)
    h_etam = r.TH1D("h_etam",";eta", 60, 0.02, 0.30)
    h_phim = r.TH1D("h_phim",";phi", 60, phimin-0.1, phimax+0.1)

    ch.Draw("p4_p.phi()>>h_phip","does_hit_p","goff")
    ch.Draw("-p4_m.phi()>>h_phim","does_hit_m","goff")
    ch.Draw("p4_p.eta()>>h_etap","does_hit_p","goff")
    ch.Draw("p4_m.eta()>>h_etam","does_hit_m","goff")

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

    if outname:
        c.SaveAs(outname+".pdf")
        c.SaveAs(outname+".png")

def plot_etaparent(ch, outname=None):

    c = r.TCanvas("c","c",800,600)
    h_etap = r.TH1D("h_etap",";eta", 60 , -2.2, 2.2)
    ch.Draw("parent_p4.eta()>>h_etap","does_hit_p || does_hit_m","goff")
    h_etap.SetLineColor(r.kBlue)
    h_etap.Draw("HIST")
    line = r.TLine()
    line.SetLineWidth(2)
    line.SetLineStyle(2)
    line.DrawLine(-2, 0, -2, h_etap.GetMaximum() / 1.2)
    line.DrawLine(2, 0, 2, h_etap.GetMaximum() / 1.2)
    if outname:
        c.SaveAs(outname+".pdf")
        c.SaveAs(outname+".png")

ntuple_tag = "v3"

basedir = "/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/ntuples_{0}/".format(ntuple_tag)
for mdir in glob.glob(os.path.join(basedir, "*")):
    mname = os.path.split(mdir)[1]
    for sdir in glob.glob(os.path.join(mdir, "*")):
        samp = os.path.split(sdir)[1]
        for qdir in glob.glob(os.path.join(sdir, "postsim_v1","q*")):
            qname = os.path.split(qdir)[1]

            print mname, qname, samp

            ch = r.TChain("Events")
            ch.Add(os.path.join(qdir, "*.root"))

            outdir = os.path.join("~/public_html/milliqan/milliq_mcgen/etaphi",ntuple_tag,mname,qname)
            os.system("mkdir -p "+outdir)
            os.system("cp ~/scripts/index.php "+outdir)
            plot_etaphi(ch, outname=os.path.join(outdir,samp))
    
            outdir = os.path.join("~/public_html/milliqan/milliq_mcgen/etaparent",ntuple_tag,mname,qname)
            os.system("mkdir -p "+outdir)
            os.system("cp ~/scripts/index.php "+outdir)
            plot_etaparent(ch, outname=os.path.join(outdir,samp))
    
