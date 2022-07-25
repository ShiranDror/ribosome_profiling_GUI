
#from scipy import stats, optimize
from statsmodels.stats.proportion import proportion_confint
#from statsmodels.proportion import proportion_confint
from scipy.stats import norm
from math import sqrt
import numpy as np
#from numpy import inf
from numba import jit

@jit
def trim_ends(x: float):
    """ just a normal clip function but designed for jit compilation (not sure how much i gain by this, its for the sport) """
    if x < 0:
        return 0
    if x > 1:
        return 1
    return x
    #return np.clip(x, 0, 1)

def wald_binom_ci(m, n, alpha, use_agresti_coull: bool = False):
    # agresti coull correction for wald binominal calulation
    if use_agresti_coull:
        adjust = norm.ppf(1-(1 - alpha/100)/2)**2
        m = (m + adjust) / 2
        n = n + adjust
    
    # wald binominal calulation
    theta_hat = m/n
    theta_se = sqrt(theta_hat*(1 - theta_hat)/n)
    z_val = norm.ppf(1-(1 - alpha/100)/2)
    return trim_ends(theta_hat-theta_se*z_val), trim_ends(theta_hat+theta_se*z_val)

def ac_binom_ci(m, n, alpha):
    return(wald_binom_ci(m, n, alpha, True))


def array_binom_ci(array_m, array_n, alpha, use_agresti_coull: bool = False):
    """ accepts to arrays. array_m is the IP, array_n is to total reads.
        returns 2 arrays of the same size, containing by position lower ci and upper ci
    """
    array_m = np.asarray(array_m)
    array_n = np.asarray(array_n)
    array_n = array_m + array_n

    # to avoide division by 0, even if it is 0/0 for some reason it still returns nan
    array_n[array_n == 0] = 1

    low_ci = np.empty(len(array_m), np.float64)
    upp_ci = np.copy(low_ci)
    array_length = len(array_n)

    for i in range(array_length):
        (low_ci[i], upp_ci[i]) = wald_binom_ci(array_m[i], array_n[i], alpha, use_agresti_coull)
    return low_ci, upp_ci
    


def get_enricment_and_ci(np_data, np_control, total_reads, control_total_reads):



    np_data[np.isnan(np_data)] = 0
    np_control[np.isnan(np_control)] = 0

    library_size_normalization_factor = control_total_reads / total_reads
    
    #(low_ci_array, upp_ci_array) = array_binom_ci(np_data, np_control, True)
    (low_ci_array, upp_ci_array) = calc_proportion_confint(np_data, np_control, True)
    low_ci_array *= library_size_normalization_factor
    upp_ci_array *= library_size_normalization_factor
    #* library_size_normalization_factor
    np_control[np_control == np.nan] = 0.04
    #enrichment = np_data / np_control
   
    # to avoide division by 0, even if it is 0/0 for some reason it still returns nan
    # enrichment[np.isnan(enrichment)] = 0 #minimum_value
    # maximum_value = np.nanmax(enrichment[enrichment != np.inf], axis=0)
    # enrichment[np.isinf(enrichment)] = maximum_value

    return (low_ci_array, upp_ci_array)

def calc_proportion_confint(ip_array, total_transcriptome_array, alpha: float = 0.05):
    """ accepts two arrays. array_m is the IP, array_n is to total reads.
        returns 2 arrays of the same size, containing by position lower ci and upper ci
    """
    ip_array = np.asarray(ip_array)
    total_transcriptome_array = np.asarray(total_transcriptome_array)
    total_transcriptome_array = ip_array + total_transcriptome_array

    # to avoide division by 0, even if it is 0/0 for some reason it still returns nan
    total_transcriptome_array[total_transcriptome_array == 0] = 1
    ci_low, ci_upp = proportion_confint(ip_array, total_transcriptome_array, alpha, "agresti_coull")

    return ci_low, ci_upp

if __name__ == "__main__":
    print()
    # test_data = np.array([0,0,0,0,1,2,3,4,5,6,7,8,9,20,1,1,0,0])
    # test_control = np.array([0,0,30,0,1,2,1,2,3,16,17,18,19,0,1,1,0,0])
    # total_reads = 1
    # total_control_reads = 6
    # (enrichment, low_ci_array, upp_ci_array) = get_enricment_and_ci(test_data, test_control, total_reads, total_control_reads)
    # print("enrichment:")
    # print(enrichment)
    # print("low_ci_array:")
    # print(low_ci_array)
    # print("high_ci_array:")
    # print(upp_ci_array)