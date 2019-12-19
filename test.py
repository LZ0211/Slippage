#!/usr/bin/env python
# coding=utf-8
from matplotlib import pyplot as plt 
from Core import Engine, Smooth
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111)
draw = lambda x,y,z:ax.plot(x,y,label=z)

eg = Engine()
eg.read_pos_data('test/LC043-DisCharge.csv')
eg.skip_window = 1
eg.diff_window = 2
eg.skip_data()
eg.diff_data()
eg.cut_range = [0,187]
eg.cut_data()
#eg.draw_data(draw)
eg.use_smooth(lambda x,y:Smooth.Gaussian(x,y,1.2))
eg.smooth_data()
#eg.draw_data(draw)

eg.read_neg_data('test/AC114-Charge.csv')
eg.skip_window = 2
eg.diff_window = 1
eg.skip_data()
eg.diff_data()
eg.cut_range = [0.2,352]
eg.cut_data()
#eg.draw_data(draw)
eg.use_smooth(lambda x,y:Smooth.Savitzky_Golay(x,y,5))
eg.smooth_data()
#eg.draw_data(draw)

eg.read_full_data('test/All-DisCharge-5%.csv')
eg.skip_window = 2
eg.diff_window = 4
eg.skip_data()
eg.diff_data()
eg.cut_range = [0,43.2]
eg.cut_data()
#eg.draw_data(draw)
eg.use_smooth(lambda x,y:Smooth.Gaussian(x,y,2))
eg.smooth_data()
eg.draw_data(draw)

eg.choise_fitting_datas('pos_skip_diff_cut_smooth','neg_skip_diff_cut_smooth','full_skip_diff_cut_smooth')

eg.init_guess()
eg.params = [0.22,0.2,0.11,0.8]
eg.fit_data()
print(eg.params)
eg.select('pos_skip_diff_cut_smooth_fitting')
eg.draw_data(draw)
eg.select('neg_skip_diff_cut_smooth_fitting')
eg.draw_data(draw)
eg.select('full_skip_diff_cut_smooth_fitting')
eg.draw_data(draw)
ax.legend(loc="best")
plt.show()

