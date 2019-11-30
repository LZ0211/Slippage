#!/usr/bin/env python
# coding=utf-8
import numpy as np
from .DataSet import DataSet
from .File import File
from .Smooth import Smooth
from .Fitting import Fitting

class Engine:
    def __init__(self):
        #缓存数据
        self.cache = {}
        self.skip = 1
        self.smooth_options = {
            "Do_Nothing": lambda x,y,v:(x,y),
            "Spline": lambda x,y,v:Smooth.Spline(x,y,v),
            "Adv_Spline": lambda x,y,v:Smooth.Adv_Spline(x,y,v),
            "Convolve": lambda x,y,v:Smooth.Convolve(x,y,5),
            "Savitzky_Golay": lambda x,y,v:Smooth.Savitzky_Golay(x,y,7,3)
        }
        self.noise_factor = [2E-4,2E-5,2E-4]
        #默认插值平滑算法
        self.smooth = lambda x,y,v:Smooth.Adv_Spline(x,y,v)
        self.fit_method = 'VQ_fit_leastsq'

    def get_cache(self,key,func):
        if not key in self.cache:
            self.cache[key] = func()
        return self.cache[key]

    #切换平滑算法
    def use_smooth_method(self,algo):
        if algo in self.smooth_options:
            self.smooth = self.smooth_options[algo]
            self.cache = {}
        else:
            #no nothing
            pass

    def add_smooth_method(self,algo):
        func = self.smooth
        if algo == 'Spline':
            self.smooth = lambda *x:Smooth.Spline(*func(*x),0.0002)
            self.cache = {}
        elif algo == 'Adv_Spline':
            self.smooth = lambda *x:Smooth.Adv_Spline(*func(*x),0.00025)
            self.cache = {}
        elif algo == 'Convolve':
            self.smooth = lambda *x:Smooth.Convolve(*func(*x),11)
            self.cache = {}
        elif algo == 'Savitzky_Golay':
            self.smooth = lambda *x:Smooth.Savitzky_Golay(*func(*x),11,3)
            self.cache = {}
    
    def dQdV(self,data,name):
        return self.get_cache(name,lambda : data.diff_invert(self.skip))

    def dVdQ(self,data,name):
        return self.get_cache(name,lambda : data.diff(self.skip))

    def read_pos_data(self,file,define='Voltage,Capacity'):
        pos_data = File(file).read_data()
        #输入数据的列定义
        cols = list(map(lambda x:x.strip(),define.strip().split(',')))
        cap_idx = cols.index('Capacity')
        vol_idx = cols.index('Voltage')
        #生成数据点
        matrix = np.array(pos_data)
        x_data = matrix[:,cap_idx]
        y_data = matrix[:,vol_idx]
        self.pos_data = DataSet(x_data,y_data)
        self.ref_pos_data = self.pos_data
        self.cache = {}

    def read_neg_data(self,file,define='Voltage,Capacity'):
        neg_data = File(file).read_data()
        cols = list(map(lambda x:x.strip(),define.strip().split(',')))
        cap_idx = cols.index('Capacity')
        vol_idx = cols.index('Voltage')
        matrix = np.array(neg_data)
        x_data = matrix[:,cap_idx]
        y_data = matrix[:,vol_idx]
        self.neg_data = DataSet(x_data,y_data)
        self.ref_neg_data = self.neg_data
        self.cache = {}

    def read_full_data(self,file,define='Voltage,Capacity'):
        data = File(file).read_data()
        cols = list(map(lambda x:x.strip(),define.strip().split(',')))
        cap_idx = cols.index('Capacity')
        vol_idx = cols.index('Voltage')
        #生成数据点
        matrix = np.array(data)
        x_data = matrix[:,cap_idx]
        y_data = matrix[:,vol_idx]
        self.full_data = DataSet(x_data,y_data)
        self.ref_full_data = self.full_data
        self.cache = {}

    #读取正负极质量
    def read_pos_weight(self,value):
        self.pos_weight = value

    def read_neg_weight(self,value):
        self.neg_weight = value

    #平滑原始数据
    def smooth_pos_data(self):
        return self.get_cache('smooth_pos_data',lambda : self.smooth(*self.pos_data(),self.noise_factor[0]))

    def smooth_neg_data(self):
        return self.get_cache('smooth_neg_data',lambda : self.smooth(*self.neg_data(),self.noise_factor[1]))

    def smooth_full_data(self):
        return self.get_cache('smooth_full_data',lambda : self.smooth(*self.full_data(),self.noise_factor[2]))
    
    #直接微分求dVdQ
    def org_pos_dVdQ(self):
        return self.dVdQ(self.pos_data,'org_pos_dVdQ')

    def org_pos_dQdV(self):
        return self.dQdV(self.pos_data,'org_pos_dQdV')

    def org_neg_dVdQ(self):
        return self.dVdQ(self.neg_data,'org_neg_dVdQ')

    def org_neg_dQdV(self):
        return self.dQdV(self.neg_data,'org_neg_dQdV')

    def org_full_dVdQ(self):
        return self.dVdQ(self.full_data,'org_full_dVdQ')

    def org_full_dQdV(self):
        return self.dQdV(self.full_data,'org_full_dQdV')

    #先平滑原始数据后求dVdQ
    def smooth_pos_dVdQ(self):
        return self.dVdQ(DataSet(*self.smooth_pos_data()),'smooth_pos_dVdQ')

    def smooth_pos_dQdV(self):
        return self.dQdV(DataSet(*self.smooth_pos_data()),'smooth_pos_dQdV')

    def smooth_neg_dVdQ(self):
        return self.dVdQ(DataSet(*self.smooth_neg_data()),'smooth_neg_dVdQ')

    def smooth_neg_dQdV(self):
        return self.dQdV(DataSet(*self.smooth_neg_data()),'smooth_neg_dQdV')

    def smooth_full_dVdQ(self):
        return self.dVdQ(DataSet(*self.smooth_full_data()),'smooth_full_dVdQ')

    def smooth_full_dQdV(self):
        return self.dQdV(DataSet(*self.smooth_full_data()),'smooth_full_dQdV')

    #使用平滑后的数据进行计算
    def use_smooth_pos_data(self):
        self.ref_pos_data= DataSet(*self.smooth(*self.ref_pos_data(),self.noise_factor[0]))

    def use_smooth_neg_data(self):
        self.ref_neg_data = DataSet(*self.smooth(*self.ref_neg_data(),self.noise_factor[1]))

    def use_smooth_full_data(self):
        self.ref_full_data = DataSet(*self.smooth(*self.ref_full_data(),self.noise_factor[2]))
    
    def use_smooth_data(self):
        self.use_smooth_pos_data()
        self.use_smooth_neg_data()
        self.use_smooth_full_data()
    
    #设置拟合数据范围
    def set_pos_range(self,head,tail):
        (x_data,y_data) = self.ref_pos_data()
        idx = np.where((x_data > head) & (x_data < tail))
        self.ref_pos_data = DataSet(x_data[idx],y_data[idx])

    def set_neg_range(self,head,tail):
        (x_data,y_data) = self.ref_neg_data()
        idx = np.where((x_data > head) & (x_data < tail))
        self.ref_neg_data = DataSet(x_data[idx],y_data[idx])

    def set_full_range(self,head,tail):
        (x_data,y_data) = self.ref_full_data()
        idx = np.where((x_data > head) & (x_data < tail))
        self.ref_full_data = DataSet(x_data[idx],y_data[idx])

    def fit_data(self,m_pos,s_pos,m_neg,s_neg):
        fittor = Fitting(self.ref_pos_data,self.ref_neg_data,self.ref_full_data)
        fittor.pos_init_guess(m_pos,s_pos)
        fittor.neg_init_guess(m_neg,s_neg)
        if self.fit_method == 'VQ_fit_leastsq':
            param = fittor.VQ_fit_leastsq().x
        elif self.fit_method == 'QV_fit_leastsq':
            param = fittor.QV_fit_leastsq().x
        elif self.fit_method == 'dVdQ_fit_leastsq':
            param = fittor.dVdQ_fit_leastsq().x
        elif self.fit_method == 'dQdV_fit_leastsq':
            param = fittor.dQdV_fit_leastsq().x
        return param

