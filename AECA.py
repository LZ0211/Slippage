#!/usr/bin/env python
# coding=utf-8
import fix_qt_import_error
import re,os,sys,random
from Core import Engine,File,Smooth
import pyqtgraph as pg
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QLineEdit, QMessageBox, QListWidgetItem, QFileDialog, QAction
from PyQt5.QtCore import QSettings, Qt

#mainWindowUI = "GUI.ui"

#(Ui_MainWindow, QtBaseClass) = uic.loadUiType(mainWindowUI)

from UI import Ui_MainWindow

class Application(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        super().__init__()
        self.dirname = os.path.dirname(os.path.abspath(__file__))
        self.core = Engine()
        self.settings=QSettings(os.path.join(self.dirname,"setting.ini"),QSettings.IniFormat)
        self.setupUi(self)
        self.initAction()
        self.show()
        self.projectFile = None
        if sys.argv.__len__() > 1:
            self.loadProjectFile(sys.argv[-1])

    #初始化绑定事件
    def initAction(self):
        #菜单栏
        self.bindOpenAction()
        self.bindSaveAction()
        self.bindToolsAction()
        self.bindEditAction()
        self.bindDataAction()
        self.bindLanguageAction()
        #退出
        self.action_Exit.triggered.connect(QApplication.exit)
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
        self.core.bind('fitting',self.updateParam)
        #数据选框
        self.bindDataListAction()
        #按钮
        self.bindButtonAction()
        self.initGraphView()
        #Help
        self.bindHelpAction()
    
    def loadProjectFile(self,file):
        if not self.projectFile == None:
            if os.path.abspath(file) == os.path.abspath(self.projectFile):
                return
            if self.warnning(self.translateText('Do you want to replace current project file?')) == QMessageBox.No:
                return
            if self.infomation(self.translateText('DO you need to save current project file?')) == QMessageBox.Yes:
                self.core.save_project(self.projectFile)
        try:
            self.core.read_project(file)
            self.projectFile = file
        except:
            self.critical(file + self.translateText(' is not an invalid AECA project file!'))

    def switchLanguage(self,language='English'):
        if self.language == language:
            return
        if language == 'English':
            self.transEnglish()
            self.initSmoothOptions()
            self.language = 'English'
        if language == 'Chinese Simplified':
            self.transChineseSimplified()
            self.initSmoothOptions()
            self.language = 'Chinese Simplified'
        if language == 'Chinese Traditional':
            self.transChineseTraditional()
            self.initSmoothOptions()
            self.language = 'Chinese Traditional'
        self.settings.setValue('Display/language',language)
        self.settings.sync()

    def bindLanguageAction(self):
        self.language = 'English'
        language = self.defaultSetting('Display/language','English')
        self.switchLanguage(language)
        self.action_English.triggered.connect(lambda :self.switchLanguage('English'))
        self.action_Chinese_Simplified.triggered.connect(lambda :self.switchLanguage('Chinese Simplified'))
        self.action_Chinese_Traditional.triggered.connect(lambda :self.switchLanguage('Chinese Traditional'))

    def bindEditAction(self):
        def rename():
            value, ok = QInputDialog.getText(self, self.translateText("Data Rename"), self.translateText("Please input new data name:"), QLineEdit.Normal, self.core.selected)
            if ok and value != '' and value != self.core.selected:
                if re.match(r'(\:|\\|\/|\*|\?|\"|<|>|\|)',value):
                    self.critical("Invalid file name!")
                else:
                    self.core.alias_data(value)
        def viewData():
            file = File.temp(str(self.core.datas[self.core.selected]))
            os.popen("start notepad "+file)

        self.action_View.triggered.connect(self.checkSelectedBefore(viewData))
        self.action_Swap.triggered.connect(self.checkSelectedBefore(self.core.invert_data))
        self.action_Rename.triggered.connect(self.checkSelectedBefore(rename))
        self.action_Delete.triggered.connect(self.checkSelectedBefore(self.core.remove_data))
        self.action_Export.triggered.connect(self.checkSelectedBefore(self.exportData))
        self.action_Delete_All.triggered.connect(self.checkSelectedBefore(self.core.remove_datas))

    def bindToolsAction(self):
        self.action_Excel2TXT.triggered.connect(lambda :self.convertFile('Excel File (*.xls;*.xlsx)','Text File (*.txt)'))
        self.action_Excel2CSV.triggered.connect(lambda :self.convertFile('Excel File (*.xls;*.xlsx)','CSV File (*.csv)'))
        self.action_CSV2TXT.triggered.connect(lambda :self.convertFile('CSV File (*.csv)','Text File (*.txt)'))
        self.action_CSV2Excel.triggered.connect(lambda :self.convertFile('CSV File (*.csv)','Excel File (*.xls;*.xlsx)'))
        self.action_TXT2CSV.triggered.connect(lambda :self.convertFile('Text File (*.txt)','CSV File (*.csv)'))
        self.action_TXT2Excel.triggered.connect(lambda :self.convertFile('Text File (*.txt)','Excel File (*.xls;*.xlsx)'))

    def bindSaveAction(self):
        def saveProject(override=True):
            if self.projectFile == None or not override:
                lastFilePath = self.defaultSetting("File/lastProjectFilePath",self.dirname)
                extension = "AECA Project File (*.apf)"
                (fileName,fileType) = QFileDialog.getSaveFileName(self,self.translateText('Save AECA Project File'),lastFilePath,extension,extension)
                if fileName == '':
                    return
                fileName = fileName.replace('/','\\')
                dirName = os.path.dirname(fileName)
                self.settings.setValue('File/lastProjectFilePath',dirName)
                self.projectFile = fileName
            self.core.save_project(self.projectFile)
            self.infomation(self.translateText('Save AECA project file successful!'))
        self.action_Save.triggered.connect(lambda: saveProject(True))
        self.action_Save_As.triggered.connect(lambda :saveProject(False))

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
        def modify_spinBox(box,value,name):
            decimals = 4-value
            box.setDecimals(decimals)
            box.setSingleStep(0.1**decimals)
            box.setMaximum(10**(5-decimals)-0.1**decimals)
            self.settings.setValue(name,value)
        self.Pos_Scale_Slider.valueChanged.connect(lambda value:modify_spinBox(self.Pos_Scale_SpinBox,value,'User/Pos_Scale'))
        self.Pos_Shift_Slider.valueChanged.connect(lambda value:modify_spinBox(self.Pos_Shift_SpinBox,value,'User/Pos_Shift'))
        self.Neg_Scale_Slider.valueChanged.connect(lambda value:modify_spinBox(self.Neg_Scale_SpinBox,value,'User/Neg_Scale'))
        self.Neg_Shift_Slider.valueChanged.connect(lambda value:modify_spinBox(self.Neg_Shift_SpinBox,value,'User/Neg_Shift'))
        self.Pos_Scale_Slider.setValue(int(self.defaultSetting('User/Pos_Scale',2)))
        self.Pos_Shift_Slider.setValue(int(self.defaultSetting('User/Pos_Shift',2)))
        self.Neg_Scale_Slider.setValue(int(self.defaultSetting('User/Neg_Scale',2)))
        self.Neg_Shift_Slider.setValue(int(self.defaultSetting('User/Neg_Shift',2)))
        
    def bindDataAction(self):
        def exportExcel():
            lastFilePath = self.defaultSetting("File/CollectFilePath",self.dirname)
            extension = "Excel File (*.xlsx)"
            (fileName,fileType) = QFileDialog.getSaveFileName(self,self.translateText('Save statistic data file'),lastFilePath,extension,extension)
            if fileName == '':
                return
            fileName = fileName.replace('/','\\')
            dirName = os.path.dirname(fileName)
            self.settings.setValue('File/CollectFilePath',dirName)
            self.core.collect.export_file(fileName)
            self.infomation(self.translateText('Export statistic data file successful!'))
        self.action_Data_Write.triggered.connect(self.core.collect_params)
        self.action_Data_Export.triggered.connect(exportExcel)
        self.action_Data_View.triggered.connect(lambda :self.core.collect.view_file())

    def bindSpinBoxAction(self):
        self.Pos_Scale_SpinBox.valueChanged.connect(lambda value:self.core.set_param(value,0))
        self.Pos_Shift_SpinBox.valueChanged.connect(lambda value:self.core.set_param(value,1))
        self.Neg_Scale_SpinBox.valueChanged.connect(lambda value:self.core.set_param(value,2))
        self.Neg_Shift_SpinBox.valueChanged.connect(lambda value:self.core.set_param(value,3))

    def bindCheckBoxAction(self):
        def checkState(box,spin,idx):
            if box.isChecked():
                spin.setReadOnly(True)
                self.core.lock_param(idx)
            else:
                spin.setReadOnly(False)
                self.core.unlock_param(idx)

        self.Pos_Scale_checkBox.stateChanged.connect(lambda :checkState(self.Pos_Scale_checkBox,self.Pos_Scale_SpinBox,0))
        self.Pos_Shift_checkBox.stateChanged.connect(lambda :checkState(self.Pos_Shift_checkBox,self.Pos_Shift_SpinBox,1))
        self.Neg_Scale_checkBox.stateChanged.connect(lambda :checkState(self.Neg_Scale_checkBox,self.Neg_Scale_SpinBox,2))
        self.Neg_Shift_checkBox.stateChanged.connect(lambda :checkState(self.Neg_Shift_checkBox,self.Neg_Shift_SpinBox,3))

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
        self.listWidget.clicked.connect(self.drawCurves)

    def bindButtonAction(self):
        self.Skip_Button.clicked.connect(self.checkSelectedBefore(self.core.skip_data))
        self.Diff_Button.clicked.connect(self.checkSelectedBefore(self.core.diff_data))
        self.Cut_Button.clicked.connect(self.checkSelectedBefore(self.core.cut_data))
        self.Smooth_Button.clicked.connect(self.checkSelectedBefore(self.tryRun(self.core.smooth_data)))
        self.Fitting_Button.clicked.connect(self.tryRun(self.core.fit_data))
        self.Scale_Button.clicked.connect(self.tryRun(self.core.scale_data))

    def bindHelpAction(self):
        self.action_UserGuide.triggered.connect(lambda :os.popen("start "+os.path.join(self.dirname,'UserGuide.pdf')))
        self.action_Author_Email.triggered.connect(lambda :self.infomation(self.translateText('Please contact author: WangC7@ATLBattery.com')))

    def initSmoothOptions(self):
        self.Methods_List.clear()
        options = ['Simple','Median','Savitzky_Golay','Gaussian','Spline']
        for option in options:
            self.Methods_List.addItem(option)
        def select_method(text):
            if text == 'Simple':
                self.Param_Name.setText(self.translateText('Smooth Window'))
                self.Smooth_Param.setValue(3)
                self.Smooth_Param.setSingleStep(2)
                self.Smooth_Param.setDecimals(0)
                self.Smooth_Param.setMinimum(3)
                self.Smooth_Param.setMaximum(99)
                self.core.use_smooth(lambda x,y:Smooth.Simple(x,y,3))
            elif  text == 'Median':
                self.Param_Name.setText(self.translateText('Smooth Window'))
                self.Smooth_Param.setValue(3)
                self.Smooth_Param.setSingleStep(2)
                self.Smooth_Param.setDecimals(0)
                self.Smooth_Param.setMinimum(3)
                self.Smooth_Param.setMaximum(99)
                self.core.use_smooth(lambda x,y:Smooth.Median(x,y,3))
            elif text == 'Savitzky_Golay':
                self.Param_Name.setText(self.translateText('Smooth Window'))
                self.Smooth_Param.setSingleStep(2)
                self.Smooth_Param.setDecimals(0)
                self.Smooth_Param.setMinimum(5)
                self.Smooth_Param.setMaximum(99)
                self.Smooth_Param.setValue(5)
                self.core.use_smooth(lambda x,y:Smooth.Savitzky_Golay(x,y,5))
            elif text == 'Gaussian':
                self.Param_Name.setText(self.translateText('Sigma'))
                self.Smooth_Param.setSingleStep(0.001)
                self.Smooth_Param.setDecimals(3)
                self.Smooth_Param.setMinimum(0)
                self.Smooth_Param.setMaximum(10)
                self.Smooth_Param.setValue(1)
                self.core.use_smooth(lambda x,y:Smooth.Gaussian(x,y,1))
            elif text == 'Spline':
                self.Param_Name.setText(self.translateText('Noise Factor'))
                self.Smooth_Param.setSingleStep(1E-6)
                self.Smooth_Param.setDecimals(6)
                self.Smooth_Param.setMinimum(0)
                self.Smooth_Param.setMaximum(1)
                self.Smooth_Param.setValue(1E-3)
                self.core.use_smooth(lambda x,y:Smooth.Spline(x,y,1E-3))

        self.Methods_List.currentTextChanged.connect(select_method)
        self.Param_Name.setText(self.translateText('Smooth Window'))
        self.Smooth_Param.setSingleStep(2)
        self.Smooth_Param.setDecimals(0)
        self.Smooth_Param.setMinimum(3)
        self.Smooth_Param.setMaximum(99)
        self.Smooth_Param.setValue(3)

    def infomation(self,text):
        return QMessageBox.information(self,self.translateText("Information"),text,QMessageBox.Yes | QMessageBox.No)
        
    def critical(self,text):
        return QMessageBox.critical(self,self.translateText("Critical"),text,QMessageBox.Yes | QMessageBox.No)

    def warnning(self,text):
        return QMessageBox.warning(self,self.translateText("Warning"),text,QMessageBox.Yes | QMessageBox.No)

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
                self.critical(self.translateText('No data selcted!'))
                return
            return fn()
        return func

    def tryRun(self,fn):
        def func(*x):
            try:
                fn()
            except Exception as identifier:
                self.critical(self.translateText(str(identifier)))
        return func

    def exportData(self):
        lastFilePath = self.defaultSetting("File/lastFilePath",self.dirname)
        defaultExtension = "Text File (*.txt)"
        extensions = "Text File (*.txt);;CSV File (*.csv);;Excel File (*.xls;*.xlsx)"
        (fileName,fileType) = QFileDialog.getSaveFileName(self,self.translateText("Save File"),lastFilePath,extensions,defaultExtension)
        if fileName == '':
            return
        File(fileName).write_data(str(self.core.datas[self.core.selected]))

    def initGraphView(self):
        self.plot = pg.PlotWidget(enableAutoRange=True)
        self.plot.setAutoVisible(y=True)
        self.plot.setTitle(title='Electrical Chemistry Datas',color='000',bold=True,size="12pt")
        self.plot.setLabel(axis='bottom',text='<h3><span style="color:#000000;font-size:8pt">Capacity (mAh)</span></h3>')
        self.plot.setBackground('fff')
        self.plot.getAxis('bottom').setPen(color='000',width=1.5)
        self.plot.getAxis('left').setPen(color='000',width=1.5)
        self.plot.showGrid(x=True,y=True, alpha=0.25)
        self.legand = self.plot.addLegend()
        self.graphicsView.addWidget(self.plot)
        self.curveList = []
        #self.curve.show()

    def updateList(self):
        keys = list(self.core.datas.keys())
        #更新文件列表
        txts = []
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            if item.checkState() == Qt.Checked:
                txts.append(item.text())
        #print(txts)
        self.listWidget.clear()
        self.Data_List.clear()
        self.Pos_List.clear()
        self.Neg_List.clear()
        self.Full_List.clear()
        for k in keys:
            self.Data_List.addItem(k)
            item = QListWidgetItem(k)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            if k in txts:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.listWidget.addItem(item)
            if re.match('|'.join(self.core.pos_tag),k):
                self.Pos_List.addItem(k)
                continue
            if re.match('|'.join(self.core.neg_tag),k):
                self.Neg_List.addItem(k)
                continue
            self.Full_List.addItem(k)
        current = self.core.selected
        if current != '':
            self.Data_List.setCurrentText(current)
        elif self.Data_List.count() > 0:
            self.Data_List.setCurrentIndex(0)
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
        if current != '':
            self.Full_List.setCurrentText(current)
        elif self.Full_List.count() > 0:
            self.Full_List.setCurrentIndex(0)
            self.core.select_full(self.Full_List.currentText())
        self.drawCurves(True)

    def updateCutRange(self):
        x_data = self.core.data()[0]
        self.Cut_From.setMinimum(x_data[0])
        self.Cut_From.setMaximum(x_data[-1])
        self.Cut_To.setMinimum(x_data[0])
        self.Cut_To.setMaximum(x_data[-1])
        self.Cut_From.setValue(x_data[0])
        self.Cut_To.setValue(x_data[-1])
        self.Data_List.setCurrentText(self.core.selected)

    def updateParam(self):
        self.Pos_Scale_SpinBox.setValue(self.core.params[0])
        self.Pos_Shift_SpinBox.setValue(self.core.params[1])
        self.Neg_Scale_SpinBox.setValue(self.core.params[2])
        self.Neg_Shift_SpinBox.setValue(self.core.params[3])
        self.RMSD.setValue(self.core.cal_RMSD())

    def drawCurves(self,force=False):
        txts = []
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            if item.checkState() == Qt.Checked:
                txts.append(item.text())
        if len(txts) == len(self.curveList):
            isSame = True
            for txt in txts:
                if not txt in self.curveList:
                    isSame = False
                    break
            if isSame == True and force == False:
                return

        self.plot.clear()
        legand = self.legand
        for x in self.curveList:
            legand.removeItem(x)
        curveType = self.defaultSetting('Curve/type','line')
        if curveType == 'scatter':
            self.drawScatterCurve(txts)
        else:
            self.drawLineCurve(txts)
        self.plot.show()
        self.curveList = txts

    def drawLineCurve(self,texts):
        width = int(self.defaultSetting('Curve/width',3))
        colors = self.defaultSetting('Curve/colors',[])
        idx = 0
        length = len(colors)
        for text in texts:
            if idx < length:
                color = colors[idx]
            else:
                color = (random.randint(0,256),random.randint(0,256),random.randint(0,256))
            pen = pg.mkPen(color=color,width=width)
            self.plot.plot(*self.core.datas[text](),pen=pen,name=text)
            idx += 1

    def drawScatterCurve(self,texts):
        size = int(self.defaultSetting('Curve/size',5))
        colors = self.defaultSetting('Curve/colors',[])
        symbols = self.defaultSetting('Curve/symbols',[])
        idx = 0
        colors_length = len(colors)
        symbols_length = len(symbols)
        for text in texts:
            if idx < colors_length:
                color = pg.mkColor(colors[idx])
            else:
                color = (random.randint(0,256),random.randint(0,256),random.randint(0,256))
            if idx < symbols_length:
                symbol = symbols[idx]
            else:
                symbol = 'o'
            self.plot.plot(*self.core.datas[text](),pen=color,symbolBrush=color, symbolPen=color, symbol=symbol, symbolSize=size, name=text)
            idx += 1

    def openDataFile(self,fn):
        lastFilePath = self.defaultSetting("File/lastFilePath",self.dirname)
        recentFiles = self.defaultSetting("File/recentFiles",[])
        defaultExtension = self.defaultSetting("FileStructure/defaultExtension","Text File (*.txt)")
        extensions = "Text File (*.txt);;CSV File (*.csv);;Excel File (*.xls;*.xlsx)"
        (fileName,fileType) =QFileDialog.getOpenFileName(self,self.translateText('Please select a data file'),lastFilePath,extensions,defaultExtension)
        if fileName == '':
            return
        fileName = fileName.replace('/','\\')
        dirName = os.path.dirname(fileName)
        self.settings.setValue('File/lastFilePath',dirName)
        try:
            fn(fileName)
            if not fileName in recentFiles:
                recentFiles.append(fileName)
            if len(recentFiles) > 10:
                recentFiles.pop(0)
            self.settings.setValue('File/recentFiles',recentFiles)
            self.settings.sync()
        except Exception as identify:
            print(identify)
            self.critical(self.translateText('Invalid Data File!'))

    def convertFile(self,old,new):
        lastFilePath = self.defaultSetting("File/lastFilePath",self.dirname)
        (fileName,fileType) = QFileDialog.getOpenFileName(self,self.translateText('Please select a data file'),lastFilePath,old,old)
        if fileName == '':
            return
        fileName = fileName.replace('/','\\')
        dirName = os.path.dirname(fileName)
        file = None
        try:
            file = File(fileName)
            file.read_data()
        except:
            self.critical(self.translateText('A error occur, please contact author for help!'))
            return
        (fileName,fileType) = QFileDialog.getSaveFileName(self,"Save File",dirName,new,new)
        if fileName == '':
            return
        file.save_as(fileName)

    def defaultSetting(self,key,default):
        value = self.settings.value(key)
        if value == None:
            self.settings.setValue(key,default)
            self.settings.sync()
            return default
        return value

    def dragEnterEvent(self,e):
        if e.mimeData().text().split('.')[-1].lower() == 'apf':
            e.accept()
        else:
            e.ignore() 

    def dropEvent(self,e):
        self.loadProjectFile(e.mimeData().text().replace('file:///',''))


if __name__ == '__main__':
    QApplication.setOrganizationName("ATL")
    QApplication.setOrganizationDomain("http://www.atlinfo.com")
    QApplication.setApplicationName("Electrical Chemistry Analysor")
    app = QApplication(sys.argv)
    mainWin = Application()
    sys.exit(app.exec_())


