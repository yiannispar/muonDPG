############ settings #############
root_files_dir=/eos/user/n/nplastir/Trigger/Golden/files/2024B/eff_2WP/
output_dir=/eos/user/n/nplastir/Trigger/Golden/plots/2024B/eff_2WP/
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

python3 eff_plots_2WP.py -o $output_dir -i $root_files_dir --legend "$dataset_legend" 

cd $current_dir

echo "DONE"