#!/usr/bin/env python
# coding=utf-8
import numpy as np
from scipy import interpolate

class DataSet:
    #数据点升序排列并删除异常波动点
    def __init__(self,x_data,y_data):
        #self.origin_data = [x_data,y_data]
        #二维数据转置
        matrix = np.array([x_data,y_data]).T
        #print(self.matrix)
        #删除重复的点
        matrix = np.unique(matrix,axis=0)
        #排序
        matrix = matrix[matrix[:,0].argsort()]
        x_data = matrix[:,0]
        y_data = matrix[:,1]
        idx = np.where(np.diff(x_data)>1E-6)
        self.x_data = x_data[idx]
        self.y_data = y_data[idx]
        self.x_min = np.min(x_data)
        self.x_max = np.max(x_data)
        self.size = self.x_data.size

    def __call__(self):
        return (self.x_data,self.y_data)

    def data(self):
        return (self.x_data,self.y_data)

    def skip_data(self,skip=None):
        if skip == None or skip == 1:
            return self
        self.x_data = self.x_data[::skip]
        self.y_data = self.y_data[::skip]
        self.x_min = np.min(self.x_data)
        self.x_max = np.max(self.x_data)
        self.size = self.x_data.size

    def invert(self):
        return DataSet(self.y_data,self.x_data)

    def diff_x(self,skip=None):
        return np.diff(np.array(self.x_data)) if skip == None or skip == 1 else self.x_data[skip:]-self.x_data[0:0-skip]

    def diff_y(self,skip=None):
        return np.diff(np.array(self.y_data)) if skip == None or skip == 1  else self.y_data[skip:]-self.y_data[0:0-skip]

    def diff(self,skip=None):
        x_data = self.x_data[1:] if skip == None else self.x_data[skip:]
        y_data = np.divide(self.diff_y(skip),self.diff_x(skip))
        return (x_data,y_data)

    def diff_invert(self,skip=None):
        return self.invert().diff(skip)

    def modify(self,p,x):
        (w1,s1)=p
        return interpolate.UnivariateSpline(self.x_data*w1-s1,self.y_data, k=3, s=0)(x)
