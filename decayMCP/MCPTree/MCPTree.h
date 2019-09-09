
#ifndef MCPTree_h
#define MCPTree_h

#include <vector>
#include <chrono>
#include <numeric>

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
    unsigned int       n_events_total;
    LorentzPtEtaPhiMf* parent_p4 = 0;
    int                parent_pdgId;
    int                decay_mode;
    LorentzPtEtaPhiMf* p4_p = 0;
    LorentzPtEtaPhiMf* p4_m = 0;
    float              xsec;
    float              xsec_up;
    float              xsec_down;
    float              BR_q1;
    float              filter_eff;
    float              weight;
    float              weight_up;
    float              weight_dn;
    float              mCP_etamin;
    float              mCP_etamax;
    float              mCP_phimin;
    float              mCP_phimax;

    MCPTree(TTree *t=0);
    void Init(TTree *t=0);
    void Fill();
    void Reset();
    void Write(TDirectory *d);
    void GetEntry(ULong64_t entry);
    TTree * tree(){ return t; }
    void progress(int nEventsTotal, int nEventsChain, int period=1000, uint smoothing=30);

  private:
    TTree *t;
    std::chrono::time_point<std::chrono::system_clock> t_old;
    std::vector<double> deq;

    TBranch *b_event = 0;
    TBranch *b_n_events_total = 0;
    TBranch *b_parent_p4 = 0;
    TBranch *b_parent_pdgId = 0;
    TBranch *b_decay_mode = 0;
    TBranch *b_p4_p = 0;
    TBranch *b_p4_m = 0;
    TBranch *b_xsec = 0;
    TBranch *b_xsec_up = 0;
    TBranch *b_xsec_down = 0;
    TBranch *b_BR_q1 = 0;
    TBranch *b_filter_eff = 0;
    TBranch *b_weight = 0;
    TBranch *b_weight_up = 0;
    TBranch *b_weight_dn = 0;
    TBranch *b_mCP_etamin = 0;
    TBranch *b_mCP_etamax = 0;
    TBranch *b_mCP_phimin = 0;
    TBranch *b_mCP_phimax = 0;

};

#endif
