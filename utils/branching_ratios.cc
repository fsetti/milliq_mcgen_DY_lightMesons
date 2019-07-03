#include <cstdio>
#include <iostream>
#include <cmath>

#include <TF1.h>

#include "branching_ratios.h"
#include "decay.h"

float br_onia(float mass, int parent_pdgId){
    // BR for 2-body decay P -> mCP+ mCP-
    // mass = mCP mass in GeV

    float mp, BRe; // mp = parent mass in MeV, BRe = BR(P -> e+e-)
    if(parent_pdgId == 113){
        mp = 775.3;
        BRe = 4.72e-5;
    }else if(parent_pdgId == 333){
        mp   =  1019.5;
        BRe = 2.97e-4;
    }else if(parent_pdgId == 223){
        mp =   782.7;
        BRe = 7.36e-5;
    }else if(parent_pdgId == 443){
        mp   =  3096.9;
        BRe = 5.96e-2;
    }else if(parent_pdgId == 100443){
        mp =  3686.1;
        BRe = 7.93e-3;
    }else if(parent_pdgId == 553){
        mp =  9460.3;
        BRe = 2.38e-2;
    }else if(parent_pdgId == 100553){
        mp = 10023.3;
        BRe = 1.91e-2;
    }else if(parent_pdgId == 200553){
        mp = 10355.2;
        BRe = 2.18e-2;
    }else if(parent_pdgId == 300553){
        mp = 10579.4;
        BRe = 1.57e-5;
    }else{
        std::cout << "ERROR! pdgId " << parent_pdgId << " is not a known -onia ID\n";
        return -1;
    }

    // convert to GeV
    mp /= 1000.0;

    if(2*mass > mp){
        std::cout << "ERROR! mCP mass is greater than half the parent mass " << mp << " GeV\n";
        return -1;
    }

    float emass = 0.000511;
    float x1 = mass / mp;
    float xe = emass / mp;
    
    return BRe * (sqrt(1-4*x1*x1) * (1+2*x1*x1)) / (sqrt(1-4*xe*xe) * (1+2*xe*xe));

}

float br_dalitz(float mass, int parent_pdgId, float mX){
    // BR of dalitz decay P -> mCP+ mCP- X
    // mass = mCP mass in GeV
    // mX = X mass in GeV

    float mp, BR; // mp = parent mass in GeV, BR = BR(P -> X gamma)
    if(parent_pdgId == 111){
        mp = 0.13497;
        BR = 0.98823;
    }else if(parent_pdgId == 221){
        mp = 0.547862;
        BR = 0.3941;
    }else if(parent_pdgId == 331){
        mp = 0.9578;
        if(mX > 0.001)
            // X is omega
            BR = 0.0262;
        else
            // X is gamma
            BR = 0.0222;
    }else if(parent_pdgId == 223){
        mp = 0.78265;
        // X is pi0
        BR = 0.0840;
    }else{
        std::cout << "ERROR! pdgId " << parent_pdgId << " is not a known dalitz-decaying particle!\n";
        return -1;
    }

    if(2*mass + mX > mp){
        std::cout << "ERROR! mCP mCP X mass is greater than the parent mass " << mp << " GeV\n";
        return -1;
    }

    float lo = (2*mass);
    float hi = (mp-mX);
    
    // TF1 f = TF1("flog", DGDLOGQ2_VDM, log(lo*lo), log(hi*hi));
    TF1 f = TF1("flin", DGDQ2_VDM, lo*lo, hi*hi);
    f.SetParameter(0, hi);
    f.SetParameter(1, mp+mX);
    f.SetParameter(2, lo);
    f.SetParameter(3, 0.7755);
    f.SetParameter(4, 0.1462);

    // float integral = f.Integral(log(lo*lo), log(hi*hi));
    float integral = f.Integral(lo*lo, hi*hi);
    // double for photon
    if(mX < 0.0001) integral *= 2;

    // the width of the dalitz decay is (integral)*(width[P->Xgamma]), so BR is (integral)*(BR[P->Xgamma])
    return integral * BR;
    

}

// for use as a root macro, print out test decays
void branching_ratios(){

    float masses[] = {0.000511, 0.010, 0.030, 0.050, 0.060, 0.090, 0.1057, 0.150, 0.200, 0.250, 0.400};
    int parent_pdgIds[] = {111,221,331,331,223};
    float mPs[] = {0.13497,0.547862,0.9578,0.9578,0.78265};
    float mXs[] = {0,0,0,0.78265,0.13497};
    
    // pi0 -> mCP mCP gamma
    for(int i=0; i<5; i++){
        printf("Decays for P=%d, mX=%.4f\n", parent_pdgIds[i], mXs[i]);
        int j=0;
        for(j=0; 2*masses[j] + mXs[i] < mPs[i] && j<11; j++){
            float BR = br_dalitz(masses[j], parent_pdgIds[i], mXs[i]);
            printf("  mMCP=%7.3f MeV: %.1e\n", masses[j]*1000, BR);
        }
    }

}
