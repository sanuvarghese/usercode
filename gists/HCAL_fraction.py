import ROOT
import sys

# Load CMSSW libraries
ROOT.gROOT.SetBatch(True)
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.gSystem.Load("libDataFormatsFWLite.so")
ROOT.FWLiteEnabler.enable()

from DataFormats.FWLite import Handle, Events

# Setup handles
pfCandidates, pfLabel = Handle("std::vector<pat::PackedCandidate>"), "packedPFCandidates"
triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults", "", "HLT")
triggerNames, triggerNamesLabel = Handle("edm::TriggerNames"), ("TriggerResults", "", "HLT")

# Histograms
hist = ROOT.TH2F("hcalFracVsPt", "HCAL fraction vs Charged Hadron p_{T};Charged Hadron p_{T} [GeV];HCAL Fraction", 50, 0, 200, 50, 0, 1)
profile = ROOT.TProfile("hcalFracProfile", "Mean HCAL Fraction vs Charged Hadron p_{T};Charged Hadron p_{T} [GeV];Mean HCAL Fraction", 50, 0, 200)

# Input files
file_list = [
    '/eos/cms/store/group/tsg/STEAM/savarghe/ChargedHadronCheck/0d14047f-77fc-4874-bfb2-1d05f0429bd5.root',
    '/eos/cms/store/group/tsg/STEAM/savarghe/ChargedHadronCheck/0ead09ba-816f-4cad-82bc-3337bd844aee.root',
    '/eos/cms/store/group/tsg/STEAM/savarghe/ChargedHadronCheck/13ac43bb-4352-436b-8781-46e7bb86d0ab.root',
    '/eos/cms/store/group/tsg/STEAM/savarghe/ChargedHadronCheck/1869c60b-cc0c-42b7-9080-739da552f6ab.root',
    '/eos/cms/store/group/tsg/STEAM/savarghe/ChargedHadronCheck/199d382d-83a3-4a06-bfa6-328d6dd537a7.root',
    '/eos/cms/store/group/tsg/STEAM/savarghe/ChargedHadronCheck/1a3e4467-ce49-49b6-9f31-4705c493f696.root',
    '/eos/cms/store/group/tsg/STEAM/savarghe/ChargedHadronCheck/2108a4d4-8b0d-4b43-99ec-3af5ae32b5d1.root',
    '/eos/cms/store/group/tsg/STEAM/savarghe/ChargedHadronCheck/21b22642-1699-4ea7-a9e0-7b91fba8daa5.root',
    '/eos/cms/store/group/tsg/STEAM/savarghe/ChargedHadronCheck/21b6a4d4-640f-4dd3-9f23-011db59d05ae.root',
    '/eos/cms/store/group/tsg/STEAM/savarghe/ChargedHadronCheck/2700c23f-ac78-460d-8b57-0bc79f6dd73e.root',
    '/eos/cms/store/group/tsg/STEAM/savarghe/ChargedHadronCheck/29be414d-39e3-4f34-8846-60fcc1526d10.root'
]

# Event loop
events = Events(file_list)
print("Starting event loop...")
evt_count = 0

for event in events:
    evt_count += 1
    if evt_count % 10000 == 0:
        print(f"Processing event #{evt_count}")

    event.getByLabel(triggerBitLabel, triggerBits)
    event.getByLabel(triggerNamesLabel, triggerNames)
    names = event.object().triggerNames(triggerBits.product())

    passedTrigger = False
    for i in range(triggerBits.product().size()):
        if "Photon45EB_TightID_TightIso" in names.triggerName(i) and triggerBits.product().accept(i):
            passedTrigger = True
            break
    if not passedTrigger:
        continue

    event.getByLabel(pfLabel, pfCandidates)

    for pfc in pfCandidates.product():
        if abs(pfc.pdgId()) not in [211]: continue
        if pfc.charge() == 0: continue
        if abs(pfc.eta()) > 1.3: continue
        pt = pfc.pt()
        if pt < 20: continue

        hcal_frac = pfc.hcalFraction()
        hist.Fill(pt, hcal_frac)
        profile.Fill(pt, hcal_frac)

print("Finished event loop. Generating plots...")

# Plot 2D
c1 = ROOT.TCanvas("c1", "HCAL Fraction 2D", 800, 600)
hist.Draw("COLZ")
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.035)
latex.DrawLatex(0.14, 0.86, "HLT_Photon45EB_TightID_TightIso")
latex.DrawLatex(0.14, 0.82, "PF Charged Hadrons: p_{T} > 20 GeV, |#eta| < 1.3")
c1.SaveAs("hcal_fraction_vs_pt.png")

# Plot profile
c2 = ROOT.TCanvas("c2", "HCAL Fraction Profile", 800, 600)
profile.SetLineColor(ROOT.kBlue+1)
profile.SetMarkerColor(ROOT.kBlue+1)
profile.SetMarkerStyle(20)
profile.Draw("E1")
latex.DrawLatex(0.14, 0.86, "HLT_Photon45EB_TightID_TightIso")
latex.DrawLatex(0.14, 0.82, "PF Charged Hadrons: p_{T} > 20 GeV, |#eta| < 1.3")
c2.SaveAs("hcal_fraction_profile_vs_pt.png")
print("Saved: hcal_fraction_vs_pt.png and hcal_fraction_profile_vs_pt.png")
