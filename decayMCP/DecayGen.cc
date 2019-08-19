#include <cmath>
#include <utility>
#include <iostream>
#include <string>

#include "TFile.h"
#include "TRandom.h"
#include "TH1D.h"

#include "DecayGen.h"
#include "MCPTree/MCPTree.h"
#include "../utils/decay.h"
#include "../utils/branching_ratios.h"

const float MINBIAS_XSEC = (69.2e-3) * 1e12; // 69.2 mb converted to pb

string DecayGen::GetDecayString(int decay_mode){
    if(decay_mode == 1)       return "B -> J/psi X, J/psi -> mCP mCP";
    else if(decay_mode == 2)  return "B -> psi(2S) X, psi(2S) -> mCP mCP";
    else if(decay_mode == 3)  return "rho -> mCP mCP";
    else if(decay_mode == 4)  return "omega -> mCP mCP";
    else if(decay_mode == 5)  return "phi -> mCP mCP";
    else if(decay_mode == 6)  return "pi0 -> mCP mCP gamma";
    else if(decay_mode == 7)  return "eta -> mCP mCP gamma";
    else if(decay_mode == 8)  return "eta' -> mCP mCP gamma";
    else if(decay_mode == 9)  return "omega -> mCP mCP pi0";
    else if(decay_mode == 10) return "eta' -> mCP mCP omega";
    else if(decay_mode == 11) return "J/psi -> mCP mCP";
    else if(decay_mode == 12) return "psi(2S) -> mCP mCP";
    else if(decay_mode == 13) return "Y(1S) -> mCP mCP";
    else if(decay_mode == 14) return "Y(2S) -> mCP mCP";
    else if(decay_mode == 15) return "Y(3S) -> mCP mCP";
    else return "BAD DECAY MODE";
}

