#include <cmath>
#include <utility>
#include <iostream>
#include <string>

#include "TFile.h"

#include "DecayGen.h"
#include "MCPTree/MCPTree.h"

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
    if(!dg.h1){
        std::cout << "Couldn't find decay info file, or histogram within file!\n";
        return 1;
    }
    if(dg.BR < 0){
        std::cout << "Illegal decay! See above error message\n";
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
