
#include "MCPTree.h"
#include "TTree.h"
#include "TDirectory.h"
#include <iostream>
#include <vector>

using namespace std;

MCPTree::MCPTree(TTree *tree){
    if(tree != NULL)
        Init(tree);
}

void MCPTree::Init(TTree *tree){
    if(tree == NULL){
        // if we don't pass a tree, open in "write" mode. pointers have to be initialized,
        // and then create the branches.
        this->tree = new TTree("Events","");

        this->p4_parent  = new LorentzPtEtaPhiMf;
        this->p4_1       = new LorentzPtEtaPhiMf;
        this->p4_2       = new LorentzPtEtaPhiMf;

        b_event      = this->tree->Branch("event", &event, "event/i");
        b_p4_parent  = this->tree->Branch("p4_parent", &p4_parent);
        b_decay_flag = this->tree->Branch("decay_flag", &decay_flag, "decay_flag/I");
        b_p4_1       = this->tree->Branch("p4_1", &p4_1);
        b_p4_2       = this->tree->Branch("p4_2", &p4_2);
        b_xsec       = this->tree->Branch("xsec", &xsec, "xsec/F");
        b_BR_q1      = this->tree->Branch("BR_q1", &BR_q1, "BR_q1/F");
        b_weight     = this->tree->Branch("weight", &weight, "weight/F");
        b_weight_up  = this->tree->Branch("weight_up", &weight_up, "weight_up/F");
        b_weight_dn  = this->tree->Branch("weight_dn", &weight_dn, "weight_dn/F");

        Reset();
    }else{
        // if we do pass a tree, open in "read" mode
        this->tree = tree;
        //this->tree->SetMakeClass(1);

        this->tree->SetBranchAddress("event", &event, &b_event);
        this->tree->SetBranchAddress("p4_parent", &p4_parent, &b_p4_parent);
        this->tree->SetBranchAddress("decay_flag", &decay_flag, &b_decay_flag);
        this->tree->SetBranchAddress("p4_1", &p4_1, &b_p4_1);
        this->tree->SetBranchAddress("p4_2", &p4_2, &b_p4_2);
        this->tree->SetBranchAddress("xsec", &xsec, &b_xsec);
        this->tree->SetBranchAddress("BR_q1", &BR_q1, &b_BR_q1);
        this->tree->SetBranchAddress("weight", &weight, &b_weight);
        this->tree->SetBranchAddress("weight_up", &weight_up, &b_weight_up);
        this->tree->SetBranchAddress("weight_dn", &weight_dn, &b_weight_dn);

    }
}

void MCPTree::Fill(){
    tree->Fill();
}

void MCPTree::Reset(){
    event = -999;
    *p4_parent = LorentzPtEtaPhiMf();
    decay_flag = -999;
    *p4_1 = LorentzPtEtaPhiMf();
    *p4_2 = LorentzPtEtaPhiMf();
    xsec = -999;
    BR_q1 = -999;
    weight = -999;
    weight_up = -999;
    weight_dn = -999;

}

void MCPTree::Write(TDirectory *d){
    d->cd();
    tree->Write();
}

void MCPTree::GetEntry(ULong64_t i){
    this->tree->GetEntry(i);
}
