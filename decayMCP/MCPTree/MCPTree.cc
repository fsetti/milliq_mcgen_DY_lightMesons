
#include "MCPTree.h"
#include "TTree.h"
#include "TDirectory.h"
#include <iostream>
#include <vector>

using namespace std;

MCPTree::MCPTree(TTree *t){
    if(t != NULL)
        Init(t);
}

void MCPTree::Init(TTree *t){
    if(t == NULL){
        // if we don't pass a tree, open in "write" mode. pointers have to be initialized,
        // and then create the branches.
        this->t = new TTree("Events","");

        this->parent_p4      = new LorentzPtEtaPhiMf;
        this->p4_p           = new LorentzPtEtaPhiMf;
        this->p4_m           = new LorentzPtEtaPhiMf;

        b_event          = this->t->Branch("event", &event, "event/i");
        b_n_events_total = this->t->Branch("n_events_total", &n_events_total, "n_events_total/i");
        b_parent_p4      = this->t->Branch("parent_p4", &parent_p4);
        b_parent_pdgId   = this->t->Branch("parent_pdgId", &parent_pdgId, "parent_pdgId/I");
        b_decay_mode     = this->t->Branch("decay_mode", &decay_mode, "decay_mode/I");
        b_p4_p           = this->t->Branch("p4_p", &p4_p);
        b_p4_m           = this->t->Branch("p4_m", &p4_m);
        b_xsec           = this->t->Branch("xsec", &xsec, "xsec/F");
        b_xsec_up        = this->t->Branch("xsec_up", &xsec_up, "xsec_up/F");
        b_xsec_down      = this->t->Branch("xsec_down", &xsec_down, "xsec_down/F");
        b_BR_q1          = this->t->Branch("BR_q1", &BR_q1, "BR_q1/F");
        b_filter_eff     = this->t->Branch("filter_eff", &filter_eff, "filter_eff/F");
        b_weight         = this->t->Branch("weight", &weight, "weight/F");
        b_weight_up      = this->t->Branch("weight_up", &weight_up, "weight_up/F");
        b_weight_dn      = this->t->Branch("weight_dn", &weight_dn, "weight_dn/F");
        b_mCP_etamin     = this->t->Branch("mCP_etamin", &mCP_etamin, "mCP_etamin/F");
        b_mCP_etamax     = this->t->Branch("mCP_etamax", &mCP_etamax, "mCP_etamax/F");
        b_mCP_phimin     = this->t->Branch("mCP_phimin", &mCP_phimin, "mCP_phimin/F");
        b_mCP_phimax     = this->t->Branch("mCP_phimax", &mCP_phimax, "mCP_phimax/F");

        Reset();
    }else{
        // if we do pass a tree, open in "read" mode
        this->t = t;
        //this->t->SetMakeClass(1);

        this->t->SetBranchAddress("event", &event, &b_event);
        this->t->SetBranchAddress("n_events_total", &n_events_total, &b_n_events_total);
        this->t->SetBranchAddress("parent_p4", &parent_p4, &b_parent_p4);
        this->t->SetBranchAddress("parent_pdgId", &parent_pdgId, &b_parent_pdgId);
        this->t->SetBranchAddress("decay_mode", &decay_mode, &b_decay_mode);
        this->t->SetBranchAddress("p4_p", &p4_p, &b_p4_p);
        this->t->SetBranchAddress("p4_m", &p4_m, &b_p4_m);
        this->t->SetBranchAddress("xsec", &xsec, &b_xsec);
        this->t->SetBranchAddress("xsec_up", &xsec_up, &b_xsec_up);
        this->t->SetBranchAddress("xsec_down", &xsec_down, &b_xsec_down);
        this->t->SetBranchAddress("BR_q1", &BR_q1, &b_BR_q1);
        this->t->SetBranchAddress("filter_eff", &filter_eff, &b_filter_eff);
        this->t->SetBranchAddress("weight", &weight, &b_weight);
        this->t->SetBranchAddress("weight_up", &weight_up, &b_weight_up);
        this->t->SetBranchAddress("weight_dn", &weight_dn, &b_weight_dn);
        this->t->SetBranchAddress("mCP_etamin", &mCP_etamin, &b_mCP_etamin);
        this->t->SetBranchAddress("mCP_etamax", &mCP_etamax, &b_mCP_etamax);
        this->t->SetBranchAddress("mCP_phimin", &mCP_phimin, &b_mCP_phimin);
        this->t->SetBranchAddress("mCP_phimax", &mCP_phimax, &b_mCP_phimax);

    }
    t_old = std::chrono::system_clock::now();
}

void MCPTree::Fill(){
    t->Fill();
}

void MCPTree::Reset(){
    event = -999;
    n_events_total = -999;
    *parent_p4 = LorentzPtEtaPhiMf();
    parent_pdgId = -999;
    decay_mode = -999;
    *p4_p = LorentzPtEtaPhiMf();
    *p4_m = LorentzPtEtaPhiMf();
    xsec = -999;
    xsec_up = -999;
    xsec_down = -999;
    BR_q1 = -999;
    filter_eff = -999;
    weight = -999;
    weight_up = -999;
    weight_dn = -999;
    mCP_etamin = -999;
    mCP_etamax = -999;
    mCP_phimin = -999;
    mCP_phimax = -999;

}

void MCPTree::Write(TDirectory *d){
    d->cd();
    t->Write();
}

void MCPTree::GetEntry(ULong64_t i){
    this->t->GetEntry(i);
}

void MCPTree::progress( int curr, int tot, int period, unsigned int smoothing) {
    if(curr%period == 0) {
        auto now = std::chrono::system_clock::now();
        double dt = ((std::chrono::duration<double>)(now - t_old)).count();
        t_old = now;
        // if (deq.size() >= smoothing) deq.pop_front();                                                                                                                                                            
        if (deq.size() >= smoothing) deq.erase(deq.begin());
        deq.push_back(dt);
        double avgdt = std::accumulate(deq.begin(),deq.end(),0.)/deq.size();
        float prate = (float)period/avgdt;
        float peta = (tot-curr)/prate;
        if (isatty(1)) {
            float pct = (float)curr/(tot*0.01);
            if( ( tot - curr ) <= period ) pct = 100.0;
            printf("\015\033[32m ---> \033[1m\033[31m%4.1f%% \033[34m [%.3f kHz, ETA: %.0f s] \033[0m\033[32m  <---\033[0m\015 ", pct, prate/1000.0, peta);
            if( ( tot - curr ) > period ) fflush(stdout);
            else cout << endl;
        }
    }
}
