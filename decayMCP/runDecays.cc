#include <cmath>
#include <utility>
#include <iostream>
#include <string>

#include "TFile.h"
#include "TRandom.h"

#include "DecayGen.h"
#include "MCPTree/MCPTree.h"

float MCP_ETAMIN = 0.16 - 0.08;
float MCP_ETAMAX = 0.16 + 0.08;
float MCP_PHIMIN = -0.03;
float MCP_PHIMAX = 1.0;

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

    char opt;
    bool help = false;
    int decay_mode = -1;
    float m_mCP = 0.001;
    int n_events = 1000, evt_offset = 0;
    uint n_events_total = 0;
    string output_name = "";
    while((opt = getopt(argc, argv, ":hd:o:m:n:N:e:")) != -1) {
        switch(opt){
        case 'h':
            help = true;
            break;
        case 'd':
            decay_mode = atoi(optarg);
            break;
        case 'o':
            output_name = string(optarg);
            break;
        case 'm':
            m_mCP = atof(optarg);
            break;
        case 'n':
            n_events = atoi(optarg);
            break;
        case 'N':
            n_events_total = atoi(optarg);
            break;
        case 'e':
            evt_offset = atoi(optarg);
            break;
        case '?':
            std::cout << "\nWARNING: unrecognized option " << argv[optind-1] << std::endl;
            break;
        case ':':
            std::cout << "\nERROR: option " << argv[optind-1] << " requires a value\n";
            help = true;
            break;
        }
    }

    if(n_events_total == 0)
        n_events_total = n_events;

    if(help || decay_mode < 0 || output_name=="" || m_mCP < 0 || n_events <= 0 || n_events_total < n_events || evt_offset < 0){
        std::cout << "\nusage:\n";
        std::cout << "    " << argv[0] << " -d decay_mode -o outfile [-m m_mCP=0.001 (GeV)] [-n n_events=1000] [-N n_events_total=n_events] [-e evtnum_offset=0] \n\n";
        std::cout << "--- DECAY MODES ---" << std::endl;
        for(int i=1; i<=15; i++)
            std::cout << "  " << i << ": " << DecayGen::GetDecayString(i) << std::endl;
        std::cout << "\n";
        return 1;
    }    

    MCP_PHIMIN = -0.03;
    MCP_PHIMAX = max(0.4, 0.35 - 0.85*log10(m_mCP));
    float deta = m_mCP >= 0.999 ? 0.06 : 0.12;
    MCP_ETAMIN = 0.16 - deta;
    MCP_ETAMAX = 0.16 + deta;
    
    DecayGen dg;
    MCPTree outtree;

    gRandom->SetSeed(0);
    
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
    
    TFile *fout = new TFile(output_name.c_str(), "RECREATE");
    outtree.Init();

    outtree.n_events_total = n_events_total;
    outtree.decay_mode = decay_mode;
    outtree.BR_q1 = dg.BR;
    outtree.weight = 1.0;
    outtree.weight_up = 1.0;
    outtree.weight_dn = 1.0;
    outtree.xsec = dg.xsec_inclusive;
    outtree.parent_pdgId = dg.parent_pdgId;
    outtree.mCP_etamin = MCP_ETAMIN;
    outtree.mCP_etamax = MCP_ETAMAX;
    outtree.mCP_phimin = MCP_PHIMIN;
    outtree.mCP_phimax = MCP_PHIMAX;

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
        outtree.event = i + evt_offset;
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
