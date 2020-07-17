# coding=utf-8
from numpy import ones, convolve
from scipy.signal import medfilt, savgol_filter
from scipy.interpolate import UnivariateSpline
from scipy.ndimage import gaussian_filter1d

class Smooth:
    @staticmethod
    def Simple(x_data,y_data,w=3):
        wi=ones(w)/float(w)
        return (x_data,convolve(y_data,wi,'same'))

    @staticmethod
    def Median(x_data,y_data,w=3):
        return (x_data,medfilt(y_data,w))

    @staticmethod
    def Gaussian(x_data,y_data,s=1.0):
        return (x_data,gaussian_filter1d(y_data, sigma=s, order=0))

    @staticmethod
    def Savitzky_Golay(x_data,y_data,w=5):
        return (x_data,savgol_filter(y_data,w,3))

    @staticmethod
    #插值法降噪
    def Spline(x_data,y_data,s=1E-6):
        f = UnivariateSpline(x_data,y_data, s=s)
        yint = f(x_data)
        return (x_data,yint)
