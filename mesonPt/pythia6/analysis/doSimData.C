{
  gROOT->ProcessLine(".L plot.C+");

  TString BennetFile =  "/home/users/bemarsh/analysis/milliqan/milliq_mcgen/mesonPt/hadded/fromPythia_v2_with_mus/minbias.root";

  TString myFile =  "/home/users/fsetti/Pythia/pythia6/trees/minBiasDW.root";
  TString outName = "/home/users/fsetti/public_html/Pythia/091219/Py6-DW_Py8-CUEPT8_noDiff";

  ratioHists ( myFile, "h_phi_pT", BennetFile, "h_phi", outName );

//  myFile =  "/home/users/fsetti/Pythia/pythia6/trees/mQ_minBias_sdDiff.root";
//  outName = "/home/users/fsetti/public_html/Pythia/021219/Py6-DW_Py8-CUEPT8_sdDiff";
//
//  ratioHists ( myFile, "h_phi_pT", BennetFile, "h_phi", outName );
}
