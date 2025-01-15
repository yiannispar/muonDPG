import ROOT
import argparse
import re
import math
import json
import utils
from utils import *

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--legend', type=str, help='dataset legend')
parser.add_argument('-o', type=str, help='output dir')
parser.add_argument('-i', type=str, help='input dir dir')
args = parser.parse_args()

# Pass arguments
output_dir = args.o
input_dir = args.i
# utils.merge_root_files(input_dir)

in_file = ROOT.TFile(input_dir + "merged_total.root","READ")
# Create canvas, receive values for margins
c, L, R, T, B = utils.create_canvas_wide("c", 0.1, 0.05)
dataset_legend, dataset_x1 = get_dataset_legend_wide(args.legend, R)

## find run numbers
run_numbers = set()
histos_list = in_file.GetListOfKeys()
for histo in histos_list:
    histo_name = histo.GetName()
    run_number = re.search('22_(.*)_phi', histo_name).group(1)
    run_numbers.add(int(run_number))
run_numbers = sorted(run_numbers)

# Define graph
h_misid_vs_run = ROOT.TGraphAsymmErrors(len(run_numbers))

TFs = ["uGMT","BMTF","OMTF","EMTF"]
WPs = ["SingleMu_22"]
vars = ["phi"]
pt_l1_label = f"p^{{#mu,L1}}_{{T}} #geq 22 GeV"
marker_colors = [CMS_color_0, CMS_color_1, CMS_color_2, CMS_color_5]

for i,tf in enumerate(TFs):
    for index, run_number in enumerate(run_numbers,start=1):
            for wp in WPs:
                for var in vars:
                    key =  tf + "_" + wp + "_" + str(run_number) + "_" + var

                    h_passed = in_file.Get(key + "_passed")
                    h_total = in_file.Get(key + "_total")
                    if h_total.Integral() != 0:
                        misid = h_passed.Integral() / h_total.Integral()
                        misid_err = (h_passed.Integral() / h_total.Integral()) * math.sqrt(h_passed.Integral()) / h_total.Integral()
                        h_misid_vs_run.SetPoint(index, run_number, misid)
                        h_misid_vs_run.SetPointEYlow(index, misid_err)
                        if misid + misid_err > 1:
                            h_misid_vs_run.SetPointEYhigh(index, 1-misid)
                        else:
                            h_misid_vs_run.SetPointEYhigh(index, misid_err)
                    else:
                        misid = 0
                        h_misid_vs_run.SetPoint(index, run_number, misid)
    
    h_misid_vs_run.SetTitle("")
    h_misid_vs_run.GetXaxis().SetTitle("Run Number")
    h_misid_vs_run.GetYaxis().SetTitle("Charge misidentification")
    h_misid_vs_run.GetXaxis().SetLimits(min(run_numbers)-10,max(run_numbers)+10)
    h_misid_vs_run.GetXaxis().SetNoExponent(True)
    h_misid_vs_run.GetYaxis().SetRangeUser(0.,0.1)
    h_misid_vs_run.SetMarkerStyle(31)
    marker_color = marker_colors[i % len(marker_colors)]  # Cycle through colors
    h_misid_vs_run.SetMarkerColor(marker_color)
    h_misid_vs_run.SetLineColor(marker_color)
    h_misid_vs_run.Draw("AP")

    utils.add_dataset_legend(dataset_x1,dataset_legend)
    utils.add_cms_label_out_wide(L,T)
    latex.DrawLatexNDC(1-R-0.155, 1-T-0.11, pt_l1_label)
    latex.DrawLatexNDC(1-R-0.18, 1-T-0.155, "L1T Quality #geq 12")
    latex.SetTextSize(0.04)
    latex.DrawLatexNDC(1-R-0.09, 1-T-0.05,tf)
    c.SaveAs(output_dir + f"misid_vs_run_{tf}.png")
    c.SaveAs(output_dir + f"misid_vs_run_{tf}.pdf")