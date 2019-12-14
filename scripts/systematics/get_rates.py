import glob
import os
import json
import numpy as np
import ROOT as r
r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(1)

# ntuple_tag = "mapp_theta5_v1"
ntuple_tag = "v8"
sim_tag = "v1_save2m_dens1p07"

lumi = 37.0 # in fb^-1

def get_rate(ch, q, type_="rate", lumi=1.0, n_events_total=None):
    h_cn = r.TH1D("h_cn","",1,0,2)
    h_up = r.TH1D("h_up","",1,0,2)
    h_dn = r.TH1D("h_dn","",1,0,2)
    if n_events_total is None:
        n_events_total = "n_events_total"
    if type_=="rate":
        sel = "does_hit_p + does_hit_m"
    elif type_=="line_rate":
        sel = "hit_p_line + hit_m_line"
    else:
        raise Exception()
    ch.Draw("1>>h_cn","({0})*({1}^2 * xsec * BR_q1 * filter_eff * weight    * 1000*{2} / {3})".format(sel,q,lumi,n_events_total), "goff")
    ch.Draw("1>>h_up","({0})*({1}^2 * xsec * BR_q1 * filter_eff * weight_up * 1000*{2} / {3})".format(sel,q,lumi,n_events_total), "goff")
    ch.Draw("1>>h_dn","({0})*({1}^2 * xsec * BR_q1 * filter_eff * weight_dn * 1000*{2} / {3})".format(sel,q,lumi,n_events_total), "goff")
    return [
        (h_cn.GetBinContent(1), h_cn.GetBinError(1)),
        (h_up.GetBinContent(1), h_up.GetBinError(1)),
        (h_dn.GetBinContent(1), h_dn.GetBinError(1)),
    ]
    
rates = {}

basedir = "/nfs-7/userdata/bemarsh/milliqan/milliq_mcgen/merged_sim/{0}_{1}/".format(ntuple_tag, sim_tag)
for mdir in glob.glob(os.path.join(basedir, "*")):
    mname = os.path.split(mdir)[1]
    m = float(mname.split("_")[1].replace("p","."))
    for qdir in glob.glob(os.path.join(mdir,"q*")):
        qname = os.path.split(qdir)[1]
        q = float(qname.split("_")[1].replace("p","."))

        if qname not in rates:
            rates[qname] = {}
        if mname not in rates[qname]:
            rates[qname][mname] = {"total":{
                    "rate_cn":0.0,
                    "rate_up":0.0,
                    "rate_dn":0.0,
                    "line_rate_cn":0.0,
                    "line_rate_up":0.0,
                    "line_rate_dn":0.0,
                    }}

        for sfile in glob.glob(os.path.join(qdir, "*.root")):
            samp = os.path.split(sfile)[1].split(".")[0]

            print mname, qname, samp

            ch = r.TChain("Events")
            ch.Add(sfile)

            rate = get_rate(ch, q, lumi=lumi)
            lrate = get_rate(ch, q, type_="line_rate", lumi=lumi)

            rates[qname][mname][samp] = {
                    "rate_cn":rate[0][0],
                    "rate_up":rate[1][0],
                    "rate_dn":rate[2][0],
                    "line_rate_cn":lrate[0][0],
                    "line_rate_up":lrate[1][0],
                    "line_rate_dn":lrate[2][0],
                }
            rates[qname][mname]["total"]["rate_cn"] += rate[0][0]
            rates[qname][mname]["total"]["rate_up"] += rate[1][0]
            rates[qname][mname]["total"]["rate_dn"] += rate[2][0]
            rates[qname][mname]["total"]["line_rate_cn"] += lrate[0][0]
            rates[qname][mname]["total"]["line_rate_up"] += lrate[1][0]
            rates[qname][mname]["total"]["line_rate_dn"] += lrate[2][0]

json.dump(rates, open(os.path.join("rates", "{0}_{1}.json".format(ntuple_tag, sim_tag)), 'w'), ensure_ascii=True, sort_keys=True, indent=4)
