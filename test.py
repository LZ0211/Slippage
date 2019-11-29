#!/usr/bin/env python
# coding=utf-8
from matplotlib import pyplot as plt 
from Core.Engine import Engine
from Core.DataSet import DataSet

fig = plt.figure()
ax = fig.add_subplot(111)

core = Engine()
core.read_pos_data('test/LC043-DisCharge.csv')
core.read_neg_data('test/AC114-Charge.csv')
core.read_full_data('test/All-DisCharge-0%.csv')
core.skip = 3
#core.use_smooth_method('Convolve')
#core.use_smooth_method('Savitzky_Golay')
core.use_smooth_full_data()
core.use_smooth_pos_data()

core.set_full_range(0.2,42)
core.set_neg_range(0.2,350)
core.set_pos_range(0.2,187)

#ax.plot(*core.ref_full_data.diff())
#ax.plot(*core.ref_neg_data.diff())
#ax.plot(*core.ref_pos_data.diff())

core.fit_method = 'dVdQ_fit_leastsq'
param = core.fit_data(0.23,0,0.11,0)
x_data = core.ref_full_data()[0]
pos_data = (x_data,core.ref_pos_data.modify(param[:2],x_data))
neg_data = (x_data,core.ref_neg_data.modify(param[2:4],x_data))
full_data = (x_data,pos_data[1]-neg_data[1])
print(param)
# ax.plot(*core.full_data.data(),label="Full Cell Data")
# ax.plot(*pos_data,label="Postive Half Cell")
# ax.plot(*neg_data,label="Negative Half Cell")
# ax.plot(*full_data,linestyle="--",label="Postive - Negative")

ax.plot(*core.ref_full_data.diff(),label="Full Cell Data")
ax.plot(*DataSet(*pos_data).diff(),label="Postive Half Cell")
ax.plot(*DataSet(*neg_data).diff(),label="Negative Half Cell")
ax.plot(*DataSet(*full_data).diff(),linestyle="--",label="Postive - Negative")

# ax.plot(*core.ref_full_data.diff_invert(),label="Full Cell Data")
# ax.plot(*DataSet(*full_data).diff_invert(),linestyle="--",label="Postive - Negative")

ax.text(0.5, 0.5, 'M(pos)=%8.5f\nS(pos)=%8.5f\nM(neg)=%8.5f\nS(neg)=%8.5f'% tuple(param))


#core.fit_data(0.25,0.0,0.16,0)


#ax.plot(*core.full_data.data())
#ax.plot(*core.smooth_full_data())

#ax.plot(*core.pos_data.data())
#ax.plot(*core.smooth_pos_data())

#ax.plot(*core.neg_data.data())
#ax.plot(*core.smooth_neg_data())

#ax.plot(*core.org_full_dQdV())
#ax.plot(*core.smooth_full_dQdV())

#ax.plot(*core.org_full_dVdQ())
#ax.plot(*core.smooth_full_dVdQ())

#ax.plot(*core.org_pos_dVdQ())
#ax.plot(*core.smooth_pos_dVdQ())

#ax.plot(*core.org_pos_dQdV())
#ax.plot(*core.smooth_pos_dQdV())

#ax.plot(*core.org_neg_dVdQ())
#ax.plot(*core.smooth_neg_dVdQ())

#ax.plot(*core.org_neg_dQdV())
#ax.plot(*core.smooth_neg_dQdV())

#x = core.full_data.x_data

#ax.plot(x, core.pos_discharge_ref.modify([0.2289385,0],x)-core.neg_discharge_ref.modify([0.12529,0],x))

#ax.plot(*core.full_data.data())

#ax.plot()

ax.legend(loc="best")
ax.set_title("Discharge",fontsize=14)
ax.set_ylabel('dV/dQ',fontsize=14)
ax.set_xlabel('Capacity(mAh)',fontsize=14)
plt.show()