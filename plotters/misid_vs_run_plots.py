import ROOT
import argparse
import utils
import re
import math
import json

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetTitleOffset(1.5,"Z")
ROOT.gStyle.SetPalette(ROOT.kBlueGreenYellow)

latex = ROOT.TLatex()
latex.SetTextSize(0.04)
latex.SetTextFont(42)
ROOT.gStyle.SetLegendTextSize(0.04)

# Colors
color_0 = ROOT.TColor.GetColor(87,144,252) #blue
color_1 = ROOT.TColor.GetColor(248,156,32) #orange
color_2 = ROOT.TColor.GetColor(228,37,54) #red
color_3 = ROOT.TColor.GetColor(150,74,139) #purple
color_4 = ROOT.TColor.GetColor(156,156,161) #gray
color_5 = ROOT.TColor.GetColor(122,33,221) #purple

#parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--legend', type=str, help='dataset legend')
parser.add_argument('-o', type=str, help='output dir')
parser.add_argument('-i', type=str, help='input dir dir')
args = parser.parse_args()

dataset_legend = args.legend
output_dir = args.o
input_dir = args.i

in_file = ROOT.TFile(input_dir + "merged_total.root","READ")
c = ROOT.TCanvas("c","c",800,800)
c.SetLeftMargin(0.11)
c.SetRightMargin(0.15)
c.SetGrid()

## find run numbers
run_numbers = set()
histos_list = in_file.GetListOfKeys()
for histo in histos_list:
    histo_name = histo.GetName()
    run_number = re.search('22_(.*)_phi', histo_name).group(1)
    run_numbers.add(int(run_number))
run_numbers = sorted(run_numbers)


h_misid_vs_run_BMTF = ROOT.TGraphAsymmErrors(len(run_numbers))
h_misid_vs_run_BMTF.SetMarkerStyle(20)
h_misid_vs_run_BMTF.SetTitle("")
h_misid_vs_run_BMTF.GetXaxis().SetTitle("Run Number")
h_misid_vs_run_BMTF.GetYaxis().SetTitle("Charge misidentification")

h_misid_vs_run_OMTF = ROOT.TGraphAsymmErrors(len(run_numbers))
h_misid_vs_run_OMTF.SetMarkerStyle(20)
h_misid_vs_run_OMTF.SetTitle("")
h_misid_vs_run_OMTF.GetXaxis().SetTitle("Run Number")
h_misid_vs_run_OMTF.GetYaxis().SetTitle("Charge misidentification")

h_misid_vs_run_EMTF = ROOT.TGraphAsymmErrors(len(run_numbers))
h_misid_vs_run_EMTF.SetMarkerStyle(20)
h_misid_vs_run_EMTF.SetTitle("")
h_misid_vs_run_EMTF.GetXaxis().SetTitle("Run Number")
h_misid_vs_run_EMTF.GetYaxis().SetTitle("Charge misidentification")

h_misid_vs_run_uGMT = ROOT.TGraphAsymmErrors(len(run_numbers))
h_misid_vs_run_uGMT.SetMarkerStyle(20)
h_misid_vs_run_uGMT.SetTitle("")
h_misid_vs_run_uGMT.GetXaxis().SetTitle("Run Number")
h_misid_vs_run_uGMT.GetYaxis().SetTitle("Charge misidentification")

TFs = ["uGMT","BMTF","OMTF","EMTF"]
WPs = ["SingleMu_22"]
vars = ["phi"]

