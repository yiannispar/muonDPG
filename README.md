L1 Muon DPG scripts (based on official NANOAOD)  

Install  
-------  
git clone https://github.com/yiannispar/muonDPG.git  

Run  
---  
```  
cd condor  
python3 run_nano.py --dataset <name of dataset> --exec <name of executable> --output <full path of output dir>  
(--nFiles <number of files to run>) (--submit) (--jobFlav <condor job flabor>) (--submitName <condor submit filename>)  
```  
If you run with ```(--submit)``` option then jobs will be automatically submitted to condor.  
if not, then run ```condor_submit <filename>```  

Make plots  
----------  
```  
cd make_plots  
. make_eff_plots.sh  
```  
You can change settings by opening ```make_eff_plots.sh```   