#!/bin/bash

# Check if the era is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <era>"
    exit 1
fi

era="$1"

############ settings #############
root_files_dir="/eos/user/n/nplastir/Trigger/files/$era"
output_dir="/eos/user/n/nplastir/Trigger/plots/$era"
###################################

current_dir=$PWD

echo "Root files dir: ${root_files_dir}"
echo "Output dir: ${output_dir}"
echo "Dataset legend: ${era}"

mkdir -p $output_dir


############ Luminosity ############

# source /cvmfs/cms-bril.cern.ch/cms-lumi-pog/brilws-docker/brilws-env

# json_dir="../JSON"

# # Iterate over all JSON files in the directory
# for json_file in $json_dir/*.json; do
#     # Extract the era from the JSON file name
#     json_era=$(basename "$json_file" .json | awk -F '_' '{print $2}')
    
#     # Check if the extracted era matches the provided era
#     if [ "$json_era" = "$era" ]; then
#         brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /fb -i "$json_file" -o "$era.csv"
#         echo "HERE"
#         break  # Stop iterating once a matching JSON file is found
#     fi
#     echo "HERE2"
# done


############ Efficiency #############
## merge root files
cd $root_files_dir/eff/
rm -rf merged_total.root
hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 eff_plots.py -o $output_dir/eff/ -i $root_files_dir/eff/ --legend "$era" 

############ Efficiency vs Quality #############
## merge root files
cd $root_files_dir/eff_qual/
rm -rf merged_total.root
hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 eff_plots_qual.py -o $output_dir/eff_qual/ -i $root_files_dir/eff_qual/ --legend "$era" 

############ Efficiency vs Run #############
## merge root files
cd $root_files_dir/eff_qual/
rm -rf merged_total.root
hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 eff_vs_run_plots.py -o $output_dir/eff_run/ -i $root_files_dir/eff_run/ --legend "$era" 

############ Charge misidentification #############
## merge root files
cd $root_files_dir/misid/
rm -rf merged_total.root
hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 misid_plots.py -o $output_dir/misid/ -i $root_files_dir/misid/ --legend "$era" 


############ Charge misidentification vs run #############
## merge root files
cd $root_files_dir/misid_run/
rm -rf merged_total.root
hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 misid_vs_run_plots.py -o $output_dir/misid_run/ -i $root_files_dir/misid_run/ --legend "$era" 

############ Charge misidentification with Tag & Probe #############
## merge root files
cd $root_files_dir/misid_TP/
rm -rf merged_total.root
hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 misid_plots_TP.py -o $output_dir/misid_TP/ -i $root_files_dir/misid_TP/ --legend "$era" 

cd $current_dir