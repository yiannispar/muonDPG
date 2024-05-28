import math
import os
import numpy as np

def add_overflow(h):
    nbins = h.GetNbinsX()+1
    e1 = h.GetBinError(nbins-1)
    e2 = h.GetBinError(nbins)
    h.AddBinContent(nbins-1, h.GetBinContent(nbins))
    h.SetBinError(nbins-1, math.sqrt(e1*e1 + e2*e2))
    h.SetBinContent(nbins, 0)
    h.SetBinError(nbins, 0)
    return h

def merge_root_files(dir):
    pwd = os.getcwd()
    os.chdir(dir)
    os.system('rm -rf merged_total.root')
    os.system('hadd merged_total.root *.root')
    os.chdir(pwd)

def efficiency_to_vector(tefficiency):
    if not tefficiency:
        print("Error: TEfficiency object is not valid.")
        return None, None, None
    
    num_bins = tefficiency.GetTotalHistogram().GetNbinsX()

    efficiency_values = []
    error_low_values = []
    error_up_values = []

    for bin in range(1, num_bins + 1):
        efficiency = tefficiency.GetEfficiency(bin)
        error_low = tefficiency.GetEfficiencyErrorLow(bin)
        error_up = tefficiency.GetEfficiencyErrorUp(bin)
        
        efficiency_values.append(efficiency)
        error_low_values.append(error_low)
        error_up_values.append(error_up)

    return efficiency_values, error_low_values, error_up_values

def calculate_ratio_with_error(num_values, num_errors_low, num_errors_up, denom_values, denom_errors_low, denom_errors_up):
    if None in (num_values, num_errors_low, num_errors_up, denom_values, denom_errors_low, denom_errors_up):
        print("Error: One or more input vectors is None.")
        return None, None, None

    num_values = np.array(num_values)
    num_errors_low = np.array(num_errors_low)
    num_errors_up = np.array(num_errors_up)
    denom_values = np.array(denom_values)
    denom_errors_low = np.array(denom_errors_low)
    denom_errors_up = np.array(denom_errors_up)

    zero_mask = (denom_values == 0)
    denom_values[zero_mask] = np.nan

    ratio_values = np.divide(num_values, denom_values, out=np.zeros_like(num_values), where=denom_values!=0)

    denom_values[zero_mask] = 0

    ratio_errors_low = ratio_values*(np.sqrt((num_errors_low / num_values) ** 2 + (denom_errors_low / denom_values) ** 2, where=num_values!=0))
    ratio_errors_up = ratio_values*(np.sqrt((num_errors_up / num_values) ** 2 + (denom_errors_up / denom_values) ** 2, where=num_values!=0))

    ratio_values[zero_mask] = 0
    ratio_errors_low[zero_mask] = 0
    ratio_errors_up[zero_mask] = 0

    return ratio_values, ratio_errors_low, ratio_errors_up