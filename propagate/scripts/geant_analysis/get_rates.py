import os
import ROOT as r
import glob
r.TH1.StatOverflows(True)
r.gROOT.ProcessLine(".L ~/scripts/rootalias.C")

TAG = "v8ext1_v1_save2m_skim0p25m_mcpData_v5_v4calib"
indir = "/nfs-7/userdata/bemarsh/milliqan/geant_ntuples/mcp_"+TAG

fout = r.TFile("rate_files/{0}.root".format(TAG), "RECREATE")

line_triplets = [
    (0,6,2),
    (1,7,3),
    (24,16,22),
    (25,17,23),
    (8,12,4),
    (9,13,5),
]

def get_rate(ch, sel="mcTruth_threeBarLine", lumi=35.0):
    if sel=="atLeast1PE_threeBarLine":
        sels = []
        for c1,c2,c3 in line_triplets:
            sels.append("(chan_nPE[{0}]>0 && chan_nPE[{1}]>0 && chan_nPE[{2}]>0)".format(c1,c2,c3))
        sel = " || ".join(sels)
    h = r.TH1D("h", "", 1, 0, 2)
    ch.Draw("1>>h","({0})*({1}*scale1fb)".format(sel, lumi), "goff")
    return h.GetBinContent(1), h.GetBinError(1)

def get_slab_nPE(ch, h, lumi=35.0):
    h.Reset()
    ch.Draw("RandomBinom(chan_nPE[20],0.6)>>+"+h.GetName(), "(mcTruth_fourSlab)*({0}*scale1fb)".format(lumi), "goff")
    ch.Draw("RandomBinom(chan_nPE[28],0.6)>>+"+h.GetName(), "(mcTruth_fourSlab)*({0}*scale1fb)".format(lumi), "goff")
    # ch.Draw("chan_nPE[20]*chan_fracMuon[20]>>+"+h.GetName(), "(mcTruth_fourSlab)*({0}*scale1fb)".format(lumi), "goff")
    # ch.Draw("chan_nPE[28]*chan_fracMuon[28]>>+"+h.GetName(), "(mcTruth_fourSlab)*({0}*scale1fb)".format(lumi), "goff")
    return h

def get_bar_nPE(ch, h, lumi=35.0):
    h.Reset()
    for c1,c2,c3 in line_triplets:        
        ch.Draw("chan_nPE[{0}]>>+{1}".format(c2,h.GetName()), 
                "(chan_muDist[{0}]>0 && chan_muDist[{1}]>0 && chan_muDist[{2}]>0)*({3}*scale1fb)".format(c1,c2,c3,lumi), "goff")
        # ch.Draw("chan_nPE[{0}]*chan_fracMuon[{0}]>>+{1}".format(c2,h.GetName()), 
                # "(chan_muDist[{0}]>0 && chan_muDist[{1}]>0 && chan_muDist[{2}]>0)*({3}*scale1fb)".format(c1,c2,c3,lumi), "goff")
    return h

def get_bar_MaxMin(ch, h, lumi=35.0):
    h.Reset()
    for c1,c2,c3 in line_triplets:        
        ch.Draw("max(max(chan_nPE[{0}],chan_nPE[{1}]),chan_nPE[{2}]) / min(min(chan_nPE[{0}],chan_nPE[{1}]),chan_nPE[{2}])>>+{3}".format(c1,c2,c3,h.GetName()), 
                "(chan_muDist[{0}]>0 && chan_muDist[{1}]>0 && chan_muDist[{2}]>0 && chan_nPE[{0}]>0 && chan_nPE[{1}]>0 && chan_nPE[{2}]>0)*({3}*scale1fb)".format(c1,c2,c3,lumi), "goff")
    return h    


rate_sels = ["mcTruth_threeBarLine", "atLeast1PE_threeBarLine"]
rates = {}
slab_nPE_hists = {}
bar_nPE_hists = {}
bar_MaxMin_hists = {}

for mdir in glob.glob(os.path.join(indir, "m_*")):
    sm = os.path.basename(mdir).replace("_","")
    m = float(sm[1:].replace("p","."))
    if sm not in slab_nPE_hists:
        slab_nPE_hists[sm] = {}
        bar_nPE_hists[sm] = {}
        bar_MaxMin_hists[sm] = {}
    for f in glob.glob(os.path.join(mdir, "q_*.root")):
        print f
        sq = os.path.basename(f).split(".")[0].replace("_","")
        q = float(sq[1:].replace("p","."))

        ch = r.TChain("Events")
        ch.Add(f)
        
        if sq not in rates:
            rates[sq] = {}
        
        for sel in rate_sels:
            if sel not in rates[sq]:
                rates[sq][sel] = []
            rate, rerr = get_rate(ch, sel)
            rates[sq][sel].append((m, (rate,rerr)))

        slab_nPE_hists[sm][sq] = r.TH1D("h_slabNPE_{0}_{1}".format(sm,sq), ";nPE", 1000, 0, 1000)
        get_slab_nPE(ch, slab_nPE_hists[sm][sq])
        binning = (1000,0,1000)
        if q > 0.05:
            binning = (1000,0,10000)
        if q > 0.1:
            binning = (1000, 0, 50000)
        bar_nPE_hists[sm][sq] = r.TH1D("h_barNPE_{0}_{1}".format(sm,sq), ";nPE", *binning)
        get_bar_nPE(ch, bar_nPE_hists[sm][sq])

        bar_MaxMin_hists[sm][sq] = r.TH1D("h_barMaxMin_{0}_{1}".format(sm,sq), ";maxNPE/minNPE", 200, 0, 100)
        get_bar_MaxMin(ch, bar_MaxMin_hists[sm][sq])

for sq in rates:
    for sel in rates[sq]:
        g = r.TGraphErrors()
        g.SetName("rate_{0}_{1}".format(sel, sq))
        for m,(rate,rerr) in sorted(rates[sq][sel]):
            if rate==0:
                continue
            N = g.GetN()
            g.SetPoint(N, m, rate)
            g.SetPointError(N, 0, rerr)
        g.Write()

for sm in slab_nPE_hists:
    for sq in slab_nPE_hists[sm]:
        slab_nPE_hists[sm][sq].Write()
        bar_nPE_hists[sm][sq].Write()
        bar_MaxMin_hists[sm][sq].Write()

fout.Close()
