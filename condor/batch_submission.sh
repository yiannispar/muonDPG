#!/bin/bash

# Check if the dataset is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <dataset>"
    exit 1
fi

dataset="$1"

# Extract the year and run number from the dataset path
year_run=$(echo "$dataset" | grep -oP '(?<=Run)([0-9]+[A-Z])' | head -1)

# Check if the year and run number are extracted successfully
if [ -z "$year_run" ]; then
    echo "Error: Unable to extract year and run number from the dataset path."
    exit 1
fi

# Construct the output directory path
output_dir="/eos/user/n/nplastir/Trigger/Golden/files/$year_run"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"


# Submit the jobs to condor
# python3 run_nano.py --dataset "$dataset" --exec eff_nano.py --output "$output_dir/eff/" --jobFlav workday --submitName eff --submit 

python3 run_nano.py --dataset "$dataset" --exec eff_nano_2WP.py --output "$output_dir/eff_2WP/" --jobFlav workday --submitName eff_2WP --submit 

python3 run_nano.py --dataset "$dataset" --exec eff_vs_qual.py --output "$output_dir/eff_qual/" --jobFlav workday --submitName eff_qual --submit 

python3 run_nano.py --dataset "$dataset" --exec eff_vs_run.py --output "$output_dir/eff_run/" --jobFlav workday --submitName eff_run --submit 

python3 run_nano.py --dataset "$dataset" --exec misid.py --output "$output_dir/misid/" --jobFlav workday --submitName misid --submit 

python3 run_nano.py --dataset "$dataset" --exec misid_vs_run.py --output "$output_dir/misid_run/" --jobFlav workday --submitName misid_run --submit 

# python3 run_nano.py --dataset "$dataset" --exec misid_TP.py --output "$output_dir/misid_TP/" --jobFlav workday --submitName misid_TP --submit 