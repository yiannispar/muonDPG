#! /usr/bin/env python

## script to make efficiency plots using official NANOAOD

import math
import ROOT
from array import array
import argparse
import sys
import os.path

## True if passed the trigger (bit indices 3 and 10)
def passedTrig(muon_eta, muon_phi, trg_eta, trg_phi, trg_id, filterBits):

  passed = False

  for idx, (trg_eta, trg_phi) in enumerate(zip(trg_eta,trg_phi)):
    if trg_id[idx] != 13: continue

    dphi = abs(math.acos(math.cos(trg_phi - muon_phi)))
    deta = abs(trg_eta - muon_eta)
    dr = math.sqrt(deta*deta+dphi*dphi)
    if dr <= 0.1: 
      if filterBits[idx]>>3&1 == 1 and filterBits[idx]>>10&1 == 1:
        passed = True

  return passed

## Configuration settings
MAX_FILE = -1        ## Maximum number of input files (use "-1" for unlimited)
MAX_EVT  = -1    ## Maximum number of events to process
PRT_EVT  = 10000     ## Print every Nth event
MIN_dR_TP      = 0.4   ## Minimum dR for T&P matching (they need to be well separated)
MAX_dR_L1_T    = 0.1   ## Maximum dR for L1T-tag matching
MAX_dR_L1_P    = 0.2   ## Maximum dR for L1T-probe matching
TAG_PT         = 27    ## Minimum offline pT for tag muon
L1_QUAL        = 12    ## Minimum L1 quality for Tag matching
REQ_ZMASS = True
#######################

def CalcDPhi( phi1, phi2 ):
  dPhi = math.acos( math.cos( phi1 - phi2 ) )
  if math.sin( phi1 - phi2 ) < 0: dPhi *= -1
  return dPhi

def CalcDR( eta1, phi1, eta2, phi2 ):
  return math.sqrt( math.pow(CalcDPhi(phi1, phi2), 2) + math.pow(eta1 - eta2, 2) )

latex = ROOT.TLatex()
latex.SetTextSize(0.04)

## parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, help='input file')
parser.add_argument('-o', type=str, help='output dir')
args = parser.parse_args()

input_file = args.i
if not input_file:
  sys.exit("No input file given")
output_dir = args.o

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetMarkerStyle(20)
ROOT.gStyle.SetMarkerSize(1)
ROOT.gStyle.SetTitleOffset(1.3)
ROOT.gROOT.ForceStyle()

## L1NTuple branches
tree  = ROOT.TChain('Events')

canvas = ROOT.TCanvas("c","c",750,750)
canvas.SetGridy()
canvas.SetGridx()

## Load input files
print ("Input file: ", input_file)
tree.Add(input_file)


## Trigger settings
trig_WP = {}
trig_WP['SingleMu']  = [12]

trig_TF = {}
trig_TF['Black'] = [0.00, 0.83]
trig_TF['Red'] = [0.83, 1.24]
trig_TF['Blue'] = [1.24, 2.40]
trig_TF['Yellow']= [1.24, 1.6]
trig_TF['Pink'] = [1.6, 2.1]
trig_TF['Green'] = [2.1, 2.40]
trig_TF['Gray'] = [0.00, 2.40]


trg_pt = {}
trg_pt['SingleMu']  = [22]

## ================ Histograms ======================
scale_pt_temp = [0, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 22, 25, 30, 35, 45, 60, 75, 100, 140, 160, 180, 200, 250, 300, 500, 1000]
scale_pt_temp_2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 55, 60]
scale_pt_2  = array('d', scale_pt_temp_2)
scale_pt  = array('d', scale_pt_temp)
scale_nPV_temp = [i for i in range(0,72,2)]
scale_nPV  = array('d', scale_nPV_temp)

eta_bins = [50, -2.5, 2.5]
phi_bins = [20, -4, 4]

