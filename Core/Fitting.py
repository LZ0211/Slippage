#!/usr/bin/env python
# coding=utf-8
import numpy as np
from scipy import optimize, signal, interpolate

class Fitting:
    def __init__(self,pos,neg,full):
        self.pos = pos()
        self.neg = neg()
        self.full = full()
        self.params = [1.0,0.0,1.0,0.0]

    #插值法生成与全电池横坐标对应的值
    def pos_init_guess(self,weight,slip):
        self.cache_pos = []
        self.params[0] = weight
        self.params[1] = slip
        pos = self.pos
        #电压不变，容量调整
        modified = (pos[0]*weight+slip,pos[1])
        self.pos_generator = interpolate.UnivariateSpline(*modified, k=3, s=0)

    def neg_init_guess(self,weight,slip):
        self.cache_neg = []
        self.params[2] = weight
        self.params[3] = slip
        neg = self.neg
        modified = (neg[0]*weight+slip,neg[1])
        self.neg_generator = interpolate.UnivariateSpline(*modified, k=3, s=0)

    def gen_pos_data(self):
        #缓存数据，避免重复运算
        if len(self.cache_pos) == 0:
            self.cache_pos.append(self.pos_generator(self.full[0]))
        return self.cache_pos[-1]

    def gen_neg_data(self):
        if len(self.cache_neg) == 0:
            self.cache_neg.append(self.neg_generator(self.full[0]))
        return self.cache_neg[-1]

    def cal_error(self):
        pos_data = self.gen_pos_data()
        neg_data = self.gen_neg_data()
        full_data = self.full[1]
        err = pos_data-neg_data-full_data
        return np.sum(err*err)

    def VQ_fit_leastsq(self):
        def cal_err(p,x,y):
            (w1,s1,w2,s2)=p
            pos = interpolate.UnivariateSpline(self.pos[0]*w1-s1,self.pos[1], k=3, s=0)(x)
            neg = interpolate.UnivariateSpline(self.neg[0]*w2-s2,self.neg[1], k=3, s=0)(x)
            return (pos - neg)/ y
        a = optimize.least_squares(cal_err, self.params, args=self.full,verbose=1,bounds=(0, 10))
        return a

    def dVdQ_fit_leastsq(self):
        diff_y = np.diff(self.full[1])
        def cal_err(p,x,y):
            (w1,s1,w2,s2)=p
            pos = interpolate.UnivariateSpline(self.pos[0]*w1-s1,self.pos[1], k=3, s=0)(x)
            neg = interpolate.UnivariateSpline(self.neg[0]*w2-s2,self.neg[1], k=3, s=0)(x)
            return (np.diff(pos) - np.diff(neg)) /diff_y
        a = optimize.least_squares(cal_err, self.params, args=self.full,verbose=1,bounds=(0, 10))
        return a

    def fit_leastsq(self):
        diff_y = np.diff(self.full[1]) * 50
        def cal_err(p,x,y):
            (w1,s1,w2,s2)=p
            pos = interpolate.UnivariateSpline(self.pos[0]*w1-s1,self.pos[1], k=3, s=0)(x)
            neg = interpolate.UnivariateSpline(self.neg[0]*w2-s2,self.neg[1], k=3, s=0)(x)
            return np.diff(pos)*50 - np.diff(neg)*50 - diff_y + pos[1:] - neg[1:] - y[1:]
        a = optimize.least_squares(cal_err, self.params, args=self.full,verbose=1,bounds=(0, 10))
        return a


    def fit(self):
        print(self.cal_error())
        pass

