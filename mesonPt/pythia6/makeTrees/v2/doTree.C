{
  gROOT->ProcessLine(".L makeTree.C+");

  TString infile, outfile;
  infile = "mQ_minBiasDW_sDiff.txt";
  outfile = "mQ_minBiasDW_sDiff_v2.root";

  cout << "-------------------------" << endl;
  makeTree( infile , outfile );
  cout << "-------------------------" << endl;
  cout << "\n \n \n " << endl;

}
