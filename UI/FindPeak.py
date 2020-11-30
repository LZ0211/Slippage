import os,sys,re
import numpy as np
from json import load
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, Signal
from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QLineEdit, QLabel,QComboBox,QDesktopWidget, QPushButton, QTextEdit, QDoubleSpinBox,QAbstractSpinBox
from pyqtgraph import PlotWidget, mkPen, mkColor, mkBrush, LinearRegionItem, ScatterPlotItem, PlotCurveItem, PlotDataItem, LinearRegionItem, InfiniteLine
from scipy.integrate import simps

class SpinBox(QDoubleSpinBox):
    def __init__(self,suffix=None,lower=0,upper=None,dec=0,step=1,val=0):
        super().__init__()
        suffix and self.setSuffix(suffix)
        upper and self.setMaximum(upper)
        self.setMinimum(lower)
        self.setDecimals(dec)
        self.setSingleStep(step)
        self.setFixedWidth(80)
        self.setValue(val)

class FindPeak(QWidget):
    def __init__(self,parent,x_data,y_data):
        super(FindPeak, self).__init__()
        self.parent = parent
        self.x = x_data
        self.y = y_data
        self.lower = np.min(x_data)
        self.upper = np.max(x_data)
        self.range = self.upper - self.lower
        self.renderWindow()
        self.initPlotView()
        self.drawCurve()
        self.setUpProcessUI()
        self.bindEvents()
        self.integral(x_data,y_data,self.lower,self.upper)

    def bindEvents(self):
        self.bindBoundEvent()
        self.bindAlgorithmEvent()
        self.bindFindEvent()

    def bindBoundEvent(self):
        def leftBoundEvent(x):
            self.lower = x
            upper = self.upper
            self.plotRegion.setRegion([x,upper])
            self.rightBound.setMinimum(x)
            self.peakCenter.setMinimum(x)
            self.peakCenter.setValue((x+upper)/2)
            self.integral(self.x,self.y,x,upper)
        def rightBoundEvent(x):
            self.upper = x
            lower = self.lower
            self.plotRegion.setRegion([lower,x])
            self.leftBound.setMaximum(x)
            self.peakCenter.setMaximum(x)
            self.peakCenter.setValue((x+lower)/2)
            self.integral(self.x,self.y,lower,x)
        def regionChangeEvent():
            lower,upper = self.plotRegion.getRegion()
            self.lower = lower
            self.upper = upper
            self.leftBound.setValue(lower)
            self.leftBound.setMaximum(upper)
            self.rightBound.setValue(upper)
            self.rightBound.setMinimum(lower)
            self.peakCenter.setMinimum(lower)
            self.peakCenter.setMaximum(upper)
            self.peakCenter.setValue((lower+upper)/2)
            self.integral(self.x,self.y,lower,upper)

        self.leftBound.valueChanged.connect(leftBoundEvent)
        self.rightBound.valueChanged.connect(rightBoundEvent)
        self.plotRegion.sigRegionChanged.connect(regionChangeEvent)

    def bindAlgorithmEvent(self):
        def updateInput(a,b,c,d,e,f):
            self.peakWidth.setEnabled(a)
            self.detectDis.setEnabled(b)
            self.noisePrt.setEnabled(c)
            self.amplitude.setEnabled(d)
            self.threshold.setEnabled(e)
            self.findBtn.setEnabled(f)

        def changeAlgorithm(algorithm):
            if algorithm == "Extremum":
                updateInput(False,False,False,False,False,True)
                pass
            elif algorithm == "Matlab Like":
                updateInput(True,True,False,True,True,False)
                pass
            elif algorithm == "Gaussian":
                updateInput(False,False,False,False,False,False)
                pass
            elif algorithm == "Lorentzian":
                updateInput(False,False,False,False,False,False)
                pass
            elif algorithm == "Pseudo-Voigt":
                updateInput(False,False,False,False,False,False)
                pass
            elif algorithm == "Continuous Wavelet Transform":
                updateInput(True,True,False,True,True,False)
                pass
        self.algorithm.currentTextChanged.connect(changeAlgorithm)
        updateInput(False,False,False,False,False,True)

    def integral(self,x_data,y_data,lower,upper):
        idx = np.where((x_data >= lower) & (x_data <= upper))
        x = x_data[idx]
        y = y_data[idx]
        self.integralArea.setValue(simps(y,x))

    def bindFindEvent(self):
        x_data = self.x
        y_data = self.y
        def findPeak():
            region = np.where((x_data >= self.lower) & (x_data <= self.upper))
            sub_data = y_data[region]
            algorithm = self.algorithm.currentText()
            shape = self.shape.currentText()
            if algorithm == "Extremum":
                if shape == "Peak":
                    peak = np.max(sub_data)
                else:
                    peak = np.min(sub_data)
                idx = np.where((x_data >= self.lower) & (x_data <= self.upper) & (y_data == peak))
                x = x_data[idx]
                y = y_data[idx]
                self.peakCenter.setValue(x)
                return self.renderPeakPoint([x,y])
            pass
        self.findBtn.clicked.connect(findPeak)

    def renderPeakPoint(self,pos):
        self.peakPoint.clear()
        self.peakPoint.addPoints([{'pos': pos, 'data': 1}])

    def renderWindow(self):
        #边框结构
        self.setGeometry(80, 80, 800, 420)
        size = self.geometry()
        screen = QDesktopWidget().screenGeometry()
        posX = (screen.width() - size.width()) / 2
        posY = (screen.height() - size.height()) / 2
        self.move(posX,posY)
        #标题
        self.setWindowTitle('Find Peak')
        self.setWindowIcon(QIcon('resource/curve.ico'))
        #布局
        layout = QGridLayout()
        self.graphicsView = QGridLayout()
        layout.addLayout(self.graphicsView, 0, 0, 1, 1)

        self.Process_Box = QGroupBox()
        self.Process_Box.setMinimumSize(200,420)
        self.Process_Box.setFlat(True)
        layout.addWidget(self.Process_Box, 0, 1, 1, 1)

        self.setLayout(layout)

    def setUpProcessUI(self):
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        self.Process_Box.setLayout(layout)

        layout.addWidget(QLabel(self.translate('Left Boundary')),0,0,1,1)
        layout.addWidget(QLabel(self.translate('Right Boundary')),1,0,1,1)
        layout.addWidget(QLabel(self.translate("Integral Area")),2,0,1,1)
        layout.addWidget(QLabel(self.translate('Peak Center')),3,0,1,1)
        layout.addWidget(QLabel(self.translate('Peak Shape')),4,0,1,1)
        layout.addWidget(QLabel(self.translate('Find Peak Algorithm')),5,0,1,1)
        layout.addWidget(QLabel(self.translate('Minimum Peak Width')),6,0,1,1)
        layout.addWidget(QLabel(self.translate('Minimum Detect Distance')),7,0,1,1)
        layout.addWidget(QLabel(self.translate('Noise Percent')),8,0,1,1)
        layout.addWidget(QLabel(self.translate("Minimum Amplitude")),9,0,1,1)
        layout.addWidget(QLabel(self.translate("Relative Threshold")),10,0,1,1)
        

        self.leftBound = SpinBox(lower=self.lower,dec=4,val=self.lower)
        self.rightBound = SpinBox(upper=self.upper,dec=4,val=self.upper)
        self.peakCenter = SpinBox(lower=self.lower,upper=self.upper,dec=4)
        self.peakWidth = SpinBox(lower=self.lower,upper=self.upper,dec=4)
        self.noisePrt = SpinBox(lower=0,upper=100,dec=4,step=1,val=10)
        self.detectDis = SpinBox(lower=1)
        self.amplitude = SpinBox(lower=1)
        self.threshold = SpinBox(lower=1)
        self.integralArea = SpinBox(upper=1E8,dec=4)
        self.integralArea.setReadOnly(True)
        self.integralArea.setButtonSymbols(QAbstractSpinBox.NoButtons)
        
        
        self.shape = QComboBox()
        self.shape.addItems(["Peak","Valley"])
        #self.shape.currentTextChanged.connect()

        self.algorithm = QComboBox()
        self.algorithm.addItems(['Extremum','Matlab Like','Gaussian','Lorentzian','Pseudo-Voigt','Continuous Wavelet Transform'])
        #self.algorithm.currentTextChanged.connect()
        #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks_cwt.html
        layout.addWidget(self.leftBound,0,1,1,1)
        layout.addWidget(self.rightBound,1,1,1,1)
        layout.addWidget(self.integralArea,2,1,1,1)
        layout.addWidget(self.peakCenter,3,1,1,1)
        layout.addWidget(self.shape,4,1,1,1)
        layout.addWidget(self.algorithm,5,1,1,1)
        layout.addWidget(self.peakWidth,6,1,1,1)
        layout.addWidget(self.detectDis,7,1,1,1)
        layout.addWidget(self.noisePrt,8,1,1,1)
        layout.addWidget(self.amplitude,9,1,1,1)
        layout.addWidget(self.threshold,10,1,1,1)
        
        self.findBtn = QPushButton(self.translate('Find Peak'))
        layout.addWidget(self.findBtn,11,0,1,2)
        pass

    def initPlotView(self):
        self.plot = PlotWidget(enableAutoRange=True)
        self.plot.setXRange(self.lower - self.range * 0.05,self.upper + self.range * 0.05)
        self.plotLegand = self.plot.addLegend()
        self.graphicsView.addWidget(self.plot)
        self.plotRegion = LinearRegionItem()
        self.plotRegion.setZValue(10)
        self.peakPoint = ScatterPlotItem(size=8, pen=mkPen(color='0000FF',width=2), symbol="+", brush=mkBrush(255, 255, 255, 240))
        self.plot.addItem(self.plotRegion, ignoreBounds=True)
        self.plot.addItem(self.peakPoint)
        self.setGraphViewStyle()

    def setGraphViewStyle(self):
        self.plot.setAutoVisible(y=True)
        self.plot.setBackground('#ffffff')
        self.plot.showGrid(x=True,y=True, alpha=0.25)
        self.plot.getAxis('bottom').setPen(color='#000000',width=1.5)
        self.plot.getAxis('left').setPen(color='#000000',width=1.5)
        self.plotRegion.setRegion([self.lower,self.upper])
        self.plotRegion.setBounds([self.lower,self.upper])

    def drawCurve(self):
        pen = mkPen(color='FF0000',width=2)
        self.plot.plot(self.x,self.y,pen=pen)
        self.plot.show()

    def translate(self,text):
        if self.parent:
            self.langText = self.parent.langText
        else:
            self.langText = load(open('SCN.translation',encoding='utf-8'))
        if text in self.langText:
            return self.langText[text]
        return text


