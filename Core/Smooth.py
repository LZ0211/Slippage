#!/usr/bin/env python
# coding=utf-8
import numpy as np

class Smooth:
    def __init__(self,data):
        self.data = data

    def SVD_smooth(self):
        pass

    def SG_smooth(self):
        pass

# import numpy as np
# import random
# import matplotlib.pyplot as plt

# ## 1.待处理信号(400个采样点)
# t = np.arange(0,40,0.1)
# r = [2*random.random() for i in range(400)]
# x = 10*np.sin(1*t)+5*np.sin(2*t)
# xr = x+r

# ## 2.一维数组转换为二维矩阵
# x2list = []
# for i in range(20):
#     x2list.append(xr[i*20:i*20+20])
# x2array = np.array(x2list)

# ## 3.奇异值分解
# U,S,V = np.linalg.svd(x2array)  
# S_list = list(S)
# ## 奇异值求和
# S_sum = sum(S)
# ##奇异值序列归一化
# S_normalization_list = [x/S_sum for x in S_list]

# ## 4.画图
# X = []
# for i in range(len(S_normalization_list)):
#     X.append(i+1)

# fig1 = plt.figure().add_subplot(111)
# fig1.plot(X,S_normalization_list)
# fig1.set_xticks(X)
# fig1.set_xlabel('Rank',size = 15)
# fig1.set_ylabel('Normalize singular values',size = 15)
# plt.show()
    
# ## 5.数据重构
# K = 1 ## 保留的奇异值阶数
# for i in range(len(S_list) - K):
#     S_list[i+K] = 0.0

# S_new = np.mat(np.diag(S_list))
# reduceNoiseMat = np.array(U * S_new * V)
# reduceNoiseList = []
# for i in range(len(x2array)):
#     for j in range(len(x2array)):
#         reduceNoiseList.append(reduceNoiseMat[i][j])
 
# ## 6.去燥效果展示       
# fig2 = plt.figure().add_subplot(111)
# fig2.plot(t,list(xr),'b',label = 'Original data')
# fig2.plot(t,reduceNoiseList,'r-',label = 'Processed data')
# fig2.legend()
# fig2.set_title('Rank is 1')
# fig2.set_xlabel('Sampling point',size = 15)
# fig2.set_ylabel('Value of data',size = 15)
# plt.show()

# # 获得矩阵的字段数量
# def width(lst):
#     i = 0;
#     for j in lst[0]:
#         i += 1
#     return i
 
 
# # 得到每个字段的平均值
# def GetAverage(mat):
#     n = len(mat)
#     m = width(mat)
#     num = [0] * m
#     for i in range(0, m):
#         for j in mat:
#             num[i] += j[i]
#         num[i] = num[i] / n
#     return num
 
 
# # 获得每个字段的标准差
# def GetVar(average, mat):
#     ListMat = []
#     for i in mat:
#         ListMat.append(list(map(lambda x: x[0] - x[1], zip(average, i))))
 
#     n = len(ListMat)
#     m = width(ListMat)
#     num = [0] * m
#     for j in range(0, m):
#         for i in ListMat:
#             num[j] += i[j] * i[j]
#         num[j] /= n
#     return num
 
# # 获得每个字段的标准差
# def GetStandardDeviation(mat):
#     return list(map(lambda x:x**0.5,mat))
# # 对数据集去噪声
# def DenoisMat(mat):
#     average = GetAverage(mat)
#     variance = GetVar(average, mat)
#     standardDeviation=GetStandardDeviation(variance)
#     section = list(map(lambda x: x[0] + 3*x[1], zip(average, standardDeviation)))
#     n = len(mat)
#     m = width(mat)
#     num = [0] * m
#     denoisMat = []
#     noDenoisMat=[]
#     for i in mat:
#         for j in range(0, m):
#             if i[j] > section[j]:
#                 denoisMat.append(i)
#                 break
#             if j==(m-1):
#                 noDenoisMat.append(i)
#     print("去除完噪声的数据：")
#     print(noDenoisMat)
#     print("噪声数据：")
#     return denoisMat