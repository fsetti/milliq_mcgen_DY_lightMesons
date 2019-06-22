{
  lastX = 40.;
  gStyle->SetOptStat(0);
  gROOT->ProcessLine(".L histio.cc");

  loadHist("ups1S_combined.root","u1s");
  loadHist("ups2S_combined.root","u2s");
  loadHist("ups3S_combined.root","u3s");

  TCanvas * c1s = new TCanvas();
  c1s->SetLogy();
  u1s_up->GetXaxis()->SetRangeUser(0.,lastX);
  u1s_central->SetLineStyle(2);
  u1s_up->SetTitle("Upsilon 1S");
  u1s_up->Draw();
  u1s_down->Draw("SAME");
  u1s_central->Draw("SAME");

  TCanvas * c2s = new TCanvas();
  c2s->SetLogy();
  u2s_up->GetXaxis()->SetRangeUser(0.,lastX);
  u2s_central->SetLineStyle(2);
  u2s_up->SetTitle("Upsilon 2S");
  u2s_up->Draw();
  u2s_down->Draw("SAME");
  u2s_central->Draw("SAME");

  TCanvas * c3s = new TCanvas();
  c3s->SetLogy();
  u3s_up->GetXaxis()->SetRangeUser(0.,lastX);
  u3s_central->SetLineStyle(2);
  u3s_up->SetTitle("Upsilon 3S");
  u3s_up->Draw();
  u3s_down->Draw("SAME");
  u3s_central->Draw("SAME");

  

}

  
