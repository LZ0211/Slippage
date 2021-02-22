import os,sys,re
import numpy as np
from json import load
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QLabel, QComboBox, QDesktopWidget, QPushButton, QMessageBox, QDoubleSpinBox, QAbstractSpinBox,QInputDialog,QLineEdit
from pyqtgraph import PlotWidget, mkPen, mkColor, mkBrush, ScatterPlotItem, PlotCurveItem, PlotDataItem

def isStartWith(str,patterm):
    return patterm == str[:len(patterm)]

class SpinBox(QDoubleSpinBox):
    def __init__(self,suffix=None,lower=0,upper=None,dec=0,step=1,val=0):
        super().__init__()
        suffix and self.setSuffix(suffix)
        upper and self.setMaximum(upper)
        self.setMinimum(lower)
        self.setDecimals(dec)
        self.setSingleStep(step)
        #self.setFixedWidth(80)
        self.setValue(val)
        self.setButtonSymbols(QAbstractSpinBox.NoButtons)

class Design(QWidget):
    colors = {
        "cathode":"#FF0000",
        "anode":"#0000FF",
        "full":"#000000"
    }
    symbols = {
        "cathode":"o",
        "anode":"s",
        "full":"t"
    }
    def __init__(self,parent):
        super(Design, self).__init__()
        self.parent = parent
        self.core = parent.core
        self.parameters = None
        self.datas = None
        self.renderWindow()
        self.initPlotView()
        self.setUpProcessUI()
        self.bindEvents()

    def bindEvents(self):
        self.generate.clicked.connect(self.genCurve)
        self.save.clicked.connect(self.saveCurve)
        self.Sheme.currentIndexChanged.connect(self.selectScheme)
        pass

    def renderWindow(self):
        #边框结构
        self.setGeometry(80, 80, 800, 420)
        size = self.geometry()
        screen = QDesktopWidget().screenGeometry()
        posX = (screen.width() - size.width()) / 2
        posY = (screen.height() - size.height()) / 2
        self.move(posX,posY)
        #标题
        self.setWindowTitle('Designer')
        self.setWindowIcon(QIcon('resource/curve.ico'))
        #布局
        layout = QGridLayout()
        self.graphicsView = QGridLayout()
        layout.addLayout(self.graphicsView, 0, 0, 1, 1)

        self.Process_Box = QGroupBox()
        self.Process_Box.setMinimumSize(240,440)
        self.Process_Box.setFlat(True)
        layout.addWidget(self.Process_Box, 0, 1, 1, 1)

        self.setLayout(layout)

    def setUpProcessUI(self):
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        self.Process_Box.setLayout(layout)

        layout.addWidget(QLabel(self.translate('Standard Cathode')),0,0,1,3)
        layout.addWidget(QLabel(self.translate('Standard Anode')),1,0,1,3)
        layout.addWidget(QLabel(self.translate('Capacity Ratio of 0.01C/0.2C')),2,0,1,3)#()
        layout.addWidget(QLabel(self.translate('Capacity of 0.2C')),3,0,1,3)
        layout.addWidget(QLabel(self.translate('1st Cycle Efficiency')),4,0,1,3)
        layout.addWidget(QLabel(self.translate('Cathode Area')),5,0,1,3)
        layout.addWidget(QLabel(self.translate('Cathode Coating Weight')),6,0,1,3)
        layout.addWidget(QLabel(self.translate('Cathode Loading')),7,0,1,3)
        layout.addWidget(QLabel(self.translate('Anode Coating Weight')),8,0,1,3)
        layout.addWidget(QLabel(self.translate("Anode Loading")),9,0,1,3)
        layout.addWidget(QLabel(self.translate("Sheme")),10,0,1,3)
        layout.addWidget(QLabel(self.translate("Discharge Start Voltage")),11,0,1,3)
        layout.addWidget(QLabel(self.translate("Discharge End Voltage")),12,0,1,3)

        self.Cathodes = QComboBox()
        self.Anodes = QComboBox()
        keys = list(self.core.datas.keys())
        keys.sort(key=lambda x:self.core.order.index(x))
        for k in keys:
            for tag in self.core.pos_tag:
                if isStartWith(k,tag):
                    self.Cathodes.addItem(k)
                    break
            for tag in self.core.neg_tag:
                if isStartWith(k,tag):
                    self.Anodes.addItem(k)
                    break
        self.Sheme = QComboBox()
        self.Sheme.addItems([self.translate("Discharge Start Voltage"),self.translate("Discharge End Voltage")])
        self.Ratio = SpinBox(lower=0,upper=10,dec=4)
        self.Capacity = SpinBox(lower=0,upper=10000,val=0,dec=4)
        self.Efficiency = SpinBox(lower=0,upper=1,val=0.98,dec=4)
        self.CathodeArea = SpinBox(lower=0,upper=1E9,dec=4)
        self.CathodeCW = SpinBox(lower=0,upper=1E9,dec=4)
        self.CathodeLoading = SpinBox(lower=0,upper=1,dec=4)
        self.AnodeCW = SpinBox(lower=0,upper=1E9,dec=4)
        self.AnodeLoading = SpinBox(lower=0,upper=1,dec=4)
        self.StartVoltage = SpinBox(lower=0,upper=5,val=4.3,dec=4)
        self.EndVoltage = SpinBox(lower=0,upper=5,val=2.7,dec=4)

        layout.addWidget(self.Cathodes,0,3,1,3)
        layout.addWidget(self.Anodes,1,3,1,3)
        layout.addWidget(self.Ratio,2,3,1,3)
        layout.addWidget(self.Capacity,3,3,1,3)
        layout.addWidget(self.Efficiency,4,3,1,3)
        layout.addWidget(self.CathodeArea,5,3,1,3)
        layout.addWidget(self.CathodeCW,6,3,1,3)
        layout.addWidget(self.CathodeLoading,7,3,1,3)
        layout.addWidget(self.AnodeCW,8,3,1,3)
        layout.addWidget(self.AnodeLoading,9,3,1,3)
        layout.addWidget(self.Sheme,10,3,1,3)
        layout.addWidget(self.StartVoltage,11,3,1,3)
        layout.addWidget(self.EndVoltage,12,3,1,3)

        self.load = QPushButton(self.translate("Load"))
        self.generate = QPushButton(self.translate("Generate"))
        self.save = QPushButton(self.translate("Save"))
        self.load.setDisabled(True)
        scheme = int(self.defaultSetting("Design/Sheme",0))
        self.Sheme.setCurrentIndex(scheme)
        self.selectScheme()
        layout.addWidget(self.load,13,0,1,2)
        layout.addWidget(self.generate,13,2,1,2)
        layout.addWidget(self.save,13,4,1,2)
        pass

    def initPlotView(self):
        self.plot = PlotWidget(enableAutoRange=True)
        self.plotLegand = self.plot.addLegend()
        self.graphicsView.addWidget(self.plot)
        self.setGraphViewStyle()

    def setGraphViewStyle(self):
        bgColor = self.defaultSetting('Graph/BackgroundColor','#ffffff')
        gridAlpha = float(self.defaultSetting('Graph/GridAlpha',0.25))
        axisColor = self.defaultSetting('Graph/AxisColor','#000000')
        axisWidth = float(self.defaultSetting('Graph/AxisWidth',1.5))
        self.plot.setAutoVisible(y=True)
        self.plot.setBackground(bgColor)
        self.plot.showGrid(x=True,y=True, alpha=gridAlpha)
        self.plot.getAxis('bottom').setPen(color=axisColor,width=axisWidth)
        self.plot.getAxis('left').setPen(color=axisColor,width=axisWidth)

    def drawCurve(self,x,y,text):
        self.plot.removeItem(text)
        curveType = self.defaultSetting('Curve/type','line')
        width = int(self.defaultSetting('Curve/width',3))
        size = int(self.defaultSetting('Curve/size',5))
        color = self.colors[text]
        symbol = self.symbols[text]
        pen = mkPen(color=color,width=width)
        text = self.translate(text)
        self.plotLegand.removeItem(text)
        if curveType == 'scatter':
            self.plot.plot(x,y,pen=pen,symbolBrush=color, symbolPen=color, symbol=symbol, symbolSize=size, name=text)
        else:
            self.plot.plot(x,y,pen=pen,name=text)
        self.plot.show()

    def genCurve(self):
        posName = self.Cathodes.currentText()
        negName = self.Anodes.currentText()
        capacity = self.Ratio.value() * self.Capacity.value()
        posMass = self.CathodeArea.value() * self.CathodeCW.value() * self.CathodeLoading.value() / 1540.25
        negMass = self.CathodeArea.value() * self.AnodeCW.value() * self.AnodeLoading.value() / 1540.25
        efficiency = self.Efficiency.value()
        if capacity*posMass*negMass*efficiency == 0 or posName == "" or negName == "":
            self.critical("Invalid Parameters!")
            return
        posLoss = capacity * (1 / efficiency - 1)
        #print(posMass,posLoss)
        posData = self.core.get_data(posName).modify_x(posMass,0)
        posLoss = posData.x_max - capacity - posLoss
        if posLoss < 0:
            return self.cathodeLess()
        posData = self.core.get_data(posName).modify_x(posMass,posLoss)
        #print(posMass,posLoss)
        if self.Sheme.currentIndex() == 1:
            terminal = posData.posValue(capacity)
            #print(terminal)
            if terminal == None:
                return self.cathodeLess()
            delta = terminal - self.EndVoltage.value()
            negData = self.core.get_data(negName).modify_x(negMass,0)
            terminal = negData.invert().posValue(delta)
            if terminal == None or terminal < capacity:
                return self.anodeLess()
            negLoss = terminal-capacity
            negData = self.core.get_data(negName).modify_x(negMass,negLoss)
        else:
            terminal = posData.posValue(0)
            if terminal == None:
                return self.cathodeLess()
            delta = terminal - self.StartVoltage.value()
            negData = self.core.get_data(negName).modify_x(negMass,0)
            #print(delta)
            terminal = negData.invert().posValue(delta)
            if terminal == None:
                return self.anodeLess()
            negLoss = terminal
            negData = self.core.get_data(negName).modify_x(negMass,negLoss)
            if negData.x_max < capacity:
                return self.anodeLess()
        fulDataX = np.linspace(0, capacity, 2000)
        fulDataY = posData.interpolate(fulDataX).y_data - negData.interpolate(fulDataX).y_data
        self.parameters = [posMass,posLoss,negMass,negLoss]
        self.datas = [posData,negData,posData.copy(fulDataX,fulDataY)]
        for x in self.plot.items():
            if isinstance(x,(ScatterPlotItem,PlotCurveItem, PlotDataItem)):
                self.plot.removeItem(x)
        self.drawCurve(*posData(),"cathode")
        self.drawCurve(*negData(),"anode")
        self.drawCurve(fulDataX,fulDataY,"full")

    def saveCurve(self):
        # (value, ok) = QInputDialog.getText(self, self.translate("Save Data"), self.translate("Please input data name"), QLineEdit.Normal, "")
        # if not ok:
        #     return
        # if self.parameters == None or self.datas == None:
        #     return
        # if value == "":
        #     self.critical("Data name can not be empty string!")
        #     return
        # elif re.match(r'(\:|\\|\/|\*|\?|\"|<|>|\|)',value):
        #     self.critical("There are invalid characters in the data name!")
        #     return
        # if (value + "_full") in self.core.datas or (value + "_anode") in self.core.datas or (value + "_cathode") in self.core.datas:
        #     ok = self.warnning("Data with the same name already exists!\nDo you want to override old datas?")
        #     if not ok:
        #         return
        # self.core.add_data((value + "_cathode"),self.datas[0],override=True)
        # self.core.add_data((value + "_anode"),self.datas[1],override=True)
        # self.core.add_data((value + "_full"),self.datas[2],override=True)
        self.core.max_capacity = self.Ratio.value() * self.Capacity.value()
        self.parent.setSetting('Core/MaxCapacity',self.core.max_capacity)
        self.core.auto_cal_param(self.parameters[0],0)
        self.core.auto_cal_param(self.parameters[1],1)
        self.core.auto_cal_param(self.parameters[2],2)
        self.core.auto_cal_param(self.parameters[3],3)
        self.core.for_fitting = [self.Cathodes.currentText(),self.Anodes.currentText(),""]
        self.core.triggle('change')
        self.core.triggle('fitting')

    def anodeLess(self):
        self.critical("The theoretical maximum anode capacity is less than the design capacity!")

    def cathodeLess(self):
        self.critical("The theoretical maximum cathode capacity is less than the design capacity!")

    def selectScheme(self,idx=0):
        if self.Sheme.currentIndex() == 0:
            self.EndVoltage.setDisabled(True)
            self.StartVoltage.setEnabled(True)
        else:
            self.StartVoltage.setDisabled(True)
            self.EndVoltage.setEnabled(True)
        self.setSetting("Design/Sheme",self.Sheme.currentIndex())

    def translate(self,text):
        if self.parent:
            self.langText = self.parent.langText
        else:
            self.langText = load(open('SCN.translation',encoding='utf-8'))
        if text in self.langText:
            return self.langText[text]
        return text

    def defaultSetting(self,key,value):
        if self.parent:
            return self.parent.defaultSetting(key,value)
        return value

    def setSetting(self,key,value):
        if self.parent:
            return self.parent.setSetting(key,value)

    def critical(self,text):
        QMessageBox.critical(self,self.translate("Critical"),self.translate(text),QMessageBox.Yes)

    def warnning(self,text):
        return QMessageBox.warning(self,self.translate("Warning"),self.translate(text),QMessageBox.No|QMessageBox.Yes)