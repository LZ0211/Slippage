#!/usr/bin/env python
# coding=utf-8
import numpy as np

class Data:
    def __init__(self,data):
        self.data = data
        self.length = len(data)

    def searchX(self,val):
        low = 0
        up = len(self.data) - 1
        while low < up:
            mid = int((low + up)/2)
            if mid == low:
                return mid
            elif self.data[mid][0] < val:
                low = mid
            elif self.data[mid][0] > val:
                up = mid - 1
        return low

    def point(self,x):
        idx = self.searchX(x)
        # if idx == self.length - 1:
        #     return -1
        # if idx == 0:
        #     return -1
        (x1,y1) = self.data[idx]
        (x2,y2) = self.data[idx+1]
        p = x2- x1
        return (y1*(x2-x)+y2*(x-x1))/p

    def shift(self,B):
        return list(map(lambda x:[x[0],self.point(x[0]+B)],self.data))

    def scale(self,A):
        return list(map(lambda x:[x[0],self.point(A*x[0])],self.data))

    def modify(self,A,B):
        return list(map(lambda x:[x[0],self.point(A*x[0]+B)],self.data))

