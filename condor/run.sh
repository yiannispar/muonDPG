#! /usr/bin/env sh

exec=$1
infile=$2
output_dir=$3
json_file=$4

cd $(CMSSW_BASE)/src/
eval `scramv1 runtime -sh`

cd $(CMSSW_BASE)/src/muonDPG/condor/src/
python3 $exec -i $infile -o $output_dir --json $json_file