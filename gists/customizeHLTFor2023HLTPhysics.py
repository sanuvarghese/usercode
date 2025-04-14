import FWCore.ParameterSet.Config as cms
from HLTrigger.Configuration.common import filters_by_type

def customizePrescaleSeeds(process):
    # Updated seed replacements dictionary with the new mappings and their reverses
    seed_replacements = {
         #disable new L1 seeds by renaming to a disabled seed.
        'L1_DoubleMu0_Upt6_SQ_er2p0': 'L1_SingleMuCosmics',
        'L1_DoubleMu0_Upt7_SQ_er2p0': 'L1_SingleMuCosmics',
        'L1_DoubleMu0_Upt8_SQ_er2p0': 'L1_SingleMuCosmics',
        'L1_DoubleMu6_Upt6_SQ_er2p0': 'L1_SingleMuCosmics',
        'L1_DoubleMu7_Upt7_SQ_er2p0': 'L1_SingleMuCosmics',
        'L1_DoubleMu8_Upt8_SQ_er2p0': 'L1_SingleMuCosmics',
        'L1_Mu12_HTT150er': 'L1_SingleMuCosmics',
        'L1_Mu14_HTT150er': 'L1_SingleMuCosmics',
        'L1_LooseIsoEG14er2p5_HTT200er': 'L1_SingleMuCosmics',
        'L1_LooseIsoEG16er2p5_HTT200er': 'L1_SingleMuCosmics',
        'L1_AXO_VLoose': 'L1_SingleMuCosmics',
        'L1_AXO_Loose': 'L1_SingleMuCosmics',
        'L1_AXO_Nominal': 'L1_SingleMuCosmics',
        'L1_AXO_Tight': 'L1_SingleMuCosmics',
        'L1_AXO_VTight': 'L1_SingleMuCosmics',
        'L1_SingleMu10_SQ14_BMTF': 'L1_SingleMuCosmics',
        'L1_SingleMu11_SQ14_BMTF': 'L1_SingleMuCosmics',
        'L1_DoubleMu0er2p0_SQ_OS_dEta_Max0p3_dPhi_0p8to1p2': 'L1_SingleMuCosmics',
        # Reverse VBF seed changes
        'L1_DoubleJet45_Mass_Min600_IsoTau45er2p1_RmOvlp_dR0p5': 'L1_DoubleJet45_Mass_Min450_IsoTau45er2p1_RmOvlp_dR0p5',
        'L1_DoubleJet45_Mass_Min550_IsoTau45er2p1_RmOvlp_dR0p5': 'L1_DoubleJet45_Mass_Min450_IsoTau45er2p1_RmOvlp_dR0p5',
        'L1_DoubleJet_65_35_DoubleJet35_Mass_Min650_DoubleJetCentral50': 'L1_DoubleJet_65_35_DoubleJet35_Mass_Min500_DoubleJetCentral50',
        'L1_DoubleJet_65_35_DoubleJet35_Mass_Min600_DoubleJetCentral50': 'L1_DoubleJet_65_35_DoubleJet35_Mass_Min500_DoubleJetCentral50',
        'L1_DoubleJet45_Mass_Min600_LooseIsoEG20er2p1_RmOvlp_dR0p2': 'L1_DoubleJet45_Mass_Min450_LooseIsoEG20er2p1_RmOvlp_dR0p2',
        'L1_DoubleJet45_Mass_Min550_LooseIsoEG20er2p1_RmOvlp_dR0p2': 'L1_DoubleJet45_Mass_Min450_LooseIsoEG20er2p1_RmOvlp_dR0p2',
        'L1_DoubleJet_85_35_DoubleJet35_Mass_Min600_Mu3OQ': 'L1_DoubleJet_85_35_DoubleJet35_Mass_Min500_Mu3OQ',
        'L1_DoubleJet_85_35_DoubleJet35_Mass_Min650_Mu3OQ': 'L1_DoubleJet_85_35_DoubleJet35_Mass_Min500_Mu3OQ',
        'L1_DoubleJet_70_35_DoubleJet35_Mass_Min550_ETMHF65': 'L1_DoubleJet_70_35_DoubleJet35_Mass_Min400_ETMHF65',
        'L1_DoubleJet_70_35_DoubleJet35_Mass_Min500_ETMHF65': 'L1_DoubleJet_70_35_DoubleJet35_Mass_Min400_ETMHF65',
        'L1_DoubleJet_110_35_DoubleJet35_Mass_Min800': 'L1_DoubleJet_110_35_DoubleJet35_Mass_Min620',
        'L1_DoubleJet_100_30_DoubleJet30_Mass_Min800': 'L1_DoubleJet_100_30_DoubleJet30_Mass_Min620',
        'L1_DoubleJet_110_35_DoubleJet35_Mass_Min850' : 'L1_DoubleJet_100_30_DoubleJet30_Mass_Min620',
        'L1_DoubleJet_100_30_DoubleJet30_Mass_Min950': 'L1_DoubleJet_100_30_DoubleJet30_Mass_Min620',
        'L1_DoubleJet_120_45_DoubleJet45_Mass_Min620': 'L1_DoubleJet_115_40_DoubleJet40_Mass_Min620',
    }

    for module in filters_by_type(process, 'HLTL1TSeed'):
        l1Seed = module.L1SeedsLogicalExpression.value()
        if any(old_seed in l1Seed for old_seed in seed_replacements):
            # Replace each old seed with the new seed
            for old_seed, new_seed in seed_replacements.items():
                l1Seed = l1Seed.replace(old_seed, new_seed)
            module.L1SeedsLogicalExpression = cms.string(l1Seed)

    return process
