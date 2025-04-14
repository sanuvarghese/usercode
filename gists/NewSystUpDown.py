import ROOT
import os
import fnmatch

# Function to calculate and transform the up/down histograms to be symmetrical
def transform_histograms_symmetric(hCentral, hUp, hDown):
    hUpTransformed = hUp.Clone()  # Clone the up histogram
    hDownTransformed = hDown.Clone()  # Clone the down histogram
    
    # Loop over each bin to apply the transformation
    for i in range(1, hCentral.GetNbinsX() + 1):
        central_value = hCentral.GetBinContent(i)
        up_value = hUp.GetBinContent(i)
        down_value = hDown.GetBinContent(i)
        
        # Calculate the maximum deviation from the central value
        max_deviation = max(abs(up_value - central_value), abs(down_value - central_value))
        
        if central_value != 0:
            relative_uncertainty = max_deviation / central_value
        else:
            relative_uncertainty = 0
        
        # Apply symmetric transformations
        hUpTransformed.SetBinContent(i, central_value * (1 + relative_uncertainty))
        hDownTransformed.SetBinContent(i, central_value * (1 - relative_uncertainty))
        
        # Keep the original bin errors
        hUpTransformed.SetBinError(i, hUp.GetBinError(i))
        hDownTransformed.SetBinError(i, hDown.GetBinError(i))
    
    return hUpTransformed, hDownTransformed

# Define the input and output directories
input_directory = "/afs/cern.ch/work/s/savarghe/NewJEC/2018/mu/A/mergedHistos/ExcControl/"
output_directory = "/afs/cern.ch/work/s/savarghe/NewJEC/2018/mu/A/transformedHistos/ExcControl/"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# List of systematics (base names without "up" or "down" suffixes)
systematics = [
    "absmpfb", "absscl", "absstat",
    "flavorqcd", "frag", "timepteta",
    "pudatamc", "puptbb", "puptec1", "puptec2", "pupthf", "puptref",
    "relfsr", "relbal", "relsample",
    "reljerec1", "reljerec2", "reljerhf",
    "relptbb", "relptec1", "relptec2", "relpthf",
    "relstatec", "relstatfsr", "relstathf",
    "singpiecal", "singpihcal"
]

base_systematics = [
    "base_JEC", "base_PUWeight", "base_bc_lhemuf", "base_bc_stat",
    "base_bfrag", "base_extp", "base_fsr", "base_intp",
    "base_isr", "base_lhemur", "base_muEff", "base_pdf",
    "base_prefire", "base_xdyb", "base_xdyc", "base_xwj"
]

# Function to navigate directories and process histograms
def process_directory(input_dir, output_dir):
    # Loop over all keys (directories and histograms) in the current directory
    for key in input_dir.GetListOfKeys():
        key_name = key.GetName()
        obj = key.ReadObj()
        
        if obj.IsA().InheritsFrom("TDirectory"):  # If the object is a directory
            # Create a new directory in the output file
            output_subdir = output_dir.mkdir(key_name)
            output_subdir.cd()
            
            # Recursively process the subdirectory
            process_directory(obj, output_subdir)
        elif obj.IsA().InheritsFrom("TH1"):  # If the object is a histogram
            # Check if the histogram is a systematic variation
            is_syst = any(syst in key_name for syst in systematics + base_systematics)
            if is_syst:
                # Identify the corresponding central histogram
                base_hist_name = key_name.split('_')[0]  # Assuming the base name is the prefix before "_up" or "_down"
                base_hist = input_dir.Get(f"{base_hist_name}/bdt_output")
                
                if "_up" in key_name:
                    # Process the "up" variation
                    down_hist_name = key_name.replace("_up", "_down")
                    down_hist = input_dir.Get(down_hist_name)
                    up_transformed, down_transformed = transform_histograms_symmetric(base_hist, obj, down_hist)
                    up_transformed.Write()  # Write the transformed "up" histogram
                    output_dir.cd()
                    down_transformed.Write()  # Write the transformed "down" histogram
                elif "_down" in key_name:
                    # "down" variation is handled in the "up" case, so skip
                    continue
            else:
                # Write the histogram to the output file as is
                output_dir.cd()
                obj.Write()

# Process each *_mu.root file in the input directory
for file_name in os.listdir(input_directory):
    if fnmatch.fnmatch(file_name, "*_mu.root"):
        # Open the input ROOT file
        input_file_path = os.path.join(input_directory, file_name)
        input_file = ROOT.TFile(input_file_path, "READ")
        
        # Create the corresponding output ROOT file
        output_file_path = os.path.join(output_directory, file_name)
        output_file = ROOT.TFile(output_file_path, "RECREATE")
        
        # Start processing from the root directory of the input file
        process_directory(input_file, output_file)
        
        # Close the ROOT files
        input_file.Close()
        output_file.Close()
        
        print(f"Processed and saved: {file_name}")

print("Transformation complete. Transformed histograms are saved with original directory structure and names.")
