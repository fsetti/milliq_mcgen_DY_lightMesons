#include <iostream>
#include <cmath>

float br_onia(float mass, int parent_pdgId){
    // mCP mass in GeV

    float mp, BRe;
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
        BRe = 2.48e-3;
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
        throw std::exception();
    }

    // convert to GeV
    mp /= 1000.0;

    if(2*mass > mp){
        std::cout << "ERROR! mCP mass is greater than half the parent mass " << mp << " GeV\n";
        throw std::exception();
    }

    float emass = 0.000511;
    float x1 = mass / mp;
    float xe = emass / mp;
    
    return BRe * (sqrt(1-4*x1*x1) * (1+2*x1*x1)) / (sqrt(1-4*xe*xe) * (1+2*xe*xe));

}
