from scipy.signal import butter, lfilter
from scipy.signal import freqs



class Filter:

    # def __init__(self):
    #     self.cutOff = 23.1 #cutoff frequency in rad/s
    #     self.fs = 188.495559 #sampling frequency in rad/s
    #     self.order = 6 #order of filter
    
    def butter_lowpass(self, cutOff, fs, order=5):
        nyq = 0.5 * fs
        normalCutoff = cutOff / nyq
        b, a = butter(order, normalCutoff, btype='low', analog = True)
        return b, a

    def butter_lowpass_filter(self, data, cutOff, fs, order=4):
        b, a = self.butter_lowpass(cutOff, fs, order=order)
        y = lfilter(b, a, data)
        return y
