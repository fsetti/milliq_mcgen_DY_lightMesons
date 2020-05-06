#include <algorithm>
#include <iostream>
#include <string>
#include <cmath>

#include "TFile.h"
#include "TGraphAsymmErrors.h"

#include "../../decayMCP/DecayGen.h"

int main(int argc, char** argv){

    DecayGen dg;
    dg.BASE_DIR = "../..";

    const float min_mass = 0.001;
    const float max_mass = 5.5;
    const int n_masses = 1000;

    TFile* fout = new TFile("xsecs.root", "RECREATE");

    TGraphAsymmErrors *gt = new TGraphAsymmErrors();
    gt->SetName("xsecs_total");

    for(int i=1; i<=15; i++){
        TGraphAsymmErrors *g = new TGraphAsymmErrors();
        g->SetName(("xsecs_"+std::to_string(i)).c_str());

        for(int j=0; j<=n_masses; j++){
            float mass = min_mass * pow(max_mass/min_mass, (float)j/n_masses);
            // std::cout << mass << std::endl;
            dg.Initialize(i, mass);
            // if this is <0, it means the BR calc failed because mCP is too heavy. So we've reached the kinematic limit
            // In this case, add an extra point right on the threshold to force graph to go down to "zero"
            if(dg.BR < 0){
                float mass_limit = dg.m_parent/2;
                if(dg.decay_type == DecayGen::DALITZ)
                    mass_limit = (dg.m_parent - dg.m_X)/2;
                g->SetPoint(g->GetN(), mass_limit, 0.001);
                g->SetPointError(g->GetN()-1, 0, 0, 0.0005,0.0005);
                break;
            }
            float xsec = dg.xsec_inclusive * dg.BR;
            xsec /= (dg.etamax - dg.etamin) / 4; // normalize to eta in [-2,2]
            float xsec_up = xsec * dg.xsec_up/dg.xsec_inclusive;
            float xsec_dn = xsec * dg.xsec_down/dg.xsec_inclusive;
            g->SetPoint(g->GetN(), mass, xsec);
            g->SetPointError(g->GetN()-1, 0, 0, xsec-xsec_dn, xsec_up-xsec);
            // get current total xsec at this mass, and add the current xsec
            double x,y, cur_xs, cur_errup, cur_errdn;
            if(gt->GetN() > j){
                gt->GetPoint(j, x, y);
                cur_xs = y;
                cur_errup = gt->GetErrorYhigh(j);
                cur_errdn = gt->GetErrorYlow(j);
            }else
                cur_xs = 0.0, cur_errup = 0.0, cur_errdn = 0.0;;
            gt->SetPoint(j, mass, cur_xs + xsec);
            // for the xsec_total graph, add in a correlated minbias xsec uncertainty (using 10/80 = 12.5%)
            if(i>=3 && i<=10){
                float frac = 10.0/80.0;
                gt->SetPointError(j, 0, 0, sqrt(pow(cur_errdn,2)+pow(xsec-xsec_dn,2)) + frac*xsec, sqrt(pow(cur_errup,2)+pow(xsec_up-xsec,2)) + frac*xsec);
            }else{
                gt->SetPointError(j, 0, 0, sqrt(pow(cur_errdn,2)+pow(xsec-xsec_dn,2)), sqrt(pow(cur_errup,2)+pow(xsec_up-xsec,2)));                
            }
        }
        fout->cd();
        g->Write(g->GetName(), TObject::kWriteDelete);
    }
    // add final point at highest kinematic threshold (half of Ups(3S) mass) at "zero"
    gt->SetPoint(gt->GetN(), 5.1776, 0.001);
    gt->SetPointError(gt->GetN()-1, 0, 0, 0.0005, 0.0005);
    gt->Write(gt->GetName(), TObject::kWriteDelete);
    fout->Close();


}
