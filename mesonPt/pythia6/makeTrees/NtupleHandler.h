#include <iostream>
#include <TROOT.h>
#include <TTree.h>
#include <TFile.h>

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   int	   nEvts;
   int	   evt  ;
   int     pID  ;
   float   px   ;
   float   py   ;
   float   pz   ;
   float   E    ;
   float   pT   ;
   float   m    ;
   float   eta  ;
   float   y    ;
   float   phi  ;
   

void InitializeTree(TTree *fTree)
{
   fTree->Branch("nEvts", &nEvts , "nEvts/I" );
   fTree->Branch("evt"  , &evt   , "evt/I" );
   fTree->Branch("pID"  , &pID   , "pID/I" );
   fTree->Branch("px"   , &px    , "px/F"  );
   fTree->Branch("py"   , &py    , "py/F"  );
   fTree->Branch("pz"   , &pz    , "pz/F"  );
   fTree->Branch("E"    , &E     , "E/F"   );
   fTree->Branch("pT"   , &pT    , "pT/F"  );
   fTree->Branch("m"    , &m     , "m/F"   );
   fTree->Branch("eta"  , &eta   , "eta/F" );
   fTree->Branch("y"    , &y     , "y/F"   );
   fTree->Branch("phi"  , &phi   , "phi/F" );
}
