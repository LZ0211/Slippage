#!/usr/bin/env python
# coding=utf-8
import numpy as np
from scipy import signal, interpolate, ndimage

class Smooth:
    @staticmethod
    def Simple(x_data,y_data,w=3):
        wi=np.ones(w)/float(w)
        return (x_data,np.convolve(y_data,wi,'same'))

    @staticmethod
    def Median(x_data,y_data,w=3):
        return (x_data,signal.medfilt(y_data,w))

    @staticmethod
    def Gaussian(x_data,y_data,s=1.0):
        return (x_data,ndimage.gaussian_filter1d(y_data, sigma=s, order=0))

    @staticmethod
    def Savitzky_Golay(x_data,y_data,w=5):
        return (x_data,signal.savgol_filter(y_data,w,3))

    @staticmethod
    #插值法降噪
    def Spline(x_data,y_data,s=1E-6):
        f = interpolate.UnivariateSpline(x_data,y_data, s=s)
        yint = f(x_data)
        return (x_data,yint)
