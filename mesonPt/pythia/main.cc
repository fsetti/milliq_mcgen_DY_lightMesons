#include <cstdlib>
#include <iostream>

#include "TFile.h"
#include "TH1D.h"

#include "Pythia8/Pythia.h"

using namespace Pythia8;

int main(int argc, char** argv) {

    if(argc < 2){
        std::cout << "usage: " << argv[0] << " <n_events>\n";
        return -1;
    }

    int nevt = atoi(argv[1]);

        // Generator. Process selection. LHC initialization. Histogram.
    Pythia pythia;
    pythia.readString("Random:setSeed = on");
    pythia.readString("Random:seed = 0");
    pythia.readString("Beams:eCM = 13000.");
    pythia.readString("SoftQCD:nonDiffractive = on");
    pythia.readString("SoftQCD:singleDiffractive = on");
    pythia.readString("SoftQCD:doubleDiffractive = on");

    // pythia8 common settings from CMSSW
    pythia.readString("Tune:preferLHAPDF = 2");
    pythia.readString("Main:timesAllowErrors = 10000");
    pythia.readString("Check:epTolErr = 0.01");
    pythia.readString("Beams:setProductionScalesFromLHEF = off");
    pythia.readString("SLHA:keepSM = on");
    pythia.readString("SLHA:minMassSM = 1000.");
    pythia.readString("ParticleDecays:limitTau0 = on");
    pythia.readString("ParticleDecays:tau0Max = 10");
    pythia.readString("ParticleDecays:allowPhotonRadiation = on");

    // pythia8 CUEP8M1 settings
    pythia.readString("Tune:pp 14");
    pythia.readString("Tune:ee 7");
    pythia.readString("MultipartonInteractions:pT0Ref=2.4024");
    pythia.readString("MultipartonInteractions:ecmPow=0.25208");
    pythia.readString("MultipartonInteractions:expPow=1.6");

    pythia.init();

    TFile *fout = new TFile("output.root","RECREATE");
    TH1D *h_pi = new TH1D("h_pi", ";p_{T} [GeV]",2000,0,100);
    TH1D *h_pi0 = new TH1D("h_pi0", ";p_{T} [GeV]",2000,0,100);
    TH1D *h_rho = new TH1D("h_rho", ";p_{T} [GeV]",2000,0,100);
    TH1D *h_omega = new TH1D("h_omega", ";p_{T} [GeV]",2000,0,100);
    TH1D *h_phi = new TH1D("h_phi", ";p_{T} [GeV]",2000,0,100);
    TH1D *h_eta = new TH1D("h_eta", ";p_{T} [GeV]",2000,0,100);
    TH1D *h_etap = new TH1D("h_etap", ";p_{T} [GeV]",2000,0,100);

    // Begin event loop. Generate event. Skip if error. List first one.
    for (int iEvent = 0; iEvent < nevt; ++iEvent) {
        if (!pythia.next()) continue;        
        for (int i = 0; i < pythia.event.size(); ++i){
            Particle& p = pythia.event[i];
            if (fabs(p.p().eta()) < 2){
                
                if (abs(p.id()) == 211)
                    h_pi->Fill(p.p().pT());
                if (abs(p.id()) == 111)
                    h_pi0->Fill(p.p().pT());
                if (abs(p.id()) == 113)
                    h_rho->Fill(p.p().pT());
                if (abs(p.id()) == 223)
                    h_omega->Fill(p.p().pT());
                if (abs(p.id()) == 333)
                    h_phi->Fill(p.p().pT());
                if (abs(p.id()) == 221)
                    h_eta->Fill(p.p().pT());
                if (abs(p.id()) == 331)
                    h_etap->Fill(p.p().pT());

            }            
        }
    }

    h_pi->Write();
    h_pi0->Write();
    h_omega->Write();
    h_rho->Write();
    h_phi->Write();
    h_eta->Write();
    h_etap->Write();
    fout->Close();

    return 0;
}
