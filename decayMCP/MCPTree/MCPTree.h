
#ifndef MCPTree_h
#define MCPTree_h

#include <vector>

#include "TROOT.h"
#include "TTree.h"
#include "TChain.h"
#include "TFile.h"
#include "TDirectory.h"

#include "Math/LorentzVector.h"
#include "Math/PtEtaPhiM4D.h"
typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > LorentzPtEtaPhiMf;

using namespace std;

class MCPTree {
  public:

    unsigned int       event;
    LorentzPtEtaPhiMf* parent_p4 = 0;
    int                parent_pdgId;
    int                decay_flag;
    LorentzPtEtaPhiMf* p4_1 = 0;
    LorentzPtEtaPhiMf* p4_2 = 0;
    float              xsec;
    float              BR_q1;
    float              weight;
    float              weight_up;
    float              weight_dn;

    MCPTree(TTree *tree=0);
    void Init(TTree *tree=0);
    void Fill();
    void Reset();
    void Write(TDirectory *d);
    void GetEntry(ULong64_t entry);
    static void progress(int nEventsTotal, int nEventsChain);

  private:
    TTree *tree;

    TBranch *b_event = 0;
    TBranch *b_parent_p4 = 0;
    TBranch *b_parent_pdgId = 0;
    TBranch *b_decay_flag = 0;
    TBranch *b_p4_1 = 0;
    TBranch *b_p4_2 = 0;
    TBranch *b_xsec = 0;
    TBranch *b_BR_q1 = 0;
    TBranch *b_weight = 0;
    TBranch *b_weight_up = 0;
    TBranch *b_weight_dn = 0;

};

#endif