for index, run_number in enumerate(run_numbers,start=1):
        for wp in WPs:
            for var in vars:
                key =  wp + "_" + str(run_number) + "_" + var

                h_passed_BMTF = in_file.Get("BMTF_" + key + "_passed")
                h_total_BMTF =in_file.Get("BMTF_" + key + "_total")
                if h_total_BMTF.Integral() != 0:
                    misid_BMTF = h_passed_BMTF.Integral() / h_total_BMTF.Integral()
                    misid_err_BMTF = (h_passed_BMTF.Integral() / h_total_BMTF.Integral()) * math.sqrt(h_passed_BMTF.Integral()) / h_total_BMTF.Integral()
                    h_misid_vs_run_BMTF.SetPoint(index, run_number, misid_BMTF)
                    h_misid_vs_run_BMTF.SetPointEYlow(index, misid_err_BMTF)
                    if misid_BMTF + misid_err_BMTF > 1:
                        h_misid_vs_run_BMTF.SetPointEYhigh(index, 1-misid_BMTF)
                    else:
                        h_misid_vs_run_BMTF.SetPointEYhigh(index, misid_err_BMTF)
                else:
                    misid_BMTF = 0
                    h_misid_vs_run_BMTF.SetPoint(index, run_number, misid_BMTF)
 
                h_passed_OMTF = in_file.Get("OMTF_" + key + "_passed")
                h_total_OMTF =in_file.Get("OMTF_" + key + "_total")
                if h_total_OMTF.Integral() != 0:
                    misid_OMTF = h_passed_OMTF.Integral() / h_total_OMTF.Integral()
                    misid_err_OMTF = (h_passed_OMTF.Integral() / h_total_OMTF.Integral()) * math.sqrt(h_passed_OMTF.Integral()) / h_total_OMTF.Integral()
                    h_misid_vs_run_OMTF.SetPoint(index, run_number, misid_OMTF)
                    h_misid_vs_run_OMTF.SetPointEYlow(index, misid_err_OMTF)
                    if misid_OMTF + misid_err_OMTF > 1:
                        h_misid_vs_run_OMTF.SetPointEYhigh(index, 1-misid_OMTF)
                    else:
                        h_misid_vs_run_OMTF.SetPointEYhigh(index, misid_err_OMTF)
                else:
                    misid_OMTF = 0
                    h_misid_vs_run_OMTF.SetPoint(index, run_number, misid_OMTF)

                h_passed_EMTF = in_file.Get("EMTF_" + key + "_passed")
                h_total_EMTF =in_file.Get("EMTF_" + key + "_total")
                if h_total_EMTF.Integral() != 0:
                    misid_EMTF = h_passed_EMTF.Integral() / h_total_EMTF.Integral()
                    misid_err_EMTF = (h_passed_EMTF.Integral() / h_total_EMTF.Integral()) * math.sqrt(h_passed_EMTF.Integral()) / h_total_EMTF.Integral()
                    h_misid_vs_run_EMTF.SetPoint(index, run_number, misid_EMTF)
                    h_misid_vs_run_EMTF.SetPointEYlow(index, misid_err_EMTF)
                    if misid_EMTF + misid_err_EMTF > 1:
                        h_misid_vs_run_EMTF.SetPointEYhigh(index, 1-misid_EMTF)
                    else:
                        h_misid_vs_run_EMTF.SetPointEYhigh(index, misid_err_EMTF)             
                else:
                    misid_EMTF = 0
                    h_misid_vs_run_EMTF.SetPoint(index, run_number, misid_EMTF)

                h_passed_uGMT = in_file.Get("uGMT_" + key + "_passed")
                h_total_uGMT =in_file.Get("uGMT_" + key + "_total")
                if h_total_uGMT.Integral() != 0:
                    misid_uGMT = h_passed_uGMT.Integral() / h_total_uGMT.Integral()
                    misid_err_uGMT = (h_passed_uGMT.Integral() / h_total_uGMT.Integral()) * math.sqrt(h_passed_uGMT.Integral()) / h_total_uGMT.Integral()
                    h_misid_vs_run_uGMT.SetPoint(index, run_number, misid_uGMT)
                    h_misid_vs_run_uGMT.SetPointEYlow(index, misid_err_uGMT)
                    if misid_uGMT + misid_err_uGMT > 1:
                        h_misid_vs_run_uGMT.SetPointEYhigh(index, 1-misid_uGMT)
                    else:
                        h_misid_vs_run_uGMT.SetPointEYhigh(index, misid_err_uGMT)          
                else:
                    misid_uGMT = 0
                    h_misid_vs_run_uGMT.SetPoint(index, run_number, misid_uGMT)


                # print(f"run_number: {run_number}, misid_BMTF: {misid_BMTF}, misid_OMTF: {misid_OMTF}, misid_EMTF: {misid_EMTF}, misid_uGMT: {misid_uGMT}")

