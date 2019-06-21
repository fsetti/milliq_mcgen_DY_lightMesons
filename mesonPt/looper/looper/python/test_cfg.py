import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

### Datasets
# MinBias:  /MinBias_TuneCUETP8M1_13TeV-pythia8/RunIISummer16DR80-NoPU_80X_mcRun2_asymptotic_v14-v1/AODSIM
# QCD pT :  /QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRStdmix-94X_mc2017_realistic_v4-v1/AODSIM
#           /QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRStdmix-94X_mc2017_realistic_v4_ext1-v1/AODSIM
#           /QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRStdmix-NoPU_92X_upgrade2017_realistic_v10-v1/AODSIM

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        # 'file:/nfs-7/userdata/bemarsh/MinBias_TuneCUETP8M1_80x_AOD.root'
        '/store/mc/RunIISummer17DRStdmix/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/AODSIM/94X_mc2017_realistic_v4_ext1-v1/20000/7C576233-17BE-E711-A49E-008CFAE45344.root'
    )
)

process.demo = cms.EDAnalyzer('looper',
    genparts = cms.InputTag("genParticles"),  
)


process.p = cms.Path(process.demo)
