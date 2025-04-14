# to apply further prescales on L1Skim and obtain re-skimmed raw files. based on Andrea's code

import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3

process = cms.Process("HLT3")


# Options                                                                                                                                    
nEvents= 10000           # number of events to process                                                                                          
outputName="L1_New.root"  # output file name                                                                                                     
                                                                                           
#from list_cff_Skim import inputFileNames
# process.source = cms.Source("PoolSource",
#     fileNames = cms.untracked.vstring(inputFileNames),
#    # lumisToProcess = cms.untracked.VLuminosityBlockRange("362439:35-362439:220"),
#     inputCommands = cms.untracked.vstring('keep *')
# )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
     '/store/data/Run2024G/HLTPhysics/RAW/v1/000/384/492/00000/57c69846-8f85-4456-8173-5f00bcf70c61.root',
    '/store/data/Run2024G/HLTPhysics/RAW/v1/000/384/492/00000/76432fb5-7bcf-493a-a247-1181ea768bf9.root',
    '/store/data/Run2024G/HLTPhysics/RAW/v1/000/384/492/00000/0898a119-41d3-43aa-a843-ece7869c1eb6.root',
    '/store/data/Run2024G/HLTPhysics/RAW/v1/000/384/492/00000/8e608f7a-e643-4f2e-b95e-f639596fb85b.root',
    '/store/data/Run2024G/HLTPhysics/RAW/v1/000/384/492/00000/9516e14a-2969-4875-a159-a9c228bcf490.root',

    ),
    inputCommands = cms.untracked.vstring('keep *')
)


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( nEvents )
)


from EventFilter.L1TRawToDigi.l1tRawToDigi_cfi import l1tRawToDigi as _l1tRawToDigi
process.l1tRawToDigi = _l1tRawToDigi.clone(
    FedIds = [ 1404 ],
    Setup = 'stage2::GTSetup',
    InputLabel = "rawDataCollector"
)
process.triggerTypePhysics = cms.EDFilter("HLTTriggerTypeFilter",
    SelectedTriggerType = cms.int32(1)
)

from L1Trigger.L1TGlobal.l1tGlobalPrescaler_cfi import l1tGlobalPrescaler as _l1tGlobalPrescaler
process.l1tGlobalPrescaler = _l1tGlobalPrescaler.clone(
    l1tResults = 'l1tRawToDigi',                                                                                                     
)

process.l1tGlobalPrescaler.l1tPrescales[24] = 0
process.l1tGlobalPrescaler.l1tPrescales[214] = 2
# process.l1tGlobalPrescaler.l1tPrescales[274] = 0        # apply the prescales you want. Index corresponds to the bit used in the L1 Skim.
# process.l1tGlobalPrescaler.l1tPrescales[275] = 0
# process.l1tGlobalPrescaler.l1tPrescales[276] = 0        
# process.l1tGlobalPrescaler.l1tPrescales[277] = 0
# process.l1tGlobalPrescaler.l1tPrescales[78] = 0
# process.l1tGlobalPrescaler.l1tPrescales[64] = 0

process.Skim = cms.Path(process.triggerTypePhysics+process.l1tRawToDigi + process.l1tGlobalPrescaler)

process.hltOutputTriggerResults = cms.OutputModule( "PoolOutputModule",
        fileName = cms.untracked.string(outputName),
            SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring("Skim")
        ),
        outputCommands = cms.untracked.vstring("drop *",
                                               "keep edmTriggerResults_*_*_HLT",)
                                                  )


process.l1filteroutput = cms.EndPath(process.hltOutputTriggerResults)

process.schedule = cms.Schedule(process.Skim,process.l1filteroutput)





