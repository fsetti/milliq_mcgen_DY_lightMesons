import glob
import os
import numpy as np
import ROOT as r
r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(1)

ntuple_tag = "v3"
sim_tag = "v3"

lumi = 30.0 # in fb^-1
area = 1.0 # in m^2
# lumi = 30.0 # in fb^-1
# area = 0.0150 # in m^2

def get_rate(ch, q, lumi=1.0):
    h = r.TH1D("h","",1,0,2)
    ch.Draw("1>>h","(does_hit_p + does_hit_m)*({0}^2 * xsec * BR_q1 * filter_eff * weight * 1000*{1} / n_events_total)".format(q,lumi),"goff")
    return (h.GetBinContent(1), h.GetBinError(1))

def get_line_rate(ch, q, lumi=1.0):
    h = r.TH1D("h","",1,0,2)
    ch.Draw("1>>h","(hit_p_line + hit_m_line)*({0}^2 * xsec * BR_q1 * filter_eff * weight * 1000*{1} / n_events_total)".format(q,lumi),"goff")
    return (h.GetBinContent(1), h.GetBinError(1))

def get_acceptance(ch):
    n_acc = ch.GetEntries()
    if n_acc == 0:
        return 0.0, 0.0, 0.0
    h = r.TH1D("h","",1,0,2)
    ch.Draw("filter_eff>>h","","goff")
    filter_eff = h.GetMean()
    ch.GetEntry(0)
    acc = float(n_acc) / ch.n_events_total
    err = np.sqrt(acc*(1-acc)/ch.n_events_total)
    acc *= filter_eff
    err *= filter_eff
    N = ch.n_events_total / filter_eff
    return acc, err, N

def get_line_acceptance(ch):
    # relative to all mCPs that hit at least 1 bar
    h = r.TH1D("h","",1,0,2)
    ch.Draw("1>>h","hit_p_nbars>0 || hit_m_nbars>0","goff")
    # ch.Draw("1>>h","(does_hit_p && fabs(hit_p_xyz.X())<0.085 && fabs(hit_p_xyz.Y())<0.055)||(does_hit_m && fabs(hit_m_xyz.X())<0.085 && fabs(hit_m_xyz.Y())<0.055)","goff")
    den = h.Integral()
    if den == 0:
        return 0.0,0.0,0.0
    ch.Draw("1>>h","hit_p_line>0 || hit_m_line","goff")
    num = h.Integral()
    acc = num / den
    err = np.sqrt(acc*(1-acc)/den)
    return acc, err, den
    
rates = {}

# basedir = "/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/ntuples_{0}/".format(ntuple_tag)
basedir = "/nfs-7/userdata/bemarsh/milliqan/milliq_mcgen/merged_sim/{0}_{1}/".format(ntuple_tag, sim_tag)
for mdir in glob.glob(os.path.join(basedir, "*")):
    mname = os.path.split(mdir)[1]
    m = float(mname.split("_")[1].replace("p","."))
    for qdir in glob.glob(os.path.join(mdir,"q*")):
        qname = os.path.split(qdir)[1]
        q = float(qname.split("_")[1].replace("p","."))

        if q not in rates:
            rates[q] = {}
        if m not in rates[q]:
            rates[q][m] = {"total":{
                    "rate":0.0,
                    "rate_err":0.0,
                    "line_rate":0.0,
                    "line_rate_err":0.0,
                    "acc":0.0,
                    "acc_err":0.0,
                    "acc_N":0.0,
                    "line_acc":0.0,
                    "line_acc_err":0.0,
                    "line_acc_N":0.0,
                    }}

        for sfile in glob.glob(os.path.join(qdir, "*.root")):
            samp = os.path.split(sfile)[1].split(".")[0]

            print mname, qname, samp

            ch = r.TChain("Events")
            ch.Add(sfile)

            rate, rerr = get_rate(ch,q,lumi=lumi*area)
            lrate, lrerr = get_line_rate(ch,q,lumi=lumi*area)
            acc, aerr, N = get_acceptance(ch)
            lacc, laerr, lN = get_line_acceptance(ch)

            rates[q][m][samp] = {
                "rate": rate, 
                "rate_err": rerr, 
                "line_rate": lrate, 
                "line_rate_err": lrerr, 
                "acc": acc, 
                "acc_err": aerr,
                "acc_N": N,
                "line_acc": lacc, 
                "line_acc_err": laerr,
                "line_acc_N": lN,
                }
            rates[q][m]["total"]["rate"] += rate
            rates[q][m]["total"]["rate_err"] = np.sqrt(rerr**2 + rates[q][m]["total"]["rate_err"]**2)    
            rates[q][m]["total"]["line_rate"] += lrate
            rates[q][m]["total"]["line_rate_err"] = np.sqrt(lrerr**2 + rates[q][m]["total"]["line_rate_err"]**2)    
            rates[q][m]["total"]["acc"] += acc*N
            rates[q][m]["total"]["acc_err"] += aerr*N
            rates[q][m]["total"]["acc_N"] += N
            rates[q][m]["total"]["line_acc"] += lacc*lN
            rates[q][m]["total"]["line_acc_err"] += laerr*lN
            rates[q][m]["total"]["line_acc_N"] += lN            

        rates[q][m]["total"]["acc"] /= rates[q][m]["total"]["acc_N"]
        rates[q][m]["total"]["acc_err"] /= rates[q][m]["total"]["acc_N"]
        rates[q][m]["total"]["line_acc"] /= rates[q][m]["total"]["line_acc_N"]
        rates[q][m]["total"]["line_acc_err"] /= rates[q][m]["total"]["line_acc_N"]


types = ["rate","line_rate","acc","line_acc"]
fout = r.TFile("rates.root","RECREATE")
grs = {}
for q in rates:
    if q not in grs:
        grs[q] = {}
    masses = sorted(rates[q].keys())
    for m in masses:
        for s in rates[q][m].keys():
            if rates[q][m][s]["rate"]==0:
                continue
            if s not in grs[q]:
                grs[q][s] = {}
                for t in types:
                    grs[q][s][t] = r.TGraphErrors()
                    grs[q][s][t].SetName("{0}_q{1}_{2}".format(t,str(q).replace(".","p"), s))
            for t in types:
                if "rate" in t and rates[q][m][s][t] == 0:
                    continue
                gr = grs[q][s][t]
                N = gr.GetN()
                gr.SetPoint(N, m, rates[q][m][s][t])
                gr.SetPointError(N, 0, rates[q][m][s][t+"_err"])
for q in grs:
    for s in grs[q]:
        for t in types:
            grs[q][s][t].Write()
fout.Close()
