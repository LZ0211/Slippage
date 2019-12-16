#!/usr/bin/env python
# coding=utf-8
import fix_qt_import_error
import re,os,sys
import numpy as np
from Core import Engine,File
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

qtCreatorFile = "GUI.ui"

(Ui_MainWindow, QtBaseClass) = uic.loadUiType(qtCreatorFile)

class Application(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        super().__init__()

        self.core = Engine()
        self.settings=QSettings("setting.ini",QSettings.IniFormat)
        self.initUI()
        self.initAction()

    def initUI(self):
        self.setupUi(self)
        #self.setWindowIcon(QIcon("resource/chemical.ico"))
        #self.setFixedSize(self.width(),self.height())
        self.show()

    def initAction(self):
        #加载数据
        self.bindOpenAction()
        self.bindToolsAction()
        #退出
        self.action_Exit.triggered.connect(QApplication.exit)
        #最近打开的文件
        self.menu_Recent_Files.aboutToShow.connect(self.updateRecentFiles)
        #滑动条
        self.bindSliderAction()
        self.bindSpinBoxAction()
        #参数框
        self.bindInputAction()
        #self.core.bind(self.updateList)

    def bindToolsAction(self):
        #extensions = "Text File (*.txt);;CSV File (*.csv);;Excel File (*.xls;*.xlsx)"
        self.action_Excel2TXT.triggered.connect(lambda :self.convertFile('Excel File (*.xls;*.xlsx)','Text File (*.txt)'))
        self.action_Excel2CSV.triggered.connect(lambda :self.convertFile('Excel File (*.xls;*.xlsx)','CSV File (*.csv)'))
        self.action_CSV2TXT.triggered.connect(lambda :self.convertFile('CSV File (*.csv)','Text File (*.txt)'))
        self.action_CSV2Excel.triggered.connect(lambda :self.convertFile('CSV File (*.csv)','Excel File (*.xls;*.xlsx)'))
        self.action_TXT2CSV.triggered.connect(lambda :self.convertFile('Text File (*.txt)','CSV File (*.csv)'))
        self.action_TXT2Excel.triggered.connect(lambda :self.convertFile('Text File (*.txt)','Excel File (*.xls;*.xlsx)'))

    def bindOpenAction(self):
        self.action_Positive_Reference.triggered.connect(self.loadPositiveRef)
        self.action_Negative_Reference.triggered.connect(self.loadNegativeRef)
        self.action_Measured_Data.triggered.connect(self.loadMeasuredData)

    def bindSliderAction(self):
        self.Pos_Scale_Slider.valueChanged.connect(lambda value:self.Pos_Scale_SpinBox.setSingleStep(0.1**value))
        self.Pos_Shift_Slider.valueChanged.connect(lambda value:self.Pos_Shift_SpinBox.setSingleStep(0.1**value))
        self.Neg_Scale_Slider.valueChanged.connect(lambda value:self.Neg_Scale_SpinBox.setSingleStep(0.1**value))
        self.Neg_Shift_Slider.valueChanged.connect(lambda value:self.Neg_Shift_SpinBox.setSingleStep(0.1**value))

    def bindSpinBoxAction(self):
        self.Pos_Scale_SpinBox.valueChanged.connect(lambda value:self.core.set_param(value,0))
        self.Pos_Shift_SpinBox.valueChanged.connect(lambda value:self.core.set_param(value,1))
        self.Neg_Scale_SpinBox.valueChanged.connect(lambda value:self.core.set_param(value,2))
        self.Neg_Shift_SpinBox.valueChanged.connect(lambda value:self.core.set_param(value,3))

    def bindInputAction(self):
        self.Skip_List.valueChanged.connect(self.core.set_skip_window)
        self.Diff_List.valueChanged.connect(self.core.set_diff_window)

    def infomation(self,text):
        QMessageBox.information(self,"Information",text,QMessageBox.Yes)
        
    def critical(self,text):
        QMessageBox.critical(self,"Critical",text,QMessageBox.Yes)

    def updateRecentFiles(self):
        self.menu_Recent_Files.clear()
        recentFiles = self.settings.value('File/recentFiles') or []
        for fname in recentFiles:
            action =QAction(fname,self,triggered=self.loadMeasuredData)
            action.setData(fname)
            self.menu_Recent_Files.addAction(action)

    def updateList(self):
        self.Data_List

    def showTable(self,table,data):
        if data == None:
            return
        table.setRowCount(data.size)
        for i in range(data.size):
            table.setItem(i,0,QTableWidgetItem(str(data.y_data[i])))
            table.setItem(i,1,QTableWidgetItem(str(data.x_data[i])))

    def loadPositiveRef(self):
        define = self.settings.value('FileStructure/posDataStructure') or self.settings.value('FileStructure/dataStructure') or 'Voltage:Capacity'
        self.openDataFile(lambda f:self.core.read_pos_data(f,define))

    def loadNegativeRef(self):
        define = self.settings.value('FileStructure/negDataStructure') or self.settings.value('FileStructure/dataStructure') or 'Voltage:Capacity'
        self.openDataFile(lambda f:self.core.read_neg_data(f,define))

    def loadMeasuredData(self):
        define = self.settings.value('FileStructure/fullDataStructure') or self.settings.value('FileStructure/dataStructure') or 'Voltage:Capacity'
        self.openDataFile(lambda f:self.core.read_full_data(f,define))

    def openDataFile(self,fn):
        lastFilePath = self.settings.value("File/lastFilePath") or './'
        recentFiles = self.settings.value('File/recentFiles') or []
        defaultExtension = self.settings.value('FileStructure/defaultExtension') or "Text Files (*.txt;*.csv)"
        extensions = "Text File (*.txt);;CSV File (*.csv);;Excel File (*.xls;*.xlsx)"
        (fileName,fileType) = QtWidgets.QFileDialog.getOpenFileName(self,'Please select a data file',lastFilePath,extensions,defaultExtension)
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
            self.critical('Invalid Data File!')

    def convertFile(self,old,new):
        lastFilePath = self.settings.value("File/lastFilePath") or './'
        (fileName,fileType) = QtWidgets.QFileDialog.getOpenFileName(self,'Please select a data file',lastFilePath,old,old)
        if fileName == '':
            return
        fileName = fileName.replace('/','\\')
        dirName = os.path.dirname(fileName)
        file = None
        try:
            file = File(fileName)
            file.read_data()
        except:
            self.critical('Invalid Data File!')
            return
        (fileName,fileType) = QtWidgets.QFileDialog.getSaveFileName(self,"Save File",dirName,new,new)
        if fileName == '':
            return
        file.save_as(fileName)



if __name__ == '__main__':
    QApplication.setOrganizationName("ATL")
    QApplication.setOrganizationDomain("http://www.atlinfo.com")
    QApplication.setApplicationName("Electrical Chemistry Analysor")
    app = QApplication(sys.argv)
    mainWin = Application()
    sys.exit(app.exec_())
