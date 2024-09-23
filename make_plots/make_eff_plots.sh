############ settings #############
root_files_dir=/afs/cern.ch/user/i/iparaske/dpg_scripts/condor/out_files/2023Dv1/eff/
output_dir=/afs/cern.ch/user/i/iparaske/dpg_scripts/plots/2023Dv1/eff/
dataset_legend="2023Dv1"
###################################

current_dir=$PWD

echo "Root files dir: ${root_files_dir}"
echo "Output dir: ${output_dir}"
echo "Dataset legend: ${dataset_legend}"

mkdir -p $output_dir

## merge root files
cd $root_files_dir
rm -rf merged_total.root
hadd merged_total.root *.root

cd $current_dir/../plotters/

python3 eff_plots.py -o $output_dir -i $root_files_dir --legend "$dataset_legend" 

cd $current_dir

echo "DONE"