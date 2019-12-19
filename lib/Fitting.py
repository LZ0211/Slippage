#!/usr/bin/env python
# coding=utf-8
from scipy import optimize, interpolate

class Fitting:
    def __init__(self,pos,neg,full):
        self.pos = pos()
        self.neg = neg()
        self.full = full()
        self.params = [1.0,0.0,1.0,0.0]
        self.locked = [False,False,False,False]
    
    def init_guess(self,a,b,c,d):
        self.params = [a,b,c,d]

    def lock_params(self,a,b,c,d):
        self.locked = [a,b,c,d]

    def fit_leastsq(self):
        params = self.params
        full = self.full
        pos = self.pos
        neg =self.neg
        slip_upper = full[0][-1]*0.5
        upper = [params[0]*1.2,slip_upper,params[2]*1.2,slip_upper]
        lower = [0,0,0,0]
        bounds = (lower,upper)
        def cal_err(p,x,y):
            (w1,s1,w2,s2)=p
            if self.locked[0]:
                w1 = self.params[0]
            if self.locked[1]:
                s1 = self.params[1]
            if self.locked[2]:
                w2 = self.params[2]
            if self.locked[3]:
                s2 = self.params[3]
            _pos = interpolate.interp1d(pos[0]*w1-s1,pos[1], fill_value="extrapolate")(x)
            _neg = interpolate.interp1d(neg[0]*w2-s2,neg[1], fill_value="extrapolate")(x)
            return _pos-_neg-y
        return optimize.least_squares(cal_err, params, args=full,verbose=1,bounds=bounds)

    def diff_fit_leastsq(self):
        params = self.params
        full = self.full
        pos = self.pos
        neg =self.neg
        slip_upper = full[0][-1]*0.5
        upper = [params[0]*1.2,slip_upper,params[2]*1.2,slip_upper]
        lower = [0,0,0,0]
        bounds = (lower,upper)
        def cal_err(p,x,y):
            (w1,s1,w2,s2)=p
            if self.locked[0]:
                w1 = self.params[0]
            if self.locked[1]:
                s1 = self.params[1]
            if self.locked[2]:
                w2 = self.params[2]
            if self.locked[3]:
                s2 = self.params[3]
            _pos = interpolate.interp1d(pos[0]*w1-s1,pos[1], fill_value="extrapolate")(x) / w1
            _neg = interpolate.interp1d(neg[0]*w2-s2,neg[1], fill_value="extrapolate")(x) / w2
            return _pos-_neg-y
        return optimize.least_squares(cal_err, params, args=full,verbose=1,bounds=bounds)

