#include <string>

#include "TFile.h"
#include "TH1D.h"

#include "MCPTree/MCPTree.h"

typedef LorentzPtEtaPhiMf LorentzVector;

bool WithinBounds(LorentzVector p4, int q);

class DecayGen {
  public:
    enum DecayType{ TWOBODY, DALITZ };
    static string GetDecayString(int decayMode);
    int Initialize(int decayMode, float m_mCP);
    int DoDecay(MCPTree& tree);
    
    TFile *finfo;
    TH1D *h1, *h2, *h3;
    int decay_mode = -1;
    string decay_string;
    float etamin, etamax; // eta bounds of parent particle
    float xsec_inclusive; // xsec before BR to mCPs (in pb)
    float BR; // branching ratio to mCP's
    float m_mCP, m_parent, m_X; // masses of mCP, parent particle, and "X" in dalitz decays
    int parent_pdgId;
    int decay_type;

};
