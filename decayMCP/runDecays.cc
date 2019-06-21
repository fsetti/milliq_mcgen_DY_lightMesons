#include <cmath>
#include <utility>
#include <iostream>
#include <string>

#include "TFile.h"
#include "TTree.h"
#include "TRandom.h"
#include "TH1D.h"

#include "MCPTree/MCPTree.h"
#include "../utils/decay.h"
#include "../utils/branching_ratios.h"

typedef LorentzPtEtaPhiMf LorentzVector;

#define TWOBODY 0
#define DALITZ 1

TFile *finfo;
TH1D *h1,*h2,*h3;
float etamin, etamax;
float xsec_inclusive;
float mMCP, m_parent, BR, m_X;
int parent_pdgId, decayType;
MCPTree outtree;

const float MINBIAS_XSEC = (69.2e-3) * 1e12; // 69.2 mb converted to pb
const float MCP_ETAMIN = 0.16 - 0.1;
const float MCP_ETAMAX = 0.16 + 0.1;
const float MCP_PHIMIN = -0.1;
const float MCP_PHIMAX = 0.6;

string GetDecayString(int decayMode){
    if(decayMode == 1)       return "B -> J/psi X, J/psi -> mCP mCP";
    else if(decayMode == 2)  return "B -> psi(2S) X, psi(2S) -> mCP mCP";
    else if(decayMode == 3)  return "rho -> mCP mCP";
    else if(decayMode == 4)  return "omega -> mCP mCP";
    else if(decayMode == 5)  return "phi -> mCP mCP";
    else if(decayMode == 6)  return "pi0 -> mCP mCP gamma";
    else if(decayMode == 7)  return "eta -> mCP mCP gamma";
    else if(decayMode == 8)  return "eta' -> mCP mCP gamma";
    else if(decayMode == 9)  return "omega -> mCP mCP pi0";
    else if(decayMode == 10) return "eta' -> mCP mCP omega";
    else if(decayMode == 11) return "J/psi -> mCP mCP";
    else if(decayMode == 12) return "psi(2S) -> mCP mCP";
    else if(decayMode == 13) return "Y(1S) -> mCP mCP";
    else if(decayMode == 14) return "Y(2S) -> mCP mCP";
    else if(decayMode == 15) return "Y(3S) -> mCP mCP";
    else return "BAD DECAY MODE";
}

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

