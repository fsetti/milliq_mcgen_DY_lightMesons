#include <algorithm>
#include <iostream>
#include <string>
#include <cmath>

#include "TFile.h"
#include "TGraph.h"

#include "../../decayMCP/DecayGen.h"

int main(){

    DecayGen dg;
    dg.BASE_DIR = "../..";

    const float min_mass = 0.001;
    const float max_mass = 5.5;
    const int n_masses = 1000;

    TFile fout = TFile("xsecs.root", "RECREATE");
    fout.Close();

    TGraph *gt = new TGraph();
    gt->SetName("xsecs_total");

    for(int i=1; i<=15; i++){
        TGraph *g = new TGraph();
        g->SetName(("xsecs_"+std::to_string(i)).c_str());

        for(int j=0; j<=n_masses; j++){
            float mass = min_mass * pow(max_mass/min_mass, (float)j/n_masses);
            std::cout << mass << std::endl;
            dg.Initialize(i, mass);
            if(dg.BR < 0){
                float mass_limit = dg.m_parent/2;
                if(dg.decay_type == DecayGen::DALITZ)
                    mass_limit = (dg.m_parent - dg.m_X)/2;
                g->SetPoint(g->GetN(), mass_limit, 0.001);
                break;
            }
            float xsec = dg.xsec_inclusive * dg.BR;
            xsec /= (dg.etamax - dg.etamin) / 2; // normalize to eta in [-1,1]
            g->SetPoint(g->GetN(), mass, xsec);
            double x,y, cur_xs;
            if(gt->GetN() > j){
                gt->GetPoint(j, x, y);
                cur_xs = y;
            }else
                cur_xs = 0.0;
            gt->SetPoint(j, mass, cur_xs + xsec);
        }
        TFile fout = TFile("xsecs.root", "UPDATE");
        g->Write(g->GetName(), TObject::kWriteDelete);
        fout.Close();
    }
    gt->SetPoint(gt->GetN(), 5.1776, 0.001);
    TFile fout2 = TFile("xsecs.root", "UPDATE");
    gt->Write(gt->GetName(), TObject::kWriteDelete);
    fout2.Close();


}
