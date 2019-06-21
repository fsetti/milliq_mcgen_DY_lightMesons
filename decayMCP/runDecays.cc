#include <cmath>
#include <utility>
#include <iostream>
#include <string>

#include "TFile.h"
#include "TRandom.h"
#include "TH1D.h"

#include "runDecays.h"
#include "MCPTree/MCPTree.h"
#include "../utils/decay.h"
#include "../utils/branching_ratios.h"

const float MINBIAS_XSEC = (69.2e-3) * 1e12; // 69.2 mb converted to pb
const float MCP_ETAMIN = 0.16 - 0.1;
const float MCP_ETAMAX = 0.16 + 0.1;
const float MCP_PHIMIN = -0.1;
const float MCP_PHIMAX = 0.6;

// check if an mCP 4-vector is within pre-defined eta/phi bounds
// note that the phi selection gets inverted based on mCP charge sign,
// since they curve opposite directions in magnetic field
bool WithinBounds(LorentzVector p4, int q){
    // q is +1 or -1 to indicate sign of charge
    if(q > 0)
        return 
            p4.eta() >= MCP_ETAMIN &&
            p4.eta() <= MCP_ETAMAX &&
            p4.phi() >= MCP_PHIMIN &&
            p4.phi() <= MCP_PHIMAX;
    else
        return 
            p4.eta() >= MCP_ETAMIN &&
            p4.eta() <= MCP_ETAMAX &&
            p4.phi() >= -MCP_PHIMAX &&
            p4.phi() <= -MCP_PHIMIN;        
}

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

    if(decay_mode >= 1 && decay_mode <= 2){
        // psi's produced from B's
        if(decay_mode == 1){
            // B -> psi X, psi -> mCP mCP
            finfo = new TFile("../oniaFromB/psi.root");
            xsec_inclusive = 1.015e6 * 2; // *2 since b's produced in pairs; from inclusive txt file *total_xsec.txt
            parent_pdgId = 443;
            m_parent = 3.0969;
        }else if(decay_mode == 2){
            // B -> psi X, psi -> mCP mCP
            finfo = new TFile("../oniaFromB/psiprime.root");
            xsec_inclusive = 2.635e5 * 2; // *2 since b's produced in pairs; from inclusive txt file *total_xsec.txt
            parent_pdgId = 100443;
            m_parent = 3.6861;
        }
        h1 = (TH1D*)finfo->Get("central");
        h2 = (TH1D*)finfo->Get("up");
        h3 = (TH1D*)finfo->Get("down");
        etamin = -1;
        etamax = 1;
        decay_type = TWOBODY;
        BR = br_onia(m_mCP, parent_pdgId);
    }else if(decay_mode >= 3 && decay_mode <= 10){
        // direct production of pi, rho, omega, phi, eta, etaprime
        finfo = new TFile("../mesonPt/pt_dists.root");
        if(decay_mode == 3){
            // rho -> mCP mCP
            h1 = (TH1D*)finfo->Get("h_rho");
            parent_pdgId = 113;
            m_parent = 0.7743;
        }
        if(decay_mode == 4 || decay_mode == 9){
            // omega -> mCP mCP or omega -> mCP mCP pi0
            h1 = (TH1D*)finfo->Get("h_omega");
            parent_pdgId = 223;
            m_parent = 0.7827;
            if(decay_mode == 9) m_X = 0.1350;
        }
        if(decay_mode == 5){
            // phi -> mCP mCP
            h1 = (TH1D*)finfo->Get("h_phi");
            parent_pdgId = 333;
            m_parent = 1.0195;
        }
        if(decay_mode == 6){
            // pi0 -> mCP mCP gamma
            h1 = (TH1D*)finfo->Get("h_pi0");
            parent_pdgId = 111;
            m_parent = 0.1350;
            m_X = 0.0;
        }
        if(decay_mode == 7){
            // eta -> mCP mCP gamma
            h1 = (TH1D*)finfo->Get("h_eta");
            parent_pdgId = 221;
            m_parent = 0.5479;
            m_X = 0.0;
        }
        if(decay_mode == 8 || decay_mode == 10){
            // eta' -> mCP mCP gamma or eta' -> mCP mCP omega
            h1 = (TH1D*)finfo->Get("h_etap");
            parent_pdgId = 331;
            m_parent = 0.9578;
            m_X = 0.0;
            if(decay_mode == 10) m_X = 0.7827;
        }
        etamin = -1;
        etamax = 1;
        // bins in this histogram are "particles per minbias event per 50 MeV bin"
        // so the integral is "particles per minbias event"
        // scale by the minbias xsec to get the xsec for producing this particle type
        xsec_inclusive = h1->Integral() * MINBIAS_XSEC;
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
            finfo = new TFile("../oniaDirect/theory_for_BPH-15-005/CMS_Jpsi_tot_0_1.2_Tev_13_CMS_1.root");
            parent_pdgId = 443;
            m_parent = 3.0969;
        }else if(decay_mode == 12){
            // direct psi(2S)
            finfo = new TFile("../oniaDirect/theory_for_BPH-15-005/CMS_Psi2S_tot_0_1.2_Tev_13_CMS_1.root");
            parent_pdgId = 100443;
            m_parent = 3.6861;
        }else if(decay_mode == 13){
            // direct Y(1S)
            finfo = new TFile("../oniaDirect/theory_for_BPH-15-005/CMS_Y1S_tot_0_0_1.2_Tev_13_CMS_1.root");
            parent_pdgId = 553;
            m_parent = 9.4603;
        }else if(decay_mode == 14){
            // direct Y(2S)
            finfo = new TFile("../oniaDirect/theory_for_BPH-15-005/CMS_Y2S_tot_0_1.2_Tev_13_CMS_1.root");
            parent_pdgId = 100553;
            m_parent = 10.023;
        }else if(decay_mode == 15){
            // direct Y(3S)
            finfo = new TFile("../oniaDirect/theory_for_BPH-15-005/CMS_Y3S_tot_0_1.2_Tev_13_CMS_1.root");
            parent_pdgId = 200553;
            m_parent = 10.355;
        }
        etamin = -1.2;
        etamax = 1.2;
        h1 = (TH1D*)finfo->Get("central");
        h2 = (TH1D*)finfo->Get("up");
        h3 = (TH1D*)finfo->Get("down");
        // bins in this histogram are dsigma/dpt, in units of nb/GeV
        // So sum bin contents, multiply by bin width, and *1000 to convert to pb
        xsec_inclusive = h1->Integral() * h1->GetBinWidth(1) * 1000; // nb to pb
        decay_type = TWOBODY;
        BR = br_onia(m_mCP, parent_pdgId);        
    }else{
        return -1;
    }
    
    return 0;
}