int DecayGen::Initialize(int decay_mode, float m_mCP){
    this->decay_mode = decay_mode;
    decay_string = GetDecayString(decay_mode);
    this->m_mCP = m_mCP;
    m_X = 9999;  // mass of X in dalitz decay A -> B+B-X;

    TFile *finfo;
    if(decay_mode >= 1 && decay_mode <= 2){
        // psi's produced from B's
        if(decay_mode == 1){
            // B -> psi X, psi -> mCP mCP
            finfo = new TFile((BASE_DIR+"/oniaFromB/psi.root").c_str());
            xsec_inclusive = 1.0167e6 * 1; // *2 since b's produced in pairs; from inclusive txt file *total_xsec.txt
            parent_pdgId = 443;
            m_parent = 3.0969;
        }else if(decay_mode == 2){
            // B -> psi X, psi -> mCP mCP
            finfo = new TFile((BASE_DIR+"/oniaFromB/psiprime.root").c_str());
            xsec_inclusive = 2.6408e5 * 1; // *2 since b's produced in pairs; from inclusive txt file *total_xsec.txt
            parent_pdgId = 100443;
            m_parent = 3.6861;
        }
        h_cn = (TH1D*)finfo->Get("central");
        h_up = (TH1D*)finfo->Get("up");
        h_dn = (TH1D*)finfo->Get("down");
        etamin = -2.0;
        etamax = 2.0;
        xsec_inclusive *= 2.0/1.0; // xsecs are given in range [-1,1]. Correct here for wider range, assuming flat eta distribution
        decay_type = TWOBODY;
        BR = br_onia(m_mCP, parent_pdgId);
        // these have uniform binning so this shouldn't matter, but do it anyway for consistency
        FixHistogram(h_cn);
        FixHistogram(h_up);
        FixHistogram(h_dn);
    }else if(decay_mode >= 3 && decay_mode <= 10){
        // direct production of pi, rho, omega, phi, eta, etaprime
        finfo = new TFile((BASE_DIR+"/mesonPt/pt_dists.root").c_str());
        if(decay_mode == 3){
            // rho -> mCP mCP
            h_cn = (TH1D*)finfo->Get("h_rho");
            parent_pdgId = 113;
            m_parent = 0.7743;
        }
        if(decay_mode == 4 || decay_mode == 9){
            // omega -> mCP mCP or omega -> mCP mCP pi0
            h_cn = (TH1D*)finfo->Get("h_omega");
            parent_pdgId = 223;
            m_parent = 0.7827;
            if(decay_mode == 9) m_X = 0.1350;
        }
        if(decay_mode == 5){
            // phi -> mCP mCP
            h_cn = (TH1D*)finfo->Get("h_phi");
            parent_pdgId = 333;
            m_parent = 1.0195;
        }
        if(decay_mode == 6){
            // pi0 -> mCP mCP gamma
            h_cn = (TH1D*)finfo->Get("h_pi0");
            parent_pdgId = 111;
            m_parent = 0.1350;
            m_X = 0.0;
        }
        if(decay_mode == 7){
            // eta -> mCP mCP gamma
            h_cn = (TH1D*)finfo->Get("h_eta");
            parent_pdgId = 221;
            m_parent = 0.5479;
            m_X = 0.0;
        }
        if(decay_mode == 8 || decay_mode == 10){
            // eta' -> mCP mCP gamma or eta' -> mCP mCP omega
            h_cn = (TH1D*)finfo->Get("h_etap");
            parent_pdgId = 331;
            m_parent = 0.9578;
            m_X = 0.0;
            if(decay_mode == 10) m_X = 0.7827;
        }
        etamin = -2.0;
        etamax = 2.0;
        // bins in this histogram are "particles per minbias event per 50 MeV bin"
        // so the integral is "particles per minbias event"
        // scale by the minbias xsec to get the xsec for producing this particle type
        xsec_inclusive = h_cn->Integral() * MINBIAS_XSEC;
        xsec_inclusive *= 2.0/2.0; // xsecs are given in range [-2,2]. No need to correct
        if(decay_mode >= 3 && decay_mode <= 5){
            // direct 2-body decay
            decay_type = TWOBODY;
            BR = br_onia(m_mCP, parent_pdgId);
        }else{
            // Dalitz decay
            decay_type = DALITZ;
            BR = br_dalitz(m_mCP, parent_pdgId, m_X);
        }
    }else if(decay_mode >= 11 && decay_mode <= 15){
        // direct onia (ccbar and bbbar) production
        if(decay_mode == 11){
            // direct J/psi
            finfo = new TFile((BASE_DIR+"/oniaDirect/CMS-13-TeV/theory/psiLowPt/merged_jpsi.root").c_str());
            parent_pdgId = 443;
            m_parent = 3.0969;
        }else if(decay_mode == 12){
            // direct psi(2S)
            finfo = new TFile((BASE_DIR+"/oniaDirect/CMS-13-TeV/theory/psiLowPt/merged_psiprime.root").c_str());
            parent_pdgId = 100443;
            m_parent = 3.6861;
        }else if(decay_mode == 13){
            // direct Y(1S)
            finfo = new TFile((BASE_DIR+"/oniaDirect/upsilon/ups1S_combined.root").c_str());
            parent_pdgId = 553;
            m_parent = 9.4603;
        }else if(decay_mode == 14){
            // direct Y(2S)
            finfo = new TFile((BASE_DIR+"/oniaDirect/upsilon/ups2S_combined.root").c_str());
            parent_pdgId = 100553;
            m_parent = 10.023;
        }else if(decay_mode == 15){
            // direct Y(3S)
            finfo = new TFile((BASE_DIR+"/oniaDirect/upsilon/ups3S_combined.root").c_str());
            parent_pdgId = 200553;
            m_parent = 10.355;
        }
        etamax = 2.0;
        if(decay_mode >= 13 && decay_mode <= 15)
            etamax = 3.0;
        etamin = -etamax;
        h_cn = (TH1D*)finfo->Get("central");
        h_up = (TH1D*)finfo->Get("up");
        h_dn = (TH1D*)finfo->Get("down");
        // bins in this histogram are dsigma/dpt, in units of nb/GeV
        // So sum bin contents, multiply by bin width, and *1000 to convert to pb
        xsec_inclusive = h_cn->Integral("width") * 1000; // nb to pb
        // upsilon xsecs are given multiplied by BR(mumu), so correct for that here
        if(decay_mode == 13) xsec_inclusive /= 0.0248;
        if(decay_mode == 14) xsec_inclusive /= 0.0193;
        if(decay_mode == 15) xsec_inclusive /= 0.0218;
        xsec_inclusive *= etamax/1.2; // xsecs are given in eta range [-1.2,1.2]. Correct to use 2.0 for eta bounds
        // convert from dsigma/dpt to dsigma/bin
        FixHistogram(h_cn);
        FixHistogram(h_up);
        FixHistogram(h_dn);
        decay_type = TWOBODY;
        BR = br_onia(m_mCP, parent_pdgId);        
    }else{
        return -1;
    }

    if(h_cn) h_cn->SetDirectory(0);
    if(h_up) h_up->SetDirectory(0);
    if(h_dn) h_dn->SetDirectory(0);
    if(finfo) finfo->Close();

    return 0;
}

int DecayGen::DoDecay(MCPTree& tree){

    if(decay_mode < 0){
        std::cout << "ERROR: must initialize DecayGen first!" << std::endl;
        return -1;
    }
    float pt = h_cn->GetRandom();
    if((decay_mode >= 1 && decay_mode <= 2) || (decay_mode >= 11 && decay_mode <= 15)){
        int ibin = h_cn->GetXaxis()->FindBin(pt);
        tree.weight_up = h_up->GetBinContent(ibin) / h_cn->GetBinContent(ibin);
        tree.weight_dn = h_dn->GetBinContent(ibin) / h_cn->GetBinContent(ibin);        
    }
    float eta = gRandom->Uniform(etamin, etamax);
    float phi = gRandom->Uniform(-M_PI, M_PI);        
    *tree.parent_p4 = LorentzVector(pt, eta, phi, m_parent);        
    if(decay_type == TWOBODY){
        std::tie(*tree.p4_p,*tree.p4_m) = Do2BodyDecay(*tree.parent_p4, m_mCP, m_mCP);
    }else{
        LorentzVector dummy;
        std::tie(dummy,*tree.p4_p,*tree.p4_m) = DoDalitz(*tree.parent_p4, m_mCP, m_X);
    }

    return 0;

}

// Some histograms are given in dsigma / dpt
// However, TH1::GetRandom assumes that it is dsigma / bin, so doesn't work correctly
// for variable binned histograms. Correct for that here
void DecayGen::FixHistogram(TH1D* h){
    for(int i=1; i<=h->GetNbinsX(); i++)
        h->SetBinContent(i, h->GetBinContent(i) * h->GetBinWidth(i));
}

