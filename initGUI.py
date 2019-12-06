#!/usr/bin/env python
# coding=utf-8
import re,os,sys
import numpy as np
from Core.Engine import Engine
from Core.DataSet import DataSet
from Core.File import File
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

qtCreatorFile = "mainWindow.ui"

(Ui_MainWindow, QtBaseClass) = uic.loadUiType(qtCreatorFile)

dataCache = {
    "full_file_list":[],
    "full_file_data":{}
}

class Application(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        super().__init__()

        self.settings=QSettings("setting.ini",QSettings.IniFormat)
        self.initUI()
        self.initAction()

    def initUI(self):
        self.setupUi(self)
        self.setWindowIcon(QIcon("resource/chemical.ico"))
        self.setFixedSize(self.width(),self.height())
        self.show()

    def initAction(self):
        self.actionPositive_Reference.triggered.connect(self.loadPositiveRef)
        self.actionNegative_Reference.triggered.connect(self.loadNegativeRef)
        self.actionMeasured_Data.triggered.connect(self.loadMeasuredData)
        self.actionExit.triggered.connect(QApplication.exit)

    def bindModel(self):
        file_list = QStringListModel()
        file_list.setStringList(dataCache['full_file_list'])
        self.full_file_list.setModel(file_list)

    def showTable(self,table,data):
        if data == None:
            return
        table.setRowCount(data.size)
        for i in range(data.size):
            table.setItem(i,0,QTableWidgetItem(str(data.y_data[i])))
            table.setItem(i,1,QTableWidgetItem(str(data.x_data[i])))

    def loadPositiveRef(self):
        define = self.settings.value('FileStructure/posDataStructure') or self.settings.value('FileStructure/dataStructure') or 'Voltage:Capacity'
        (fileName,data) = self.openDataFile(define)
        self.showTable(self.pos_data_table,data)

    def loadNegativeRef(self):
        define = self.settings.value('FileStructure/negDataStructure') or self.settings.value('FileStructure/dataStructure') or 'Voltage:Capacity'
        (fileName,data) = self.openDataFile(define)
        self.showTable(self.neg_data_table,data)

    def loadMeasuredData(self):
        define = self.settings.value('FileStructure/fullDataStructure') or self.settings.value('FileStructure/dataStructure') or 'Voltage:Capacity'
        (fileName,data) = self.openDataFile(define)
        self.showTable(self.full_data_table,data)
        dataCache['full_file_list'].append(fileName)
        dataCache['full_file_data'][fileName] = data

    def openDataFile(self,define):
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
        if not fileName in recentFiles:
            recentFiles.append(fileName)
        if len(recentFiles) > 10:
            recentFiles.pop(0)
        self.settings.setValue('File/recentFiles',recentFiles)
        self.settings.sync()
        try:
            data = File(fileName).read_data()
        except Exception as error:
            QMessageBox.critical(self,"Error","Invalid Data File!",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            return
        cols = list(map(lambda x:x.strip(),define.strip().split(':')))
        cap_idx = cols.index('Capacity')
        vol_idx = cols.index('Voltage')
        matrix = np.array(data)
        x_data = matrix[:,cap_idx]
        y_data = matrix[:,vol_idx]
        data = DataSet(x_data,y_data)
        return (fileName,data)


if __name__ == '__main__':
    QApplication.setOrganizationName("ATL")
    QApplication.setOrganizationDomain("http://www.atlinfo.com")
    QApplication.setApplicationName("Electrical Chemistry Analysor")
    app = QApplication(sys.argv)
    mainWin = Application()
    sys.exit(app.exec_())
