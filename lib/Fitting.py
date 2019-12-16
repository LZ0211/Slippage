#!/usr/bin/env python
# coding=utf-8
from scipy import optimize, interpolate

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
        self.pos_generator = interpolate.interp1d(*modified,kind='cubic')

    def neg_init_guess(self,weight,slip):
        self.cache_neg = []
        self.params[2] = weight
        self.params[3] = slip
        neg = self.neg
        modified = (neg[0]*weight+slip,neg[1])
        self.neg_generator = interpolate.interp1d(*modified,kind='cubic')

    def fit_leastsq(self):
        params = self.params
        full = self.full
        pos = self.pos
        neg =self.neg
        slip_upper = full[0][-1]*0.5
        bounds = ((0,0,0,0),(params[0]*1.2,slip_upper,params[2]*1.2,slip_upper))
        def cal_err(p,x,y):
            (w1,s1,w2,s2)=p
            #_pos = interpolate.UnivariateSpline(pos[0]*w1-s1,pos[1])(x)
            _pos = interpolate.interp1d(pos[0]*w1-s1,pos[1], fill_value="extrapolate")(x)
            #_neg = interpolate.UnivariateSpline(neg[0]*w2-s2,neg[1])(x)
            _neg = interpolate.interp1d(neg[0]*w2-s2,neg[1], fill_value="extrapolate")(x)
            return _pos-_neg-y
        return optimize.least_squares(cal_err, params, args=full,verbose=1,bounds=bounds)

    def diff_fit_leastsq(self):
        params = self.params
        full = self.full
        pos = self.pos
        neg =self.neg
        slip_upper = full[0][-1]*0.5
        bounds = ((0,0,0,0),(params[0]*1.2,slip_upper,params[2]*1.2,slip_upper))
        def cal_err(p,x,y):
            (w1,s1,w2,s2)=p
            #_pos = interpolate.UnivariateSpline(pos[0]*w1-s1,pos[1])(x)
            _pos = interpolate.interp1d(pos[0]*w1-s1,pos[1], fill_value="extrapolate")(x) / w1
            #_neg = interpolate.UnivariateSpline(neg[0]*w2-s2,neg[1])(x)
            _neg = interpolate.interp1d(neg[0]*w2-s2,neg[1], fill_value="extrapolate")(x) / w2
            return _pos-_neg-y
        return optimize.least_squares(cal_err, params, args=full,verbose=1,bounds=bounds)

