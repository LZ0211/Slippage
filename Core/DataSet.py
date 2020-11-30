# coding=utf-8
import numpy as np
from scipy.interpolate import interp1d

class DataSet:
    DecimalsX = 6
    DecimalsY = 12
    #数据点升序排列并删除异常波动点
    def __init__(self,x_data,y_data):
        #x保留小数点后6位
        x_data = np.around(x_data, decimals=self.DecimalsX)
        #Y保留小数点后12位
        y_data = np.around(y_data, decimals=self.DecimalsY)
        #删除重复的点
        x_data,idx = np.unique(x_data,return_index=True)
        y_data = y_data[idx]
        #排序
        idx = np.argsort(x_data)
        x_data = x_data[idx]
        y_data = y_data[idx]
        self.x_data = x_data
        self.y_data = y_data
        self.x_min = np.min(x_data)
        self.x_max = np.max(x_data)
        self.size = self.x_data.size

    def __call__(self):
        return (self.x_data,self.y_data)

    def __str__(self):
        return '\n'.join(map(lambda x:'\t'.join(map(str,x)),np.array([self.x_data,self.y_data]).T))

    def tolist(self):
        return (np.array([self.x_data,self.y_data]).T).tolist()

    def data(self):
        return (self.x_data,self.y_data)

    def skip(self,skip=None):
        if skip == None or skip == 1:
            return self
        size = self.size - self.size % skip
        _size = int(size / skip)
        x_data = np.mean(self.x_data[0:size].reshape(_size,skip),axis=1)
        x_data = np.insert(x_data,0,self.x_data[0])
        x_data = np.append(x_data,self.x_data[-1])
        y_data = np.mean(self.y_data[0:size].reshape(_size,skip),axis=1)
        y_data = np.insert(y_data,0,self.y_data[0])
        y_data = np.append(y_data,self.y_data[-1])
        return DataSet(x_data,y_data)

    def inter(self,count=1000,order=1):
        if order == 0:
            order = 'nearest'
        elif order == 1:
            order = 'linear'
        elif order == 2:
            order = 'quadratic'
        elif order == 3:
            order = 'cubic'
        x_data = np.linspace(self.x_min,self.x_max,count)
        y_data = interp1d(self.x_data,self.y_data,kind=order)(x_data)
        return DataSet(x_data,y_data)

    def invert(self):
        return DataSet(self.y_data,self.x_data)

    def diff_x(self,skip=1):
        return self.x_data[2*skip:] - self.x_data[0:0-2*skip]

    def diff_y(self,skip=1):
        return self.y_data[2*skip:] - self.y_data[0:0-2*skip]

    def diff(self,skip=1):
        #head = self.x_data[0:skip]
        #tail = self.x_data[0-skip:]
        x_data = self.x_data[skip:0-skip]
        y_data = np.divide(self.diff_y(skip),self.diff_x(skip))
        extrapolate = interp1d(x_data,y_data,kind='quadratic',fill_value="extrapolate")
        #head = extrapolate(head)
        #tail = extrapolate(tail)
        #y_data = np.insert(y_data,0,head)
        #y_data = np.append(y_data,tail)
        x_data = self.x_data
        y_data = extrapolate(x_data)
        return DataSet(x_data,y_data)

    def diff_invert(self,skip=1):
        return self.invert().diff(skip)

    def modify_x(self,w,s):
        return DataSet(self.x_data*w-s,self.y_data)

    def modify_y(self,w,s):
        return DataSet(self.x_data,self.y_data*w-s)

    def serialize(self):
        return [self.x_data.tolist(),self.y_data.tolist()]
