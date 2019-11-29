import os
import ROOT as r
r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)

ntuple_tag = "v5"
sim_tag = "v6_kuhn_save2m"

indir = "/nfs-7/userdata/bemarsh/milliqan/milliq_mcgen/merged_sim/muons_{0}_{1}".format(ntuple_tag, sim_tag)

outdir = "/home/users/bemarsh/public_html/milliqan/milliq_mcgen/plots/muons/{0}_{1}".format(ntuple_tag, sim_tag)
os.system("mkdir -p "+outdir)
os.system("cp ~/scripts/index.php "+outdir)

f_qcd = r.TFile(os.path.join(indir, "qcd.root"))
f_nonbc = r.TFile(os.path.join(indir, "qcd_nonbc.root"))
f_w = r.TFile(os.path.join(indir, "w.root"))
f_dy = r.TFile(os.path.join(indir, "dy.root"))

t_qcd = f_qcd.Get("Events")
t_nonbc = f_nonbc.Get("Events")
t_w = f_w.Get("Events")
t_dy = f_dy.Get("Events")

ch = r.TChain("Events")
ch.Add(os.path.join(indir, "qcd*.root"))
ch.Add(os.path.join(indir, "dy*.root"))
ch.Add(os.path.join(indir, "w*.root"))

# pT stack plot

h_pt_qcd = r.TH1D("h_pt_qcd", ";p_{T} [GeV]", 100, 0, 100)
h_pt_nonbc = r.TH1D("h_pt_nonbc", ";p_{T} [GeV]", 100, 0, 100)
h_pt_w = r.TH1D("h_pt_w", ";p_{T} [GeV]", 100, 0, 100)
h_pt_dy = r.TH1D("h_pt_dy", ";p_{T} [GeV]", 100, 0, 100)
h_hit_pt = r.TH1D("h_hit_pt",";p_{T} [GeV]", 100, 0, 100)
h_pt_slabs = r.TH1D("h_pt_slabs",";p_{T} [GeV]", 100, 0, 100)
h_ptthresh = r.TH1D("h_ptthresh", "", 100,0,100)

weight = "(xsec*filter_eff/n_events_total)"
t_qcd.Draw("p4_p.pt()>>h_pt_qcd", weight, "goff")
t_nonbc.Draw("p4_p.pt()>>h_pt_nonbc", weight, "goff")
t_w.Draw("p4_p.pt()>>h_pt_w", weight, "goff")
t_dy.Draw("p4_p.pt()>>h_pt_dy", weight, "goff")
ch.Draw("hit_p_p4.Pz()>>h_hit_pt", weight, "goff")
ch.Draw("hit_p_p4.Pz()>>h_pt_slabs", "({0})*(hit_p_slabs==15)".format(weight), "goff")
ch.Draw("p4_p.pt() - hit_p_p4.Pz()>>h_ptthresh", weight, "goff")

total_rate = h_hit_pt.Integral()
slab_rate = h_pt_slabs.Integral()
ptthresh = h_ptthresh.GetMean()

h_pt_qcd.SetLineColor(r.kBlack)
h_pt_qcd.SetFillColor(r.kAzure-1)
h_pt_nonbc.SetLineColor(r.kBlack)
h_pt_nonbc.SetFillColor(r.kAzure+7)
h_pt_w.SetLineColor(r.kBlack)
h_pt_w.SetFillColor(r.kSpring-5)
h_pt_dy.SetLineColor(r.kBlack)
h_pt_dy.SetFillColor(r.kOrange)
h_hit_pt.SetLineWidth(2)
h_hit_pt.SetLineColor(r.kRed+2)

c = r.TCanvas()
c.SetLogy()
c.cd()

stack = r.THStack("hs","")
stack.Add(h_pt_dy)
stack.Add(h_pt_w)
stack.Add(h_pt_nonbc)
stack.Add(h_pt_qcd)

stack.Draw("HIST")
h_hit_pt.Draw("HIST SAME")

stack.GetXaxis().SetTitle("p_{T} (at IP) [GeV]")
stack.GetYaxis().SetTitle("Muons / pb^{-1} / m^{2} / 1 GeV")
stack.GetXaxis().SetTitleSize(0.04)
stack.GetYaxis().SetTitleSize(0.04)

leg = r.TLegend(0.6,0.55,0.87,0.87)
leg.SetBorderSize(0)
leg.AddEntry(h_pt_qcd, "QCD (bc)", 'f')
leg.AddEntry(h_pt_nonbc, "QCD (non-bc)", 'f')
leg.AddEntry(h_pt_w, "W #rightarrow #mu#nu", 'f')
leg.AddEntry(h_pt_dy, "Drell-Yan", 'f')
leg.AddEntry(h_hit_pt, "p_{T} upon hit", 'l')
leg.Draw()

text = r.TLatex()
text.SetNDC(1)
text.SetTextFont(42)
text.SetTextSize(0.045)
text.SetTextAlign(33)
text.DrawLatex(0.87, 0.53, "Total rate: {0:.1f} muons / pb^{{-1}} / m^{{2}}".format(total_rate))
text.DrawLatex(0.87, 0.48, "Slab rate: {0:.3f} muons / pb^{{-1}}".format(slab_rate))
text.DrawLatex(0.87, 0.42, "p_{{T}} threshold: {0:.2f} GeV".format(ptthresh))

c.SaveAs(os.path.join(outdir, "h_pt.png"))
c.SaveAs(os.path.join(outdir, "h_pt.pdf"))

## kinematic plots
plots = {
    "thetaX" : {
        "var" : "atan(hit_p_p4.Px() / hit_p_p4.Pz())*180/pi",
        "xaxis" : "theta X [deg]",
        "bins" : (100,-10,10),
        "log" : False,
        },
    "thetaY" : {
        "var" : "atan(hit_p_p4.Py() / hit_p_p4.Pz())*180/pi",
        "xaxis" : "theta Y [deg]",
        "bins" : (100,-10,10),
        "log" : False,
        },
    "eta" : {
        "var" : "p4_p.eta()",
        "xaxis" : "eta",
        "bins" : (100,0.0,0.3),
        "log" : False,
        },
    "phi" : {
        "var" : "sim_q*p4_p.phi()",
        "xaxis" : "phi",
        "bins" : (100,-0.3,0.3),
        "log" : False,
        },
}

for pname,info in plots.items():
    c = r.TCanvas()
    c.SetLogy(info["log"])

    hp = r.TH1D("hp_"+pname, ";"+info["xaxis"], *info["bins"])
    hm = r.TH1D("hm_"+pname, ";"+info["xaxis"], *info["bins"])

    weight = "(xsec*filter_eff/n_events_total)"
    ch.Draw("{0}>>hp_{1}".format(info["var"], pname), weight+"*(sim_q>0)", "goff") 
    ch.Draw("{0}>>hm_{1}".format(info["var"], pname), weight+"*(sim_q<0)", "goff") 

    hp.SetLineColor(r.kBlue)
    hp.SetLineWidth(2)
    hm.SetLineColor(r.kRed)
    hm.SetLineWidth(2)

    hp.Draw("HIST")
    hm.Draw("HIST SAME")

    c.SaveAs(os.path.join(outdir, "h_{0}.png".format(pname)))
    c.SaveAs(os.path.join(outdir, "h_{0}.pdf".format(pname)))