h_dr = {}
h_offpt= {}
h_l1pt={}
h_rep={}
h_2d={}
for TF in trig_TF.keys():
  key = TF + '_'
  h_dr[key] = ROOT.TH1F("h_dr_%s" % key,";#DeltaR;",100,0,1)
  h_offpt[key] = ROOT.TH1F("offline_pt_%s" % key,"offline_pt;",100,0,1000)
  h_l1pt[key]= ROOT.TH1F("l1_pt_%s" % key,"l1_pt;",100,0,1000)
  h_rep[key]= ROOT.TProfile("response_%s" % key, "response", 100, 0, 100, 0, 5)
  h_2d[key] =ROOT.TH2F("response2_%s" % key,"response2", 100 ,0, 100, 100, 0,5)

  
## =========================================
json_file = LumiList.LumiList(filename = args.json)

# Loop over over events in TFile
for iEvt in range(tree.GetEntries()):
  if MAX_EVT > 0 and iEvt > MAX_EVT: break
  if iEvt % PRT_EVT == 0: print ('Event #', iEvt)

  tree.GetEntry(iEvt)

  run = tree.run
  luminosityBlock = tree.luminosityBlock
  if not json_file.contains(run,luminosityBlock): continue

  # Require HLT muon trigger
  #if tree.HLT_IsoMu27 != 1 or tree.HLT_Mu50 != 1: continue

  # good vertex
  if tree.Flag_goodVertices != 1: continue

  # need 2 reco muons for T&P
  if tree.nMuon < 2: continue

  ## Lists of tag and probe RECO muon indices
  iTags, iL1Tags, iProbes = [], [], []

  nPV = tree.PV_npvs

  ##########################################################
  ###  Loop over RECO muons to find all valid tag muons  ###
  ##########################################################
  for iTag in range(tree.nMuon):

    ## Compute tag muon coordinates at 2nd station, require to be valid
    recoEta = tree.Muon_eta[iTag]
    recoPhi = tree.Muon_phi[iTag]

    recoAbsEta = abs(recoEta)

    if recoAbsEta > 2.5: continue

    recoIsTight = tree.Muon_tightId[iTag]
    recoIsLoose = tree.Muon_looseId[iTag]

    ## Require tag muon to pass Muon POG tight ID
    if not recoIsTight: continue

    ## Require prompt muons
    recoDxy = tree.Muon_dxy[iTag]
    recoDz  = tree.Muon_dz[iTag]
    if abs(recoDxy) > 0.2 or abs(recoDz) > 0.5: continue

    #muon_passed_trigger = passedTrig(recoEta, recoPhi, tree.TrigObj_eta, tree.TrigObj_phi, tree.TrigObj_id, tree.TrigObj_filterBits)
    #if not muon_passed_trigger: continue

    # ## Require tag muon to pass pT and isolation cuts
    # if tree.Muon_pt[iTag]  < TAG_PT: continue

    # find matching L1 muon
    for iL1 in range(tree.nL1Mu):
      #if tree.L1Mu_hwQual[iL1] < L1_QUAL: continue
      #if tree.L1Mu_pt[iL1]   < TAG_PT - 4.01: continue
      if tree.L1Mu_bx[iL1] != 0: continue           # Bunch Crossing = 0 
      l1_eta = tree.L1Mu_etaAtVtx[iL1]
      l1_phi = tree.L1Mu_phiAtVtx[iL1]
      if CalcDR( l1_eta, l1_phi, recoEta, recoPhi ) > MAX_dR_L1_T: continue
      if not iTag in iTags:
        iTags.append(iTag)
        iL1Tags.append(iL1)

  ## End loop: for iTag in range(reco_tree.Muon.nMuons):

  ## Quit the event if there are no tag muons
  if len(iTags) == 0: continue

  ############################################################
  ###  Loop over RECO muons to find all valid probe muons  ###
  ############################################################

  xTags = []
  for iProbe in range(tree.nMuon):

    ## Compute tag muon coordinates at 2nd station, require to be valid
    recoEta = tree.Muon_eta[iProbe]
    recoPhi = tree.Muon_phi[iProbe]
    recoPt = tree.Muon_pt[iProbe]

    recoAbsEta = abs(recoEta)

    if recoAbsEta > 2.5: continue

    recoIsTight = tree.Muon_tightId[iProbe]
    recoIsLoose = tree.Muon_looseId[iProbe]
    

    ## Require probe muon to pass Muon POG tight ID
    if not recoIsTight: continue

    ## Require prompt muons
    recoDxy = tree.Muon_dxy[iProbe]
    recoDz  = tree.Muon_dz[iProbe]
    if abs(recoDxy) > 0.2 or abs(recoDz) > 0.5: continue


    ## Try to find at least on valid tag muon for this probe
    xTag = -1
    ## Loop over tag muon candidates
    for iTag in iTags:
        ## Make sure tag and probe are not the same muon
        if iTag == iProbe: continue
        ## Require tag and probe muons to be well separated
        tagEta = tree.Muon_eta[iTag]
        tagPhi = tree.Muon_phi[iTag]
        tagPt = tree.Muon_pt[iTag]

        if CalcDR( tagEta, tagPhi, recoEta, recoPhi ) < MIN_dR_TP: continue
        if REQ_ZMASS:
          lorentz_v_tag = ROOT.TLorentzVector()
          lorentz_v_probe = ROOT.TLorentzVector()

          lorentz_v_tag.SetPtEtaPhiM (tagPt, tagEta, tagPhi, tree.Muon_mass[iTag])
          lorentz_v_probe.SetPtEtaPhiM (recoPt, recoEta, recoPhi, tree.Muon_mass[iProbe])

          lorentz_tot = lorentz_v_tag + lorentz_v_probe
          mass = lorentz_tot.M()
          if mass < 75 and mass > 105: continue
          
        ## If tag passes requirements, store its index and quit the loop
        xTag = iTag
        break
    ## End loop: for iTag in iTags

    ## Valid probe only if there is a corresponding tag
    if xTag < 0: continue
    iProbes.append(iProbe)
    xTags.append(xTag)

  ## End loop: for iProbe in range(tree.muon_size):

  ## Quit the event if there are no probe muons
  if(len(iProbes) == 0): continue

  ## loop over probe muons to find matched L1 muon
  for iProbe in iProbes:

    matched_tag = xTags[iProbes.index(iProbe)]
    matched_tag_l1 = iL1Tags[iTags.index(matched_tag)]

    recoEta = tree.Muon_eta[iProbe]
    recoPhi = tree.Muon_phi[iProbe]
    recoAbsEta = abs(recoEta)
    recoPt = tree.Muon_pt[iProbe]

    for tf in trig_TF:
      ## Only consider reco muons in TF eta range
      if not (recoAbsEta > trig_TF[tf][0] and recoAbsEta < trig_TF[tf][1]): continue
    
      key = tf + '_'

        #matched = False  

        # look for L1 muons to match
      for iL1 in range(tree.nL1Mu):
        if iL1 == matched_tag_l1: continue
        if tree.L1Mu_bx[iL1] != 0: continue  
        l1_eta = tree.L1Mu_etaAtVtx[iL1]
        l1_phi = tree.L1Mu_phiAtVtx[iL1]
        l1_pt = tree.L1Mu_pt[iL1]

          #if matched: continue
        #if tree.L1Mu_hwQual[iL1] < L1_QUAL : continue 
        if CalcDR( l1_eta, l1_phi, recoEta, recoPhi ) < 0.1:
          h_dr[key].Fill(CalcDR( l1_eta, l1_phi, recoEta, recoPhi ))
          h_offpt[key].Fill(recoPt)
          h_l1pt[key].Fill(l1_pt)
          h_rep[key].Fill(recoPt,l1_pt/recoPt)
          h_2d[key].Fill(recoPt,l1_pt/recoPt)


    ## End loop: for iProbe in iProbes:
  ## End loop: for iEvt in range(tree.GetEntries()):

## write output to root file
out_file = ROOT.TFile(output_dir + "/" + os.path.basename(input_file), "RECREATE")
out_file.cd()

for tf in trig_TF:
  key = tf + '_'
  h_dr[key].Draw()
  h_dr[key].Write()
  h_offpt[key].Draw()
  h_offpt[key].Write()
  h_l1pt[key].Draw()
  h_l1pt[key].Write()
  h_rep[key].Draw()
  h_rep[key].Write()
  h_2d[key].Draw("colz")
  h_2d[key].Write()
out_file.Write()

