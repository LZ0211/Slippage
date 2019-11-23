#!/usr/bin/env python
# coding=utf-8
import sys,os,re
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

qtCreatorFile = "AECA.ui"

(Ui_MainWindow, QtBaseClass) = uic.loadUiType(qtCreatorFile)


class Figure_Canvas(FigureCanvas):
    def __init__(self,parent=None,width=5,height=4,dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self,data):
        self.axes = self.figure.add_subplot(111)
        self.axes.hold(False)
        self.axes.grid('on')
        self.axes.plot(data)
        self.draw()


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
        self.show()

    def initAction(self):
        self.actionPositive_Reference.triggered.connect(self.loadPositiveRef)
        self.actionNegative_Reference.triggered.connect(self.loadNegativeRef)
        self.actionMeasured_Data.triggered.connect(self.loadMeasuredData)
        self.actionExit.triggered.connect(QApplication.exit)
        self.tablePositiveData.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tablePositiveData.customContextMenuRequested.connect(lambda x:self.tableLeftMenu(self.tablePositiveData,x))

    def loadPositiveRef(self):
        fileName = self.openFile('Please load the positive reference data',"Text Files (*.txt;*.csv)")
        datas = map(lambda x:re.split(r'\s+',x.strip()),open(fileName).read().strip().split('\n'))
        datas = list(datas)
        length = len(datas)
        self.tablePositiveData.setRowCount(length)
        for i in range(length):
            self.tablePositiveData.setItem(i,0,QTableWidgetItem(datas[i][0]))
            self.tablePositiveData.setItem(i,1,QTableWidgetItem(datas[i][1]))

    def tableLeftMenu(self,table,pos):
        idx = 0
        indexs = table.selectedItems()
        if len(indexs) > 1:
            idx = table.selectionModel().currentIndex().row()
        menu = QMenu()
        print(idx)
        insert = menu.addAction("Insert Row")
        delete = menu.addAction("Delete Row")
        action = menu.exec_(table.mapToGlobal(pos))
        if action == insert:
            table.insertRow(idx)
        if action == delete:
            table.removeRow(idx)
        

    def loadNegativeRef(self):
        fileName = self.openFile('Please load the negative reference data',"Text Files (*.txt;*.csv)")

    def loadMeasuredData(self):
        fileName = self.openFile('Please load the measured reference data',"Text Files (*.txt;*.csv)")

    def openFile(self,text,types):
        lastFilePath = self.settings.value("File/lastFilePath") or './'
        recentFiles = self.settings.value('File/recentFiles') or []
        print(lastFilePath)
        (fileName,fileType) = QtWidgets.QFileDialog.getOpenFileName(self,text,lastFilePath,types)
        if fileName == None:
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
        return fileName


if __name__ == '__main__':
    QApplication.setOrganizationName("ATL")
    QApplication.setOrganizationDomain("http://www.atlinfo.com")
    QApplication.setApplicationName("Electrical Chemistry Analysor")
    app = QApplication(sys.argv)
    mainWin = Application()
    sys.exit(app.exec_())
