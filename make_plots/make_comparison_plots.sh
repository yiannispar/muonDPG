#!/bin/bash

era1="$1"
era2="$2"

############ settings #############
root_files_dir1="/eos/user/n/nplastir/Trigger/files/$era1"
output_dir="/eos/user/n/nplastir/Trigger/plots/${era1}vs${era2}"
root_files_dir2="/eos/user/n/nplastir/Trigger/files/$era2"
###################################

current_dir=$PWD

echo "Root files dir: ${root_files_dir1} and ${root_files_dir2}"
echo "Output dir: ${output_dir}"
echo "Dataset legend: ${era1} and ${era2}"

mkdir -p $output_dir

mkdir -p $output_dir/eff_comparison/


cd $current_dir/../plotters/

python3 eff_plots_comparison.py -o $output_dir/eff_comparison/ -i1 $root_files_dir1/eff/ -i2 $root_files_dir2/eff/ --legend1 $era1 --legend2 $era2


cd $current_dir