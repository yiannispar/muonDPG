import argparse
import sys
import os

## parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--exec', type=str, help='executable')
parser.add_argument('--dataset', type=str, help='dataset')
parser.add_argument('--submit', help='submit to condor',action='store_true')
parser.add_argument('--jobFlav', type=str, help='condor job flavour', default="espresso")
parser.add_argument('-o','--output', type=str, help='output dir')
parser.add_argument('--submitName', type=str, help='name of the condor submit file', default="submit_nano.sh")
parser.add_argument('--nFiles', type=str, help='number of files to run')
args = parser.parse_args()

if args.exec == None:
    print("you need to specify the executable")
    sys.exit(-1)

if args.dataset == None:
    print("you need to specify the dataset")
    sys.exit(-1)

if args.output == None:
    print("you need to specify the output dir")
    sys.exit(-1)

executable = args.exec
dataset = args.dataset

## find files using DAS
das_query = 'dasgoclient --query="file dataset=' + dataset + '"'
if args.nFiles:
    das_query += " -limit " + args.nFiles
query_out = os.popen(das_query)
files_found = ['root://xrootd-cms.infn.it/'+_file.strip() for _file in query_out]

print("Will run " + executable)
print("Dataset " + dataset)
print(str(len(files_found)) + " files found")
print("Will write output to " + args.output)

## make log dir if not exists
if not os.path.exists('log'):
   os.makedirs('log')

## create the file list at the end of the submit file
def format_files_in_queue(files_found):
    file_string = ""
    for index, file_ in enumerate(files_found):
        if index != len(files_found) - 1: file_string += file_ + ","
        else: file_string += file_
    return file_string

## write condor submit file
condor_submit_file = open(args.submitName,"w")
condor_submit_file.write('''
executable = ''' + os.getcwd() + "/../src/" + executable + '''
use_x509userproxy = true

arguments = -i $(Item) -o ''' + args.output + '''

error   = log/err.$(Process)
output  = log/out.$(Process)
log     = log/logFile.log

+JobFlavour = "''' + args.jobFlav + '''"
    
queue 1 in (''' + format_files_in_queue(files_found) + ''')  
''')

condor_submit_file.close()

## submit jobs to condor
if args.submit:
    query_out = os.popen("condor_submit " + args.submitName)
    print("Jobs submitted to condor")
else: print(args.submitName + " created but jobs have not been submitted to condor")