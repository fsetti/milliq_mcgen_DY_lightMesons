{
  gStyle->SetOptStat(0);
  
  gROOT->ProcessLine(".L histio.cc");

  loadHist("../CMS_13_TeV/data/ups1S.root", "cms_1S");
  loadHist("../Atlas_7_TeV/Atlas_1S.root", "atl_1S");

  TCanvas * c1S = new TCanvas();
  c1S->SetLogy();
    
  atl_1S_up->GetXaxis()->SetRangeUser(15.,30.);
  atl_1S_up->SetLineColor(2);
  atl_1S_down->SetLineColor(2);
  atl_1S_central->SetLineColor(2);
  atl_1S_central->SetLineStyle(2);
  cms_1S_central->SetLineStyle(2);
  atl_1S_up->SetTitle("Upsilon 1S");
  
  atl_1S_up->Draw();
  atl_1S_down->Draw("SAME");
  atl_1S_central->Draw("SAME");
  cms_1S_up->Draw("SAME");
  cms_1S_down->Draw("SAME");
  cms_1S_central->Draw("SAME");



  loadHist("../CMS_13_TeV/data/ups2S.root", "cms_2S");
  loadHist("../Atlas_7_TeV/Atlas_2S.root", "atl_2S");

  TCanvas * c2S = new TCanvas();
  c2S->SetLogy();
    
  atl_2S_up->GetXaxis()->SetRangeUser(15.,30.);
  atl_2S_up->SetLineColor(2);
  atl_2S_down->SetLineColor(2);
  atl_2S_central->SetLineColor(2);
  atl_2S_central->SetLineStyle(2);
  cms_2S_central->SetLineStyle(2);
  atl_2S_up->SetTitle("Upsilon 2S");
  
  atl_2S_up->Draw();
  atl_2S_down->Draw("SAME");
  atl_2S_central->Draw("SAME");
  cms_2S_up->Draw("SAME");
  cms_2S_down->Draw("SAME");
  cms_2S_central->Draw("SAME");


  loadHist("../CMS_13_TeV/data/ups3S.root", "cms_3S");
  loadHist("../Atlas_7_TeV/Atlas_3S.root", "atl_3S");

  TCanvas * c3S = new TCanvas();
  c3S->SetLogy();
    
  atl_3S_up->GetXaxis()->SetRangeUser(15.,30.);
  atl_3S_up->SetLineColor(2);
  atl_3S_down->SetLineColor(2);
  atl_3S_central->SetLineColor(2);
  atl_3S_central->SetLineStyle(2);
  cms_3S_central->SetLineStyle(2);
  atl_3S_up->SetTitle("Upsilon 3S");
  
  atl_3S_up->Draw();
  atl_3S_down->Draw("SAME");
  atl_3S_central->Draw("SAME");
  cms_3S_up->Draw("SAME");
  cms_3S_down->Draw("SAME");
  cms_3S_central->Draw("SAME");
  
  
}
