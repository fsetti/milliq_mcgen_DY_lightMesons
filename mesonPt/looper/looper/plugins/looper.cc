// -*- C++ -*-
//
// Package:    looper/looper
// Class:      looper
// 
/**\class looper looper.cc looper/looper/plugins/looper.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  bmarsh@umail.ucsb.edu 6-10-2015
//         Created:  Mon, 10 Sep 2018 20:55:43 GMT
//
//


// system include files
#include <memory>
#include <vector>

// ROOT includes
#include <TH1D.h>
#include <TH2D.h>
#include <TFile.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "RecoTauTag/TauTagTools/interface/GeneratorTau.h"
//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class looper : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit looper(const edm::ParameterSet&);
      ~looper();

    edm::EDGetTokenT<reco::GenParticleCollection> genPartsT_;

   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

    TFile *fout;
    TH1D *h_nevents, *h_etaall;
    TH1D *h_pi0, *h_pi, *h_omega, *h_rho, *h_phi, *h_eta, *h_etap;
    TH2D *h_pteta;
    // TTree *tree;

      // ----------member data ---------------------------
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
looper::looper(const edm::ParameterSet& iConfig) : 
    genPartsT_( consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("genparts")))
{
}

looper::~looper(){}

//
// member functions
//

// ------------ method called for each event  ------------
void
looper::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

    edm::Handle<reco::GenParticleCollection> genParts_h;
    iEvent.getByToken(genPartsT_, genParts_h);
    const reco::GenParticleCollection* genParts = genParts_h.product();
    // std::cout << "----- PRUNED -----" << std::endl;
    h_nevents->Fill(1);
    for(uint i=0; i<genParts->size(); i++){
        const reco::GenParticle& gp = genParts->at(i);
        if(fabs(gp.eta()) > 2)
            continue;

        h_pteta->Fill(gp.pt(), gp.eta());
        h_etaall->Fill(gp.eta());

        if(gp.status()==1 && abs(gp.pdgId()) == 211)
            h_pi->Fill(gp.pt());
        if(gp.status()==2 && gp.pdgId() == 111)
            h_pi0->Fill(gp.pt());
        if(gp.status()==2 && gp.pdgId() == 113)
            h_rho->Fill(gp.pt());
        if(gp.status()==2 && gp.pdgId() == 223)
            h_omega->Fill(gp.pt());
        if(gp.status()==2 && gp.pdgId() == 333)
            h_phi->Fill(gp.pt());
        if(gp.status()==2 && gp.pdgId() == 221)
            h_eta->Fill(gp.pt());
        if(gp.status()==2 && gp.pdgId() == 331)
            h_etap->Fill(gp.pt());
    }


}


// ------------ method called once each job just before starting event loop  ------------
void 
looper::beginJob()
{

    fout = new TFile("output.root", "RECREATE");

    h_nevents = new TH1D("h_nevents","",1,0,2);
    h_etaall = new TH1D("h_etaall",";#eta",100,-2,2);

    h_pi = new TH1D("h_pi",";p_{T} [GeV]",2000,0,100);
    h_pi0 = new TH1D("h_pi0",";p_{T} [GeV]",2000,0,100);
    h_rho = new TH1D("h_rho",";p_{T} [GeV]",2000,0,100);
    h_omega = new TH1D("h_omega",";p_{T} [GeV]",2000,0,100);
    h_phi = new TH1D("h_phi",";p_{T} [GeV]",2000,0,100);
    h_eta = new TH1D("h_eta",";p_{T} [GeV]",2000,0,100);
    h_etap = new TH1D("h_etap",";p_{T} [GeV]",2000,0,100);

    h_pteta = new TH2D("h_pteta", ";p_{T} [GeV];#eta", 500, 0, 50, 80, -2, 2);
}

// ------------ method called once each job just after ending the event loop  ------------
void 
looper::endJob() 
{
    fout->cd();
    h_nevents->Write();
    h_etaall->Write();
    h_pteta->Write();
    h_pi->Write();
    h_pi0->Write();
    h_rho->Write();
    h_omega->Write();
    h_phi->Write();
    h_eta->Write();
    h_etap->Write();
    fout->Close();

    delete h_nevents;
    delete h_etaall;
    delete h_pteta;
    delete h_pi;
    delete h_pi0;
    delete h_rho;
    delete h_omega;
    delete h_phi;
    delete h_eta;
    delete h_etap;
    delete fout;
}

//define this as a plug-in
DEFINE_FWK_MODULE(looper);
