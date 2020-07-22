# coding=utf-8
import re,math,os,json,zipfile
import numpy as np
from scipy.interpolate import interp1d
from .DataSet import DataSet
from .File import File, Table
from .Smooth import Smooth
from .Fitting import Fitting


def hasSubstr(str,patterm):
    try:
        str.index(patterm)
        return True
    except:
        return False

def isSameStr(str,patterm):
    return str == patterm

def isStartWith(str,patterm):
    return isSameStr(patterm,str[:len(patterm)])

class Engine:
    def __init__(self):
        self.datas = {}
        self.selected = ''
        self.for_fitting = ['','','']
        self.for_display = []
        self.params = [1,0,1,0,0,0]
        self.params_max = [1E3,1E3,1E3,1E3,1E3,1E3]
        self.locked = [False,False,False,False,False,False]
        self.scale_param = [1,0]
        self.skip_window = 1
        self.diff_window = 1
        self.cut_range = [0,100]
        self.pos_tag = []
        self.neg_tag = []
        self.fitting_method = 'VQ'
        self.auto_cal = False
        self.max_capacity = 0
        self.auto_scale = False
        self.auto_guess = False
        self.use_max_capacity = False
        self.max_points = 500
        self.suffix_smooth = '_M'
        self.suffix_diff = '_D'
        self.suffix_cut = '_C'
        self.suffix_invert = '_I'
        self.suffix_skip = '_S'
        self.suffix_scaledVdQ = '_F'
        self.suffix_scaleVQ = '_N'
        self.suffix_gen = '_G'

        self.events = {
            'select':[],
            'change':[],
            'fitting':[],
            'cut':[],
            'smooth':[]
        }
        self.trigger = False
        self.collect = Table()

    def new_project(self):
        self.datas = {}
        self.selected = ''
        self.for_fitting = ['','','']
        self.for_display = []
        self.params = [1,0,1,0,0,0]
        self.locked = [False,False,False,False,False,False]
        self.scale_param = [1,0]
        self.skip_window = 1
        self.diff_window = 1
        self.cut_range = [0,100]
        self.pos_tag = []
        self.neg_tag = []
        self.fitting_method = 'VQ'
        self.triggle('change')
        self.triggle('select')
        self.triggle('fitting')

    def save_project(self,filename):
        z = zipfile.ZipFile(filename, 'w' ,zipfile.ZIP_DEFLATED)
        for (k,v) in self.datas.items():
            z.writestr('data/'+k,json.dumps(v.serialize()))
        z.writestr('selected',self.selected)
        z.writestr('for_fitting',json.dumps(self.for_fitting))
        z.writestr('for_display',json.dumps(self.for_display))
        z.writestr('params',json.dumps(self.params))
        z.writestr('locked',json.dumps(self.locked))
        z.writestr('scale_param',json.dumps(self.scale_param))
        z.writestr('cut_range',json.dumps(self.cut_range))
        z.writestr('pos_tag',json.dumps(self.pos_tag))
        z.writestr('neg_tag',json.dumps(self.neg_tag))
        self.collect.save_file()
        z.writestr('collect',open(self.collect.filename,'rb').read())
        z.close()

    def load_project_data(self,z,k):
        try:
            data = json.loads(z.read(k))
            setattr(self,k,data)
        except:
            pass

    def read_project(self,filename):
        z = zipfile.ZipFile(filename)
        files = z.namelist()
        self.datas.clear()
        for file in files:
            if re.match(r'^data\/',file):
                self.datas[file.replace('data/','')] = DataSet(*json.loads(z.read(file)))
        self.selected = z.read('selected').decode('utf-8')
        self.load_project_data(z,'for_fitting')
        self.load_project_data(z,'for_display')
        self.load_project_data(z,'params')
        self.load_project_data(z,'locked')
        self.load_project_data(z,'scale_param')
        self.load_project_data(z,'cut_range')
        self.load_project_data(z,'pos_tag')
        self.load_project_data(z,'neg_tag')
        self.collect = Table(z.read('collect'))
        z.close()
        #兼容旧版本文件
        if len(self.params) < 6:
            self.params = [1,0,1,0,0,0]
            self.locked = [False,False,False,False,False,False]
            self.init_guess()
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

    def auto_cal_param(self,value,idx):
        #print(self.count_fit_data())
        if self.max_capacity <= 0 or not self.auto_cal:
            self.params[idx] = value
            return
        X_max = self.max_capacity
        pos_max = self.datas[self.for_fitting[0]].x_max
        neg_max = self.datas[self.for_fitting[1]].x_max
        if idx == 0:
            X = pos_max * value
            if X >= X_max + self.params_max[1] + self.params_max[4]:
                self.params[1] = self.params_max[1]
                self.params[4] = self.params_max[4]
                self.params[0] = (X_max + self.params[1] + self.params[4]) /  pos_max
            elif X >= X_max + self.params_max[1]:
                self.params[0] = value
                self.params[1] = self.params_max[1]
                self.params[4] = X - X_max - self.params[1]
            elif X >= X_max:
                self.params[0] = value
                self.params[1] = X - X_max - self.params[4]
                #self.params[4] = 0
            else:
                self.params[0] = X_max / pos_max
                self.params[1] = 0
                self.params[4] = 0
        if idx == 1:
            scale = self.params[0]
            X = pos_max * scale
            rs = X-X_max-value
            if rs >= self.params_max[4]:
                #self.params[4] = self.params_max[4]
                #self.params[1] = value
                #self.params[0] = (X_max + self.params[1] + self.params[4]) /  pos_max
                return
            elif rs >= 0:
                self.params[4] = rs
                self.params[1] = value
            else:
                self.params[4] = 0
                self.params[1] = X-X_max
        if idx == 4:
            scale = self.params[0]
            X = pos_max * scale
            ls = X-X_max-value
            if ls >= self.params_max[1]:
                #self.params[4] = value
                #self.params[1] = self.params_max[1]
                #self.params[0] = (X_max + self.params[1] + self.params[4]) /  pos_max
                return
            elif ls >= 0:
                self.params[4] = value
                self.params[1] = ls
            else:
                self.params[4] = X-X_max
                self.params[1] = 0
        if idx == 2:
            X = neg_max * value
            if X >= X_max + self.params_max[3] + self.params_max[5]:
                self.params[3] = self.params_max[1]
                self.params[5] = self.params_max[5]
                self.params[2] = (X_max + self.params[3] + self.params[5]) /  neg_max
            elif X >= X_max + self.params_max[3]:
                self.params[2] = value
                self.params[3] = self.params_max[3]
                self.params[5] = X - X_max - self.params[3]
            elif X >= X_max:
                self.params[2] = value
                self.params[3] = X - X_max - self.params[5]
                #self.params[5] = 0
            else:
                self.params[2] = X_max / neg_max
                self.params[3] = 0
                self.params[5] = 0
        if idx == 3:
            scale = self.params[2]
            X = neg_max * scale
            rs = X-X_max-value
            if rs >= self.params_max[5]:
                #self.params[5] = self.params_max[5]
                #self.params[3] = value
                #self.params[2] = (X_max + self.params[3] + self.params[5]) /  neg_max
                return
            elif rs >= 0:
                self.params[5] = rs
                self.params[3] = value
            else:
                self.params[5] = 0
                self.params[3] = X-X_max
        if idx == 5:
            scale = self.params[2]
            X = neg_max * scale
            ls = X-X_max-value
            if ls >= self.params_max[3]:
                #self.params[5] = value
                #self.params[3] = self.params_max[3]
                #self.params[2] = (X_max + self.params[3] + self.params[5]) /  neg_max
                return
            elif ls >= 0:
                self.params[5] = value
                self.params[3] = ls
            else:
                self.params[5] = X-X_max
                self.params[3] = 0

    def set_param(self,value,idx):
        self.auto_cal_param(value,idx)
        self.triggle('fitting')      

    def set_fitting_method(self,method,state):
        if state == True:
            self.fitting_method = method

    def lock_param(self,idx):
        self.locked[idx] = True
    
    def unlock_param(self,idx):
        self.locked[idx] = False

    def triggle(self,event):
        self.trigger = True
        for f in self.events[event]:
            f()
        self.trigger = False

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
        self.auto_guess and self.init_guess()
        return True

    def select_neg(self,key):
        if not key in self.datas:
            return False
        self.for_fitting[1] = key
        self.auto_guess and self.init_guess()
        return True

    def select_full(self,key):
        if not key in self.datas:
            self.for_fitting[2] = key
            return self.triggle('select')
        self.for_fitting[2] = key
        self.auto_guess and self.init_guess()
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

    def clear_data(self,text):
        changed = False
        if text in self.datas:
            changed = True
            del self.datas[text]
            if text in self.for_fitting:
                idx = self.for_fitting.index(text)
                self.for_fitting[idx] = ''
            if text in self.for_display:
                idx = self.for_display.index(text)
                self.for_display.pop(idx)
            if text in self.pos_tag:
                self.pos_tag.pop(self.pos_tag.index(text))
            if text in self.neg_tag:
                self.neg_tag.pop(self.neg_tag.index(text))
        if not self.selected in self.datas:
            self.selected = ''
        return changed

    def clear_datas(self,texts):
        if len(texts) == 0:
            return
        for text in texts:
            self.clear_data(text)
        self.triggle('change')

    def remove_data(self):
        selected = self.selected
        if selected == '':
            return
        self.clear_data(selected)
        self.triggle('change')

    def batch_remove_data(self):
        selected = self.selected
        if selected == '':
            return
        keys = list(self.datas.keys())
        keys = list(filter(lambda x:isStartWith(x,selected),keys))
        self.clear_datas(keys)
        self.triggle('change')

    def alias_data(self,name):
        selected = self.selected
        if not selected in self.datas:
            return
        data = self.datas[selected]
        self.datas[name] = data
        del self.datas[selected]
        #更新正负极数据标签
        for tag in self.pos_tag:
            if isStartWith(selected,tag):
                self.pos_tag.append(name)
                break
        for tag in self.neg_tag:
            if isStartWith(selected,tag):
                self.neg_tag.append(name)
                break
        #如果修改的对象是在别的列表中已选中
        if selected in self.for_fitting:
            idx = self.for_fitting.index(selected)
            self.for_fitting[idx] = name
        if selected in self.for_display:
            idx = self.for_display.index(selected)
            self.for_display[idx] = name
        #更新UI列表
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
        self.modify_data(self.smooth,self.suffix_smooth)

    def diff_data(self):
        self.modify_data(self.diff,self.suffix_diff)

    def cut_data(self):
        self.modify_data(self.cut,self.suffix_cut)

    def invert_data(self):
        self.modify_data(self.invert,self.suffix_invert)

    def skip_data(self):
        self.modify_data(self.skip,self.suffix_skip)

    def count_fit_data(self):
        value = 0
        if self.for_fitting[0]:
            value += 1
        if self.for_fitting[1]:
            value += 2
        if self.for_fitting[2]:
            value += 4
        return value

    def init_guess(self):
        data_count = self.count_fit_data()
        #模式2
        if self.max_capacity > 0 and self.auto_cal:
            #print(data_count)
            X_max = self.max_capacity
            if data_count % 4 == 1:
                self.params[0] = X_max / self.datas[self.for_fitting[0]].x_max
            if data_count % 4 == 2:
                self.params[2] = X_max / self.datas[self.for_fitting[1]].x_max
            if data_count % 4 == 3:
                self.params[0] = X_max / self.datas[self.for_fitting[0]].x_max
                self.params[2] = X_max / self.datas[self.for_fitting[1]].x_max
            return self.triggle('fitting')
        #模式1
        if data_count < 7:
            return
        if self.locked[0] or self.locked[2]:
            return
        if not self.locked[0]:
            self.params[0] = self.datas[self.for_fitting[2]].x_max / self.datas[self.for_fitting[0]].x_max
            self.params[1] = 0
            self.params[4] = 0
        if not self.locked[2]:
            self.params[2] = self.datas[self.for_fitting[2]].x_max / self.datas[self.for_fitting[1]].x_max
            self.params[3] = 0
            self.params[5] = 0
        self.triggle('fitting')

    def fit_data(self):
        if self.count_fit_data() < 7:
            return
        if self.auto_cal and self.max_capacity > 0:
            return
        pos = self.datas[self.for_fitting[0]]
        neg = self.datas[self.for_fitting[1]]
        full = self.datas[self.for_fitting[2]]
        #print(self.for_fitting,self.params)
        fittor = Fitting(pos,neg,full)
        fittor.init_guess(*self.params[0:4])
        fittor.lock_params(*self.locked[0:4])
        if self.fitting_method == 'VQ':
            params = fittor.fit_leastsq().x
        elif self.fitting_method == 'dVdQ':
            params = fittor.diff_fit_leastsq().x
        params = params.tolist()
        (w1,s1,w2,s2) = params
        self.auto_cal_param(w1,0)
        self.auto_cal_param(s1,1)
        self.auto_cal_param(w2,2)
        self.auto_cal_param(s2,3)
        self.auto_cal_param(full.x_max - w1 * pos.x_max - s1,4)
        self.auto_cal_param(full.x_max - w2 * pos.x_max - s2,5)
        self.triggle('fitting')
        self.auto_scale and self.scale_data()
        return params

    def cal_RMSD(self):
        if self.count_fit_data() < 7:
            return 0
        #模式2
        if self.auto_cal and self.max_capacity > 0:
            return 0
        #模式1
        pos = self.datas[self.for_fitting[0]]()
        neg = self.datas[self.for_fitting[1]]()
        full = self.datas[self.for_fitting[2]]()
        x_data = full[0]
        y_data = full[1]
        (w1,s1,w2,s2) = self.params[0:4]
        pos_y = interp1d(pos[0]*w1-s1,pos[1], fill_value="extrapolate")(x_data)
        neg_y = interp1d(neg[0]*w2-s2,neg[1], fill_value="extrapolate")(x_data)
        if self.fitting_method == 'VQ':
            sub = pos_y-neg_y-y_data
        else:
            sub = pos_y/w1-neg_y/w2-y_data
        return math.sqrt(np.sum(sub*sub)/x_data.size)

    def scale_data(self):
        #模式2
        if self.auto_cal and self.max_capacity > 0:
            suffix = self.suffix_gen
            pos_name = self.for_fitting[0]
            neg_name = self.for_fitting[1]
            if pos_name:
                pos = self.datas[pos_name]
                pos = pos.modify_x(*self.params[0:2])
                self.datas[pos_name+suffix] = pos
            if neg_name:
                neg = self.datas[neg_name]
                neg = neg.modify_x(*self.params[2:4])
                self.datas[neg_name+suffix] = neg
            if pos_name and neg_name:
                key = 'Full_' + re.split(r'[\-_\s]+',pos_name)[0] + '_' + re.split(r'[\-_\s]+',neg_name)[0]
                if self.use_max_capacity:
                    lower = 0
                    upper = self.max_capacity
                else:
                    lower = max(pos.x_min,neg.x_min)
                    upper = min(pos.x_max,neg.x_max)
                x_data = np.linspace(lower, upper, int(max(self.max_capacity,self.max_points)))
                y1 = interp1d(*pos(), fill_value="extrapolate")(x_data)
                y2 = interp1d(*neg(), fill_value="extrapolate")(x_data)
                self.datas[key+suffix] = DataSet(x_data,y1-y2)
                self.for_display = [pos_name+suffix,neg_name+suffix,key+suffix]
            if pos_name or neg_name:
                self.triggle('change')
            return
        #模式1
        if self.count_fit_data() < 7:
            return
        pos_name,neg_name,full_name = self.for_fitting
        pos = self.datas[pos_name]
        neg = self.datas[neg_name]
        full = self.datas[full_name]
        if self.fitting_method == 'VQ':
            suffix = self.suffix_scaleVQ
            pos = pos.modify_x(*self.params[0:2])
            neg = neg.modify_x(*self.params[2:4])
        else:
            suffix = self.suffix_scaledVdQ
            pos = pos.modify_x(*self.params[0:2]).modify_y(1/self.params[0],0)
            neg = neg.modify_x(*self.params[2:4]).modify_y(1/self.params[2],0)
        x_data,y_data = full()
        pos_y = interp1d(*pos(), fill_value="extrapolate")(x_data)
        neg_y = interp1d(*neg(), fill_value="extrapolate")(x_data)
        self.datas[pos_name + suffix] = pos
        self.datas[neg_name + suffix] = neg
        self.datas[full_name + suffix] = DataSet(x_data,pos_y-neg_y)
        self.for_display = [pos_name + suffix, neg_name + suffix, full_name + suffix, full_name]
        self.triggle('change')

    def display_all(self):
        self.for_display = self.datas.keys()
        self.triggle('change')

    def undisplay_all(self):
        self.for_display = []
        self.triggle('change')
