import glob
import os
import ROOT as r
from math import pi
r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(1)

ntuple_tag = "v6"
sim_tag = "v1"

ms = [0.01, 0.1, 0.4, 1.0, 3.0]
qs = [0.01,0.1]

colors = [r.kOrange-3, r.kGreen+1, r.kGreen+3, r.kAzure-4, r.kBlue+1]

pdefs = {
    "pt" : {
        "dstr" : "p4_#.pt()",
        "bins" : (100,0,10),
        "title" : ";p_{T} [GeV]",
        "islog" : True,
        },
    "eta" : {
        "dstr" : "p4_#.eta()",
        "bins" : (50,0.0,0.3),
        "title" : ";#eta(mCP)",
        },
    "phi" : {
        "dstr" : "p4_#.phi()",
        "bins" : (50,-2,2),
        "title" : ";#phi(mCP)",
        },
    "eta_parent" : {
        "dstr" : "parent_p4.eta()",
        "bins" : (50,-2,2),
        "title" : ";#eta(parent)",
        },
    "phi_parent" : {
        "dstr" : "parent_p4.phi()",
        "bins" : (50,-pi,pi),
        "title" : ";#phi(parent)",
        },
    "momentum_loss" : {
        "dstr" : "p4_#.P() - hit_#_p4.P()",
        "bins" : (50,0,1),
        "title" : ";momentum loss [GeV]",
        "islog" : True,
        },
    "hit_pz" : {
        "dstr" : "hit_#_p4.Pz()",
        "bins" : (100,0,10),
        "title" : ";hit pz [GeV]",
        "islog" : True,
        },
    "hit_pt" : {
        "dstr" : "hit_#_p4.Pt()",
        "bins" : (100,0,0.3),
        "title" : ";hit pt [GeV]",
        },
    "hit_theta" : {
        "dstr" : "atan(hit_#_p4.Pt()/hit_#_p4.Pz())*180/pi",
        "bins" : (80,0,5),
        "title" : ";hit theta [deg]",
        },
    "hit_thetax" : {
        "dstr" : "atan(hit_#_p4.Px()/hit_#_p4.Pz())*180/pi",
        "bins" : (80,-4,4),
        "title" : ";hit thetax [deg]",
        },
    "hit_thetay" : {
        "dstr" : "atan(hit_#_p4.Py()/hit_#_p4.Pz())*180/pi",
        "bins" : (80,-4,4),
        "title" : ";hit thetay [deg]",
        },
    "hit_x" : {
        "dstr" : "hit_#_xyz.X()",
        "bins" : (50,-1,1),
        "title" : ";hit X [m]"
        },
    "hit_y" : {
        "dstr" : "hit_#_xyz.Y()",
        "bins" : (50,-1,1),
        "title" : ";hit Y [m]"
        },
}

basedir = "/nfs-7/userdata/bemarsh/milliqan/milliq_mcgen/merged_sim/{0}_{1}/".format(ntuple_tag, sim_tag)
for q in qs:
    qstr = "q_"+str(q).replace(".","p")
    outdir = os.path.join("~/public_html/milliqan/milliq_mcgen/plots/kinematics/{0}_{1}/{2}".format(ntuple_tag, sim_tag, qstr))
    os.system("mkdir -p "+outdir)
    os.system("cp ~/scripts/index.php "+outdir)

    hists = {}

    weight_str = "{0} * xsec * BR_q1 * filter_eff * weight * 1000.0 / n_events_total".format(q**2)
        
    for m in ms:
        mstr = "m_"+str(m).replace(".","p")
        hists[m] = {}
        
        ch = r.TChain("Events")
        ch.Add(os.path.join(basedir,mstr,qstr,"*.root"))

        for pname, pinfo in pdefs.items():
            hists[m][pname] = r.TH1D("h_{0}_{1}_{2}".format(qstr,mstr,pname), pinfo["title"], *pinfo["bins"])
            hists[m][pname+"m"] = r.TH1D("hm_{0}_{1}_{2}".format(qstr,mstr,pname), pinfo["title"], *pinfo["bins"])

            ch.Draw("{0}>>h_{1}_{2}_{3}".format(pinfo["dstr"].replace("#","p"),qstr,mstr,pname), "(does_hit_p)*({})".format(weight_str), "goff")
            ch.Draw("{0}>>hm_{1}_{2}_{3}".format(pinfo["dstr"].replace("#","m"),qstr,mstr,pname), "(does_hit_m)*({})".format(weight_str), "goff")    

            hists[m][pname].Add(hists[m][pname+"m"])
            hists[m][pname].Scale(1.0/hists[m][pname].Integral(0,-1))
            
    for pname,pinfo in pdefs.items():
        c = r.TCanvas()
        c.SetCanvasSize(800,600)

        islog = pinfo["islog"] if "islog" in pinfo else False
        c.SetLogy(islog)

        hmax = reduce(max, [hists[m][pname].GetMaximum() for m in ms])

        leg = r.TLegend(0.7,0.6,0.88,0.88)
        for im,m in enumerate(ms):
            mstr = "m_"+str(m).replace(".","p")
            hists[m][pname].SetLineColor(colors[im])
            hists[m][pname].SetLineWidth(2)

            if im==0:
                hists[m][pname].SetMaximum(hmax * 1.2)                
                if islog:
                    hists[m][pname].SetMaximum(hmax * 10)
                    hists[m][pname].SetMinimum(1e-3)
                hists[m][pname].Draw("HIST")
            else:
                hists[m][pname].Draw("HIST SAME")

            leg.AddEntry(hists[m][pname], "m = {0}".format(m), 'l')

        leg.Draw()

        c.SaveAs(os.path.join(outdir, pname+".png"))
        c.SaveAs(os.path.join(outdir, pname+".pdf"))


