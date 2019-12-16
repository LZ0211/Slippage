#!/usr/bin/env python
# coding=utf-8
import re
import numpy as np
from scipy import interpolate
from .DataSet import DataSet
from .File import File
from .Smooth import Smooth
from .Fitting import Fitting

class Engine:
    def __init__(self):
        self.datas = {}
        self.selected = ''
        self.for_fitting = []
        self.params = [1,0,1,0]
        self.scale_param = [1,0]
        self.skip_window = 1
        self.diff_window = 1
        self.cut_range = [0,float("inf")]
        self.fitting_method = 'dVdQ'
        self.events = []

    def set_skip_window(self,value):
        self.skip_window = value

    def set_diff_window(self,value):
        self.diff_window = value

    def set_param(self,value,idx):
        self.params[idx] = value
        
    def alias(self,name):
        if self.selected in self.datas:
            self.datas[name] = self.datas[self.selected]
            del self.datas[self.selected]
            self.selected = name
            self.triggle()

    def triggle(self):
        for f in self.events:
            f()

    def bind(self,f):
        self.events.append(f)

    def select(self,key):
        if not key in self.datas:
            return False
        self.selected = key
        return True

    def cut(self,datas):
        (x_data,y_data) = datas()
        lower = min(self.cut_range)
        upper = max(self.cut_range)
        idx = np.where((x_data > lower) & (x_data < upper))
        return DataSet(x_data[idx],y_data[idx])

    def diff(self,datas):
        return datas.diff(self.diff_window)

    def invert(self,datas):
        return datas.invert()

    def skip(self,datas):
        return datas.skip(self.skip_window)

    def scale(self,datas):
        if self.fitting_method == 'VQ':
            return datas.modify_x(*self.scale_param)
        if self.fitting_method == 'dVdQ':
            return datas.modify_x(*self.scale_param).modify_y(1/self.scale_param[0],0)

    def data(self):
        if self.selected in self.datas:
            return self.datas[self.selected]()

    def use_smooth(self,fn):
        self.smooth = lambda data:DataSet(*fn(*data()))

    def clear_datas(self,reg):
        keys = self.datas.keys()
        for k in keys:
            if re.match(reg,k):
                del self.datas[k]
        self.triggle()

    def read_data(self,file,define):
        data = File(file).read_data()
        #输入数据的列定义
        if define == None:
            define = 'Voltage:Capacity'
        cols = list(map(lambda x:x.strip(),define.strip().split(':')))
        cap_idx = cols.index('Capacity')
        vol_idx = cols.index('Voltage')
        #生成数据点
        matrix = np.array(data)
        x_data = matrix[:,cap_idx]
        y_data = matrix[:,vol_idx]
        return (x_data,y_data)

    def read_pos_data(self,file,define=None):
        self.clear_datas(r'^pos.*')
        data = self.read_data(file,define)
        self.datas['pos'] = DataSet(*data)
        self.selected = 'pos'
        self.triggle()

    def read_neg_data(self,file,define=None):
        self.clear_datas(r'^neg.*')
        data = self.read_data(file,define)
        self.datas['neg'] = DataSet(*data)
        self.selected = 'neg'
        self.triggle()

    def read_full_data(self,file,define=None):
        self.clear_datas(r'^full.*')
        data = self.read_data(file,define)
        self.datas['full'] = DataSet(*data)
        self.selected = 'full'
        self.triggle()

    def modify_data(self,func,name):
        key = self.selected
        if key in self.datas:
            new_name = key+name
            self.datas[new_name] = func(self.datas[key])
            self.selected = new_name
            self.triggle()

    def smooth_data(self):
        self.modify_data(self.smooth,'_smooth')

    def diff_data(self):
        self.modify_data(self.diff,'_diff')

    def cut_data(self):
        self.modify_data(self.cut,'_cut')

    def invert_data(self):
        self.modify_data(self.invert,'_invert')

    def skip_data(self):
        self.modify_data(self.skip,'_skip')

    def scale_data(self):
        self.modify_data(self.scale,'_scale')

    def draw_data(self,draw):
        draw(*self.data(),self.selected)
    
    def choise_fitting_datas(self,pos,neg,full):
        if not pos in self.datas:
            return
        if not neg in self.datas:
            return
        if not full in self.datas:
            return
        self.for_fitting = [pos,neg,full]

    def init_guess(self):
        if not len(self.for_fitting) == 3:
            return
        self.params[0] = self.datas[self.for_fitting[2]].x_max / self.datas[self.for_fitting[0]].x_max
        self.params[2] = self.datas[self.for_fitting[2]].x_max / self.datas[self.for_fitting[1]].x_max

    def fit_data(self):
        if not len(self.for_fitting) == 3:
            return None
        pos = self.datas[self.for_fitting[0]]
        neg = self.datas[self.for_fitting[1]]
        full = self.datas[self.for_fitting[2]]
        fittor = Fitting(pos,neg,full)
        fittor.pos_init_guess(*self.params[0:2])
        fittor.neg_init_guess(*self.params[2:4])
        if self.fitting_method == 'VQ':
            params = fittor.fit_leastsq().x
        elif self.fitting_method == 'dVdQ':
            params = fittor.diff_fit_leastsq().x
        self.params = params
        (w1,s1,w2,s2) = params
        x_data = full.x_data
        pos_y = interpolate.interp1d(pos.x_data*w1-s1,pos.y_data, fill_value="extrapolate")(x_data)
        neg_y = interpolate.interp1d(neg.x_data*w2-s2,neg.y_data, fill_value="extrapolate")(x_data)
        if self.fitting_method == 'VQ':
            self.datas[self.for_fitting[0]+'_fitting'] = DataSet(x_data,pos_y)
            self.datas[self.for_fitting[1]+'_fitting'] = DataSet(x_data,neg_y)
            self.datas[self.for_fitting[2]+'_fitting'] = DataSet(x_data,pos_y-neg_y)
        elif self.fitting_method == 'dVdQ':
            self.datas[self.for_fitting[0]+'_fitting'] = DataSet(x_data,pos_y/w1)
            self.datas[self.for_fitting[1]+'_fitting'] = DataSet(x_data,neg_y/w2)
            self.datas[self.for_fitting[2]+'_fitting'] = DataSet(x_data,pos_y/w1-neg_y/w2)
        self.triggle()
        return params


