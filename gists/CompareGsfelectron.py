import ROOT
from DataFormats.FWLite import Events, Handle
 

input_file = 'file:/eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3124/sanu/multiarch.root' # change to pre3.root for pre3.

electron_handle = Handle('std::vector<reco::Electron>')
electron_label = ('hltEgammaGsfElectrons', '', 'HLTX')

events = Events(input_file)

# Loop over events
for i, event in enumerate(events):
    print(f"Event {i}")

    # Get the electrons from the event
    event.getByLabel(electron_label, electron_handle)
    electrons = electron_handle.product()

    if not electrons:
        print("No GsfElectrons found in this event")
        continue

    # Loop over the electrons
    for electron in electrons:
        E = electron.superCluster().energy() # Energy from the superCluster
        p = electron.gsfTrack().p() # Momentum from the gsfTrack
        eta = electron.gsfTrack().eta()
        phi = electron.gsfTrack().phi()
        oneOverE_minus_oneOverP = (1.0/E) - (1.0/p) if E > 0 and p > 0 else None

        print(f"Electron: E={E}, p={p} , eta ={eta}, phi={phi}, 1/E - 1/p={oneOverE_minus_oneOverP}")