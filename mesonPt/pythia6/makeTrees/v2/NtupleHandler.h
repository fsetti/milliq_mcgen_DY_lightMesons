#include <iostream>
#include <TROOT.h>
#include <TTree.h>
#include <TFile.h>

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   int	   evt ;
   vector<int  >   *pID ;
   vector<float>   *px  ;
   vector<float>   *py  ;
   vector<float>   *pz  ;
   vector<float>   *E   ;
   vector<float>   *pT  ;
   vector<float>   *m   ;
   vector<float>   *eta ;
   vector<float>   *phi ;
   

void InitializeTree(TTree *fTree)
{
   fTree->Branch("evt" , &evt , "evt/I" );
   fTree->Branch("pID" , &pID , "pID/I" );
   fTree->Branch("px"  , &px  , "px/F"  );
   fTree->Branch("py"  , &py  , "py/F"  );
   fTree->Branch("pz"  , &pz  , "pz/F"  );
   fTree->Branch("E"   , &E   , "E/F"   );
   fTree->Branch("pT"  , &pT  , "pT/F"  );
   fTree->Branch("m"   , &m   , "m/F"   );
   fTree->Branch("eta" , &eta , "eta/F" );
   fTree->Branch("phi" , &phi , "phi/F" );
}

void ClearBranches()
{
   pID->clear();
   px->clear();
   py->clear();
   pz->clear();
   E->clear();
   pT->clear();
   m->clear();
   eta->clear();
   phi->clear();
}
