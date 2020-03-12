#!/usr/bin/env python
# coding=utf-8
import re,math,os,json,zipfile
import numpy as np
from scipy import interpolate
from .DataSet import DataSet
from .File import File, Table
from .Smooth import Smooth
from .Fitting import Fitting

class Engine:
    def __init__(self):
        self.datas = {}
        self.selected = ''
        self.for_fitting = ['','','']
        self.params = [1,0,1,0]
        self.locked = [False,False,False,False]
        self.scale_param = [1,0]
        self.skip_window = 1
        self.diff_window = 1
        self.cut_range = [0,100]
        self.pos_tag = []
        self.neg_tag = []
        self.fitting_method = 'VQ'
        self.events = {
            'select':[],
            'change':[],
            'fitting':[],
            'cut':[],
            'smooth':[]
        }
        self.collect = Table()

    def save_project(self,filename):
        z = zipfile.ZipFile(filename, 'w' ,zipfile.ZIP_DEFLATED)
        for (k,v) in self.datas.items():
            z.writestr('data/'+k,json.dumps(v.serialize()))
        z.writestr('selected',self.selected)
        z.writestr('for_fitting',json.dumps(self.for_fitting))
        z.writestr('params',json.dumps(self.params))
        z.writestr('locked',json.dumps(self.locked))
        z.writestr('scale_param',json.dumps(self.scale_param))
        z.writestr('cut_range',json.dumps(self.cut_range))
        z.writestr('pos_tag',json.dumps(self.pos_tag))
        z.writestr('neg_tag',json.dumps(self.neg_tag))
        self.collect.save_file()
        z.writestr('collect',open(self.collect.filename,'rb').read())
        z.close()

    def read_project(self,filename):
        z = zipfile.ZipFile(filename)
        files = z.namelist()
        self.datas.clear()
        for file in files:
            if re.match(r'^data\/',file):
                self.datas[file.replace('data/','')] = DataSet(*json.loads(z.read(file)))
        self.selected = z.read('selected').decode('utf-8')
        self.for_fitting = json.loads(z.read('for_fitting'))
        self.params = json.loads(z.read('params'))
        self.locked = json.loads(z.read('locked'))
        self.scale_param = json.loads(z.read('scale_param'))
        self.cut_range = json.loads(z.read('cut_range'))
        self.pos_tag = json.loads(z.read('pos_tag'))
        self.neg_tag = json.loads(z.read('neg_tag'))
        self.collect = Table(z.read('collect'))
        z.close()
        self.triggle('change')
        self.triggle('select')
        self.triggle('fitting')

    def collect_params(self):
        symbol = self.for_fitting[2]
        if not symbol in self.datas:
            return
        storage = self.datas[symbol].x_max
        self.collect.write_params([storage,symbol,self.params[0],self.params[1],self.params[2],self.params[3],self.cal_RMSD()])

    def set_skip_window(self,value):
        self.skip_window = value

    def set_diff_window(self,value):
        self.diff_window = value

    def set_cut_from(self,value):
        self.cut_range[0] = value

    def set_cut_to(self,value):
        self.cut_range[1] = value

    def set_param(self,value,idx):
        self.params[idx] = value

    def set_fitting_method(self,method,state):
        if state == True:
            self.fitting_method = method

    def lock_param(self,idx):
        self.locked[idx] = True
    
    def unlock_param(self,idx):
        self.locked[idx] = False

    def triggle(self,event):
        for f in self.events[event]:
            f()

    def bind(self,event,f):
        self.events[event].append(f)

    def select(self,key):
        if not key in self.datas:
            return False
        self.selected = key
        self.triggle('select')
        return True

    def select_pos(self,key):
        if not key in self.datas:
            return False
        self.for_fitting[0] = key
        self.init_guess()
        return True

    def select_neg(self,key):
        if not key in self.datas:
            return False
        self.for_fitting[1] = key
        self.init_guess()
        return True

    def select_full(self,key):
        if not key in self.datas:
            return False
        self.for_fitting[2] = key
        self.init_guess()
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

    def data(self,key=None):
        if self.selected in self.datas:
            return self.datas[self.selected]()

    def add_data(self,key,val):
        idx = 0
        _key = key
        while _key in self.datas:
            idx += 1
            _key = key + str(idx)
        self.datas[_key] = val
        self.triggle('change')        

    def use_smooth(self,fn):
        self.smooth = lambda data:DataSet(*fn(*data()))

    def get_data(self):
        if self.selected in self.datas:
            return self.datas[self.selected]

    def clear_datas(self,text,full=False):
        if full == True:
            reg = r'^%s$' % text
        else:
            reg = r'^%s' % text
        keys = list(self.datas.keys())
        changed = False
        for k in keys:
            if re.match(reg,k):
                changed = True
                del self.datas[k]
                if k in self.for_fitting:
                    idx = self.for_fitting.index(k)
                    self.for_fitting[idx] = ''
        if not self.selected in self.datas:
            self.selected = ''
        if changed:
            self.triggle('change')

    def remove_datas(self):
        if self.selected != '':
            self.clear_datas(self.selected)

    def remove_data(self):
        if self.selected != '':
            self.clear_datas(self.selected,True)

    def alias_data(self,name):
        selected = self.selected
        if not selected in self.datas:
            return
        data = self.datas[selected]
        self.datas[name] = data
        del self.datas[selected]
        if re.match('|'.join(self.pos_tag),selected):
            self.pos_tag.append(name)
        if re.match('|'.join(self.neg_tag),selected):
            self.neg_tag.append(name)
        #修改已选中
        if selected in self.for_fitting:
            idx = self.for_fitting.index(selected)
            self.for_fitting[idx] = name
        self.selected = name
        self.triggle('change')
        self.triggle('select')
        self.triggle('fitting')

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

    def read_pos_data(self,filename,define=None):
        data = self.read_data(filename,define)
        (filepath, tempfilename) = os.path.split(filename)
        (filename, filetype) = os.path.splitext(tempfilename)
        self.pos_tag.append(filename)
        self.add_data(filename,DataSet(*data))
        self.select(filename)

    def read_neg_data(self,filename,define=None):
        data = self.read_data(filename,define)
        (filepath, tempfilename) = os.path.split(filename)
        (filename, filetype) = os.path.splitext(tempfilename)
        self.neg_tag.append(filename)
        self.add_data(filename,DataSet(*data))
        self.select(filename)

    def read_full_data(self,filename,define=None):
        data = self.read_data(filename,define)
        (filepath, tempfilename) = os.path.split(filename)
        (filename, filetype) = os.path.splitext(tempfilename)
        self.add_data(filename,DataSet(*data))
        self.select(filename)

    def modify_data(self,func,name):
        key = self.selected
        if key in self.datas:
            new_name = key+name
            self.add_data(new_name,func(self.datas[key]))
            self.select(new_name)

    def smooth_data(self):
        self.modify_data(self.smooth,'_M')

    def diff_data(self):
        self.modify_data(self.diff,'_D')

    def cut_data(self):
        self.modify_data(self.cut,'_C')

    def invert_data(self):
        self.modify_data(self.invert,'_I')

    def skip_data(self):
        self.modify_data(self.skip,'_S')

    def init_guess(self):
        if self.for_fitting[0]=='' or self.for_fitting[1]=='' or self.for_fitting[2]=='':
            return
        if self.locked[0] or self.locked[2]:
            return
        if not self.locked[0]:
            self.params[0] = self.datas[self.for_fitting[2]].x_max / self.datas[self.for_fitting[0]].x_max
        if not self.locked[2]:
            self.params[2] = self.datas[self.for_fitting[2]].x_max / self.datas[self.for_fitting[1]].x_max
        self.triggle('fitting')

    def fit_data(self):
        if self.for_fitting[0]=='' or self.for_fitting[1]=='' or self.for_fitting[2]=='':
            return
        pos = self.datas[self.for_fitting[0]]
        neg = self.datas[self.for_fitting[1]]
        full = self.datas[self.for_fitting[2]]
        #print(self.for_fitting,self.params)
        fittor = Fitting(pos,neg,full)
        fittor.init_guess(*self.params)
        fittor.lock_params(*self.locked)
        if self.fitting_method == 'VQ':
            params = fittor.fit_leastsq().x
        elif self.fitting_method == 'dVdQ':
            params = fittor.diff_fit_leastsq().x
        self.params = params.tolist()
        (w1,s1,w2,s2) = self.params
        x_data = full.x_data
        pos_y = interpolate.interp1d(pos.x_data*w1-s1,pos.y_data, fill_value="extrapolate")(x_data)
        neg_y = interpolate.interp1d(neg.x_data*w2-s2,neg.y_data, fill_value="extrapolate")(x_data)
        if self.fitting_method == 'VQ':
            self.datas[self.for_fitting[0]+'_F'] = DataSet(x_data,pos_y)
            self.datas[self.for_fitting[1]+'_F'] = DataSet(x_data,neg_y)
            self.datas[self.for_fitting[2]+'_F'] = DataSet(x_data,pos_y-neg_y)
        elif self.fitting_method == 'dVdQ':
            self.datas[self.for_fitting[0]+'_F'] = DataSet(x_data,pos_y/w1)
            self.datas[self.for_fitting[1]+'_F'] = DataSet(x_data,neg_y/w2)
            self.datas[self.for_fitting[2]+'_F'] = DataSet(x_data,pos_y/w1-neg_y/w2)
        self.triggle('change')
        self.triggle('fitting')
        return params

    def cal_RMSD(self):
        if self.for_fitting[0]=='' or self.for_fitting[1]=='' or self.for_fitting[2]=='':
            return 0
        pos = self.datas[self.for_fitting[0]]()
        neg = self.datas[self.for_fitting[1]]()
        full = self.datas[self.for_fitting[2]]()
        x_data = full[0]
        y_data = full[1]
        (w1,s1,w2,s2) = self.params
        pos_y = interpolate.interp1d(pos[0]*w1-s1,pos[1], fill_value="extrapolate")(x_data)
        neg_y = interpolate.interp1d(neg[0]*w2-s2,neg[1], fill_value="extrapolate")(x_data)
        if self.fitting_method == 'VQ':
            sub = pos_y-neg_y-y_data
        else:
            sub = pos_y/w1-neg_y/w2-y_data
        return math.sqrt(np.sum(sub*sub)/x_data.size)

    def scale_data(self):
        pos = None
        neg = None
        key = self.for_fitting[0]
        if key != '':
            pos = self.datas[key]
            if self.fitting_method == 'VQ':
                self.datas[key+'_N'] = pos.modify_x(*self.params[0:2])
            else:
                self.datas[key+'_N'] = pos.modify_x(*self.params[0:2]).modify_y(1/self.params[0],0)
            pos = self.datas[key+'_N']
        key = self.for_fitting[1]
        if key != '':
            neg = self.datas[key]
            if self.fitting_method == 'VQ':
                self.datas[key+'_N'] = neg.modify_x(*self.params[2:4])
            else:
                self.datas[key+'_N'] = neg.modify_x(*self.params[2:4]).modify_y(1/self.params[2],0)
            neg = self.datas[key+'_N']
        key = self.for_fitting[2]
        if key == '':
            if pos != None or neg != None:
                self.triggle('change')
            return
        if pos != None and neg != None:
            full = self.datas[self.for_fitting[2]]()
            x_data = full[0]
            pos_y = interpolate.interp1d(*pos(), fill_value="extrapolate")(x_data)
            neg_y = interpolate.interp1d(*neg(), fill_value="extrapolate")(x_data)
            self.datas[key+'_N'] = DataSet(x_data,pos_y-neg_y)
            self.triggle('change')
