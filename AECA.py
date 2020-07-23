# coding=utf-8
import fix_qt_import_error
import re,os,sys,random,traceback,subprocess,platform
#sys.path = ['','libs','libs/python.zip','libs/env']
from Core import Engine,File,Smooth
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QSplashScreen, QInputDialog, QLineEdit, QMessageBox, QListWidgetItem, QFileDialog, QAction, qApp,QMenu
from PyQt5.QtCore import QSettings, Qt,QPoint
from PyQt5.QtGui import QPixmap,QCursor
from pyqtgraph import PlotWidget, mkPen, mkColor

from UI import Ui_MainWindow
from Preference import Preference

class Application(QMainWindow, Ui_MainWindow):

    def __init__(self):
        splash = QSplashScreen(QPixmap("resource/init.png"))
        splash.show()
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        #super().__init__()
        self.dirname = os.path.dirname(os.path.abspath(__file__))
        self.core = Engine()
        self.settings=QSettings(os.path.join(self.dirname,"setting.ini"),QSettings.IniFormat)
        self.setupUi(self)
        self.initAction()
        self.show()
        #方便判断
        self.projectFile = None
        #self.preference = Preference(self)
        splash.finish(self)
        self.system = platform.system()
        self.pathSeg = '\\' if self.system == 'Windows' else '/'

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
        self.action_Exit.triggered.connect(QApplication.exit)
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

    #弹出配置窗口
    def displayPreference(self):
        self.preference.show()
        #冻结当前窗口，子窗口关闭时取消冻结
        self.setEnabled(False)

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
                tempfile = tempfile.replace('/','\\').replace('\\',self.pathSeg)
            file = File.temp(str(self.core.datas[self.core.selected]),tempfile)
            if self.system == 'Windows':
                subprocess.Popen([file],shell=True)
            else:
                subprocess.Popen(['open %s' % file],shell=True)

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
                fileName = fileName.replace('/','\\').replace('\\',self.pathSeg)
                dirName = os.path.dirname(fileName)
                self.settings.setValue('File/lastProjectFilePath',dirName)
                self.projectFile = fileName
            self.core.save_project(self.projectFile)
            self.information('Save AECA project file successful!')
        def openProject():
            lastFilePath = self.defaultSetting("File/lastProjectFilePath",self.dirname)
            extension = "AECA Project File (*.apf)"
            (fileName,fileType) = QFileDialog.getOpenFileName(self,self.translateText('Please select a AECA project file'),lastFilePath,extension,extension)
            if fileName == '':
                return
            fileName = fileName.replace('/','\\').replace('\\',self.pathSeg)
            self.loadProjectFile(fileName)
        def newProject():
            if not self.projectFile == None:
                if self.prompt('DO you need to save current project file?') == QMessageBox.Yes:
                    self.core.save_project(self.projectFile)
            self.core.new_project()

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
            fileName = fileName.replace('/','\\').replace('\\',self.pathSeg)
            dirName = os.path.dirname(fileName)
            self.settings.setValue('File/CollectFilePath',dirName)
            self.core.collect.export_file(fileName)
            self.information('Export statistic data file successful!')
        def viewExcel():
            tempdir = self.defaultSetting('UI/TempDirectory','')
            if tempdir == '':
                tempfile = None
            else:
                tempfile = os.path.join(tempdir,'temp.xlsx')
                tempfile = tempfile.replace('/','\\').replace('\\',self.pathSeg)
            tempfile = self.core.collect.view_file(tempfile)
            if self.system == 'Windows':
                subprocess.Popen([tempfile],shell=True)
            else:
                subprocess.Popen(['open %s' % tempfile],shell=True)
        self.action_Data_Write.triggered.connect(self.core.collect_params)
        self.action_Data_Export.triggered.connect(exportExcel)
        self.action_Data_View.triggered.connect(viewExcel)

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
                self.core.use_smooth(lambda x,y:Smooth.Simple(x,y,int(v)))
            elif  text == 'Median':
                self.core.use_smooth(lambda x,y:Smooth.Median(x,y,int(v)))
            elif text == 'Savitzky_Golay':
                self.core.use_smooth(lambda x,y:Smooth.Savitzky_Golay(x,y,int(v)))
            elif text == 'Gaussian':
                self.core.use_smooth(lambda x,y:Smooth.Gaussian(x,y,v))
            elif text == 'Spline':
                self.core.use_smooth(lambda x,y:Smooth.Spline(x,y,v))

        self.Skip_List.valueChanged.connect(self.core.set_skip_window)
        self.Diff_List.valueChanged.connect(self.core.set_diff_window)
        self.Cut_From.valueChanged.connect(self.core.set_cut_from)
        self.Cut_To.valueChanged.connect(self.core.set_cut_to)
        self.Cut_From.valueChanged.connect(self.Cut_To.setMinimum)
        self.Cut_To.valueChanged.connect(self.Cut_From.setMaximum)
        self.Smooth_Param.valueChanged.connect(select_method)

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

        self.listWidget.clicked.connect(self.updateCurve)
        self.listWidget.doubleClicked.connect(viewItem)
        self.listWidget.customContextMenuRequested.connect(showMenu)

    def bindButtonAction(self):
        self.Skip_Button.clicked.connect(self.checkSelectedBefore(self.core.skip_data))
        self.Diff_Button.clicked.connect(self.checkSelectedBefore(self.core.diff_data))
        self.Cut_Button.clicked.connect(self.checkSelectedBefore(self.core.cut_data))
        self.Smooth_Button.clicked.connect(self.checkSelectedBefore(self.tryRun(self.core.smooth_data)))
        self.Fitting_Button.clicked.connect(self.tryRun(self.core.fit_data))
        self.Scale_Button.clicked.connect(self.tryRun(self.core.scale_data))
        self.Guess_Button.clicked.connect(self.tryRun(self.core.init_guess))

    def bindHelpAction(self):
        self.action_UserGuide.triggered.connect(lambda : subprocess.Popen([os.path.join(self.dirname,'UserGuide.pdf')],shell=True) if self.system == 'Windows' else subprocess.Popen(['open %s' % os.path.join(self.dirname,'UserGuide.pdf')],shell=True))
        self.action_Author_Email.triggered.connect(lambda :self.information('Please contact author: WangC7@ATLBattery.com'))

    def initCoreFunction(self):
        self.core.auto_scale = int(self.defaultSetting('Core/AutoScale',0)) > 0
        self.core.auto_cal = int(self.defaultSetting('Core/AutoCalParam',0)) > 0
        self.core.max_capacity = float(self.defaultSetting('Core/MaxCapacity',0))
        self.core.use_max_capacity = int(self.defaultSetting('Core/UseMaxCapacity',0)) > 0
        self.core.max_points = int(self.defaultSetting('Core/MaxPoints',500))
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

        self.core.suffix_cut = self.defaultSetting('Core/SuffixCut','_C')
        self.core.suffix_diff = self.defaultSetting('Core/SuffixDiff','_D')
        self.core.suffix_smooth = self.defaultSetting('Core/SuffixSmooth','_M')
        self.core.suffix_invert = self.defaultSetting('Core/SuffixInvert','_I')
        self.core.suffix_skip = self.defaultSetting('Core/SuffixSkip','_S')
        self.core.suffix_scaledVdQ = self.defaultSetting('Core/SuffixScale1','_F')
        self.core.suffix_scaleVQ = self.defaultSetting('Core/SuffixScale2','_N')
        self.core.suffix_gen = self.defaultSetting('Core/SuffixGen','_G')

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
                self.core.use_smooth(lambda x,y:Smooth.Simple(x,y,3))
            elif  text == 'Median':
                self.Smooth_Label.setText(self.translateText('Smooth Window'))
                self.Smooth_Param.setValue(3)
                self.Smooth_Param.setSingleStep(2)
                self.Smooth_Param.setDecimals(0)
                self.Smooth_Param.setMinimum(3)
                self.Smooth_Param.setMaximum(99)
                self.core.use_smooth(lambda x,y:Smooth.Median(x,y,3))
            elif text == 'Savitzky_Golay':
                self.Smooth_Label.setText(self.translateText('Smooth Window'))
                self.Smooth_Param.setSingleStep(2)
                self.Smooth_Param.setDecimals(0)
                self.Smooth_Param.setMinimum(5)
                self.Smooth_Param.setMaximum(99)
                self.Smooth_Param.setValue(5)
                self.core.use_smooth(lambda x,y:Smooth.Savitzky_Golay(x,y,5))
            elif text == 'Gaussian':
                self.Smooth_Label.setText(self.translateText('Sigma'))
                self.Smooth_Param.setSingleStep(0.001)
                self.Smooth_Param.setDecimals(3)
                self.Smooth_Param.setMinimum(0)
                self.Smooth_Param.setMaximum(10)
                self.Smooth_Param.setValue(1)
                self.core.use_smooth(lambda x,y:Smooth.Gaussian(x,y,1))
            elif text == 'Spline':
                self.Smooth_Label.setText(self.translateText('Noise Factor'))
                self.Smooth_Param.setSingleStep(1E-6)
                self.Smooth_Param.setDecimals(6)
                self.Smooth_Param.setMinimum(0)
                self.Smooth_Param.setMaximum(1)
                self.Smooth_Param.setValue(1E-3)
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
        self.legand = self.plot.addLegend()
        self.graphicsView.addWidget(self.plot)
        self.setGraphViewStyle()

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
        #删除曲线legand
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            text = item.text()
            self.legand.removeItem(text)
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
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
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
        self.Pos_Scale_SpinBox.setValue(self.core.params[0])
        self.Pos_Shift_SpinBox.setValue(self.core.params[1])
        self.Neg_Scale_SpinBox.setValue(self.core.params[2])
        self.Neg_Shift_SpinBox.setValue(self.core.params[3])
        self.Pos_Shift2_SpinBox.setValue(self.core.params[4])
        self.Neg_Shift2_SpinBox.setValue(self.core.params[5])
        self.Pos_Scale_checkBox.setChecked(self.core.locked[0])
        self.Pos_Shift_checkBox.setChecked(self.core.locked[1])
        self.Neg_Scale_checkBox.setChecked(self.core.locked[2])
        self.Neg_Shift_checkBox.setChecked(self.core.locked[3])
        self.Pos_Shift2_checkBox.setChecked(self.core.locked[4])
        self.Neg_Shift2_checkBox.setChecked(self.core.locked[5])
        self.RMSD.setValue(self.core.cal_RMSD())

    def updateCurve(self):
        current = self.listWidget.currentItem()
        if current != None:
            name = current.text()
            self.core.selected = name
            self.Data_List.setCurrentText(name)
        txts = []
        for_display = self.core.for_display
        legand = self.legand
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
        self.plot.clear()
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            text = item.text()
            self.legand.removeItem(text)
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
        fileName = fileName.replace('/','\\').replace('\\',self.pathSeg)
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
        fileName = fileNames[0].replace('/','\\').replace('\\',self.pathSeg)
        dirName = os.path.dirname(fileName)
        self.settings.setValue('File/lastFilePath',dirName)
        for fileName in fileNames:
            fileName = fileName.replace('/','\\').replace('\\',self.pathSeg)
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
        fileName = fileName.replace('/','\\').replace('\\',self.pathSeg)
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
            self.settings.setValue('File/lastProjectFilePath',os.path.dirname(file))
        except:
            #输出错误堆栈信息
            open('error.log','w+').write(traceback.format_exc())
            self.critical(file + self.translateText(' is not an invalid AECA project file!'))
            #Window平台直接记事本打开
            if self.system == 'Windows':
                subprocess.Popen(['error.log'],shell=True)
            else:
                subprocess.Popen(['open error.log'],shell=True)

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
        print(fileName)
        #windows
        if self.system == 'Windows':
            fileName = re.sub(r'^file:///','',fileName)
            #虚拟桌面
            fileName = re.sub(r'^file:','',fileName)
        else:
            fileName = re.sub(r'^file://','',fileName)
        #self.information(fileName)
        self.loadProjectFile(fileName)

    def closeEvent(self, QCloseEvent):
        if self.preference:
            self.preference.close()
        QCloseEvent.accept()


if __name__ == '__main__':
    QApplication.setOrganizationName("ATL")
    QApplication.setOrganizationDomain("http://www.atlinfo.com")
    QApplication.setApplicationName("Electrical Chemistry Analysor")
    app = QApplication(sys.argv)
    mainWin = Application()
    #拖拽文件到App上的时候直接打开
    if sys.argv.__len__() > 1:
        mainWin.loadProjectFile(sys.argv[-1])
    sys.exit(app.exec_())


