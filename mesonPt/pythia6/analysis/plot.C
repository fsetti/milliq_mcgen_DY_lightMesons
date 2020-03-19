#include <stdlib.h>
#include <iostream>
#include <string>
#include "TFile.h"
#include "TCanvas.h"
#include "TH1D.h"
#include "TProfile.h"
#include "THStack.h"
#include "TString.h"
#include "TStyle.h"
#include "TLegend.h"


void ratioHists(TString path1, TString h1Name, TString path2, TString h2Name, TString outPath ){


        TFile* file1 = TFile::Open(path1);
        TH1D *h1_Copy = (TH1D*)file1->Get(h1Name);
        TH1D *h1 = (TH1D*)h1_Copy->Clone(h1Name);
        h1->SetDirectory(0);
        file1->Close();

        TFile* file2 = TFile::Open(path2);
        TH1D *h2_Copy = (TH1D*)file2->Get(h2Name);
        TH1D *h2_Scale = (TH1D*)file2->Get("h_nevents");
        TH1D *h2 = (TH1D*)h2_Copy->Clone(h2Name);
        h2->SetDirectory(0);
	h2->Scale(1./h2_Scale->GetEntries());
        file2->Close();


        if ( h1->GetEntries() != 0 && h2->GetEntries() != 0 ){

		TCanvas *c = new TCanvas("c", "canvas", 800, 800);

		TPad *pad1 = new TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
		pad1->SetBottomMargin(0.1); // Upper and lower plot are joined
		pad1->SetLogy();         // Vertical grid
		pad1->SetGridx();         // Vertical grid
		pad1->SetGridy();         // Vertical grid
		pad1->Draw();             // Draw the upper pad: pad1
		pad1->cd();               // pad1 becomes the current pad
		h1->SetStats(0);          // No statistics on upper plot
		h2->SetStats(0);          // No statistics on upper plot
		h2->GetXaxis()->SetRangeUser(0.,10);
		if ( h2->GetMaximum() < h1->GetMaximum() ) h2->SetMaximum(2.1*h1->GetMaximum());
		h2->Draw();               // Draw h1
		h1->Draw("SAME");         // Draw h2 on top of h1
		h1->GetXaxis()->SetTitle("#phi p_{T}");
	        TLegend *legend = new TLegend(.75, .75, .95, .95);
                legend->AddEntry(h1, "Pythia6-DW");
                legend->AddEntry(h2, "Pythia8-CUETP");
                legend->Draw();

		h1->SetMarkerStyle(31);
		h2->SetMarkerStyle(31);
		h2->SetMarkerColor(2);

		c->cd();          // Go back to the main canvas before defining pad2
		TPad *pad2 = new TPad("pad2", "pad2", 0, 0.05, 1, 0.3);
		pad2->SetTopMargin(0.1);
		pad2->SetBottomMargin(0.2);
		pad2->SetGridy(); // vertical grid
		pad2->Draw();
		pad2->cd();       // pad2 becomes the current pad

		TH1D *h3 = (TH1D*)h1->Clone("h3");
		h3->SetLineColor(kBlack);
		h3->SetMinimum(0.1);  // Define Y ..
		h3->SetMaximum(2.); // .. range
//		h3->Sumw2();
		h3->SetStats(0);      // No statistics on lower plot
		h3->Divide(h2);
		h3->GetXaxis()->SetRangeUser(0.,10);
		h3->Draw("ep");       // Draw the ratio plot

		h3->SetMarkerStyle(8);

		h3->SetTitle(""); // Remove the ratio title
		h3->GetYaxis()->SetTitle("Py6-DW  /  Py8-CU ");
		h3->GetYaxis()->SetNdivisions(505);
		h3->GetYaxis()->SetTitleSize(20);
		h3->GetYaxis()->SetTitleFont(43);
		h3->GetYaxis()->SetTitleOffset(1.55);
		h3->GetYaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
		h3->GetYaxis()->SetLabelSize(15);

		h3->GetXaxis()->SetTitle("p_{T}");
		h3->GetXaxis()->SetTitleSize(20);
		h3->GetXaxis()->SetTitleFont(43);
		h3->GetXaxis()->SetTitleOffset(4.);
		h3->GetXaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
		h3->GetXaxis()->SetLabelSize(15);

		c->SaveAs(outPath+".png");

		c->Close();
        }

}




