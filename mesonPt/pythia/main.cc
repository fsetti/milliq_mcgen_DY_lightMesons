#include <cstdlib>
#include <iostream>

#include "TFile.h"
#include "TH1D.h"

#include "Pythia8/Pythia.h"

using namespace Pythia8;

bool is_b(int id){
    id = abs(id);
    return ((id/100)%10==5 || (id/1000)%10==5);
}

bool is_c(int id){
    id = abs(id);
    return ((id/100)%10==4 || (id/1000)%10==4);
}

int main(int argc, char** argv) {

    if(argc < 4){
        std::cout << "usage: " << argv[0] << " <mode> <tune> <n_events> <seed=0>\n";
        return -1;
    }

    int mode = atoi(argv[1]);
    int tune = atoi(argv[2]);
    int nevt = atoi(argv[3]);
    int seed = 0;
    if(argc >= 5)
        seed = atoi(argv[4]);

        // Generator. Process selection. LHC initialization. Histogram.
    Pythia pythia;
    pythia.readString("Random:setSeed = on");
    pythia.readString("Random:seed = "+std::to_string(seed));
    pythia.readString("Beams:eCM = 13000.");
    if(mode == 0){
        // MinBias
        pythia.readString("SoftQCD:nonDiffractive = on");
        pythia.readString("SoftQCD:singleDiffractive = on");
        pythia.readString("SoftQCD:doubleDiffractive = on");
    }else{
        // QCD pT binned
        pythia.readString("HardQCD:all = on");
        if(mode == 1) {
            pythia.readString("PhaseSpace:pTHatMin = 15");
            pythia.readString("PhaseSpace:pTHatMax = 30");
        }else if(mode == 2) {
            pythia.readString("PhaseSpace:pTHatMin = 30");
            pythia.readString("PhaseSpace:pTHatMax = 50");
        }else if(mode == 3) {
            pythia.readString("PhaseSpace:pTHatMin = 50");
            pythia.readString("PhaseSpace:pTHatMax = 80");
        }else if(mode == 4) {
            pythia.readString("PhaseSpace:pTHatMin = 80");
            pythia.readString("PhaseSpace:pTHatMax = 120");
        }else{
            std::cout << "Invalid decay mode: " << mode << std::endl;
            return -1;
        }
    }
    // turn on pi/K decays
    pythia.readString("ParticleDecays:limitTau0 = off");
    pythia.readString("ParticleDecays:limitCylinder = on");
    pythia.readString("ParticleDecays:xyMax = 2000");
    pythia.readString("ParticleDecays:zMax = 4000");
    pythia.readString("130:mayDecay = on");
    pythia.readString("211:mayDecay = on");
    pythia.readString("321:mayDecay = on");


    // pythia8 common settings from CMSSW
    pythia.readString("Tune:preferLHAPDF = 2");
    pythia.readString("Main:timesAllowErrors = 10000");
    pythia.readString("Check:epTolErr = 0.01");
    pythia.readString("Beams:setProductionScalesFromLHEF = off");
    pythia.readString("SLHA:keepSM = on");
    pythia.readString("SLHA:minMassSM = 1000.");
    // pythia.readString("ParticleDecays:limitTau0 = on");
    // pythia.readString("ParticleDecays:tau0Max = 10");
    pythia.readString("ParticleDecays:allowPhotonRadiation = on");

    // pythia8 Monash2013 settings
    if(tune <= 1){
        pythia.readString("Tune:pp 14");
        pythia.readString("Tune:ee 7");
    }
    // pythia8 CUETP8M1 settings (apply ON TOP OF monash 2013)
    if(tune == 1){
        pythia.readString("MultipartonInteractions:pT0Ref=2.4024");
        pythia.readString("MultipartonInteractions:ecmPow=0.25208");
        pythia.readString("MultipartonInteractions:expPow=1.6");
    }
    // A2-CTEQ6L1
    if(tune == 7){
        pythia.readString("Tune:pp 7");
    }
    // A2-MSTW2008LO
    if(tune == 8){
        pythia.readString("Tune:pp 8");
    }

    pythia.init();

    TFile *fout = new TFile("output.root","RECREATE");
    TH1D *h_nevents = new TH1D("h_nevents", "", 1, 0, 2);
    TH1D *h_etaall = new TH1D("h_etaall", ";#eta", 100, 3, 3);
    TH1D *h_pi = new TH1D("h_pi", ";p_{T} [GeV]",2000,0,100);
    TH1D *h_pi0 = new TH1D("h_pi0", ";p_{T} [GeV]",2000,0,100);
    TH1D *h_rho = new TH1D("h_rho", ";p_{T} [GeV]",2000,0,100);
    TH1D *h_omega = new TH1D("h_omega", ";p_{T} [GeV]",2000,0,100);
    TH1D *h_phi = new TH1D("h_phi", ";p_{T} [GeV]",2000,0,100);
    TH1D *h_eta = new TH1D("h_eta", ";p_{T} [GeV]",2000,0,100);
    TH1D *h_etap = new TH1D("h_etap", ";p_{T} [GeV]",2000,0,100);
    TH1D *h_mu = new TH1D("h_mu", ";p_{T} [GeV]",2000,0,100);
    TH1D *h_mu_nonbc = new TH1D("h_mu_nonbc", ";p_{T} [GeV]",2000,0,100);
    TH1D *h_mu_mother = new TH1D("h_mu_mother", ";mother id",6000,0.5,6000.5);

    // Begin event loop. Generate event. Skip if error. List first one.
    for (int iEvent = 0; iEvent < nevt; ++iEvent) {
        if (!pythia.next()) continue;        
        h_nevents->Fill(1);
        for (int i = 0; i < pythia.event.size(); ++i){
            Particle& p = pythia.event[i];
            if (fabs(p.p().eta()) < 2){
                
                h_etaall->Fill(p.p().eta());

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

                if(abs(p.id()) == 13 && p.status()==91){
                    int mid = pythia.event[p.mother1()].id();
                    h_mu->Fill(p.p().pT());
                    // std::cout << "Found mu! status = " << p.status() << "; mother id = " << pythia.event[p.mother1()].id() << std::endl;
                    if(!is_b(mid) && !is_c(mid)){
                        h_mu_nonbc->Fill(p.p().pT());
                        if(p.p().pT() > 15)
                            h_mu_mother->Fill(abs(mid));
                    }
                }
            }            
        }
    }

    h_nevents->Write();
    h_etaall->Write();
    h_pi->Write();
    h_pi0->Write();
    h_omega->Write();
    h_rho->Write();
    h_phi->Write();
    h_eta->Write();
    h_etap->Write();
    h_mu->Write();
    h_mu_nonbc->Write();
    h_mu_mother->Write();
    fout->Close();

    return 0;
}
