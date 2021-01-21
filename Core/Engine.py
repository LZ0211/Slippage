# coding=utf-8
import re,math,os,json,zipfile,urllib
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
        #保存数据
        self.datas = {}
        #数据序列
        self.order = []
        #当前选择的数据，和UI绑定联动
        self.selected = ''
        #用于拟合的三组数据名称
        self.for_fitting = ['','','']
        #当前显示的数据，由前端更新数据
        self.for_display = []
        #拟合参数
        self.params = [1,0,1,0,0,0]
        self.params_max = [1E3,2E3,1E3,2E3,2E3,2E3]
        self.locked = [False,False,False,False,False,False]
        self.scale_param = [1,0]
        #采点间隔
        self.skip_window = 1
        #微分间隔
        self.diff_window = 1
        #插值阶数
        self.inter_order = 3
        #数据切割范围
        self.cut_range = [0,100]
        #正极数据名称
        self.pos_tag = []
        #负极数据米高处
        self.neg_tag = []
        #拟合算法
        self.fitting_algorithm = "Manhattan"
        #拟合方式
        self.fitting_method = 'VQ'
        #是否自动选中最新生成的数据
        self.auto_select = True
        #是否自动计算拟合参数
        self.auto_cal = False
        #设置最大容量，用于有半电池数据生成全电池数据
        self.max_capacity = 0
        #拟合后是否自动缩放
        self.auto_scale = False
        #用于拟合的三组数据的时候是否自动计算初猜
        self.auto_guess = False
        #是否在全电池容量区间内生成新的数据点，若为否则基于原始数据和缩放平移参数生成，包含范围以外的数据点
        self.use_max_capacity = False
        #总的数据点数，用于计算RMSD和生成拟合的数据
        self.max_points = 1000
        #是否记录操作
        self.record_operation = False
        #文件编辑后缀
        self.suffixs = {
            "smooth":"_M",
            "diff":"_D",
            "cut":"_C",
            "invert":"_I",
            "skip":"_S",
            "inter": "_P",
            "scaledVdQ":"_F",
            "scaleVQ":"_N",
            "gen":"_G",
            "normalize": "_SOC",
            "capacity":"_CAP"
        }

        self.events = {
            'select':[],
            'change':[],
            'fitting':[],
            'cut':[],
            'smooth':[]
        }
        self.trigger = False
        self.collect = Table()
        self.records = []

    #新建项目文件的时候自动初始化
    def new_project(self):
        self.datas = {}
        self.order = []
        self.records = []
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
        #触发更新UI
        self.triggle('change')
        self.triggle('select')
        self.triggle('fitting')

    #保存项目文件
    def save_project(self,filename):
        z = zipfile.ZipFile(filename, 'w' ,zipfile.ZIP_DEFLATED)
        for (k,v) in self.datas.items():
            z.writestr('data/'+urllib.parse.quote(k),json.dumps(v.serialize()))
        z.writestr('selected',self.selected)
        z.writestr('order',json.dumps(self.order))
        z.writestr('for_fitting',json.dumps(self.for_fitting))
        z.writestr('for_display',json.dumps(self.for_display))
        z.writestr('params',json.dumps(self.params))
        z.writestr('locked',json.dumps(self.locked))
        z.writestr('scale_param',json.dumps(self.scale_param))
        z.writestr('cut_range',json.dumps(self.cut_range))
        z.writestr('pos_tag',json.dumps(self.pos_tag))
        z.writestr('neg_tag',json.dumps(self.neg_tag))
        z.writestr('records',json.dumps(self.records))
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
                try:
                    name = urllib.parse.unquote(file).replace('data/','')
                    #print(file,name)
                    self.add_data(name,DataSet(*json.loads(z.read(file))),False)
                except Exception as identify:
                    print(identify)
                    pass
        self.selected = z.read('selected').decode('utf-8')
        self.load_project_data(z,'order')
        self.load_project_data(z,'for_fitting')
        self.load_project_data(z,'for_display')
        self.load_project_data(z,'params')
        self.load_project_data(z,'locked')
        self.load_project_data(z,'scale_param')
        self.load_project_data(z,'cut_range')
        self.load_project_data(z,'pos_tag')
        self.load_project_data(z,'neg_tag')
        self.load_project_data(z,'records')
        try:
            self.collect = Table(z.read('collect'))
        except:
            pass
        z.close()
        #兼容旧版本文件
        if len(self.params) < 6:
            self.params = [1,0,1,0,0,0]
            self.locked = [False,False,False,False,False,False]
            self.init_guess()
        self.triggle('change')
        self.triggle('select')
        self.triggle('fitting')

    def log_record(self,operation,param,source,target):
        self.records.append([operation,param,source,target])

    def read_record(self,name,all=False):
        stack = []
        while name:
            found = False
            for record in self.records[::-1]:
                if record[3] == name:
                    stack.append(record)
                    found = True
                    if all:
                        name = record[2]
                    else:
                        return stack
            if not found:
                return stack

    def collect_params(self):
        if self.count_fit_data() < 7:
            return
        symbol = self.for_fitting[2]
        pos = self.for_fitting[0]
        neg = self.for_fitting[1]
        storage = self.get_data(symbol).x_max
        self.collect.write_params([
            storage,
            symbol,
            self.params[0],
            self.params[1],
            self.params[2],
            self.params[3],
            self.cal_RMSD(),
            self.params[1],
            self.params[0] * self.get_data(pos).x_max - self.params[1] - storage,
            self.params[3],
            self.params[2] * self.get_data(neg).x_max - self.params[3] - storage
        ])
        self.triggle('change')

    def set_data_decimal_x(self,x):
        DataSet.DecimalsX = x

    def set_data_decimal_y(self,y):
        DataSet.DecimalsY = y

    def set_fitting_algorithm(self,algorithm):
        Fitting.Algorithm = algorithm

    def set_skip_window(self,value):
        self.skip_window = value

    def set_diff_window(self,value):
        self.diff_window = value

    def set_cut_from(self,value):
        self.cut_range[0] = value

    def set_cut_to(self,value):
        self.cut_range[1] = value

    def set_inter_order(self,value):
        self.inter_order = value

    def auto_cal_param(self,value,idx):
        #print(self.count_fit_data())
        #print(idx,value)
        def auto(X_max,pos_max,neg_max):
            if not X_max:
                return
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
        if self.for_fitting[0]:
            pos_max = self.get_data(self.for_fitting[0]).x_max
        else:
            pos_max = None
        if self.for_fitting[1]:
            neg_max = self.get_data(self.for_fitting[1]).x_max
        else:
            neg_max = None
        if not pos_max and idx in [0,1,4]:
            return
        if not neg_max and idx in [2,3,5]:
            return
        if self.max_capacity <= 0:
            if not self.auto_cal:
                self.params[idx] = value
                return
            elif self.count_fit_data() < 7:
                return
            else:
                X_max = self.get_data(self.for_fitting[2]).x_max
                return auto(X_max,pos_max,neg_max)
        auto(self.max_capacity,pos_max,neg_max)

    def set_param(self,value,idx):
        #print("set_param")
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

    def inter(self,datas):
        return datas.inter(self.max_points,self.inter_order)

    def scale(self,datas):
        if self.fitting_method == 'VQ':
            return datas.modify_x(*self.scale_param)
        if self.fitting_method == 'dVdQ':
            return datas.modify_x(*self.scale_param).modify_y(1/self.scale_param[0],0)

    def data(self,key=None):
        if key == None:
            key = self.selected
        if key in self.datas:
            return self.datas[key]()

    def add_data(self,key,val,trigger=True,override=False):
        idx = 0
        _key = key
        while _key in self.datas and override == False:
            idx += 1
            _key = key + str(idx)
        self.datas[_key] = val
        self.order.append(_key)
        trigger and self.triggle('change')
        return _key

    def use_smooth(self,fn):
        self.smooth = lambda data:DataSet(*fn(*data()))

    def get_data(self,key):
        #print(self.datas)
        if key == None:
            key = self.selected
        if key in self.datas:
            return self.datas[key]

    def clear_data(self,text):
        changed = False
        next = None
        last = None
        for item in self.datas:
            if changed == True:
                next = item
                break
            elif item == text:
                changed = True
            else:
                last = item
        if changed:
            del self.datas[text]
            self.order.remove(text)
            self.log_record("delete",None,text,None)
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
            self.selected = next or last or ""
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
        data = self.get_data(selected)
        self.datas[name] = data
        del self.datas[selected]
        self.order[self.order.index(selected)] = name
        self.log_record("rename",None,selected,name)
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

    def read_pos_data(self,file,define=None):
        data = self.read_data(file,define)
        (filepath, tempfilename) = os.path.split(file)
        (filename, filetype) = os.path.splitext(tempfilename)
        self.pos_tag.append(filename)
        self.add_data(filename,DataSet(*data))
        self.log_record("readfile",None,file,filename)
        self.select(filename)

    def read_neg_data(self,file,define=None):
        data = self.read_data(file,define)
        (filepath, tempfilename) = os.path.split(file)
        (filename, filetype) = os.path.splitext(tempfilename)
        self.neg_tag.append(filename)
        self.add_data(filename,DataSet(*data))
        self.log_record("readfile",None,file,filename)
        self.select(filename)

    def read_full_data(self,file,define=None):
        data = self.read_data(file,define)
        (filepath, tempfilename) = os.path.split(file)
        (filename, filetype) = os.path.splitext(tempfilename)
        self.add_data(filename,DataSet(*data))
        self.log_record("readfile",None,file,filename)
        self.select(filename)

    def modify_data(self,func,operation):
        key = self.selected
        if key in self.datas:
            suffix = self.suffixs[operation]
            new_name = key + suffix
            new_name = self.add_data(new_name,func(self.get_data(key)))
            if operation == "smooth":
                self.log_record("smooth",self.smooth_method[::],key,new_name)
            elif operation == "diff":
                self.log_record("diff",self.diff_window,key,new_name)
            elif operation == "cut":
                self.log_record("cut",self.cut_range[::],key,new_name)
            elif operation == "invert":
                self.log_record("invert",None,key,new_name)
            elif operation == "skip":
                self.log_record("skip",self.skip_window,key,new_name)
            elif operation == "inter":
                self.log_record("inter",[self.max_points,self.inter_order],key,new_name)
            elif operation == 'normalize':
                self.log_record('normalize',None,key,new_name)
            elif operation == 'capacity':
                self.log_record('capacity',self.max_capacity,key,new_name)
            self.auto_select and self.select(new_name)

    def smooth_data(self):
        self.modify_data(self.smooth,'smooth')

    def diff_data(self):
        self.modify_data(self.diff,'diff')

    def cut_data(self):
        self.modify_data(self.cut,'cut')

    def invert_data(self):
        self.modify_data(self.invert,'invert')

    def skip_data(self):
        self.modify_data(self.skip,'skip')

    def inter_data(self):
        self.modify_data(self.inter,'inter')

    def normalize_data(self):
        def normalize(datas):
            return datas.normalize_x()
        self.modify_data(normalize,'normalize')

    def capacity_data(self):
        def capacity(datas):
            return datas.modify_x(self.max_capacity/datas.x_max,0)
        self.modify_data(capacity,'capacity')

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
        #print("init guess")
        data_count = self.count_fit_data()
        #模式2
        if self.max_capacity > 0 and self.auto_cal:
            #print(data_count)
            X_max = self.max_capacity
            if data_count % 4 == 1:
                self.params[0] = X_max / self.get_data(self.for_fitting[0]).x_max
            if data_count % 4 == 2:
                self.params[2] = X_max / self.get_data(self.for_fitting[1]).x_max
            if data_count % 4 == 3:
                self.params[0] = X_max / self.get_data(self.for_fitting[0]).x_max
                self.params[2] = X_max / self.get_data(self.for_fitting[1]).x_max
            return self.triggle('fitting')
        #模式1
        if data_count < 7:
            return
        if self.locked[0] or self.locked[2]:
            return
        if not self.locked[0]:
            self.params[0] = self.get_data(self.for_fitting[2]).x_max / self.get_data(self.for_fitting[0]).x_max
            self.params[1] = 0
            self.params[4] = 0
        if not self.locked[2]:
            self.params[2] = self.get_data(self.for_fitting[2]).x_max / self.get_data(self.for_fitting[1]).x_max
            self.params[3] = 0
            self.params[5] = 0
        self.triggle('fitting')

    def fit_data(self):
        if self.count_fit_data() < 7:
            return
        if self.auto_cal and self.max_capacity > 0:
            return
        pos = self.get_data(self.for_fitting[0])
        neg = self.get_data(self.for_fitting[1])
        full = self.get_data(self.for_fitting[2])
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
        self.auto_cal_param(w1 * pos.x_max - full.x_max - s1,4)
        self.auto_cal_param(w2 * neg.x_max - full.x_max - s2,5)
        self.triggle('fitting')
        self.auto_scale and self.scale_data()
        return params

    def RMSD(self,p1,p2,lower=None,upper=None):
        data_1 = self.get_data(p1)
        data_2 = self.get_data(p2)
        if lower == None:
            lower = max(data_1.x_min,data_2.x_min)
        if upper == None:
            upper = min(data_1.x_max,data_2.x_max)
        x_data = np.linspace(lower,upper,self.max_points)
        y_1 = interp1d(*data_1(), fill_value="extrapolate")(x_data)
        y_2 = interp1d(*data_2(), fill_value="extrapolate")(x_data)
        sub = y_1 - y_2
        return math.sqrt(np.sum(sub*sub)/self.max_points)

    def cal_RMSD(self,_lower=None,_upper=None):
        if self.count_fit_data() < 7:
            return 0
        #模式2
        if self.auto_cal and self.max_capacity > 0:
            return 0
        #模式1
        #print(self.for_fitting)
        
        pos_data = self.get_data(self.for_fitting[0])
        neg_data = self.get_data(self.for_fitting[1])
        full_data = self.get_data(self.for_fitting[2])
        #print(pos_data,neg_data,full_data)
        lower = max(pos_data.x_min,neg_data.x_min,full_data.x_min)
        upper = min(pos_data.x_max,neg_data.x_max,full_data.x_max)
        if _lower:
            lower = max(_lower,lower)
        if _upper:
            upper = min(_upper,upper)
        x_data = np.linspace(lower,upper,self.max_points)
        y_data = interp1d(*full_data(), fill_value="extrapolate")(x_data)
        (w1,s1,w2,s2) = self.params[0:4]
        if self.fitting_method == 'VQ':
            pos = pos_data.modify_x(w1,s1)
            neg = neg_data.modify_x(w2,s2)
        else:
            pos = pos_data.modify_x(w1,s1).modify_y(1/w1,0)
            neg = neg_data.modify_x(w2,s2).modify_y(1/w2,0)
        pos_y = interp1d(*pos(), fill_value="extrapolate")(x_data)
        neg_y = interp1d(*neg(), fill_value="extrapolate")(x_data)
        sub = pos_y-neg_y-y_data
        return math.sqrt(np.sum(sub*sub)/self.max_points)

    def scale_data(self):
        #模式2
        if self.auto_cal and self.max_capacity > 0:
            suffix = self.suffixs["gen"]
            pos_name = self.for_fitting[0]
            neg_name = self.for_fitting[1]
            if pos_name:
                pos = self.get_data(pos_name)
                pos = pos.modify_x(*self.params[0:2])
                new_pos_name = pos_name+suffix
                self.add_data(new_pos_name,pos,override=True)
                self.log_record("scale",self.params[0:2],pos_name,new_pos_name)
            if neg_name:
                neg = self.get_data(neg_name)
                neg = neg.modify_x(*self.params[2:4])
                new_neg_name = neg_name+suffix
                self.add_data(new_neg_name,neg,override=True)
                self.log_record("scale",self.params[2:4],neg_name,new_neg_name)
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
                new_full_name = key + suffix
                self.add_data(new_full_name,DataSet(x_data,y1-y2),override=True)
                self.log_record("combine",None,[new_pos_name,new_neg_name],new_full_name)
                self.for_display = [new_pos_name,new_neg_name,new_full_name]
            if pos_name or neg_name:
                self.triggle('change')
            return
        #模式1
        if self.count_fit_data() < 7:
            return
        pos_name,neg_name,full_name = self.for_fitting
        pos = self.get_data(pos_name)
        neg = self.get_data(neg_name)
        full = self.get_data(full_name)
        if self.fitting_method == 'VQ':
            suffix = self.suffixs["scaleVQ"]
            pos = pos.modify_x(*self.params[0:2])
            neg = neg.modify_x(*self.params[2:4])
        else:
            suffix = self.suffixs["scaledVdQ"]
            pos = pos.modify_x(*self.params[0:2]).modify_y(1/self.params[0],0)
            neg = neg.modify_x(*self.params[2:4]).modify_y(1/self.params[2],0)
        x_data,y_data = full()
        pos_y = interp1d(*pos(), fill_value="extrapolate")(x_data)
        neg_y = interp1d(*neg(), fill_value="extrapolate")(x_data)
        new_pos_name = pos_name + suffix
        new_neg_name = neg_name + suffix
        new_full_name = full_name + suffix
        self.add_data(new_pos_name,pos,override=True)
        self.add_data(new_neg_name,neg,override=True)
        self.add_data(new_full_name,DataSet(x_data,pos_y-neg_y),override=True)
        self.log_record("scale",self.params[0:2],pos_name,new_pos_name)
        self.log_record("scale",self.params[2:4],neg_name,new_neg_name)
        self.log_record("combine",None,[new_pos_name,new_neg_name],new_full_name)
        self.for_display = [new_pos_name, new_neg_name, new_full_name, full_name]
        self.triggle('change')

    def export_scale_data(self):
        if self.count_fit_data() < 7:
            return
        pos_name,neg_name,full_name = self.for_fitting
        pos = self.get_data(pos_name)
        neg = self.get_data(neg_name)
        full = self.get_data(full_name)
        pos = pos.modify_x(*self.params[0:2])
        neg = neg.modify_x(*self.params[2:4])
        x_data = np.linspace(0,full.x_max,self.max_points)
        pos_y = interp1d(*pos(), fill_value="extrapolate")(x_data)
        neg_y = interp1d(*neg(), fill_value="extrapolate")(x_data)
        ful_y = interp1d(*full(), fill_value="extrapolate")(x_data)
        data = np.vstack((x_data,pos_y,neg_y,pos_y - neg_y,ful_y)).T
        data = data.tolist()
        header = ['容量','拟合正极电压','拟合负极电压','拟合全电池电压','测试全电池电压']
        data.insert(0,header)
        return data

    def display_all(self):
        self.for_display = self.datas.keys()
        self.triggle('change')

    def undisplay_all(self):
        self.for_display = []
        self.triggle('change')

    def compare_datas(self,sa,sb,count):
        a = self.get_data(sa)
        b = self.get_data(sb)
        lower = max(a.x_min,b.x_min)
        upper = min(a.x_max,b.x_max)
        maximum = max(a.x_max,b.x_max)
        array = np.linspace(lower,upper,count+1)
        percent = array * 100 / maximum
        X = np.linspace(lower,upper,2000)
        Y1 = interp1d(*a(), fill_value="extrapolate")(X)
        Y2 = interp1d(*b(), fill_value="extrapolate")(X)
        table = [
            ['区间比例'],
            ['容量范围'],
            ['测试曲线电压范围'],
            ['拟合曲线电压范围'],
            ['电压极差mV'],
            ['极差电压对应容量mAh'],
            ['极差电压对应容量%'],
            ['容量极差mAh'],
            ['容量极差%'],
            ['极差容量对应电压V'],
        ]
        for i in range(len(array)-1):
            lower = array[i]
            upper = array[i+1]
            region = np.where((X >= lower) & (X <= upper))
            sub_x = X[region]
            sub_y1 = Y1[region]
            sub_y2 = Y2[region]
            table[0].append('%.2f %% ~ %.2f %%' % (percent[i],percent[i+1]))
            table[1].append('%.2f ~ %.2f' % (lower,upper))
            table[2].append('%.4f ~ %.4f' % (sub_y1[0],sub_y1[-1]))
            table[3].append('%.4f ~ %.4f' % (sub_y2[0],sub_y2[-1]))
            dif_y = sub_y2 - sub_y1
            abs_dif_y = np.abs(dif_y)
            pos = np.argmax(abs_dif_y)
            table[4].append('%.2f' % (dif_y[pos] * 1000))
            table[5].append('%.2f' % sub_x[pos])
            table[6].append('%.2f %%' % (sub_x[pos] * 100 / maximum))
            if min(sub_y1) > max(sub_y2):
                table[7].append('-∞')
                table[8].append('-∞')
                table[9].append('—')
            elif min(sub_y2) > max(sub_y1):
                table[7].append('+∞')
                table[8].append('+∞')
                table[9].append('—')
            else:
                lower = max(np.min(sub_y1),np.min(sub_y2))
                upper = min(np.max(sub_y1),np.max(sub_y2))
                Y = np.linspace(lower,upper,500)
                X1 = interp1d(sub_y1,sub_x, fill_value="extrapolate")(Y)
                X2 = interp1d(sub_y2,sub_x, fill_value="extrapolate")(Y)
                dif_x = X2 - X1
                abs_dif_x = np.abs(dif_x)
                pos = np.argmax(abs_dif_x)
                table[7].append('%.2f' % dif_x[pos])
                table[8].append('%.2f %%' % (dif_x[pos] * 100 / maximum))
                table[9].append('%.4f' % Y[pos])
        return table
            
