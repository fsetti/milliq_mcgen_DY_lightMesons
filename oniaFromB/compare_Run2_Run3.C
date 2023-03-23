{

  // Set this to false if you want to do psiprime
  bool psi;

  // Ask the user: psi or psiprime?
  // Apparently "return" does not work on unnamed macros, so
  // if we have a problem we set goodFlag=false and wrap
  // everything around an "if (goodFlag)" statement
  int flag;
  bool goodFlag = true;
  std::cout << "Enter 1 for psi, 2 for psiprime" << std::endl;
  std::cin >> flag;
  if (flag==1) {
    std::cout << "We will do the psi" << std::endl;
    psi = true;
  } else if (flag==2) {
    std::cout << "We will do the psiprime" << std::endl;
    psi = false;
  } else {
    std::cout << "Illegal entry" << std::endl;
    goodFlag = false;
  }
     
  // No stat box please
  gStyle->SetOptStat(0);
  // gStyle->SetOptTitle(0);


  if (goodFlag) {
  
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
    TH1D* cenRatio = new TH1D(*r2_central);
    cenRatio->Divide(r2_central);
    TH1D* upRatio = new TH1D(*r2_up);
    upRatio->Divide(r2_central);
    TH1D* downRatio = new TH1D(*r2_down);
    downRatio->Divide(r2_central);

  
    TH1D* new_cenRatio = new TH1D(*r3_central);
    new_cenRatio->Divide(r2_central);
    TH1D* new_upRatio = new TH1D(*r3_up);
    new_upRatio->Divide(r2_central);
    TH1D* new_downRatio = new TH1D(*r3_down);
    new_downRatio->Divide(r2_central);

  // Set colors, style, titles, naximum
    cenRatio->SetLineColor(kBlue);
    upRatio->SetLineColor(kBlue);
    downRatio->SetLineColor(kBlue);
    new_cenRatio->SetLineColor(kRed);
    new_upRatio->SetLineColor(kRed);
    new_downRatio->SetLineColor(kRed);
  
    upRatio->SetLineStyle(10);
    downRatio->SetLineStyle(10);
    new_upRatio->SetLineStyle(10);
    new_downRatio->SetLineStyle(10);

    upRatio->SetMaximum(2.);
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
    new_upRatio->Draw("HISTSAME");
    new_downRatio->Draw("HISTSAME");
    new_cenRatio->Draw("HISTSAME");

    // save to pdf
    if (psi) {
      c1->SaveAs("psi_fromB_Run2_Run3_comparison.pdf");
    } else {
      c1->SaveAs("psiprime_fromB_Run2_Run3_comparison.pdf");
    }
  }
}
