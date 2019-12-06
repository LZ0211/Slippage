#!/usr/bin/env python
# coding=utf-8
from matplotlib import pyplot as plt 
from Core.Engine import Engine
from Core.DataSet import DataSet
from Core.File import File
import numpy as np
import re,os,sys

core = Engine()
#默认值
core.skip = 3
core.fit_method = 'dVdQ_fit_leastsq'
core.use_smooth_method('Savitzky_Golay')
core.param = [1,0,1,0]

def reset():
    core.ref_pos_data = core.pos_data
    core.ref_neg_data = core.neg_data
    core.ref_full_data = core.full_data

def plot_pos_VQ_curve():
    if core.ref_pos_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.ref_pos_data(),label="Postive Half Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('Voltage(V)',fontsize=14)
    ax.set_xlabel('Capacity(mAh)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_neg_VQ_curve():
    if core.ref_neg_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.ref_neg_data(),label="Negative Half Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('Voltage(V)',fontsize=14)
    ax.set_xlabel('Capacity(mAh)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_full_VQ_curve():
    if core.ref_full_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.ref_full_data(),label="Full Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('Voltage(V)',fontsize=14)
    ax.set_xlabel('Capacity(mAh)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_pos_dVdQ_curve():
    if core.ref_pos_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.ref_pos_data.diff(),label="Postive Half Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('dV/dQ',fontsize=14)
    ax.set_xlabel('Capacity(mAh)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_neg_dVdQ_curve():
    if core.ref_neg_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.ref_neg_data.diff(),label="Negative Half Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('dV/dQ',fontsize=14)
    ax.set_xlabel('Capacity(mAh)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_full_dVdQ_curve():
    if core.ref_full_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.ref_full_data.diff(),label="Full Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('dV/dQ',fontsize=14)
    ax.set_xlabel('Capacity(mAh)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_pos_dQdV_curve():
    if core.ref_pos_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.ref_pos_data.diff_invert(),label="Postive Half Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('dQ/dV',fontsize=14)
    ax.set_xlabel('Voltage(V)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_neg_dQdV_curve():
    if core.ref_neg_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.ref_neg_data.diff_invert(),label="Negative Half Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('dQ/dV',fontsize=14)
    ax.set_xlabel('Voltage(V)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_full_dQdV_curve():
    if core.ref_full_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.ref_full_data.diff_invert(),label="Full Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('dQ/dV',fontsize=14)
    ax.set_xlabel('Voltage(V)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_smooth_pos_VQ_curve():
    if core.pos_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.smooth_pos_data(),label="Postive Half Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('Voltage(V)',fontsize=14)
    ax.set_xlabel('Capacity(mAh)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_smooth_neg_VQ_curve():
    if core.neg_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.smooth_neg_data(),label="Negative Half Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('Voltage(V)',fontsize=14)
    ax.set_xlabel('Capacity(mAh)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_smooth_full_VQ_curve():
    if core.full_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.smooth_full_data(),label="Full Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('Voltage(V)',fontsize=14)
    ax.set_xlabel('Capacity(mAh)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_smooth_pos_dVdQ_curve():
    if core.pos_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.smooth_pos_dVdQ(),label="Postive Half Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('dV/dQ',fontsize=14)
    ax.set_xlabel('Capacity(mAh)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_smooth_neg_dVdQ_curve():
    if core.neg_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.smooth_neg_dVdQ(),label="Negative Half Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('dV/dQ',fontsize=14)
    ax.set_xlabel('Capacity(mAh)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_smooth_full_dVdQ_curve():
    if core.full_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.smooth_full_dVdQ(),label="Full Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('dV/dQ',fontsize=14)
    ax.set_xlabel('Capacity(mAh)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_smooth_pos_dQdV_curve():
    if core.pos_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.smooth_pos_dQdV(),label="Postive Half Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('dQ/dV',fontsize=14)
    ax.set_xlabel('Voltage(V)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_smooth_neg_dQdV_curve():
    if core.neg_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.smooth_neg_dQdV(),label="Negative Half Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('dQ/dV',fontsize=14)
    ax.set_xlabel('Voltage(V)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def plot_smooth_full_dQdV_curve():
    if core.full_data == None:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.smooth_full_dQdV(),label="Full Cell")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('dQ/dV',fontsize=14)
    ax.set_xlabel('Voltage(V)',fontsize=14)
    ax.legend(loc="best")
    plt.show()

def set_init_guess(x):
    core.param = tuple(map(float,re.split(r'\s+',x)))

def start_fitting():
    res = core.fit_data(*core.param)
    core.param = res
    print('M(pos)=%8.5f\nS(pos)=%8.5f\nM(neg)=%8.5f\nS(neg)=%8.5f'% tuple(core.param))
    show_menu({
        "返回" : return_menu,
        "绘制拟合的VQ曲线" : plot_fitting_VQ_curve,
        "绘制拟合的dVdQ曲线" : plot_fitting_dVdQ_curve,
        "导出拟合结果" : export_fitting_result
    },False)

def plot_fitting_VQ_curve():
    if core.neg_data == None:
        return
    if core.pos_data == None:
        return
    if core.full_data == None:
        return
    param = core.param
    x_data = core.ref_full_data()[0]
    pos_data = core.ref_pos_data.modify(param[:2],x_data)
    neg_data = core.ref_neg_data.modify(param[2:4],x_data)
    full_data = (x_data,pos_data[1]-neg_data[1])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.ref_full_data(),label="Full Cell Data")
    ax.plot(*pos_data,label="Postive Half Cell")
    ax.plot(*neg_data,label="Negative Half Cell")
    ax.plot(*full_data,linestyle="--",label="Postive - Negative")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('Voltage(V)',fontsize=14)
    ax.set_xlabel('Capacity(mAh)',fontsize=14)
    ax.text(0.5, 0.5, 'M(pos)=%8.5f\nS(pos)=%8.5f\nM(neg)=%8.5f\nS(neg)=%8.5f'% tuple(param))
    ax.legend(loc="best")
    plt.show()

def plot_fitting_dVdQ_curve():
    if core.neg_data == None:
        return
    if core.pos_data == None:
        return
    if core.full_data == None:
        return
    param = core.param
    x_data = core.ref_full_data()[0]
    pos_data = core.ref_pos_data.modify(param[:2],x_data)
    neg_data = core.ref_neg_data.modify(param[2:4],x_data)
    full_data = (x_data,pos_data[1]-neg_data[1])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(*core.ref_full_data.diff(),label="Full Cell Data")
    ax.plot(*DataSet(*pos_data).diff(),label="Postive Half Cell")
    ax.plot(*DataSet(*neg_data).diff(),label="Negative Half Cell")
    ax.plot(*DataSet(*full_data).diff(),linestyle="--",label="Postive - Negative")
    ax.set_title("Discharge",fontsize=14)
    ax.set_ylabel('dV/dQ',fontsize=14)
    ax.set_xlabel('Capacity(mAh)',fontsize=14)
    ax.text(0.01, 0.001, 'M(pos)=%8.5f\nS(pos)=%8.5f\nM(neg)=%8.5f\nS(neg)=%8.5f'% tuple(param))
    ax.legend(loc="best")
    plt.show()

def export_fitting_result():
    param = core.param
    x_data = core.ref_full_data()[0]
    pos_data = core.ref_pos_data.modify(param[:2],x_data)
    neg_data = core.ref_neg_data.modify(param[2:4],x_data)
    full_data = (x_data,pos_data[1]-neg_data[1])
    File('dVdQ-full.txt').write_data(np.array(full_data).T)
    File('dVdQ-pos.txt').write_data(np.array(pos_data).T)
    File('dVdQ-neg.txt').write_data(np.array(neg_data).T)

def reset_pos():
    core.ref_pos_data = core.pos_data

def reset_neg():
    core.ref_neg_data = core.neg_data

def reset_full():
    core.ref_full_data = core.full_data

history = []

def show_menu(menu,cls=True):
    if cls == True:
        os.system('cls')
    global history
    history.append(menu)
    i = 0
    arr = []
    for (k,v) in menu.items():
        print('[%s] %s'%(i,k))
        arr.append(v)
        i += 1
    try:
        idx = int(input('请选择：'))
        fn = arr[idx]
        if fn.__code__.co_argcount == 0:
            fn()
        else:
            val = input('请输入：')
            fn(val)
        if arr[0] == return_menu:
            refresh_menu()
        else:
            return_menu()
    except Exception as e:
        print(e)
        refresh_menu(False)
        pass


def return_menu():
    global history
    if len(history) >= 2:
        history.pop(-1)
        show_menu(history.pop(-1))
    else:
        refresh_menu()

def refresh_menu(cls=True):
    global history
    show_menu(history.pop(-1),cls)

main_menu = {
    "退出" : lambda :exit(),
    "输入正极数据" : lambda x:core.read_pos_data(x),
    "输入负极数据" : lambda x:core.read_neg_data(x),
    "输入全电池数据" : lambda x:core.read_full_data(x),
    "下一步" : lambda : show_menu(sub_menu)
}

sub_menu = {
    "返回" : return_menu,
    "显示曲线" : lambda :show_menu(curve_menu),
    "平滑曲线" : lambda :show_menu(smooth_menu),
    "拟合曲线" : lambda :show_menu(fitting_menu)
}

curve_menu = {
    "返回" : return_menu,
    "正极曲线" : lambda : show_menu(pos_curve_menu),
    "负极曲线" : lambda : show_menu(neg_curve_menu),
    "全电池曲线" : lambda : show_menu(full_curve_menu)
}

pos_curve_menu = {
    "返回" : return_menu,
    "VQ曲线" : plot_pos_VQ_curve,
    "dVdQ曲线" : plot_pos_dVdQ_curve,
    "dQdV曲线" : plot_pos_dQdV_curve
}

neg_curve_menu = {
    "返回" : return_menu,
    "VQ曲线" : plot_neg_VQ_curve,
    "dVdQ曲线" : plot_neg_dVdQ_curve,
    "dQdV曲线" : plot_neg_dQdV_curve
}

full_curve_menu = {
    "返回" : return_menu,
    "VQ曲线" : plot_full_VQ_curve,
    "dVdQ曲线" : plot_full_dVdQ_curve,
    "dQdV曲线" : plot_full_dQdV_curve
}

smooth_menu = {
    "返回" : return_menu,
    "正极曲线平滑" : lambda : show_menu(pos_smooth_menu),
    "负极曲线平滑" : lambda : show_menu(neg_smooth_menu),
    "全电池曲线平滑" : lambda : show_menu(full_smooth_menu)
}

filter_menu = {
    '插值滤波' : lambda : core.use_smooth_method('Spline'),
    '改进插值滤波' : lambda : core.use_smooth_method('Adv_Spline'),
    '滑动平均滤波' : lambda : core.use_smooth_method('Convolve'),
    'Savitzky Golay滤波[默认]' : lambda : core.use_smooth_method('Savitzky_Golay')
}

pos_smooth_menu = {
    "返回" : return_menu,
    "重置" : reset_pos,
    "设置采点间隔" : lambda x:core.ref_pos_data.skip_data(int(x)),
    "设置噪声因子" : lambda x:core.set_pos_noise_factor(float(x)),
    "切换滤波器" : lambda :show_menu(filter_menu),
    "显示平滑后的曲线" : lambda : show_menu(smooth_pos_curve_menu),
    "使用平滑后的数据进行拟合": lambda :core.use_smooth_pos_data()
}

smooth_pos_curve_menu = {
    "返回" : return_menu,
    "VQ曲线" : plot_smooth_pos_VQ_curve,
    "dVdQ曲线" : plot_smooth_pos_dVdQ_curve,
    "dQdV曲线" : plot_smooth_pos_dQdV_curve
}

neg_smooth_menu = {
    "返回" : return_menu,
    "重置" : reset_neg,
    "设置采点间隔" : lambda x:core.ref_neg_data.skip_data(int(x)),
    "设置噪声因子" : lambda x:core.set_neg_noise_factor(float(x)),
    "切换滤波器" : lambda :show_menu(filter_menu),
    "显示平滑后的曲线" : lambda : show_menu(smooth_neg_curve_menu),
    "使用平滑后的数据进行拟合": lambda :core.use_smooth_neg_data()
}

smooth_neg_curve_menu = {
    "返回" : return_menu,
    "VQ曲线" : plot_smooth_neg_VQ_curve,
    "dVdQ曲线" : plot_smooth_neg_dVdQ_curve,
    "dQdV曲线" : plot_smooth_neg_dQdV_curve
}

full_smooth_menu = {
    "返回" : return_menu,
    "重置" : reset_full,
    "设置采点间隔" : lambda x:core.ref_full_data.skip_data(int(x)),
    "设置噪声因子" : lambda x:core.set_full_noise_factor(float(x)),
    "切换滤波器" : lambda :show_menu(filter_menu),
    "显示平滑后的曲线" : lambda : show_menu(smooth_full_curve_menu),
    "使用平滑后的数据进行拟合": lambda :core.use_smooth_full_data()
}

smooth_full_curve_menu = {
    "返回" : return_menu,
    "VQ曲线" : plot_smooth_full_VQ_curve,
    "dVdQ曲线" : plot_smooth_full_dVdQ_curve,
    "dQdV曲线" : plot_smooth_full_dQdV_curve
}

fitting_methods = {
    "返回" : return_menu,
    'V-Q曲线最小二乘法拟合':lambda :exec("core.fit_method = 'VQ_fit_leastsq'"),
    'dV/dQ-Q曲线最小二乘法拟合':lambda :exec("core.fit_method = 'dVdQ_fit_leastsq'")
}

fitting_menu = {
    "返回" : return_menu,
    "选择拟合方式" : lambda : show_menu(fitting_methods),
    "设置初猜" : set_init_guess,
    "开始拟合" : start_fitting,
    "设置正极曲线拟合区间" :  lambda x: core.set_pos_range(*tuple(map(float,re.split(r'\s+',x)))),
    "设置负极曲线拟合区间" :  lambda x: core.set_neg_range(*tuple(map(float,re.split(r'\s+',x)))),
    "设置全电池曲线拟合区间" :  lambda x: core.set_full_range(*tuple(map(float,re.split(r'\s+',x)))),
}

show_menu(main_menu)