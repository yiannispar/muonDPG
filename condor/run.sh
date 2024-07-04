#! /usr/bin/env sh

## arguments
exec=$1
infile=$2
output_dir=$3
json_file=$4
pwd=$5

## needed to load CMSSW libraries/packages
cd $pwd/../../
eval `scramv1 runtime -sh`

export X509_USER_PROXY=/afs/cern.ch/user/i/iparaske/private/x509up

## run executable
cd $pwd/../src/
python3 $exec -i $infile -o $output_dir --json $json_file