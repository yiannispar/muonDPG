############ settings #############
root_files_dir=/afs/cern.ch/user/n/nplastir/Trigger/CMSSW_13_0_3/src/muonDPG/output/out_misid_TP/
output_dir=/afs/cern.ch/user/n/nplastir/Trigger/CMSSW_13_0_3/src/muonDPG/plots/
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

python3 misid_plots_TP.py -o $output_dir -i $root_files_dir --legend "$dataset_legend" 

cd $current_dir

echo "DONE"