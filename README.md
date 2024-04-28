L1 Muon DPG scripts (based on official NANOAOD)  

Install  
-------  
```  
cmsrel CMSSW_13_0_3  
cd CMSSW_13_0_3/src  
cmsenv  
git clone https://github.com/yiannispar/muonDPG.git  
voms-proxy-init -voms cms 
```  
Run  
---  
```  
cd muonDPG/condor  
python3 run_nano.py --dataset <name of dataset> --exec <name of executable> --output <full path of output dir>  
(--nFiles <number of files to run>) (--submit) (--jobFlav <condor job flabor>) (--submitName <condor submit filename>)  
```  
**Notes:**  
- If you run with ```(--submit)``` option then jobs will be automatically submitted to condor. If not, then run ```condor_submit <filename>```  
- Name of executable is the filename of the code you want to run (under ```src``` directory, eg ```eff_nano.py```)  
- Condor job flavour is the maximum time limit for each job. (https://batchdocs.web.cern.ch/local/submit.html)  

Make plots  
----------  
```  
cd make_plots  
. make_eff_plots.sh  
```  
You can change settings by opening ```make_eff_plots.sh```   


Batch Submission
----------
Before submitting the jobs make sure that you have enabled the certificate for the DAS.

```
voms-proxy-init -voms cms 
```

```
cd muonDPG/condor
./batch_submission.sh <name of dataset>
```

```
cd muonDPG/make_plots
./make_plots.sh <era of dataset>
```