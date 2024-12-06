import os
import argparse

def generate_batch_submission_script(output_base_dir, include_eff, include_run, include_all):
    batch_submission_content = f"""#!/bin/bash

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
output_dir="{output_base_dir}/files/$year_run"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Submit the jobs to condor
python3 run_nano.py --dataset "$dataset" --exec eff_nano_2WP.py --output "$output_dir/eff_2WP/" --jobFlav workday --submitName eff_2WP_${{year_run}}.sh --submit

python3 run_nano.py --dataset "$dataset" --exec misid.py --output "$output_dir/misid/" --jobFlav workday --submitName misid_${{year_run}}.sh --submit 
"""
    if include_all:
        include_eff=True
        include_run=True

    if include_eff:
        batch_submission_content +=f"""
python3 run_nano.py --dataset "$dataset" --exec eff_22_15.py --output "$output_dir/eff_22_15/" --jobFlav workday --submitName eff_22_15_${{year_run}}.sh --submit

python3 run_nano.py --dataset "$dataset" --exec eff_22_11.py --output "$output_dir/eff_22_11/" --jobFlav workday --submitName eff_22_11_${{year_run}}.sh --submit

python3 run_nano.py --dataset "$dataset" --exec eff_vs_qual.py --output "$output_dir/eff_qual/" --jobFlav workday --submitName eff_qual_${{year_run}}.sh --submit 
"""        
    if include_run:
        batch_submission_content +=f"""
python3 run_nano.py --dataset "$dataset" --exec eff_vs_run.py --output "$output_dir/eff_run/" --jobFlav workday --submitName eff_run_${{year_run}}.sh --submit

python3 run_nano.py --dataset "$dataset" --exec misid_vs_run.py --output "$output_dir/misid_run/" --jobFlav workday --submitName misid_run_${{year_run}}.sh --submit
"""

    script_path = "./condor/batch_submission.sh"
    os.makedirs(os.path.dirname(script_path), exist_ok=True)
    with open(script_path, "w") as file:
        file.write(batch_submission_content)

    os.chmod(script_path, 0o755)
    print(f"Generated {script_path}")


def generate_make_plots_script(output_base_dir, include_eff, include_run, include_all):
    make_plots_content = f"""#!/bin/bash

# Check if the era is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <era>"
    exit 1
fi

era="$1"

############ settings #############
root_files_dir="{output_base_dir}/files/$era"
output_dir="{output_base_dir}/plots/$era"
###################################

current_dir=$PWD

echo "Root files dir: ${{root_files_dir}}"
echo "Output dir: ${{output_dir}}"
echo "Dataset legend: ${{era}}"

mkdir -p $output_dir

############ Efficiency_2WP #############
mkdir -p $output_dir/eff_2WP/
cd $root_files_dir/eff_2WP/

rm -rf merged_total.root
hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 eff_plots_2WP.py -o $output_dir/eff_2WP/ -i $root_files_dir/eff_2WP/ --legend "$era"

############ Charge misidentification #############
mkdir -p $output_dir/misid/
cd $root_files_dir/misid/

rm -rf merged_total.root
hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 misid_plots.py -o $output_dir/misid/ -i $root_files_dir/misid/ --legend "$era"

cd $current_dir

"""
    if include_all:
        include_eff=True
        include_run=True

    if include_eff:
        make_plots_content += f"""
############ Efficiency_22_15 #############
mkdir -p $output_dir/eff_22_15/
cd $root_files_dir/eff_22_15/

rm -rf merged_total.root
hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 eff_plots_22_15.py -o $output_dir/eff_22_15/ -i $root_files_dir/eff_22_15/ --legend "$era"

############ Efficiency_22_11 #############
mkdir -p $output_dir/eff_22_11/
cd $root_files_dir/eff_22_11/

rm -rf merged_total.root
hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 eff_plots_22_11.py -o $output_dir/eff_22_11/ -i $root_files_dir/eff_22_11/ --legend "$era"

############ Efficiency vs Quality #############
mkdir -p $output_dir/eff_qual/
cd $root_files_dir/eff_qual/

rm -rf merged_total.root
hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 eff_plots_qual.py -o $output_dir/eff_qual/ -i $root_files_dir/eff_qual/ --legend "$era"

"""
    if include_run:
        make_plots_content += f"""
############ Efficiency vs Run #############
mkdir -p $output_dir/eff_run/
cd $root_files_dir/eff_run/

rm -rf merged_total.root
hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 eff_vs_run_plots.py -o $output_dir/eff_run/ -i $root_files_dir/eff_run/ --legend "$era" 

############ Charge misidentification vs run #############
mkdir -p $output_dir/misid_run/
cd $root_files_dir/misid_run/

rm -rf merged_total.root
hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 misid_vs_run_plots.py -o $output_dir/misid_run/ -i $root_files_dir/misid_run/ --legend "$era"
"""


    script_path = "./make_plots/make_plots.sh"
    os.makedirs(os.path.dirname(script_path), exist_ok=True)
    with open(script_path, "w") as file:
        file.write(make_plots_content)

    os.chmod(script_path, 0o755)
    print(f"Generated {script_path}")



def generate_make_plots_scripts(output_base_dir, include_eff, include_run, include_all):
    options= [eff_2WP, misid]
    if include_all:
        include_eff=True
        include_run=True
    if include_eff:
        options+=[eff_22_15, eff_22_11, eff_qual]
    if include_run:
        options+=[eff_vs_run, misid_vs_run]
    for option in options:
        make_plots_content = f"""#!/bin/bash
# Check if the era is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <era>"
    exit 1
fi

era="$1"

############ settings #############
root_files_dir="{output_base_dir}/files/$era/{option}"
output_dir="{output_base_dir}/plots/$era/{option}/"
###################################

current_dir=$PWD

echo "Root files dir: ${{root_files_dir}}"
echo "Output dir: ${{output_dir}}"
echo "Dataset legend: ${{era}}"

mkdir -p $output_dir/

rm -rf merged_total.root
hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 {option}.py -o $output_dir/ -i $root_files_dir/ --legend "$era"

cd $current_dir

echo "DONE"
"""
    
        script_path = f"./make_plots/make_plots_{option}.sh"
        os.makedirs(os.path.dirname(script_path), exist_ok=True)
        with open(script_path, "w") as file:
            file.write(make_plots_content)

        os.chmod(script_path, 0o755)
        print(f"Generated {script_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate files for automated creation of DPG plots")
    parser.add_argument("-o", "--output", required=True, type=str, help="Output directory for the DPG files and plots")
    parser.add_argument("--eff", required=False, default=False, action='store_true', help="Include additional efficiency plots")
    parser.add_argument("--run", required=False, default=False, action='store_true', help="Include additional plots for variables vs the run number")
    parser.add_argument("--all", required=False, default=False, action='store_true', help="Include all additional plots")
    args = parser.parse_args()

    # Generate scripts
    generate_batch_submission_script(args.output, args.eff, args.run, args.all)
    generate_make_plots_script(args.output, args.eff, args.run, args.all)
    generate_make_plots_scripts(args.output, args.eff, args.run, args.all)
