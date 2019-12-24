{
  gROOT->ProcessLine(".L makeTree.C+");

  TString infile, outfile;
  infile  = "minBiasDW" ;
  outfile = "minBiasDW.root";

  cout << "-------------------------" << endl;
  makeTree_ch( infile , outfile );
  cout << "-------------------------" << endl;
  cout << "\n \n \n " << endl;

  infile  = "minBiasDW_Diff" ;
  outfile = "minBiasDW_Diff.root";

  cout << "-------------------------" << endl;
  makeTree_ch( infile , outfile );
  cout << "-------------------------" << endl;
  cout << "\n \n \n " << endl;
}
