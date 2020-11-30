import re,os,random,traceback,subprocess,platform
from Core import Engine,File,Smooth
from PyQt5.QtWidgets import QMainWindow, QApplication, QSplashScreen, QInputDialog, QLineEdit, QMessageBox, QListWidgetItem, QFileDialog, QAction, qApp,QMenu,QStyleFactory
from PyQt5.QtCore import QSettings, Qt,QPoint
from PyQt5.QtGui import QPixmap,QCursor
from pyqtgraph import PlotWidget, mkPen, mkColor, LinearRegionItem, ScatterPlotItem, PlotCurveItem, PlotDataItem, LinearRegionItem, InfiniteLine

from .Window import Ui_MainWindow
from .Preference import Preference
from .FindPeak import FindPeak

class Application(QMainWindow, Ui_MainWindow):

    def __init__(self,dirname):
        splash = QSplashScreen(QPixmap("resource/init.png"))
        splash.show()
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        #super().__init__()
        self.dirname = dirname
        self.settings = QSettings(os.path.join(dirname,"setting.ini"),QSettings.IniFormat)
        self.core = Engine()
        self.setupUi(self)
        self.initAction()
        self.initStyle()
        self.show()
        #方便判断
        self.projectFile = None
        self.fileChanged = False
        #self.preference = Preference(self)
        splash.finish(self)
        self.system = platform.system()
        self.pathSeg = '\\' if self.system == 'Windows' else '/'

    #格式化路径
    def formatPath(self,path):
        return path.replace('/','\\').replace('\\',self.pathSeg)

    #预览文件
    def previewFile(self,file):
        if self.system == 'Windows':
            subprocess.Popen([file],shell=True)
        else:
            subprocess.Popen(['open %s' % file],shell=True)

    def initStyle(self):
        def useTheme(style):
            def fn():
                QApplication.setStyle(QStyleFactory.create(style))
                QApplication.setPalette(QApplication.style().standardPalette())
                self.setSetting('UI/Theme',style)
            return fn
        keys = QStyleFactory.keys()
        for key in keys:
            action = QAction(self.menu_Theme)
            action.setText(key.capitalize())
            action.triggered.connect(useTheme(key))
            self.menu_Theme.addAction(action)
        useTheme(self.defaultSetting('UI/Theme',keys[0]))()
    #初始化绑定事件
    def initAction(self):
        #开始菜单
        self.bindOpenAction()
        #项目文件读取
        self.bindProjectAction()
        #工具栏
        self.bindToolsAction()
        #编辑菜单
        self.bindEditAction()
        #数据操作菜单
        self.bindDataAction()
        #切换语言
        self.bindLanguageAction()
        #退出
        self.action_Exit.triggered.connect(self.close)
        #配置
        self.action_Preferences.triggered.connect(self.displayPreference)
        #最近打开的文件
        self.menu_Recent_Files.aboutToShow.connect(self.updateRecentFiles)
        #滑动条
        self.bindSliderAction()
        self.bindSpinBoxAction()
        self.bindCheckBoxAction()
        #参数框
        self.bindInputAction()
        self.bindRadioAction()
        #添加平滑选项
        self.initSmoothOptions()
        #绑定内核事件
        self.core.bind('change',self.updateList)
        self.core.bind('select',self.updateCutRange)
        self.core.bind('select',self.updateSelected)
        self.core.bind('fitting',self.updateParam)
        self.core.bind('change',self.listenProjectFileState)
        #设置内核功能
        self.initCoreFunction()
        #数据选框
        self.bindDataListAction()
        #按钮
        self.bindButtonAction()
        #绘图窗口
        self.initGraphView()
        #Help
        self.bindHelpAction()
        #寻峰
        self.action_Data_FindPeak.triggered.connect(self.findDataPeak)

    #弹出配置窗口
    def displayPreference(self):
        self.preference.show()
        #冻结当前窗口，子窗口关闭时取消冻结
        self.setEnabled(False)

    def listenProjectFileState(self):
        title = self.windowTitle()
        if title[0] != "*":
            self.setWindowTitle("* " + title)

    def bindLanguageAction(self):
        def switchLanguage(language=None):
            default = self.defaultSetting('Display/language','English')
            if default == language:
                return
            if language == None:
                language = default
            if language == 'English':
                self.transEnglish()
                self.initSmoothOptions()
                self.preference = Preference(self)
            if language == 'Chinese Simplified':
                self.transChineseSimplified()
                self.initSmoothOptions()
                self.preference = Preference(self)
            if language == 'Chinese Traditional':
                self.transChineseTraditional()
                self.initSmoothOptions()
                self.preference = Preference(self)
            self.setSetting('Display/language',language)
        self.action_English.triggered.connect(lambda :switchLanguage('English'))
        self.action_Chinese_Simplified.triggered.connect(lambda :switchLanguage('Chinese Simplified'))
        self.action_Chinese_Traditional.triggered.connect(lambda :switchLanguage('Chinese Traditional'))
        switchLanguage()

    def bindEditAction(self):
        def rename():
            value, ok = QInputDialog.getText(self, self.translateText("Data Rename"), self.translateText("Please input new data name:"), QLineEdit.Normal, self.core.selected)
            if ok and value != '' and value != self.core.selected:
                if re.match(r'(\:|\\|\/|\*|\?|\"|<|>|\|)',value):
                    self.critical("Invalid file name!")
                else:
                    self.core.alias_data(value)
        def viewData():
            tempdir = self.defaultSetting('UI/TempDirectory','')
            if tempdir == '':
                tempfile = None
            else:
                tempfile = os.path.join(tempdir,'temp.txt')
                tempfile = self.formatPath(tempfile)
            file = File.temp(str(self.core.datas[self.core.selected]),tempfile)
            self.previewFile(file)

        self.action_View.triggered.connect(self.checkSelectedBefore(viewData))
        self.action_Swap.triggered.connect(self.checkSelectedBefore(self.core.invert_data))
        self.action_Rename.triggered.connect(self.checkSelectedBefore(rename))
        self.action_Delete.triggered.connect(lambda :self.alertBeforeDelete(self.checkSelectedBefore(self.core.remove_data)))
        self.action_Export.triggered.connect(self.checkSelectedBefore(self.exportData))
        self.action_Delete_All.triggered.connect(lambda :self.alertBeforeDelete(self.checkSelectedBefore(self.core.batch_remove_data)))

    def bindToolsAction(self):
        self.action_Excel2TXT.triggered.connect(lambda :self.convertFile('Excel File (*.xls;*.xlsx)','Text File (*.txt)'))
        self.action_Excel2CSV.triggered.connect(lambda :self.convertFile('Excel File (*.xls;*.xlsx)','CSV File (*.csv)'))
        self.action_CSV2TXT.triggered.connect(lambda :self.convertFile('CSV File (*.csv)','Text File (*.txt)'))
        self.action_CSV2Excel.triggered.connect(lambda :self.convertFile('CSV File (*.csv)','Excel File (*.xls;*.xlsx)'))
        self.action_TXT2CSV.triggered.connect(lambda :self.convertFile('Text File (*.txt)','CSV File (*.csv)'))
        self.action_TXT2Excel.triggered.connect(lambda :self.convertFile('Text File (*.txt)','Excel File (*.xls;*.xlsx)'))

    def bindProjectAction(self):
        def saveProject(override=True):
            if self.projectFile == None or not override:
                lastFilePath = self.defaultSetting("File/lastProjectFilePath",self.dirname)
                extension = "AECA Project File (*.apf)"
                (fileName,fileType) = QFileDialog.getSaveFileName(self,self.translateText('Save AECA Project File'),lastFilePath,extension,extension)
                if fileName == '':
                    return
                fileName = self.formatPath(fileName)
                dirName = os.path.dirname(fileName)
                self.settings.setValue('File/lastProjectFilePath',dirName)
                self.projectFile = fileName
            self.core.save_project(self.projectFile)
            self.setWindowTitle("ATL-Electrical Chemistry Analysor  -  " + self.projectFile)
            self.information('Save AECA project file successful!')
        def openProject():
            lastFilePath = self.defaultSetting("File/lastProjectFilePath",self.dirname)
            extension = "AECA Project File (*.apf)"
            (fileName,fileType) = QFileDialog.getOpenFileName(self,self.translateText('Please select a AECA project file'),lastFilePath,extension,extension)
            if fileName == '':
                return
            fileName = self.formatPath(fileName)
            self.loadProjectFile(fileName)
        def newProject():
            if not self.projectFile == None:
                if self.prompt('DO you need to save current project file?') == QMessageBox.Yes:
                    self.core.save_project(self.projectFile)
            self.core.new_project()
            self.setWindowTitle("ATL-Electrical Chemistry Analysor")

        self.action_Save.triggered.connect(lambda: saveProject(True))
        self.action_Save_As.triggered.connect(lambda :saveProject(False))
        self.action_Project.triggered.connect(openProject)
        self.action_New.triggered.connect(newProject)

    def bindOpenAction(self):
        def loadPositiveRef():
            define = self.defaultSetting('FileStructure/posDataStructure','Voltage:Capacity')
            self.openDataFile(lambda f:self.core.read_pos_data(f,define))
        def loadNegativeRef():
            define = self.defaultSetting('FileStructure/negDataStructure','Voltage:Capacity')
            self.openDataFile(lambda f:self.core.read_neg_data(f,define))
        def loadMeasuredData():
            define = self.defaultSetting('FileStructure/fullDataStructure','Voltage:Capacity')
            self.openDataFile(lambda f:self.core.read_full_data(f,define))
        self.action_Positive_Reference.triggered.connect(loadPositiveRef)
        self.action_Negative_Reference.triggered.connect(loadNegativeRef)
        self.action_Measured_Data.triggered.connect(loadMeasuredData)

    def bindSliderAction(self):
        boxs = [
            self.Pos_Scale_SpinBox,
            self.Pos_Shift_SpinBox,
            self.Neg_Scale_SpinBox,
            self.Neg_Shift_SpinBox,
            self.Pos_Shift2_SpinBox,
            self.Neg_Shift2_SpinBox,
        ]
        keys = ['Pos_Scale','Pos_Shift','Neg_Scale','Neg_Shift','Pos_Shift2','Neg_Shift2']
        def modify_spinBox(idx):
            box = boxs[idx]
            key = keys[idx]
            def func(value):
                #print(value)
                #调节spinbox上下限和步长
                decimals = 4 - value
                maximum = 10 ** (1 + value)
                box.setSingleStep(0.1 ** decimals)
                box.setMaximum(maximum)
                #保存配置
                self.settings.setValue('User/'+key,value)
                self.core.params_max[idx] = maximum
            return func

        #滑块事件
        self.Pos_Scale_Slider.valueChanged.connect(modify_spinBox(0))
        self.Pos_Shift_Slider.valueChanged.connect(modify_spinBox(1))
        self.Pos_Shift2_Slider.valueChanged.connect(modify_spinBox(4))
        self.Neg_Scale_Slider.valueChanged.connect(modify_spinBox(2))
        self.Neg_Shift_Slider.valueChanged.connect(modify_spinBox(3))
        self.Neg_Shift2_Slider.valueChanged.connect(modify_spinBox(5))
        #启动后读取配置
        self.Pos_Scale_Slider.setValue(int(self.defaultSetting('User/Pos_Scale',2)))
        self.Pos_Shift_Slider.setValue(int(self.defaultSetting('User/Pos_Shift',2)))
        self.Pos_Shift2_Slider.setValue(int(self.defaultSetting('User/Pos_Shift2',2)))
        self.Neg_Scale_Slider.setValue(int(self.defaultSetting('User/Neg_Scale',2)))
        self.Neg_Shift_Slider.setValue(int(self.defaultSetting('User/Neg_Shift',2)))
        self.Neg_Shift2_Slider.setValue(int(self.defaultSetting('User/Neg_Shift2',2)))
        
    def bindDataAction(self):
        def exportExcel():
            lastFilePath = self.defaultSetting("File/CollectFilePath",self.dirname)
            extension = "Excel File (*.xlsx)"
            (fileName,fileType) = QFileDialog.getSaveFileName(self,self.translateText('Save statistic data file'),lastFilePath,extension,extension)
            if fileName == '':
                return
            fileName = self.formatPath(fileName)
            dirName = os.path.dirname(fileName)
            self.settings.setValue('File/CollectFilePath',dirName)
            self.core.collect.export_file(fileName)
            self.information('Export statistic data file successful!')

        def exportElectrodes():
            data = self.core.export_scale_data()
            if data == None:
                return
            lastFilePath = self.defaultSetting("File/ElectrodesSheetPath",self.dirname)
            extension = "Excel File (*.xlsx)"
            (fileName,fileType) = QFileDialog.getSaveFileName(self,self.translateText('Save electrodes sheet'),lastFilePath,extension,extension)
            if fileName == '':
                return
            fileName = self.formatPath(fileName)
            dirName = os.path.dirname(fileName)
            self.settings.setValue('File/ElectrodesSheetPath',dirName)
            File(fileName).write_data(data)
            self.information('Export electrodes sheet successful!')

        def viewExcel():
            tempdir = self.defaultSetting('UI/TempDirectory','')
            tempfile = None
            if tempdir != '':
                tempfile = os.path.join(tempdir,'temp.xlsx')
                tempfile = self.formatPath(tempfile)
            tempfile = self.core.collect.view_file(tempfile)
            self.previewFile(tempfile)

        def viewPotential():
            data = self.core.export_scale_data()
            if data == None:
                return
            self.information('\n'.join([
                self.translateText('Positive Full Charge Potential: ') + "%.3f" % data[1][1] + "\t" + self.translateText('Positive Full Discharge Potential: ') + "%.3f" % data[-1][1],
                self.translateText('Negative Full Charge Potential: ') + "%.3f" % data[1][2] + "\t" + self.translateText('Negative Full Discharge Potential: ') + "%.3f" % data[-1][2],
                self.translateText('Cell Full Charge Potential: ') + "%.3f" % data[1][3] + "\t" + self.translateText('Cell Full Discharge Potential: ') + "%.3f" % data[-1][3],
                self.translateText('Measured Full Charge Potential: ')  + "%.3f" % data[1][4] + "\t" + self.translateText('Measured Full Discharge Potential: ') + "%.3f" % data[-1][4],
                self.translateText('Positive Left Shift: ') + "%.3f" % self.core.params[1],
                self.translateText('Positive Right Shift: ') + "%.3f" % self.core.params[4],
                self.translateText('Negative Left Shift: ') + "%.3f" % self.core.params[3],
                self.translateText('Negative Right Shift: ') + "%.3f" % self.core.params[5]
            ]))
        self.action_Data_Write.triggered.connect(self.core.collect_params)
        self.action_Data_Export.triggered.connect(exportExcel)
        self.action_Data_View.triggered.connect(viewExcel)
        self.action_Sheet_Export.triggered.connect(exportElectrodes)
        self.action_Electrode_Export.triggered.connect(viewPotential)

    def bindSpinBoxAction(self):
        #修改UI参数自动设置内核参数
        self.Pos_Scale_SpinBox.valueChanged.connect(lambda value:self.core.set_param(value,0))
        self.Pos_Shift_SpinBox.valueChanged.connect(lambda value:self.core.set_param(value,1))
        
        self.Neg_Scale_SpinBox.valueChanged.connect(lambda value:self.core.set_param(value,2))
        self.Neg_Shift_SpinBox.valueChanged.connect(lambda value:self.core.set_param(value,3))

        self.Pos_Shift2_SpinBox.valueChanged.connect(lambda value:self.core.set_param(value,4))
        self.Neg_Shift2_SpinBox.valueChanged.connect(lambda value:self.core.set_param(value,5))

    def bindCheckBoxAction(self):
        spinBoxs = [
            self.Pos_Scale_SpinBox,
            self.Pos_Shift_SpinBox,
            self.Neg_Scale_SpinBox,
            self.Neg_Shift_SpinBox,
            self.Pos_Shift2_SpinBox,
            self.Neg_Shift2_SpinBox,
        ]
        checkBoxs = [
            self.Pos_Scale_checkBox,
            self.Pos_Shift_checkBox,
            self.Neg_Scale_checkBox,
            self.Neg_Shift_checkBox,
            self.Pos_Shift2_checkBox,
            self.Neg_Shift2_checkBox,
        ]
        def checkState(idx):
            box = checkBoxs[idx]
            spin = spinBoxs[idx]
            def func():
                if box.isChecked():
                    spin.setReadOnly(True)
                    self.core.lock_param(idx)
                else:
                    spin.setReadOnly(False)
                    self.core.unlock_param(idx)
            return func

        self.Pos_Scale_checkBox.stateChanged.connect(checkState(0))
        self.Pos_Shift_checkBox.stateChanged.connect(checkState(1))
        self.Neg_Scale_checkBox.stateChanged.connect(checkState(2))
        self.Neg_Shift_checkBox.stateChanged.connect(checkState(3))
        self.Pos_Shift2_checkBox.stateChanged.connect(checkState(4))
        self.Neg_Shift2_checkBox.stateChanged.connect(checkState(5))

    def bindInputAction(self):
        def select_method(v):
            text = self.Methods_List.currentText()
            if text == 'Simple':
                self.core.smooth_method = ['Simple', int(v)]
                self.core.use_smooth(lambda x,y:Smooth.Simple(x,y,int(v)))
            elif  text == 'Median':
                self.core.smooth_method = ['Median', int(v)]
                self.core.use_smooth(lambda x,y:Smooth.Median(x,y,int(v)))
            elif text == 'Savitzky_Golay':
                self.core.smooth_method = ['Savitzky_Golay', int(v)]
                self.core.use_smooth(lambda x,y:Smooth.Savitzky_Golay(x,y,int(v)))
            elif text == 'Gaussian':
                self.core.smooth_method = ['Gaussian', float(v)]
                self.core.use_smooth(lambda x,y:Smooth.Gaussian(x,y,v))
            elif text == 'Spline':
                self.core.smooth_method = ['Spline', float(v)]
                self.core.use_smooth(lambda x,y:Smooth.Spline(x,y,v))

        self.Skip_List.valueChanged.connect(self.core.set_skip_window)
        self.Diff_List.valueChanged.connect(self.core.set_diff_window)
        self.Cut_From.valueChanged.connect(self.core.set_cut_from)
        self.Cut_To.valueChanged.connect(self.core.set_cut_to)
        self.Cut_From.valueChanged.connect(self.Cut_To.setMinimum)
        self.Cut_To.valueChanged.connect(self.Cut_From.setMaximum)
        self.Smooth_Param.valueChanged.connect(select_method)
        self.Insert_List.valueChanged.connect(self.core.set_inter_order)

    def bindRadioAction(self):
        self.VQ_Radio.toggled.connect(lambda checked:self.core.set_fitting_method('VQ',checked))
        self.dVdQ_Radio.toggled.connect(lambda checked:self.core.set_fitting_method('dVdQ',checked))

    def bindDataListAction(self):
        self.Data_List.activated[str].connect(self.core.select)
        self.Pos_List.activated[str].connect(self.core.select_pos)
        self.Neg_List.activated[str].connect(self.core.select_neg)
        self.Full_List.activated[str].connect(self.core.select_full)

        self.list_action_delete.triggered.connect(self.action_Delete.trigger)
        self.list_action_rename.triggered.connect(self.action_Rename.trigger)
        self.list_action_view.triggered.connect(self.action_View.trigger)
        self.list_action_export.triggered.connect(self.action_Export.trigger)
        self.list_action_delall.triggered.connect(lambda :self.alertBeforeDelete(lambda:self.core.clear_datas(list(map(lambda x:x.text(),self.listWidget.selectedItems())))))
        self.list_action_display.triggered.connect(self.core.display_all)
        self.list_action_undisplay.triggered.connect(self.core.undisplay_all)
        self.list_action_record.triggered.connect(lambda :viewOperationRecords())
        
        def viewItem(*argv):
            name = self.listWidget.currentItem().text()
            self.core.selected = name
            self.action_View.trigger()
        def showMenu(pos):
            item = self.listWidget.currentItem()
            items = self.listWidget.selectedItems()
            if item == None or len(items) == 0:
                return
            self.listMenu.exec_(QCursor.pos())

        def updateOrder():
            order = []
            for i in range(self.listWidget.count()):
                order.append(self.listWidget.item(i).text())
            self.core.order = order
        
        def viewOperationRecords(*argv):
            def record2text(record):
                operation,param,source,target = tuple(record)
                if operation == 'readfile':
                    return self.translateText('readfile from {source} and then named as {target}').format(source=source, target=target)
                if operation == 'rename':
                    return self.translateText('rename {source} to {target}').format(source=source, target=target)
                if operation == 'invert':
                    return self.translateText('invert data {source} to generate {target}').format(source=source, target=target)
                if operation == 'cut':
                    return self.translateText('cut data {source} in range from {start} to {end} and generate {target}').format(source=source, start=param[0], end=param[1], target=target)
                if operation == 'smooth':
                    return self.translateText('smooth data {source} use {algorithm} method and {parameter} parameter to generate {target}').format(source=source, algorithm=param[0], parameter=param[1], target=target)
                if operation == 'skip':
                    return self.translateText('skip data {source} in step of {step} to generate {target}').format(source=source,step=param,target=target)
                if operation == 'diff':
                    return self.translateText('diff data {source} in step of {step} to generate {target}').format(source=source,step=param,target=target)
                if operation == 'inter':
                    return self.translateText('interpolate {source} data to generate {points} points use {order} order spline algorithm').format(source=source,points=param[0],order=param[1],target=target)
                if operation[0:5] == 'scale':
                    return self.translateText('scale data {source} use scale coefficient {scale} and shift coefficient {shift} to generate {target}').format(source=source,scale=round(param[0],4),shift=round(param[1],4),target=target)
                if operation == 'combine':
                    return self.translateText('combine data {source0} and {source1} to generate {target}').format(source0=source[0],source1=source[1],target=target)
            records = self.core.read_record(self.core.selected,True)
            records.reverse()
            text = ""
            idx = 1
            for record in records:
                text += "%s. %s\n" % (idx, record2text(record))
                idx += 1
            self.information(text)

        self.listWidget.clicked.connect(self.updateCurve)
        self.listWidget.doubleClicked.connect(viewItem)
        self.listWidget.customContextMenuRequested.connect(showMenu)
        self.listWidget.changed.connect(updateOrder)
        self.listWidget.changed.connect(self.listenProjectFileState)

    def bindButtonAction(self):
        self.Skip_Button.clicked.connect(self.checkSelectedBefore(self.core.skip_data))
        self.Diff_Button.clicked.connect(self.checkSelectedBefore(self.core.diff_data))
        self.Cut_Button.clicked.connect(self.checkSelectedBefore(self.core.cut_data))
        self.Insert_Button.clicked.connect(self.checkSelectedBefore(self.core.inter_data))
        self.Smooth_Button.clicked.connect(self.checkSelectedBefore(self.tryRun(self.core.smooth_data)))
        self.Fitting_Button.clicked.connect(self.tryRun(self.core.fit_data))
        self.Scale_Button.clicked.connect(self.tryRun(self.core.scale_data))
        self.Guess_Button.clicked.connect(self.tryRun(self.core.init_guess))

    def bindHelpAction(self):
        self.action_Author_Email.triggered.connect(lambda :self.information('Please contact author: WangC7@ATLBattery.com'))
        self.action_UserGuide.triggered.connect(lambda : self.previewFile(os.path.join(self.dirname,'resource/UserGuide.pdf')))

    def initCoreFunction(self):
        self.core.auto_select = int(self.defaultSetting('Core/AutoSelect',0)) > 0
        self.core.auto_scale = int(self.defaultSetting('Core/AutoScale',0)) > 0
        self.core.auto_cal = int(self.defaultSetting('Core/AutoCalParam',0)) > 0
        self.core.auto_guess = int(self.defaultSetting('Core/AutoGuess',0)) > 0
        self.core.max_capacity = float(self.defaultSetting('Core/MaxCapacity',0))
        self.core.use_max_capacity = int(self.defaultSetting('Core/UseMaxCapacity',0)) > 0
        self.core.record_operation = int(self.defaultSetting('Core/OperationRecord',0)) > 0
        self.core.max_points = int(self.defaultSetting('Core/MaxPoints',500))
        self.core.set_data_decimal_x(int(self.defaultSetting('Core/DecimalsX',6)))
        self.core.set_data_decimal_y(int(self.defaultSetting('Core/DecimalsY',12)))
        self.core.set_fitting_algorithm(self.defaultSetting('Core/Fitting','Manhattan'))
        if not self.core.auto_cal or self.core.max_capacity <= 0:
            self.Pos_Shift2_Label.setDisabled(True)
            self.Pos_Shift2_Slider.setDisabled(True)
            self.Pos_Shift2_SpinBox.setDisabled(True)
            self.Pos_Shift2_checkBox.setDisabled(True)
            self.Neg_Shift2_Label.setDisabled(True)
            self.Neg_Shift2_Slider.setDisabled(True)
            self.Neg_Shift2_SpinBox.setDisabled(True)
            self.Neg_Shift2_checkBox.setDisabled(True)
            self.Pos_Scale_checkBox.setEnabled(True)
            self.Pos_Shift_checkBox.setEnabled(True)
            self.Neg_Scale_checkBox.setEnabled(True)
            self.Neg_Shift_checkBox.setEnabled(True)
            self.Fitting_Button.setEnabled(True)
            self.Full_List.setCurrentIndex(0)
            self.Full_List.setEnabled(True)
            self.action_Data_Write.setEnabled(True)
            self.action_Data_View.setEnabled(True)
            self.action_Data_Export.setEnabled(True)
        else:
            self.Pos_Shift2_Label.setEnabled(True)
            self.Pos_Shift2_Slider.setEnabled(True)
            self.Pos_Shift2_SpinBox.setEnabled(True)
            self.Pos_Shift2_checkBox.setDisabled(True)
            self.Neg_Shift2_Label.setEnabled(True)
            self.Neg_Shift2_Slider.setEnabled(True)
            self.Neg_Shift2_SpinBox.setEnabled(True)
            self.Neg_Shift2_checkBox.setDisabled(True)
            self.Pos_Scale_checkBox.setDisabled(True)
            self.Pos_Shift_checkBox.setDisabled(True)
            self.Neg_Scale_checkBox.setDisabled(True)
            self.Neg_Shift_checkBox.setDisabled(True)
            self.Fitting_Button.setDisabled(True)
            self.Full_List.setCurrentText('')
            self.Full_List.setDisabled(True)
            self.action_Data_Write.setDisabled(True)
            self.action_Data_View.setDisabled(True)
            self.action_Data_Export.setDisabled(True)
        self.core.suffixs = {
            "smooth":self.defaultSetting('Core/SuffixSmooth','_M'),
            "diff":self.defaultSetting('Core/SuffixDiff','_D'),
            "cut":self.defaultSetting('Core/SuffixCut','_C'),
            "invert":self.defaultSetting('Core/SuffixInvert','_I'),
            "skip":self.defaultSetting('Core/SuffixSkip','_S'),
            "inter": self.defaultSetting('Core/SuffixInter','_P'),
            "scaledVdQ":self.defaultSetting('Core/SuffixScale1','_F'),
            "scaleVQ":self.defaultSetting('Core/SuffixScale2','_N'),
            "gen":self.defaultSetting('Core/SuffixGen','_G')
        }

    def initSmoothOptions(self):
        self.Methods_List.clear()
        options = ['Simple','Median','Savitzky_Golay','Gaussian','Spline']
        for option in options:
            self.Methods_List.addItem(option)
        def select_method(text):
            if text == 'Simple':
                self.Smooth_Label.setText(self.translateText('Smooth Window'))
                self.Smooth_Param.setValue(3)
                self.Smooth_Param.setSingleStep(2)
                self.Smooth_Param.setDecimals(0)
                self.Smooth_Param.setMinimum(3)
                self.Smooth_Param.setMaximum(99)
                self.core.smooth_method = ['Simple', 3]
                self.core.use_smooth(lambda x,y:Smooth.Simple(x,y,3))
            elif  text == 'Median':
                self.Smooth_Label.setText(self.translateText('Smooth Window'))
                self.Smooth_Param.setValue(3)
                self.Smooth_Param.setSingleStep(2)
                self.Smooth_Param.setDecimals(0)
                self.Smooth_Param.setMinimum(3)
                self.Smooth_Param.setMaximum(99)
                self.core.smooth_method = ['Median', 3]
                self.core.use_smooth(lambda x,y:Smooth.Median(x,y,3))
            elif text == 'Savitzky_Golay':
                self.Smooth_Label.setText(self.translateText('Smooth Window'))
                self.Smooth_Param.setSingleStep(2)
                self.Smooth_Param.setDecimals(0)
                self.Smooth_Param.setMinimum(5)
                self.Smooth_Param.setMaximum(99)
                self.Smooth_Param.setValue(5)
                self.core.smooth_method = ['Savitzky_Golay', 5]
                self.core.use_smooth(lambda x,y:Smooth.Savitzky_Golay(x,y,5))
            elif text == 'Gaussian':
                self.Smooth_Label.setText(self.translateText('Sigma'))
                self.Smooth_Param.setSingleStep(0.001)
                self.Smooth_Param.setDecimals(3)
                self.Smooth_Param.setMinimum(0)
                self.Smooth_Param.setMaximum(10)
                self.Smooth_Param.setValue(1)
                self.core.smooth_method = ['Gaussian', 1]
                self.core.use_smooth(lambda x,y:Smooth.Gaussian(x,y,1))
            elif text == 'Spline':
                self.Smooth_Label.setText(self.translateText('Noise Factor'))
                self.Smooth_Param.setSingleStep(1E-6)
                self.Smooth_Param.setDecimals(6)
                self.Smooth_Param.setMinimum(0)
                self.Smooth_Param.setMaximum(1)
                self.Smooth_Param.setValue(1E-3)
                self.core.smooth_method = ['Spline', 1E-3]
                self.core.use_smooth(lambda x,y:Smooth.Spline(x,y,1E-3))

        self.Methods_List.currentTextChanged.connect(select_method)
        self.Smooth_Label.setText(self.translateText('Smooth Window'))
        self.Smooth_Param.setSingleStep(2)
        self.Smooth_Param.setDecimals(0)
        self.Smooth_Param.setMinimum(3)
        self.Smooth_Param.setMaximum(99)
        self.Smooth_Param.setValue(3)

    def prompt(self,text,msg='information'):
        if msg == 'critical':
            return QMessageBox.critical(self,self.translateText("Critical"),self.translateText(text),QMessageBox.Yes | QMessageBox.No)
        elif msg == 'warnning':
            return QMessageBox.warning(self,self.translateText("Warning"),self.translateText(text),QMessageBox.Yes | QMessageBox.No)
        else:
            return QMessageBox.information(self,self.translateText("Information"),self.translateText(text),QMessageBox.Yes | QMessageBox.No)

    def information(self,text):
        return QMessageBox.information(self,self.translateText("Information"),self.translateText(text),QMessageBox.Yes)
        
    def critical(self,text):
        return QMessageBox.critical(self,self.translateText("Critical"),self.translateText(text),QMessageBox.Yes)

    def warnning(self,text):
        return QMessageBox.warning(self,self.translateText("Warning"),self.translateText(text),QMessageBox.Yes)

    def updateRecentFiles(self):
        self.menu_Recent_Files.clear()
        recentFiles = self.defaultSetting('File/recentFiles',[])
        for fname in recentFiles:
            action =QAction(fname,self,triggered=lambda:self.core.read_full_data(fname))
            action.setData(fname)
            self.menu_Recent_Files.addAction(action)

    def checkSelectedBefore(self,fn):
        def func(*x):
            if self.core.selected == '':
                self.critical('No data selcted!')
                return
            return fn()
        return func

    def alertBeforeDelete(self,fn):
        if int(self.defaultSetting('UI/AlertBeforeDelete',0)) == 0:
            return fn()
        if self.prompt('Are you sure you want to delete?',msg='warnning') == QMessageBox.Yes:
            return fn()

    def tryRun(self,fn):
        def func(*x):
            try:
                fn()
            except Exception as identifier:
                self.critical(str(identifier))
        return func

    def exportData(self):
        lastFilePath = self.defaultSetting("File/lastFilePath",self.dirname)
        defaultExtension = "Text File (*.txt)"
        extensions = "All (*.txt;*.csv;*.xls;*.xlsx);;Text File (*.txt);;CSV File (*.csv);;Excel File (*.xls;*.xlsx)"
        (fileName,fileType) = QFileDialog.getSaveFileName(self,self.translateText("Save File"),lastFilePath,extensions,defaultExtension)
        if not fileName:
            return
        File(fileName).write_data(self.core.datas[self.core.selected].tolist())

    def initGraphView(self):
        self.plot = PlotWidget(enableAutoRange=True)
        self.plot.setXRange(0,100)
        self.plotLegand = self.plot.addLegend()
        self.graphicsView.addWidget(self.plot)
        self.plotRegion = LinearRegionItem()
        self.plotRegion.setZValue(10)
        self.plotRegion.setRegion([0, 100])
        self.plotRegion.sigRegionChanged.connect(self.changeRegion)
        if int(self.defaultSetting('UI/SelectRegion',0)) > 0:
            self.plot.addItem(self.plotRegion, ignoreBounds=True)
        self.setGraphViewStyle()

    def changeRegion(self):
        if int(self.defaultSetting('UI/SelectRegion',0)) > 0:
            lower,upper = self.plotRegion.getRegion()
            self.RMSD.setText('%.4E' % self.core.cal_RMSD(lower,upper))

    def updateRegionSelector(self):
        for x in self.plot.items():
            if isinstance(x,(LinearRegionItem,InfiniteLine)):
                self.plot.removeItem(x)
        if int(self.defaultSetting('UI/SelectRegion',0)) > 0:
            self.plot.addItem(self.plotRegion, ignoreBounds=True)
            lower = float('inf')
            upper = float('-inf')
            for text in self.core.for_display:
                lower = min(lower,self.core.get_data(text).x_min)
                upper = max(upper,self.core.get_data(text).x_max)
            self.plotRegion.setRegion([lower,upper])

    def setGraphViewStyle(self):
        self.plot.setAutoVisible(y=True)
        titleText = self.defaultSetting('Graph/TitleText','Electrical Chemistry Datas')
        titleColor = self.defaultSetting('Graph/TitleColor','#000000')
        titleSize = str(self.defaultSetting('Graph/TitleSize','12')) + 'pt'
        bottumText = self.defaultSetting('Graph/BottumText','Capacity (mAh)')
        bottumColor = self.defaultSetting('Graph/BottumColor','#000000')
        bottumSize = self.defaultSetting('Graph/BottumSize',8)
        bottum = '<span style="color:%s;font-weight:700;font-size:%spt">%s</span>' % (bottumColor,bottumSize,bottumText)
        bgColor = self.defaultSetting('Graph/BackgroundColor','#ffffff')
        gridX = int(self.defaultSetting('Graph/GridX',1)) > 0
        gridY = int(self.defaultSetting('Graph/GridY',1)) > 0
        gridAlpha = float(self.defaultSetting('Graph/GridAlpha',0.25))
        axisColor = self.defaultSetting('Graph/AxisColor','#000000')
        axisWidth = float(self.defaultSetting('Graph/AxisWidth',1.5))

        self.plot.setTitle(title=titleText,color=titleColor,bold=True,size=titleSize)
        self.plot.setLabel(axis='bottom',text=bottum)
        self.plot.setBackground(bgColor)
        self.plot.showGrid(x=gridX,y=gridY, alpha=gridAlpha)
        self.plot.getAxis('bottom').setPen(color=axisColor,width=axisWidth)
        self.plot.getAxis('left').setPen(color=axisColor,width=axisWidth)

    def updateList(self):
        keys = list(self.core.datas.keys())
        keys.sort(key=lambda x:self.core.order.index(x))
        #删除曲线legand
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            text = item.text()
            self.plotLegand.removeItem(text)
        #print(txts)
        self.listWidget.clear()
        self.Data_List.clear()
        self.Pos_List.clear()
        self.Neg_List.clear()
        self.Full_List.clear()

        def isStartWith(str,patterm):
            return patterm == str[:len(patterm)]

        for k in keys:
            self.Data_List.addItem(k)
            item = QListWidgetItem(k)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)
            if k in self.core.for_display:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.listWidget.addItem(item)
            isFull = True
            for tag in self.core.pos_tag:
                if isStartWith(k,tag):
                    self.Pos_List.addItem(k)
                    isFull = False
                    break
            for tag in self.core.neg_tag:
                if isStartWith(k,tag):
                    self.Neg_List.addItem(k)
                    isFull = False
                    break
            isFull and self.Full_List.addItem(k)
        self.Full_List.addItem('')
        self.updateSelected()
        self.drawCurves()

    def updateCutRange(self):
        data = self.core.data()
        if data == None:
            return
        x_data = data[0]
        self.Cut_From.setMinimum(x_data[0])
        self.Cut_From.setMaximum(x_data[-1])
        self.Cut_To.setMinimum(x_data[0])
        self.Cut_To.setMaximum(x_data[-1])
        self.Cut_From.setValue(x_data[0])
        self.Cut_To.setValue(x_data[-1])
        self.Data_List.setCurrentText(self.core.selected)

    def updateSelected(self):
        current = self.core.selected
        if current != '':
            self.Data_List.setCurrentText(current)
            self.listWidget.setCurrentRow(self.Data_List.currentIndex())
        elif self.Data_List.count() > 0:
            self.Data_List.setCurrentIndex(0)
            self.listWidget.setCurrentRow(0)
            self.core.select(self.Data_List.currentText())
        current = self.core.for_fitting[0]
        if current != '':
            self.Pos_List.setCurrentText(current)
        elif self.Pos_List.count() > 0:
            self.Pos_List.setCurrentIndex(0)
            self.core.select_pos(self.Pos_List.currentText())
        current = self.core.for_fitting[1]
        if current != '':
            self.Neg_List.setCurrentText(current)
        elif self.Neg_List.count() > 0:
            self.Neg_List.setCurrentIndex(0)
            self.core.select_neg(self.Neg_List.currentText())
        current = self.core.for_fitting[2]
        self.Full_List.setCurrentText(current)

    def updateParam(self):
        #print("updateParam")
        #func = self.core.set_param
        #self.core.set_param = lambda x,y:None
        self.Pos_Scale_SpinBox.setValue(self.core.params[0])
        self.Pos_Shift_SpinBox.setValue(self.core.params[1])
        self.Neg_Scale_SpinBox.setValue(self.core.params[2])
        self.Neg_Shift_SpinBox.setValue(self.core.params[3])
        self.Pos_Shift2_SpinBox.setValue(self.core.params[4])
        self.Neg_Shift2_SpinBox.setValue(self.core.params[5])
        #self.core.set_param = func
        self.Pos_Scale_checkBox.setChecked(self.core.locked[0])
        self.Pos_Shift_checkBox.setChecked(self.core.locked[1])
        self.Neg_Scale_checkBox.setChecked(self.core.locked[2])
        self.Neg_Shift_checkBox.setChecked(self.core.locked[3])
        self.Pos_Shift2_checkBox.setChecked(self.core.locked[4])
        self.Neg_Shift2_checkBox.setChecked(self.core.locked[5])
        self.RMSD.setText('%.4E' % self.core.cal_RMSD())

    def updateCurve(self):
        current = self.listWidget.currentItem()
        if current != None:
            name = current.text()
            self.core.selected = name
            self.Data_List.setCurrentText(name)
        txts = []
        for_display = self.core.for_display
        legand = self.plotLegand
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            if item.checkState() == Qt.Checked:
                txts.append(item.text())
        if len(txts) == len(for_display):
            for txt in txts:
                if not txt in for_display:
                    break
                return
        this_display = []
        for curve in for_display:
            if curve in txts:
                this_display.append(curve)
        for curve in txts:
            legand.removeItem(curve)
            if not curve in this_display:
                this_display.append(curve)
        self.core.for_display = this_display
        self.drawCurves()

    def drawCurves(self):
        for x in self.plot.items():
            if isinstance(x,(ScatterPlotItem,PlotCurveItem, PlotDataItem)):
                self.plot.removeItem(x)
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            text = item.text()
            self.plotLegand.removeItem(text)
            #self.plot.removeItem(text)
            if text in self.core.for_display:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
        curveType = self.defaultSetting('Curve/type','line')
        if curveType == 'scatter':
            self.drawScatterCurve()
        else:
            self.drawLineCurve()

    def drawLineCurve(self):
        width = int(self.defaultSetting('Curve/width',3))
        colors = self.defaultSetting('Curve/colors',['FF0000', '0000FF', '00FF00', 'FFFF00', 'FF00FF', '00FFFF'])
        idx = 0
        length = len(colors)
        for text in self.core.for_display:
            if idx < length:
                color = colors[idx]
            else:
                color = (random.randint(0,256),random.randint(0,256),random.randint(0,256))
            pen = mkPen(color=color,width=width)
            self.plot.plot(*self.core.datas[text](),pen=pen,name=text)
            idx += 1
        self.plot.show()

    def drawScatterCurve(self):
        size = int(self.defaultSetting('Curve/size',5))
        colors = self.defaultSetting('Curve/colors',['FF0000', '0000FF', '00FF00', 'FFFF00', 'FF00FF', '00FFFF'])
        symbols = self.defaultSetting('Curve/symbols',['o', 's', 't', 't1', 't2', 't3', 'd', '+', 'x', 'p', 'h', 'star'])
        idx = 0
        colors_length = len(colors)
        symbols_length = len(symbols)
        for text in self.core.for_display:
            if idx < colors_length:
                color = mkColor(colors[idx])
            else:
                color = (random.randint(0,256),random.randint(0,256),random.randint(0,256))
            if idx < symbols_length:
                symbol = symbols[idx]
            else:
                symbol = 'o'
            self.plot.plot(*self.core.datas[text](),pen=color,symbolBrush=color, symbolPen=color, symbol=symbol, symbolSize=size, name=text)
            idx += 1
        self.plot.show()

    def findDataPeak(self):
        if not self.core.selected:
            return
        self.child = FindPeak(self,*self.core.data())
        self.child.show()

    def openDataFile(self,fn):
        if int(self.defaultSetting("UI/OpenMultiFiles",0)) == 1:
            return self.openDataFiles(fn)
        lastFilePath = self.defaultSetting("File/lastFilePath",self.dirname)
        recentFiles = self.defaultSetting("File/recentFiles",[])
        defaultExtension = self.defaultSetting("FileStructure/defaultExtension","Text File (*.txt)")
        extensions = "All (*.txt;*.csv;*.xls;*.xlsx);;Text File (*.txt);;CSV File (*.csv);;Excel File (*.xls;*.xlsx)"
        (fileName,fileType) =QFileDialog.getOpenFileName(self,self.translateText('Please select a data file'),lastFilePath,extensions,defaultExtension)
        if fileName == '':
            return
        fileName = self.formatPath(fileName)
        dirName = os.path.dirname(fileName)
        self.settings.setValue('File/lastFilePath',dirName)
        try:
            fn(fileName)
        except Exception as identify:
            print(identify)
            self.critical('Invalid Data File!')
        if not fileName in recentFiles:
            recentFiles.append(fileName)
        if len(recentFiles) > 10:
            recentFiles.pop(0)
        self.settings.setValue('File/recentFiles',recentFiles)
        self.settings.sync()

    def openDataFiles(self,fn):
        lastFilePath = self.defaultSetting("File/lastFilePath",self.dirname)
        recentFiles = self.defaultSetting("File/recentFiles",[])
        defaultExtension = self.defaultSetting("FileStructure/defaultExtension","Text File (*.txt)")
        extensions = "All (*.txt;*.csv;*.xls;*.xlsx);;Text File (*.txt);;CSV File (*.csv);;Excel File (*.xls;*.xlsx)"
        (fileNames,fileType) =QFileDialog.getOpenFileNames(self,self.translateText('Please select a data file'),lastFilePath,extensions,defaultExtension)
        if len(fileNames) == 0:
            return
        fileName = self.formatPath(fileNames[0])
        dirName = os.path.dirname(fileName)
        self.settings.setValue('File/lastFilePath',dirName)
        for fileName in fileNames:
            fileName = self.formatPath(fileName)
            try:
                fn(fileName)
            except Exception as identify:
                print(identify)
                self.critical('Invalid Data File!')
            if not fileName in recentFiles:
                recentFiles.append(fileName)
            if len(recentFiles) > 10:
                recentFiles.pop(0)
        self.settings.setValue('File/recentFiles',recentFiles)
        self.settings.sync()

    def convertFile(self,old,new):
        lastFilePath = self.defaultSetting("File/lastFilePath",self.dirname)
        (fileName,fileType) = QFileDialog.getOpenFileName(self,self.translateText('Please select a data file'),lastFilePath,old,old)
        if fileName == '':
            return
        fileName = self.formatPath(fileName)
        dirName = os.path.dirname(fileName)
        file = None
        try:
            file = File(fileName)
            file.read_data()
        except:
            self.critical('A error occur, please contact author for help!')
            return
        (fileName,fileType) = QFileDialog.getSaveFileName(self,"Save File",dirName,new,new)
        if fileName == '':
            return
        file.save_as(fileName)

    def loadProjectFile(self,file):
        if not self.projectFile == None:
            if self.prompt('Do you want to replace current project file?','warnning') == QMessageBox.No:
                return
            if self.prompt('DO you need to save current project file?') == QMessageBox.Yes:
                self.core.save_project(self.projectFile)
        try:
            self.core.read_project(file)
            self.projectFile = file
            self.setWindowTitle("ATL-Electrical Chemistry Analysor  -  " + file)
            self.settings.setValue('File/lastProjectFilePath',os.path.dirname(file))
            self.updateRegionSelector()
        except:
            #输出错误堆栈信息
            open('error.log','w+').write(traceback.format_exc())
            self.critical(file + self.translateText(' is not an invalid AECA project file!'))
            self.previewFile('error.log')

    def defaultSetting(self,key,default):
        value = self.settings.value(key)
        if value == None or value == '':
            self.settings.setValue(key,default)
            self.settings.sync()
            return default
        return value

    def setSetting(self,key,value):
        self.settings.setValue(key,value)
        self.settings.sync()

    def dragEnterEvent(self,e):
        if e.mimeData().text().split('.')[-1].lower() == 'apf':
            e.accept()
        else:
            e.ignore() 

    def dropEvent(self,e):
        fileName = e.mimeData().text()
        if self.system == 'Windows':
            fileName = re.sub(r'^file:///','',fileName)
            #虚拟桌面
            fileName = re.sub(r'^file:','',fileName)
        else:
            fileName = re.sub(r'^file://','',fileName)
        self.loadProjectFile(fileName)

    def closeEvent(self, QCloseEvent):
        #未保存文件
        if self.windowTitle()[0] == "*":
            #强制退出
            if self.prompt("The project file hasn't been saved,\nDo you confirm to exit?",msg='warnning') == QMessageBox.Yes:
                if self.preference:
                    self.preference.close()
                QCloseEvent.accept()
            else:
                QCloseEvent.ignore()
        else:
            if self.preference:
                self.preference.close()
            QCloseEvent.accept()
