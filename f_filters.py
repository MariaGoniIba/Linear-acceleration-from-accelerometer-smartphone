import numpy as np
from scipy import signal
from scipy.signal import butter, filtfilt

def LPfilter(data, t):
    # Butterworth low pass filter 4th order cutoff freq 20 Hz

    # sample frequency
    t = t.to_numpy()
    t_inter = t[1:] - t[0:-1]
    fs = 1 / np.mean(t_inter)
    fs = np.around(fs, -2)  # not to get decimals

    # filter parameters
    nyquist = fs / 2
    fc = 20

    # create filter coefficients
    b, a = signal.butter(4, fc / nyquist, btype='low', analog=False)

    # Apply the filter
    data_filt = filtfilt(b, a, data)

    return data_filt


def HPfilter(data, t):
    # Butterworth high pass filter 3th order cutoff freq 0.3 Hz

    # sample frequency
    t = t.to_numpy()
    t_inter = t[1:] - t[0:-1]
    fs = 1 / np.mean(t_inter)
    fs = np.around(fs, -2)  # not to get decimals

    nyquist = fs / 2
    fc = 0.3

    # create filter coefficients
    b, a = signal.butter(3, fc / nyquist, btype='high', analog=False)

    # Apply the filter
    data_filt = filtfilt(b, a, data)

    return data_filt