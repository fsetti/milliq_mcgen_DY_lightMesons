#include "NtupleHandler.h"


void selection( TTree *chain, TString output_filename ) 
{
  double weight = 1./100000;


  TFile *outFile = new TFile(output_filename.Data(),"RECREATE");
  outFile->cd();

  TH1::SetDefaultSumw2();
  TH1D *h_pT;
  h_pT = new TH1D("pT","phi pT ", 32,0,32);


  InitializeChain(chain);

  //Number of events to loop over
  Int_t nentries = (Int_t)chain->GetEntries();


/////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////
//	Main Event Loop 
  for(int ia = 0; ia<nentries; ia++){

    chain->GetEntry(ia);

    bool synchBoards = false;                   // only consider events with synched boards
    if ((event_trigger_time_tag_b1==event_trigger_time_tag_b0) || (groupTDC_b1->at(0) == groupTDC_b0->at(0))) synchBoards = true;
    if ( (!synchBoards  && Data) || ( !beam && Data ) ) continue;



    vector<vector<float>> slabPulses;
    slabPulses = SlabSelection( chan,height,ptime,nPE,time_module_calibrated );
    if ( slabPulses.size() == 0 ) continue;
    std::sort(slabPulses.begin(), slabPulses.end(), sort_wrt_channel);
    float dt_cal = slabPulses.at(2)[4] - slabPulses.at(0)[4];
    if ( fabs( dt_cal ) > maxSlabdT ) continue;	// require dt_cal between -12 and +12 ns from dt_cal distribution

   
/////////////////////////////////////////////////////////////////////////////
//	Muon Selection - hits in straight line 

    vector<vector<float>> nonNeighPulses, neighPulses;
    nonNeighPulses = NonNeighBarSelection ( chan,height,ptime,nPE,time_module_calibrated, trigBars);
    neighPulses = NeighBarSelection ( chan,height,ptime,nPE,time_module_calibrated, trigBars);

/////////////////////////////////////////////////////////////////////////////
//	Organise the plotting  

    if ( Data ) {
	for ( unsigned int i=0; i<nonNeighPulses.size(); i++){
		h_nNnPE->Fill ( nonNeighPulses.at(i).at(3) );
		if ( nonNeighPulses.at(i).at(3) < 20 ) nNchanHits[(int)nonNeighPulses.at(i).at(0)]+=1;
	}
	//	repeat for neighbouring channels
	for ( unsigned int i=0; i<neighPulses.size(); i++){
		h_NnPE->Fill ( neighPulses.at(i).at(3) );
		if ( neighPulses.at(i).at(3) < 20 ) NchanHits[(int)neighPulses.at(i).at(0)]+=1;
    	}
    }


    if ( !Data ) {
        currentFile = chain->GetFile();
        currentFileName = currentFile->GetName();
        if ( currentFileName == "/nfs-7/userdata/fsetti/sim_run3_qcd.root" ) weight = weight_qcd;
        if ( currentFileName == "/nfs-7/userdata/fsetti/sim_run3_qcd_nonbc.root" ) weight = weight_qcd_nonbc;
        if ( currentFileName == "/nfs-7/userdata/fsetti/sim_run3_dy.root" ) weight = weight_DY;
        if ( currentFileName == "/nfs-7/userdata/fsetti/sim_run3_w.root" ) weight = weight_W;

	for ( unsigned int i=0; i<nonNeighPulses.size(); i++){
		h_nNnPE->Fill ( nonNeighPulses.at(i).at(3) , weight );
		if ( nonNeighPulses.at(i).at(3) < 20 ) nNchanHits[(int)nonNeighPulses.at(i).at(0)]+=weight;
	}	
	
	//	repeat for neighbouring channels
	for ( unsigned int i=0; i<neighPulses.size(); i++){
		h_NnPE->Fill ( neighPulses.at(i).at(3) , weight );
		if ( neighPulses.at(i).at(3) < 20 ) NchanHits[(int)neighPulses.at(i).at(0)]+=weight;
	}
    }

//	end of main loop
  }
  for ( unsigned int i=0; i<nChannels; i++){
	h_chN->SetBinContent( i+1, NchanHits[i] );
	h_chnN->SetBinContent( i+1, nNchanHits[i] );
  }

  outFile->cd();

  h_NnPE->Write();
  h_nNnPE->Write();

  h_chN->Write();
  h_chnN->Write();

  outFile->Write();
  outFile->Close();

}
