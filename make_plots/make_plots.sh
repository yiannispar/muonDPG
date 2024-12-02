#!/bin/bash

# Check if the era is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <era>"
    exit 1
fi

era="$1"

############ settings #############
root_files_dir="/eos/user/n/nplastir/Trigger/DPS_2024/final/files/$era"
output_dir="/eos/user/n/nplastir/Trigger/DPS_2024/final/plots/$era"
###################################

current_dir=$PWD

echo "Root files dir: ${root_files_dir}"
echo "Output dir: ${output_dir}"
echo "Dataset legend: ${era}"

mkdir -p $output_dir

# mkdir -p $output_dir/eff_22_11/
# mkdir -p $output_dir/eff_22_15/
# mkdir -p $output_dir/eff_11_doublequal/
# mkdir -p $output_dir/eff/
# mkdir -p $output_dir/eff_2WP/
# # mkdir -p $output_dir/eff_qual/
# # mkdir -p $output_dir/eff_run/
# mkdir -p $output_dir/misid/
# # mkdir -p $output_dir/misid_TP/
# # mkdir -p $output_dir/misid_run/

# ############ Efficiency #############
# ## merge root files
# cd $root_files_dir/eff/
# # rm -rf merged_total.root
# # hadd merged_total.root *.root

# cd $current_dir/../plotters/

# python3 eff_plots.py -o $output_dir/eff/ -i $root_files_dir/eff/ --legend "$era" 

############ Efficiency_2WP #############
## merge root files
cd $root_files_dir/eff_2WP/
rm -rf merged_total.root
hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 eff_plots_2WP.py -o $output_dir/eff_2WP/ -i $root_files_dir/eff_2WP/ --legend "$era" 

# ############ Efficiency_2WP #############
# ## merge root files
# cd $root_files_dir/eff_22_11/
# # rm -rf merged_total.root
# # hadd merged_total.root *.root

# cd $current_dir/../plotters/

# python3 eff_plots_22_11.py -o $output_dir/eff_22_11/ -i $root_files_dir/eff_22_11/ --legend "$era" 


# ############ Efficiency_2WP #############
# ## merge root files
# cd $root_files_dir/eff_22_15/
# # rm -rf merged_total.root
# # hadd merged_total.root *.root

# cd $current_dir/../plotters/

# python3 eff_plots_22_15.py -o $output_dir/eff_22_15/ -i $root_files_dir/eff_22_15/ --legend "$era" 


# ############ Efficiency_2WP #############
# ## merge root files
# # cd $root_files_dir/eff_11_doublequal/
# # rm -rf merged_total.root
# # hadd merged_total.root *.root

# # cd $current_dir/../plotters/

# # python3 eff_plots_11_doublequal.py -o $output_dir/eff_11_doublequal/ -i $root_files_dir/eff_11_doublequal/ --legend "$era" 



# # ############ Efficiency vs Quality #############
# # ## merge root files
# # cd $root_files_dir/eff_qual/
# # # rm -rf merged_total.root
# # # hadd merged_total.root *.root

# # cd $current_dir/../plotters/

# # python3 eff_plots_qual.py -o $output_dir/eff_qual/ -i $root_files_dir/eff_qual/ --legend "$era" 

# # ############ Efficiency vs Run #############
# # ## merge root files
# # cd $root_files_dir/eff_run/
# # rm -rf merged_total.root
# # hadd merged_total.root *.root

# # cd $current_dir/../plotters/

# # python3 eff_vs_run_plots.py -o $output_dir/eff_run/ -i $root_files_dir/eff_run/ --legend "$era" 

# ############ Charge misidentification #############
# ## merge root files
# cd $root_files_dir/misid/
# # rm -rf merged_total.root
# # hadd merged_total.root *.root

# cd $current_dir/../plotters/

# python3 misid_plots.py -o $output_dir/misid/ -i $root_files_dir/misid/ --legend "$era" 


# # ############ Charge misidentification vs run #############
# # ## merge root files
# # cd $root_files_dir/misid_run/
# # rm -rf merged_total.root
# # hadd merged_total.root *.root

# # cd $current_dir/../plotters/

# # python3 misid_vs_run_plots.py -o $output_dir/misid_run/ -i $root_files_dir/misid_run/ --legend "$era" 

# # # ############ Charge misidentification with Tag & Probe #############
# # # ## merge root files
# # # cd $root_files_dir/misid_TP/
# # # rm -rf merged_total.root
# # # hadd merged_total.root *.root

# # # cd $current_dir/../plotters/

# # # python3 misid_plots_TP.py -o $output_dir/misid_TP/ -i $root_files_dir/misid_TP/ --legend "$era" 

# cd $current_dir