h_misid_vs_run_BMTF.GetXaxis().SetLimits(min(run_numbers),max(run_numbers))
h_misid_vs_run_BMTF.GetYaxis().SetRangeUser(0.,0.1)
h_misid_vs_run_BMTF.Draw("AP")
latex.SetTextSize(0.04)
latex.DrawLatexNDC(0.80,0.91,dataset_legend)
latex.DrawLatexNDC(0.76,0.86,"BMTF")
# latex.DrawLatexNDC(0.14, 0.86, "Reco p_{T} #geq 26 GeV")
latex.DrawLatexNDC(0.14, 0.86, "L1 Qual #geq 12")
latex.SetTextSize(0.045)
latex.DrawLatexNDC(0.1, 0.91, "#font[61]{CMS}")
latex.SetTextSize(0.0346)
latex.DrawLatexNDC(0.195, 0.91, "#font[52]{Internal}")
c.SaveAs(output_dir + "misid_vs_run_BMTF.png")

h_misid_vs_run_OMTF.GetXaxis().SetLimits(min(run_numbers),max(run_numbers))
h_misid_vs_run_OMTF.GetYaxis().SetRangeUser(0.,0.1)
h_misid_vs_run_OMTF.Draw("AP")
latex.SetTextSize(0.04)
latex.DrawLatexNDC(0.80,0.91,dataset_legend)
latex.DrawLatexNDC(0.76,0.86,"OMTF")
# latex.DrawLatexNDC(0.14, 0.86, "Reco p_{T} #geq 26 GeV")
latex.DrawLatexNDC(0.14, 0.86, "L1 Qual #geq 12")
latex.SetTextSize(0.045)
latex.DrawLatexNDC(0.1, 0.91, "#font[61]{CMS}")
latex.SetTextSize(0.0346)
latex.DrawLatexNDC(0.195, 0.91, "#font[52]{Internal}")
c.SaveAs(output_dir + "misid_vs_run_OMTF.png")

h_misid_vs_run_EMTF.GetXaxis().SetLimits(min(run_numbers),max(run_numbers))
h_misid_vs_run_EMTF.GetYaxis().SetRangeUser(0.,0.1)
h_misid_vs_run_EMTF.Draw("AP")
latex.SetTextSize(0.04)
latex.DrawLatexNDC(0.80,0.91,dataset_legend)
latex.DrawLatexNDC(0.76,0.86,"EMTF")
# latex.DrawLatexNDC(0.14, 0.86, "Reco p_{T} #geq 26 GeV")
latex.DrawLatexNDC(0.14, 0.86, "L1 Qual #geq 12")
latex.SetTextSize(0.045)
latex.DrawLatexNDC(0.1, 0.91, "#font[61]{CMS}")
latex.SetTextSize(0.0346)
latex.DrawLatexNDC(0.195, 0.91, "#font[52]{Internal}")
c.SaveAs(output_dir + "misid_vs_run_EMTF.png")

h_misid_vs_run_uGMT.GetXaxis().SetLimits(min(run_numbers),max(run_numbers))
h_misid_vs_run_uGMT.GetYaxis().SetRangeUser(0.,0.1)
h_misid_vs_run_uGMT.Draw("AP")
latex.SetTextSize(0.04)
latex.DrawLatexNDC(0.80,0.91,dataset_legend)
latex.DrawLatexNDC(0.76,0.86,"uGMT")
# latex.DrawLatexNDC(0.14, 0.86, "Reco p_{T} #geq 26 GeV")
latex.DrawLatexNDC(0.14, 0.86, "L1 Qual #geq 12")
latex.SetTextSize(0.045)
latex.DrawLatexNDC(0.1, 0.91, "#font[61]{CMS}")
latex.SetTextSize(0.0346)
latex.DrawLatexNDC(0.195, 0.91, "#font[52]{Internal}")
c.SaveAs(output_dir + "misid_vs_run_uGMT.png")