void ratioHists_v2 (TString path1, TString path2, TString h1Name, TString outPath ){


        TFile* file1 = TFile::Open(path1);
        TH1D *h1_Copy = (TH1D*)file1->Get(h1Name);
        TH1D *h1 = (TH1D*)h1_Copy->Clone(h1Name);
        h1->SetDirectory(0);
        file1->Close();

        TFile* file2 = TFile::Open(path2);
        TH1D *h2_Copy = (TH1D*)file2->Get(h1Name);
        TH1D *h2 = (TH1D*)h2_Copy->Clone(h1Name);
        h2->SetDirectory(0);
        file2->Close();

        if ( h1->GetEntries() != 0 && h2->GetEntries() != 0 ){

		TCanvas *c = new TCanvas("c", "canvas", 800, 800);
		gStyle->SetOptStat("ou");

		TPad *pad1 = new TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
		pad1->SetBottomMargin(0.1); // Upper and lower plot are joined
//		pad1->SetLogy();         // Vertical grid
		pad1->SetGridx();         // Vertical grid
		pad1->SetGridy();         // Vertical grid
		pad1->Draw();             // Draw the upper pad: pad1
		pad1->cd();               // pad1 becomes the current pad
		h1->SetStats(0);          // No statistics on upper plot
//		h1->SetMinimum(0.11);
		if ( h1->GetMaximum() < h2->GetMaximum() ) h1->SetMaximum(2.1*h2->GetMaximum());
		h1->Draw();               // Draw h1
		h2->Draw("HIST,SAME");         // Draw h2 on top of h1
		h1->GetXaxis()->SetTitle("chan #");
	        TLegend *legend = new TLegend(.75, .75, .95, .95);
                legend->AddEntry(h1, "Data");
                legend->AddEntry(h2, "MC");
                legend->Draw();

		c->cd();          // Go back to the main canvas before defining pad2
		TPad *pad2 = new TPad("pad2", "pad2", 0, 0.05, 1, 0.3);
		pad2->SetTopMargin(0.1);
		pad2->SetBottomMargin(0.2);
		pad2->SetGridy(); // vertical grid
		pad2->Draw();
		pad2->cd();       // pad2 becomes the current pad

		TH1D *h3 = (TH1D*)h1->Clone("h3");
		h3->SetMinimum(1);  // Define Y ..
		h3->SetMaximum(2); // .. range
//		h3->Sumw2();
		h3->SetStats(0);      // No statistics on lower plot
		h3->Divide(h2);
		h3->Draw("ep");       // Draw the ratio plot

//		h1->SetLineColor(kBlue+1);
//		h1->SetLineWidth(3);
		h1->SetMarkerStyle(19);
		h3->SetLineColor(kBlack);
		h3->SetMarkerStyle(19);


		h2->SetLineColor(kRed);
		h2->SetLineWidth(3);

		h3->SetTitle(""); // Remove the ratio title


		h3->GetYaxis()->SetTitle("Data/MC   ");
		h3->GetYaxis()->SetNdivisions(505);
		h3->GetYaxis()->SetTitleSize(20);
		h3->GetYaxis()->SetTitleFont(43);
		h3->GetYaxis()->SetTitleOffset(1.55);
		h3->GetYaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
		h3->GetYaxis()->SetLabelSize(15);

		h3->GetXaxis()->SetTitle("nPE");
		h3->GetXaxis()->SetTitleSize(20);
		h3->GetXaxis()->SetTitleFont(43);
		h3->GetXaxis()->SetTitleOffset(4.);
		h3->GetXaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
		h3->GetXaxis()->SetLabelSize(15);

		c->SaveAs(outPath+".png");

		c->Close();
        }

}

