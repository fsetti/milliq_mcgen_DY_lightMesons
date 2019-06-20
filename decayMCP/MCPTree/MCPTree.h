
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
    LorentzPtEtaPhiMf* p4_p = 0;
    LorentzPtEtaPhiMf* p4_m = 0;
    float              xsec;
    float              BR_q1;
    float              filter_eff;
    float              weight;
    float              weight_up;
    float              weight_dn;

    MCPTree(TTree *t=0);
    void Init(TTree *t=0);
    void Fill();
    void Reset();
    void Write(TDirectory *d);
    void GetEntry(ULong64_t entry);
    TTree * tree(){ return t; }
    static void progress(int nEventsTotal, int nEventsChain);

  private:
    TTree *t;

    TBranch *b_event = 0;
    TBranch *b_parent_p4 = 0;
    TBranch *b_parent_pdgId = 0;
    TBranch *b_decay_flag = 0;
    TBranch *b_p4_p = 0;
    TBranch *b_p4_m = 0;
    TBranch *b_xsec = 0;
    TBranch *b_BR_q1 = 0;
    TBranch *b_filter_eff = 0;
    TBranch *b_weight = 0;
    TBranch *b_weight_up = 0;
    TBranch *b_weight_dn = 0;

};

#endif
