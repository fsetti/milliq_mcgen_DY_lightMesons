#include <cmath>
#include <utility>
#include <iostream>

#include "TFile.h"
#include "TTree.h"
#include "TRandom.h"
#include "TH1F.h"

#include "MCPTree/MCPTree.h"
#include "../utils/decayMQ.h"

typedef LorentzPtEtaPhiMf LorentzVector;

TFile *finfo;
float etamin, etamax;
float xsec_inclusive;
float mMCP, m_parent, BR;
int parent_pdgId;
MCPTree outtree;


int initialize(int decayMode){
    if(decayMode == 1){
        finfo = new TFile("../oniaFromB/psi.root");
        etamin = -1;
        etamax = 1;
        xsec_inclusive = 1.015e6;
        parent_pdgId = 443;
        m_parent = 3.0969;
    }else if(decayMode == 2){
        finfo = new TFile("../oniaFromB/psiprime.root");
        etamin = -1;
        etamax = 1;
        xsec_inclusive = 2.635e5;
        parent_pdgId = 100443;
        m_parent = 3.6861;
    }else{
        return -1;
    }
    
    return 0;
}

void DoDecay(){

    TH1F* pt_central = (TH1F*)finfo->Get("central");
    TH1F* pt_up = (TH1F*)finfo->Get("up");
    TH1F* pt_dn = (TH1F*)finfo->Get("down");
    
    float pt = pt_central->GetRandom();
    int ibin = pt_central->GetXaxis()->FindBin(pt);
    outtree.weight_up = pt_up->GetBinContent(ibin) / pt_central->GetBinContent(ibin);
    outtree.weight_dn = pt_dn->GetBinContent(ibin) / pt_central->GetBinContent(ibin);
    
    float eta = gRandom->Uniform(etamin, etamax);
    float phi = gRandom->Uniform(-M_PI, M_PI);

    *outtree.parent_p4 = LorentzVector(pt, eta, phi, m_parent);
    
    std::tie(*outtree.p4_1,*outtree.p4_2) = Do2BodyDecay(*outtree.parent_p4, mMCP, mMCP);

}

int main(int argc, char **argv){

    if(argc < 6){
        std::cout << "usage: runDecays <decayMode> <mMCP> <BR> <nEvents> <outfile>" << std::endl;
        std::cout << "--DECAY MODES--" << std::endl;
        std::cout << "  1: b -> psi X, psi -> mCP mCP" << std::endl;
        std::cout << "  2: b -> psi' X, psi' -> mCP mCP" << std::endl;
        return 1;
    }

    int decayMode = atoi(argv[1]);
    mMCP = atof(argv[2]);
    BR = atof(argv[3]);
    int nEvents = atoi(argv[4]);    
    
    if(initialize(decayMode)){
        std::cout << "Invalid decay mode!\n";
        return 1;
    }
    if(!finfo){
        std::cout << "Couldn't find decay info file!\n";
        return 1;
    }
    
    TFile *fout = new TFile(argv[5], "RECREATE");
    outtree.Init();

    outtree.decay_flag = decayMode;
    outtree.BR_q1 = BR;
    outtree.weight = 1.0;
    outtree.xsec = xsec_inclusive;
    outtree.parent_pdgId = parent_pdgId;

    for(uint i=0; i<nEvents; i++){
        outtree.event = i;
        DoDecay();
        outtree.Fill();
    }

    outtree.Write(fout);

    fout->Close();
    return 0;
}
