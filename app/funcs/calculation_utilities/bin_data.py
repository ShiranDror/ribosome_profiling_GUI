import numpy as np
import math
import scipy.ndimage.filters as ndif

def running_mean_uniform_filter1d(x, N):
    #output = ndif.uniform_filter1d(x, N, mode='nearest', origin=-(N//2))[:-(N-1)]
    conv = np.convolve(x, np.ones((N,))/N, mode='same')
    #x_ = np.insert(x, 0, 0)
    #w = N
    #sliding_average = x_[:w].sum() / w + np.cumsum(x_[w:] - x_[:-w]) / w
    
    return conv
    #return np.convolve(x, np.ones((50,))/50, mode='full')

def bin_data(normalized_data_array, window):
    """ returns binned numpy array  """
    # override
    return running_mean_uniform_filter1d(normalized_data_array, window)

    if window > 1 and normalized_data_array is not None:

        binned_array = np.empty(len(normalized_data_array), dtype= 'float')

        for i in range(len(normalized_data_array)):
            binned_array[i] = np.mean(normalized_data_array[i:i + window])

        return binned_array

    return normalized_data_array

def bin_array_sum(arr, window):
    if window > 1:
        binned_array = np.empty(len(arr), dtype= 'float')
        for i in range(len(arr)):
            binned_array[i] = np.sum(arr[i:i + window])
            
        return binned_array
    return arr
            
def bin_and_shrink(arr, window):
    if window > 1:
        binned_array = np.empty(math.ceil(len(arr) / window), dtype= 'float')
        index = 0
        for i in range(0, len(arr), window):
            binned_array[index] = np.sum(arr[i:i + window])
            index += 1

            
        return binned_array
    return arr