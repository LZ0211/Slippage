# coding=utf-8
import numpy as np

class DataSet:
    #数据点升序排列并删除异常波动点
    def __init__(self,x_data,y_data):
        #保留小数点后6位
        x_data = np.around(x_data, decimals=6)
        y_data = np.around(y_data, decimals=6)
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

    def data(self):
        return (self.x_data,self.y_data)

    def skip(self,skip=None):
        if skip == None or skip == 1:
            return self
        size = self.size - self.size % skip
        _size = int(size / skip)
        x_data = np.mean(self.x_data[0:size].reshape(_size,skip),axis=1)
        y_data = np.mean(self.y_data[0:size].reshape(_size,skip),axis=1)
        return DataSet(x_data,y_data)

    def invert(self):
        return DataSet(self.y_data,self.x_data)

    def diff_x(self,skip=1):
        return self.x_data[2*skip:] - self.x_data[0:0-2*skip]

    def diff_y(self,skip=1):
        return self.y_data[2*skip:] - self.y_data[0:0-2*skip]

    def diff(self,skip=1):
        x_data = self.x_data[skip:0-skip]
        y_data = np.divide(self.diff_y(skip),self.diff_x(skip))
        return DataSet(x_data,y_data)

    def diff_invert(self,skip=1):
        return self.invert().diff(skip)

    def modify_x(self,w,s):
        return DataSet(self.x_data*w-s,self.y_data)

    def modify_y(self,w,s):
        return DataSet(self.x_data,self.y_data*w-s)

    def serialize(self):
        return [self.x_data.tolist(),self.y_data.tolist()]
