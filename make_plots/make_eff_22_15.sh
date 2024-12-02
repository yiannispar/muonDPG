############ settings #############
root_files_dir=/eos/user/n/nplastir/Trigger/DPS_2024/files/2024B/
output_dir=/eos/user/n/nplastir/Trigger/DPS_2024/plots/2024B/eff_22_15/
dataset_legend="2024B"
###################################

current_dir=$PWD

echo "Root files dir: ${root_files_dir}"
echo "Output dir: ${output_dir}"
echo "Dataset legend: ${dataset_legend}"

mkdir -p $output_dir

## merge root files
# cd $root_files_dir
# rm -rf merged_total.root
# hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 eff_plots_22_15.py -o $output_dir -i $root_files_dir --legend "$dataset_legend" 

cd $current_dir

echo "DONE"