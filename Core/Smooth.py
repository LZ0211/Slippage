#!/usr/bin/env python
# coding=utf-8
import numpy as np
from scipy import signal, interpolate

class Smooth:
    @staticmethod
    #根据相变方程拟合
    def Phase_Formular(x_data,y_data):
        #寻找相变点
        pass

    @staticmethod
    #Savitzky_Golay滤波器
    def Savitzky_Golay(x_data,y_data,window,order):
        # f = interpolate.UnivariateSpline(x_data,y_data, k=2, s=0)
        # xint = np.linspace(x_data[0],x_data[-1],x_data.size*5)
        # yint = f(xint)
        xint = x_data
        yint = y_data
        return (xint,signal.savgol_filter(yint,window,order))

    @staticmethod
    #滑动平均滤波
    def Convolve(x_data,y_data,w):
        # f = interpolate.UnivariateSpline(x_data,y_data, k=2, s=0)
        # xint = np.linspace(x_data[0],x_data[-1],x_data.size*5)
        # yint = f(xint)
        xint = x_data
        yint = y_data
        wi=np.ones(w)/float(w)
        return (xint,np.convolve(yint,wi,'same'))

    @staticmethod
    #插值法降噪
    def Spline(x_data,y_data,s):
        f = interpolate.UnivariateSpline(x_data,y_data, k=2, s=s)
        yint = f(x_data)
        return (x_data,yint)

    @staticmethod
    #改进的插值法降噪
    def Adv_Spline(x_data,y_data,s):
        #非均匀插值
        xint = np.diff(x_data)
        dx = np.append(xint,xint[-1]*2-xint[-2])
        d1 = x_data - dx*0.5
        #d2 = x_data + dx*0.33
        xint = np.append(x_data,d1)
        #过滤重复的点
        xint = np.unique(xint)
        #排序
        xint.sort()
        #插值函数
        f1 = interpolate.UnivariateSpline(x_data,y_data, k=2, s=s)
        #f2 = interpolate.UnivariateSpline(x_data,y_data, k=3, s=0)
        #创建插值后的数据点
        yint1 = f1(xint)
        #yint2 = f2(xint)
        #求微分
        dx = np.diff(xint)
        dy1 = np.diff(yint1)
        diff = np.diff(dx/dy1)
        #dx2 = 
        #筛选满足条件的数据点
        idx = np.where(np.absolute(diff) < 1E5)
        x_int = xint[idx]
        y_int = yint1[idx]
        start = 0
        end = y_int.size
        for i in range(x_int.size):
            #print(x_int[i],x_data[0])
            if x_int[i] < x_data[0]:
                start = i
            if x_int[i] > x_data[-1]:
                end = i
                break
        return (x_int[start:end],y_int[start:end])
