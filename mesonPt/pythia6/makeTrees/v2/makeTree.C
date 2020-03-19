#include "TMath.h"
#include "TLorentzVector.h"
#include "NtupleHandler.h"
#include "fstream"


const float minEta = 2;

void makeTree( TString infile_str, TString outfile_str ){

        TFile *outfile = new TFile(("../../trees/"+outfile_str).Data(),"RECREATE");
        outfile->cd(); 
        
        TTree *t = new TTree("t","Pythia6 output");
        InitializeTree(t);
        

        FILE *infile;
        infile = fopen( "../../scripts/" + infile_str, "r" );
        if (!infile) {
                cerr << "Could not open fill file.\n";
        }       
        
        int in_evt = 1;
        int in_pID;
        float in_px, in_py, in_pz, in_E, in_pT, in_m;
        while( fscanf(infile, "%i %i %f %f %f %f %f", &in_evt, &in_pID, &in_px, &in_py, &in_pz, &in_E, &in_m ) && in_evt != -1 ){
                if ( evt != in_evt ){
//                        t->Fill(); 
//                        ClearBranches();
                }       
                evt = in_evt ;
                
                TLorentzVector lorVec;
                lorVec.SetPxPyPzE(in_px,in_py,in_pz,in_E);
                if ( fabs( lorVec.Eta() ) > minEta ) continue;  // impose eta < 2 cut
                pID->push_back(in_pID ); 
                
                px->push_back(in_px );
                py->push_back(in_py );
                pz->push_back(in_pz );
                E->push_back( in_E  );
                m->push_back( in_m  );
                phi->push_back(lorVec.Phi());
                
                pT->push_back(lorVec.Pt()) ;
                eta->push_back(lorVec.Eta());
        }       
        fclose(infile);
        
        outfile->cd();
        t->Write();
        outfile->Write();
}       

