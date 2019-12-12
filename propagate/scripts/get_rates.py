import glob
import os
import json
import numpy as np
import ROOT as r
r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(1)

# ntuple_tag = "mapp_theta5_v1"
ntuple_tag = "v8"
sim_tag = "v1_save2m"
use_metadata = False

lumi = 35.0 # in fb^-1
area = 1.0 # in m^2
# lumi = 30.0 # in fb^-1
# area = 0.0150 # in m^2

def get_rate(ch, q, type_="rate", lumi=1.0, n_events_total=None):
    h = r.TH1D("h","",1,0,2)
    if n_events_total is None:
        n_events_total = "n_events_total"
    if type_=="rate":
        sel = "does_hit_p + does_hit_m"
    elif type_=="line_rate":
        sel = "hit_p_line + hit_m_line"
    elif type_=="threeLayer_rate":
        sel = "(hit_p_nlayers>=3) + (hit_m_nlayers>=3)"
    else:
        raise Exception()
    ch.Draw("1>>h","({0})*({1}^2 * xsec * BR_q1 * filter_eff * weight * 1000*{2} / {3})".format(sel,q,lumi,n_events_total), "goff")
    return (h.GetBinContent(1), h.GetBinError(1))

def get_acceptance(ch, n_events_total=None):
    n_acc = ch.GetEntries()
    if n_acc == 0:
        return 0.0, 0.0, 0.0
    h = r.TH1D("h","",1,0,2)
    ch.Draw("filter_eff>>h","","goff")
    filter_eff = h.GetMean()
    if n_events_total is None:
        ch.GetEntry(0)
        n_events_total = ch.n_events_total
    acc = float(n_acc) / n_events_total
    err = np.sqrt(acc*(1-acc)/n_events_total)
    acc *= filter_eff
    err *= filter_eff
    N = n_events_total / filter_eff
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

if use_metadata:
    metadata = {}
    basedir = "/hadoop/cms/store/user/bemarsh/milliqan/milliq_mcgen/ntuples_{0}".format(ntuple_tag)
    for mdir in glob.glob(os.path.join(basedir, "m_*")):
        mname = os.path.split(mdir)[1]
        metadata[mname] = {}
        for sdir in glob.glob(os.path.join(mdir, "*")):
            samp = os.path.split(sdir)[1]
            metadata[mname][samp] = json.load(open(os.path.join(sdir, "metadata.json")))

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
                    "threeLayer_rate":0.0,
                    "threeLayer_rate_err":0.0,
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

            # # for buggy xsecs
            xscorr = 1.0

            ne = None
            if use_metadata:
                ne = metadata[mname][samp]["n_events"]
            rate, rerr = get_rate(ch,q,lumi=lumi*area*xscorr, n_events_total=ne)
            lrate, lrerr = get_rate(ch,q,type_="line_rate",lumi=lumi*area*xscorr, n_events_total=ne)
            lyrate, lyrerr = get_rate(ch,q,type_="threeLayer_rate",lumi=lumi*area*xscorr, n_events_total=ne)
            acc, aerr, N = get_acceptance(ch, n_events_total=ne)
            lacc, laerr, lN = get_line_acceptance(ch)

            rates[q][m][samp] = {
                "rate": rate, 
                "rate_err": rerr, 
                "line_rate": lrate, 
                "line_rate_err": lrerr, 
                "threeLayer_rate": lyrate, 
                "threeLayer_rate_err": lyrerr, 
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
            rates[q][m]["total"]["threeLayer_rate"] += lyrate
            rates[q][m]["total"]["threeLayer_rate_err"] = np.sqrt(lyrerr**2 + rates[q][m]["total"]["threeLayer_rate_err"]**2)    
            rates[q][m]["total"]["acc"] += acc*N
            rates[q][m]["total"]["acc_err"] += aerr*N
            rates[q][m]["total"]["acc_N"] += N
            rates[q][m]["total"]["line_acc"] += lacc*lN
            rates[q][m]["total"]["line_acc_err"] += laerr*lN
            rates[q][m]["total"]["line_acc_N"] += lN            

        rates[q][m]["total"]["acc"] /= max(1,rates[q][m]["total"]["acc_N"])
        rates[q][m]["total"]["acc_err"] /= max(1,rates[q][m]["total"]["acc_N"])
        rates[q][m]["total"]["line_acc"] /= max(1,rates[q][m]["total"]["line_acc_N"])
        rates[q][m]["total"]["line_acc_err"] /= max(1,rates[q][m]["total"]["line_acc_N"])


types = ["rate","line_rate","threeLayer_rate","acc","line_acc"]
os.system("mkdir -p rate_files")
fout = r.TFile("rate_files/{0}_{1}.root".format(ntuple_tag,sim_tag),"RECREATE")
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
