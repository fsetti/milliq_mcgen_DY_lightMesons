{

  // Set this to false if you want to do psiprime
  bool psi = false;
  
  // No stat box please
  gStyle->SetOptStat(0);
  // gStyle->SetOptTitle(0);

  // Load Wouter's nice utility
  gROOT->ProcessLine(".L ../oniaDirect/upsilon/histio.cc");

  // Psi or Psiprime histograms with a r2/r3 superscript
  if (psi) {
    loadHist("run2/psi.root","r2");
    loadHist("run3/psi.root","r3");
  } else {
    loadHist("run2/psiprime.root","r2");
    loadHist("run3/psiprime.root","r3");
  }
    
  // A canvas with a grid
  TCanvas* c1 = new TCanvas();
  c1->SetGrid();

  // Take ratios to the run 2 central value
  TH1D* upRatio = new TH1D(*r2_up);
  upRatio->Divide(r2_central);
  TH1D* downRatio = new TH1D(*r2_down);
  downRatio->Divide(r2_central);
  TH1D* cenRatio = new TH1D(*r3_central);
  cenRatio->Divide(r2_central);

  // Set colors, style, titles 
  cenRatio->SetLineColor(kRed);
  upRatio->SetLineColor(kBlue);
  downRatio->SetLineColor(kBlue);
  upRatio->SetLineStyle(10);
  downRatio->SetLineStyle(10);
  upRatio->GetXaxis()->SetTitle("Pt (GeV/c)");
  if (psi) {
    upRatio->SetTitle("Psi");
  } else {
    upRatio->SetTitle("Psiprime");
  }

  // Plot them 
  upRatio->Draw("HIST");
  downRatio->Draw("HISTSAME");
  cenRatio->Draw("HISTSAME");

  // save to pdf
  if (psi) {
    c1->SaveAs("psi_fromB_Run2_Run3_comparison.pdf");
  } else {
    c1->SaveAs("psiprime_fromB_Run2_Run3_comparison.pdf");
  }
}
