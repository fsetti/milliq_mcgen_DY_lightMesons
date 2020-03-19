#include "TMath.h"
#include "TH1D.h"
#include "TLorentzVector.h"
#include "NtupleHandler.h"
#include "fstream"


const float minEta = 2;

void makeTree( TString infile_str, TString outfile_str ){

	TFile *outfile = new TFile(("../trees/"+outfile_str).Data(),"RECREATE");
	outfile->cd();
	
	TH1D *h_phi_pT;
	h_phi_pT = new TH1D("h_phi_pT","#phi pT", 2000,0,100);

	TTree *t = new TTree("t","Pythia6 output");
	InitializeTree(t);


	FILE *infile;
	infile = fopen( "../rawFiles/" + infile_str, "r" );
	if (!infile) {
		cerr << "Could not open fill file.\n";
	}

	int in_evt, in_pID;
	float in_px, in_py, in_pz, in_E, in_pT, in_m;
	while( fscanf(infile, "%i %i %f %f %f %f %f", &in_evt, &in_pID, &in_px, &in_py, &in_pz, &in_E, &in_m ) && in_evt > 0 ){
		evt = in_evt ;
		pID = in_pID ;

		px  = in_px  ;
		py  = in_py  ;
		pz  = in_pz  ;
		E   = in_E   ;
		m   = in_m   ;

		TLorentzVector lorVec;
		lorVec.SetPxPyPzE(px,py,pz,E);

		pT  = lorVec.Pt() ;
		eta = lorVec.Eta();
		y   = lorVec.Rapidity();
		phi = lorVec.Phi();

		if ( fabs( eta ) > minEta ) continue;	// impose eta < 2 cut

		t->Fill();
		if ( pID == 333 ) h_phi_pT->Fill( pT );
	}
	fclose(infile);
	if ( in_evt < 0 ) nEvts = -in_evt;
	t->Fill();

	h_phi_pT->Scale(1./((float)nEvts));

	outfile->cd();
	t->Write();
	h_phi_pT->Write();
	outfile->Write();
}




void makeTree_ch( TString infile_str, TString outfile_str ){

	TFile *outfile = new TFile(("../trees/"+outfile_str).Data(),"RECREATE");
	outfile->cd();
	
	TH1D *h_phi_pT;
	h_phi_pT = new TH1D("h_phi_pT","#phi pT", 2000,0,100);

	TTree *t = new TTree("t","Pythia6 output");
	InitializeTree(t);


	FILE *infile[10];
	for ( int i=0; i<10; i++){
		infile[i] = fopen( "../rawFiles/" + infile_str + "_" + std::to_string(i+1) + ".txt", "r" );
	}

	int totNevents = 0;
	for ( unsigned int i=0; i<10; i++){
		int in_evt, in_pID;
		float in_px, in_py, in_pz, in_E, in_pT, in_m;
		while( fscanf(infile[i], "%i %i %f %f %f %f %f", &in_evt, &in_pID, &in_px, &in_py, &in_pz, &in_E, &in_m ) && in_evt > 0 ){
			evt = in_evt ;
			pID = in_pID ;

			px  = in_px  ;
			py  = in_py  ;
			pz  = in_pz  ;
			E   = in_E   ;
			m   = in_m   ;

			TLorentzVector lorVec;
			lorVec.SetPxPyPzE(px,py,pz,E);

			pT  = lorVec.Pt() ;
			eta = lorVec.Eta();
			y   = lorVec.Rapidity();
			phi = lorVec.Phi();

			if ( fabs( eta ) > minEta ) continue;	// impose eta < 2 cut

			t->Fill();
			if ( pID == 333 ) h_phi_pT->Fill( pT );
		}
		fclose(infile[i]);
		if ( in_evt < 0 ) totNevents = totNevents - in_evt;
	}
	nEvts = totNevents;
	t->Fill();

	h_phi_pT->Scale(1./((float)nEvts));

	outfile->cd();
	t->Write();
	h_phi_pT->Write();
	outfile->Write();
}




void makeTree_val( TString infile_str, TString outfile_str ){

	TFile *outfile = new TFile(("../trees/"+outfile_str).Data(),"RECREATE");
	outfile->cd();
	
	TH1D *h_phi_pT;
	h_phi_pT = new TH1D("h_phi_pT","#phi pT", 10,0.5,1.2);

	TTree *t = new TTree("t","Pythia6 output");
	InitializeTree(t);


	FILE *infile[10];
	for ( int i=0; i<10; i++){
		infile[i] = fopen( "../rawFiles/" + infile_str + "_" + std::to_string(i+1) + ".txt", "r" );
	}
//	if (!infile) {
//		cerr << "Could not open fill file.\n";
//	}

	int totNevents = 0;
	for ( unsigned int i=0; i<10; i++){
		int in_evt, in_pID;
		float in_px, in_py, in_pz, in_E, in_pT, in_m;
		while( fscanf(infile[i], "%i %i %f %f %f %f %f", &in_evt, &in_pID, &in_px, &in_py, &in_pz, &in_E, &in_m ) && in_evt > 0 ){
			evt = in_evt ;
			pID = in_pID ;

			px  = in_px  ;
			py  = in_py  ;
			pz  = in_pz  ;
			E   = in_E   ;
			m   = in_m   ;

			TLorentzVector lorVec;
			lorVec.SetPxPyPzE(px,py,pz,E);

			pT  = lorVec.Pt() ;
			eta = lorVec.Eta();
			y   = lorVec.Rapidity();
			phi = lorVec.Phi();

//			if ( fabs( eta ) > minEta ) continue;	// impose eta < 2 cut

			t->Fill();
			if ( pID == 333  && fabs(y) < 0.8 && pT > 0.5 && TMath::Sqrt(px*px+py*py+pz*pz) < 1.2 ) h_phi_pT->Fill( pT );
		}
		fclose(infile[i]);
		if ( in_evt < 0 ) totNevents = totNevents - in_evt;
	}
	nEvts = totNevents;
	t->Fill();

	h_phi_pT->Scale(1./((float)nEvts));

	outfile->cd();
	t->Write();
	h_phi_pT->Write();
	outfile->Write();
}