int DecayGen::DoDecay(MCPTree& tree){

    if(decay_mode < 0){
        std::cout << "ERROR: must initialize DecayGen first!" << std::endl;
        return -1;
    }

    float pt = h1->GetRandom();
    if((decay_mode >= 1 && decay_mode <= 2) || (decay_mode >= 11 && decay_mode <= 15)){
        int ibin = h1->GetXaxis()->FindBin(pt);
        tree.weight_up = h2->GetBinContent(ibin) / h1->GetBinContent(ibin);
        tree.weight_dn = h3->GetBinContent(ibin) / h1->GetBinContent(ibin);        
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

int main(int argc, char **argv){

    if(argc < 5){
        std::cout << "usage: runDecays <decay_mode> <m_mCP> <n_events> <outfile>" << std::endl;
        std::cout << "--DECAY MODES--" << std::endl;
        for(int i=1; i<=15; i++)
            std::cout << "  " << i << ": " << DecayGen::GetDecayString(i) << std::endl;
        return 1;
    }

    int decay_mode = atoi(argv[1]);
    float m_mCP = atof(argv[2]);
    int n_events = atoi(argv[3]);    

    DecayGen dg;
    MCPTree outtree;
    
    if(dg.Initialize(decay_mode, m_mCP)){
        std::cout << "Invalid decay mode!\n";
        return 1;
    }
    if(!dg.finfo or dg.finfo->IsZombie()){
        std::cout << "Couldn't find decay info file!\n";
        return 1;
    }
    
    TFile *fout = new TFile(argv[4], "RECREATE");
    outtree.Init();

    outtree.decay_flag = decay_mode;
    outtree.BR_q1 = dg.BR;
    outtree.weight = 1.0;
    outtree.weight_up = 1.0;
    outtree.weight_dn = 1.0;
    outtree.xsec = dg.xsec_inclusive;
    outtree.parent_pdgId = dg.parent_pdgId;

    std::cout << "\n";
    std::cout << "**********************************************" << std::endl;
    std::cout << "*   Milli-Charged Particle Decay Generator   *" << std::endl;
    std::cout << "**********************************************" << std::endl;
    std::cout << "  Doing decay mode: " << dg.decay_string << std::endl;
    std::cout << "    mCP mass (GeV): " << dg.m_mCP << std::endl;
    std::cout << "         xsec (pb): " << dg.xsec_inclusive << std::endl;
    std::cout << "           BR(q=1): " << dg.BR << std::endl;
    std::cout << "      parent_pdgId: " << dg.parent_pdgId << std::endl;
    std::cout << "    m_parent (GeV): " << dg.m_parent << std::endl;
    std::cout << "        decay type: " << (dg.decay_type==DecayGen::DALITZ ? "Dalitz" : "Two-body") << std::endl;
    if(dg.decay_type == DecayGen::DALITZ)
        std::cout << "         m_X (GeV): " << dg.m_X << std::endl;
    std::cout << "----------------------------------------------" << std::endl;
    std::cout << "    parent eta min: " << dg.etamin << std::endl;
    std::cout << "    parent eta max: " << dg.etamax << std::endl;
    std::cout << "       mCP eta min: " << MCP_ETAMIN << std::endl;
    std::cout << "       mCP eta max: " << MCP_ETAMAX << std::endl;
    std::cout << " mCP phi min (q>0): " << MCP_PHIMIN << std::endl;
    std::cout << " mCP phi max (q>0): " << MCP_PHIMAX << std::endl;
    std::cout << "----------------------------------------------" << std::endl;
    

    outtree.tree()->SetBranchStatus("filter_eff", 0); // turn off and fill later once we're done
    unsigned long n_attempts = 0;
    for(uint i=0; i<n_events; i++){
        outtree.progress(i, n_events, 200);
        outtree.event = i;
        do{            
            dg.DoDecay(outtree);
            n_attempts++;
        } while (!(WithinBounds(*outtree.p4_p, 1) || WithinBounds(*outtree.p4_m, -1)));
        outtree.Fill();
    }

    // fill the filter_eff branch
    outtree.filter_eff = (float)n_events / n_attempts;
    std::cout << "    Total attempted events: " << n_attempts << std::endl;
    std::cout << "Computed filter efficiency: " << outtree.filter_eff << std::endl;
    outtree.tree()->SetBranchStatus("filter_eff", 1);
    TBranch *beff = outtree.tree()->GetBranch("filter_eff");
    for(uint i=0; i<n_events; i++){
        outtree.tree()->GetEntry(i);
        beff->Fill();
    }
    std::cout << "\n";

    outtree.Write(fout);

    fout->Close();
    return 0;
}