int Initialize(int decayMode){
    m_X = 9999;  // mass of X in dalitz decay A -> B+B-X;
    if(decayMode >= 1 && decayMode <= 2){
        if(decayMode == 1){
            // B -> psi X, psi -> mCP mCP
            finfo = new TFile("../oniaFromB/psi.root");
            xsec_inclusive = 1.015e6 * 2; // *2 since b's produced in pairs
            parent_pdgId = 443;
            m_parent = 3.0969;
        }else if(decayMode == 2){
            // B -> psi X, psi -> mCP mCP
            finfo = new TFile("../oniaFromB/psiprime.root");
            xsec_inclusive = 2.635e5 * 2; // *2 since b's produced in pairs
            parent_pdgId = 100443;
            m_parent = 3.6861;
        }
        h1 = (TH1D*)finfo->Get("central");
        h2 = (TH1D*)finfo->Get("up");
        h3 = (TH1D*)finfo->Get("down");
        etamin = -1;
        etamax = 1;
        decayType = TWOBODY;
        BR = br_onia(mMCP, parent_pdgId);
    }else if(decayMode >= 3 && decayMode <= 10){
        finfo = new TFile("../mesonPt/pt_dists.root");
        if(decayMode == 3){
            // rho -> mCP mCP
            h1 = (TH1D*)finfo->Get("h_rho");
            parent_pdgId = 113;
            m_parent = 0.7743;
        }
        if(decayMode == 4 || decayMode == 9){
            // omega -> mCP mCP or omega -> mCP mCP pi0
            h1 = (TH1D*)finfo->Get("h_omega");
            parent_pdgId = 223;
            m_parent = 0.7827;
            if(decayMode == 9) m_X = 0.1350;
        }
        if(decayMode == 5){
            // phi -> mCP mCP
            h1 = (TH1D*)finfo->Get("h_phi");
            parent_pdgId = 333;
            m_parent = 1.0195;
        }
        if(decayMode == 6){
            // pi0 -> mCP mCP gamma
            h1 = (TH1D*)finfo->Get("h_pi0");
            parent_pdgId = 111;
            m_parent = 0.1350;
            m_X = 0.0;
        }
        if(decayMode == 7){
            // eta -> mCP mCP gamma
            h1 = (TH1D*)finfo->Get("h_eta");
            parent_pdgId = 221;
            m_parent = 0.5479;
            m_X = 0.0;
        }
        if(decayMode == 8 || decayMode == 10){
            // eta' -> mCP mCP gamma or eta' -> mCP mCP omega
            h1 = (TH1D*)finfo->Get("h_etap");
            parent_pdgId = 331;
            m_parent = 0.9578;
            m_X = 0.0;
            if(decayMode == 10) m_X = 0.7827;
        }
        etamin = -1;
        etamax = 1;
        xsec_inclusive = h1->Integral() * MINBIAS_XSEC;
        if(decayMode >= 3 && decayMode <= 5){
            // direct 2-body decay
            decayType = TWOBODY;
            BR = br_onia(mMCP, parent_pdgId);
        }else{
            // Dalitz decay
            decayType = DALITZ;
            BR = br_dalitz(mMCP, parent_pdgId, m_X);
        }
    }else if(decayMode >= 11 && decayMode <= 15){
        if(decayMode == 11){
            // direct J/psi
            finfo = new TFile("../oniaDirect/theory_for_BPH-15-005/CMS_Jpsi_tot_0_1.2_Tev_13_CMS_1.root");
            parent_pdgId = 443;
            m_parent = 3.0969;
        }else if(decayMode == 12){
            // direct psi(2S)
            finfo = new TFile("../oniaDirect/theory_for_BPH-15-005/CMS_Psi2S_tot_0_1.2_Tev_13_CMS_1.root");
            parent_pdgId = 100443;
            m_parent = 3.6861;
        }else if(decayMode == 13){
            // direct Y(1S)
            finfo = new TFile("../oniaDirect/theory_for_BPH-15-005/CMS_Y1S_tot_0_0_1.2_Tev_13_CMS_1.root");
            parent_pdgId = 553;
            m_parent = 9.4603;
        }else if(decayMode == 14){
            // direct Y(2S)
            finfo = new TFile("../oniaDirect/theory_for_BPH-15-005/CMS_Y2S_tot_0_1.2_Tev_13_CMS_1.root");
            parent_pdgId = 100553;
            m_parent = 10.023;
        }else if(decayMode == 15){
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
        xsec_inclusive = h1->Integral() * h1->GetBinWidth(1) * 1000; // nb to pb
        decayType = TWOBODY;
        BR = br_onia(mMCP, parent_pdgId);        
    }else{
        return -1;
    }
    
    return 0;
}

void DoDecay(int decayMode){

    float pt = h1->GetRandom();
    if((decayMode >= 1 && decayMode <= 2) || (decayMode >= 11 && decayMode <= 15)){
        int ibin = h1->GetXaxis()->FindBin(pt);
        outtree.weight_up = h2->GetBinContent(ibin) / h1->GetBinContent(ibin);
        outtree.weight_dn = h3->GetBinContent(ibin) / h1->GetBinContent(ibin);        
    }
    float eta = gRandom->Uniform(etamin, etamax);
    float phi = gRandom->Uniform(-M_PI, M_PI);        
    *outtree.parent_p4 = LorentzVector(pt, eta, phi, m_parent);        
    if(decayType == TWOBODY){
        std::tie(*outtree.p4_p,*outtree.p4_m) = Do2BodyDecay(*outtree.parent_p4, mMCP, mMCP);
    }else{
        LorentzVector dummy;
        std::tie(dummy,*outtree.p4_p,*outtree.p4_m) = DoDalitz(*outtree.parent_p4, mMCP, m_X);
    }

}

int main(int argc, char **argv){

    if(argc < 5){
        std::cout << "usage: runDecays <decayMode> <mMCP> <nEvents> <outfile>" << std::endl;
        std::cout << "--DECAY MODES--" << std::endl;
        for(int i=1; i<=15; i++)
            std::cout << "  " << i << ": " << GetDecayString(i) << std::endl;
        return 1;
    }

    int decayMode = atoi(argv[1]);
    mMCP = atof(argv[2]);
    int nEvents = atoi(argv[3]);    
    
    if(Initialize(decayMode)){
        std::cout << "Invalid decay mode!\n";
        return 1;
    }
    if(!finfo or finfo->IsZombie()){
        std::cout << "Couldn't find decay info file!\n";
        return 1;
    }
    
    TFile *fout = new TFile(argv[4], "RECREATE");
    outtree.Init();

    outtree.decay_flag = decayMode;
    outtree.BR_q1 = BR;
    outtree.weight = 1.0;
    outtree.weight_up = 1.0;
    outtree.weight_dn = 1.0;
    outtree.xsec = xsec_inclusive;
    outtree.parent_pdgId = parent_pdgId;

    std::cout << "\n";
    std::cout << "**********************************************" << std::endl;
    std::cout << "*   Milli-Charged Particle Decay Generator   *" << std::endl;
    std::cout << "**********************************************" << std::endl;
    std::cout << "  Doing decay mode: " << GetDecayString(decayMode) << std::endl;
    std::cout << "    mCP mass (GeV): " << mMCP << std::endl;
    std::cout << "         xsec (pb): " << xsec_inclusive << std::endl;
    std::cout << "           BR(q=1): " << BR << std::endl;
    std::cout << "      parent_pdgId: " << parent_pdgId << std::endl;
    std::cout << "    m_parent (GeV): " << m_parent << std::endl;
    std::cout << "        decay type: " << (decayType==DALITZ ? "Dalitz" : "Two-body") << std::endl;
    if(decayType == DALITZ)
        std::cout << "         m_X (GeV): " << m_X << std::endl;
    std::cout << "----------------------------------------------" << std::endl;
    std::cout << "    parent eta min: " << etamin << std::endl;
    std::cout << "    parent eta max: " << etamax << std::endl;
    std::cout << "       mCP eta min: " << MCP_ETAMIN << std::endl;
    std::cout << "       mCP eta max: " << MCP_ETAMAX << std::endl;
    std::cout << " mCP phi min (q>0): " << MCP_PHIMIN << std::endl;
    std::cout << " mCP phi max (q>0): " << MCP_PHIMAX << std::endl;
    std::cout << "----------------------------------------------" << std::endl;
    

    outtree.tree()->SetBranchStatus("filter_eff", 0); // turn off and fill later once we're done
    unsigned long nAttempts = 0;
    for(uint i=0; i<nEvents; i++){
        outtree.progress(i, nEvents, 200);
        outtree.event = i;
        do{            
            DoDecay(decayMode);
            nAttempts++;
        } while (!(WithinBounds(*outtree.p4_p, 1) || WithinBounds(*outtree.p4_m, -1)));
        outtree.Fill();
    }

    // fill the filter_eff branch
    outtree.filter_eff = (float)nEvents / nAttempts;
    std::cout << "    Total attempted events: " << nAttempts << std::endl;
    std::cout << "Computed filter efficiency: " << outtree.filter_eff << std::endl;
    outtree.tree()->SetBranchStatus("filter_eff", 1);
    TBranch *beff = outtree.tree()->GetBranch("filter_eff");
    for(uint i=0; i<nEvents; i++){
        outtree.tree()->GetEntry(i);
        beff->Fill();
    }
    std::cout << "\n";

    outtree.Write(fout);

    fout->Close();
    return 0;
}
