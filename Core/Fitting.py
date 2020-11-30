# coding=utf-8
from scipy.optimize import least_squares
from scipy.interpolate import interp1d
import numpy as np

class Fitting:
    Algorithm = "Manhattan"
    def __init__(self,pos,neg,full):
        self.pos = pos()
        self.neg = neg()
        self.full = full()
        self.params = [1.0,0.0,1.0,0.0]
        self.locked = [False,False,False,False]
        self.select_distance()
    
    def init_guess(self,a,b,c,d):
        self.params = [a,b,c,d]

    def lock_params(self,a,b,c,d):
        self.locked = [a,b,c,d]

    def select_distance(self):
        if self.Algorithm == "Manhattan":
            self.distance = self.Manhattan
        elif self.Algorithm == "Euclidean":
            self.distance = self.Euclidean
        elif self.Algorithm == "Minkowski":
            self.distance = self.Minkowski
        elif self.Algorithm == "Cosine":
            self.distance = self.Cosine

    def Manhattan(self,x,y):
        return x-y

    def Euclidean(self,x,y):
        return (x-y) ** 2

    def Minkowski(self,x,y):
        return (x-y) ** 3

    def Cosine(self,x,y):
        return np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))

    def fit_leastsq(self):
        params = self.params
        full = self.full
        pos = self.pos
        neg =self.neg
        slip_upper = full[0][-1]*0.66
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
            _x = np.linspace(x[0],x[-1], int(x[-1]/0.2) )
            _pos = interp1d(pos[0]*w1-s1,pos[1], fill_value="extrapolate")(_x)
            _neg = interp1d(neg[0]*w2-s2,neg[1], fill_value="extrapolate")(_x)
            _cal =  _pos - _neg
            _ful = interp1d(x,y, fill_value="extrapolate")(_x)
            return self.distance(_cal,_ful)
        return least_squares(cal_err, params, args=full,verbose=1,bounds=bounds)

    def diff_fit_leastsq(self):
        params = self.params
        full = self.full
        pos = self.pos
        neg =self.neg
        slip_upper = full[0][-1]*0.66
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
            _x = np.linspace(x[0],x[-1], int(x[-1]/0.2) )
            _pos = interp1d(pos[0]*w1-s1,pos[1], fill_value="extrapolate")(_x) / w1
            _neg = interp1d(neg[0]*w2-s2,neg[1], fill_value="extrapolate")(_x) / w2
            _cal =  _pos - _neg
            _ful = interp1d(x,y, fill_value="extrapolate")(_x)
            return self.distance(_cal,_ful)
        return least_squares(cal_err, params, args=full,verbose=1,bounds=bounds)

