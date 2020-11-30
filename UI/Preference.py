import os,sys,re
from json import load
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QBrush, QColor, QCursor, QPalette, QPainter, QFont, QPen
from PyQt5.QtCore import Qt, Signal, QRect
from PyQt5.QtWidgets import QWidget, QFileDialog, QListWidget, QListWidgetItem, QApplication, QStackedWidget, QRadioButton, QAbstractItemView, QHBoxLayout, QFormLayout, QGridLayout, QLineEdit, QCheckBox, QLabel,QComboBox,QDesktopWidget, QPushButton, QSpinBox, QColorDialog, QMenu, QAction, QTextEdit, QDoubleSpinBox, QSlider, QFrame

class ColorBar(QFrame):
    clicked = Signal()
    doubleClicked = Signal()
    def __init__(self,color='#000000'):
        super().__init__()
        self.setFixedSize(80,20)
        self.setColor(color)

    def setColor(self,color='#ffffff'):
        self.color = color
        self.setStyleSheet('border-width:1px;border-style:solid;border-color:rgb(120, 120, 120);background-color:' + color)

    def getColor(self):
        return self.color

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()

    def mouseDoubleClickEvent(self, e):
        self.doubleClicked.emit()

class SwitchButton(QSlider):
    def __init__(self, parent=None):
        super(SwitchButton, self).__init__(parent)
        self.resize(50, 20)
        self.setFixedSize(50,20)
        self.setMinimum(0)
        self.setMaximum(1)
        self.setOrientation(Qt.Orientation.Horizontal)

    def paintEvent(self, event):
        """绘制按钮"""
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        # 定义字体样式
        font = QFont('Microsoft YaHei')
        font.setPixelSize(10)
        font.setWeight(500)
        painter.setFont(font)
        # 开关为开的状态
        if self.value() == 1:
            # 绘制背景
            painter.setPen(Qt.NoPen)
            brush = QBrush(QColor('#2292DD'))
            painter.setBrush(brush)
            painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height() // 2, self.height() // 2)
            # 绘制圆圈
            painter.setPen(Qt.NoPen)
            brush.setColor(QColor('#ffffff'))
            painter.setBrush(brush)
            painter.drawRoundedRect(32, 2, 16, 16, 8, 8)
            # 绘制文本
            painter.setPen(QPen(QColor('#ffffff')))
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QRect(10, 2, 36, 16), Qt.AlignLeft, 'ON')
        else:
            # 绘制背景
            painter.setPen(Qt.NoPen)
            brush = QBrush(QColor('#FFFFFF'))
            painter.setBrush(brush)
            painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height()//2, self.height()//2)
            # 绘制圆圈
            pen = QPen(QColor('#999999'))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawRoundedRect(2, 2, 16, 16, 8, 8)
            # 绘制文本
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QRect(20, 2, 36, 16), Qt.AlignLeft, 'OFF')

class SpinBox(QDoubleSpinBox):
    def __init__(self,suffix=None,lower=0,upper=None,dec=0,step=1):
        super().__init__()
        suffix and self.setSuffix(suffix)
        upper and self.setMaximum(upper)
        self.setMinimum(lower)
        self.setDecimals(dec)
        self.setSingleStep(step)
        self.setFixedWidth(80)

class Preference(QWidget):
    def __init__(self,parent=None):
        super(Preference, self).__init__()
        self.langText = {}
        self.parent = parent
        self.setupUI()
        self.center()

    def center(self):
        size = self.geometry()
        screen = QDesktopWidget().screenGeometry()
        posX = (screen.width() - size.width()) / 2
        posY = (screen.height() - size.height()) / 2
        self.move(posX,posY)

    def setupUI(self):
        #self.setGeometry(500, 400, 10, 10)
        #self.setFixedSize(500, 400)
        self.setWindowTitle('Preference')
        self.setWindowIcon(QIcon('resource/curve.ico'))

        self.list = QListWidget()
        self.list.setFixedWidth(120)
        self.list.insertItem(0,self.translate('File Structure'))
        self.list.insertItem(1,self.translate('Curve'))
        self.list.insertItem(2,self.translate('Graph'))
        self.list.insertItem(3,self.translate('Core Function'))
        self.list.insertItem(4,self.translate('UI Function'))

        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()
        self.stack5 = QWidget()

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()
        self.tab5UI()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)
        self.stack.addWidget(self.stack4)
        self.stack.addWidget(self.stack5)

        hbox = QHBoxLayout()
        hbox.addWidget(self.list)
        hbox.addWidget(self.stack)
        self.setLayout(hbox)

        self.list.currentRowChanged.connect(self.display)

    def tab1UI(self):
        layout = QFormLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        def extensions():
            cb = QComboBox()
            cb.addItems(['All (*.txt;*.csv;*.xls;*.xlsx)','Text File (*.txt)','CSV File (*.csv)','Excel File (*.xls;*.xlsx)'])
            return cb

        def structures():
            cb = QComboBox()
            cb.setEditable(True)
            cb.addItems(['Voltage:Capacity','Capacity:Voltage'])
            return cb

        def hotfix(key):
            def func(value):
                self.setSetting('FileStructure/'+key,value)
            return func

        items = [
            ["defaultExtension",extensions(),'Default File Extension','Text File (*.txt)'],
            ["dataStructure",structures(),'Default File Extension','Voltage:Capacity'],
            ["posDataStructure",structures(),'Positive Data Structure','Voltage:Capacity'],
            ["negDataStructure",structures(),'Negative Data Structure','Voltage:Capacity'],
            ["fullDataStructure",structures(),'Full Cell Data Structure','Voltage:Capacity']
        ]

        for item in items:
            (k,v,label,default) = tuple(item)
            layout.addRow(QLabel(self.translate(label)),v)
            v.setCurrentText(self.defaultSetting('FileStructure/'+k,default))
            v.currentTextChanged.connect(hotfix(k))

        self.stack1.setLayout(layout)

    def tab2UI(self):
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        radio_line = QRadioButton('line')
        radio_scatter = QRadioButton('scatter')
        layout.addWidget(QLabel(self.translate('Curve Type')),0,0,1,1)
        layout.addWidget(radio_line,0,1,1,1)
        layout.addWidget(radio_scatter,0,2,1,1)

        lineWidth = SpinBox(lower=1)
        layout.addWidget(QLabel(self.translate('Curve Width')),1,0,1,1)
        layout.addWidget(lineWidth,1,1,1,1)

        symbolSize = SpinBox(lower=1)
        layout.addWidget(QLabel(self.translate('Symbol Size')),2,0,1,1)
        layout.addWidget(symbolSize,2,1,1,1)

        def saveColors():
            array = []
            for i in range(colorList.count()):
                item = colorList.item(i)
                color = item.background().color()
                array.append(color)
            self.setSetting('Curve/colors',array)

        colorList = QListWidget()
        colorList.setFixedWidth(80)
        colorList.setDragEnabled(True)
        colorList.setProperty("showDropIndicator", True)
        colorList.setDragDropMode(QAbstractItemView.DragDrop)
        colorList.setDefaultDropAction(Qt.MoveAction)
        drop = colorList.dropEvent
        colorList.dropEvent = lambda x:drop(x) or saveColors()
        layout.addWidget(QLabel(self.translate('Color Sequence')),3,0,1,1)
        layout.addWidget(colorList,3,1,7,1)

        applyBtn = QPushButton(self.translate('Apply'))
        layout.addWidget(applyBtn,10,0,1,4)

        ctype = self.defaultSetting('Curve/type','line')
        if ctype == 'line':
            radio_line.setChecked(True)
        else:
            radio_scatter.setChecked(True)

        lineWidth.setValue(int(self.defaultSetting('Curve/width',3)))
        symbolSize.setValue(int(self.defaultSetting('Curve/size',5)))

        colors = self.defaultSetting('Curve/colors',['#FF0000', '#0000FF', '#00FF00', '#FFFF00', '#FF00FF', '#00FFFF'])
        for color in colors:
            item = QListWidgetItem()
            #item.setText(color)
            #item.setTextColor(QColor(color))
            brush = QBrush(QColor(color))
            brush.setStyle(Qt.SolidPattern)
            item.setBackground(brush)
            colorList.addItem(item)

        def changeColor():
            items = colorList.selectedItems()
            if len(items) == 0:
                return
            item = items[0]
            currentcolor = item.background().color()
            color = QColorDialog.getColor(currentcolor)
            if not QColor.isValid(color):
                return
            brush = QBrush(QColor(color))
            brush.setStyle(Qt.SolidPattern)
            item.setBackground(brush)
            saveColors()

        def showMenu():
            item = colorList.currentItem()
            if not item:
                delColorAction.setDisabled(True)
            else:
                delColorAction.setEnabled(True)
            menu.exec_(QCursor.pos())
            
        def addColor():
            color = QColorDialog.getColor(QColor('#000000'))
            if not QColor.isValid(color):
                return
            item = QListWidgetItem()
            brush = QBrush(QColor(color))
            brush.setStyle(Qt.SolidPattern)
            item.setBackground(brush)

            citem = colorList.currentItem()
            if not citem:
                colorList.addItem(item)
            else:
                colorList.insertItem(colorList.currentRow(),item)
            saveColors()

        def delColor():
            colorList.takeItem(colorList.currentRow())
            saveColors()

        menu = QMenu(colorList)
        addColorAction = QAction(self.translate('Add Color'),menu)
        delColorAction = QAction(self.translate('Del Color'),menu)
        menu.addAction(addColorAction)
        menu.addAction(delColorAction)
        addColorAction.triggered.connect(addColor)
        delColorAction.triggered.connect(delColor)

        colorList.setContextMenuPolicy(Qt.CustomContextMenu)
        colorList.customContextMenuRequested.connect(showMenu)

        radio_line.toggled.connect(lambda :self.setSetting('Curve/type','line'))
        radio_scatter.toggled.connect(lambda :self.setSetting('Curve/type','scatter'))
        lineWidth.valueChanged.connect(lambda x:self.setSetting('Curve/width',x))
        symbolSize.valueChanged.connect(lambda x:self.setSetting('Curve/size',x))
        colorList.doubleClicked.connect(changeColor)
        applyBtn.clicked.connect(self.drawCurves)

        self.stack2.setLayout(layout)

    def tab3UI(self):
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        def changeColor(obj,key):
            def func():
                bg = QColor(obj.getColor())
                color = QColorDialog.getColor(bg)
                if not QColor.isValid(color):
                    return
                obj.setColor(color.name())
                self.setSetting('Graph/'+key,color.name())
            return func

        def hotfix(key):
            def func(value):
                self.setSetting('Graph/'+key,value)
            return func

        items = [
            ["TitleText",QLineEdit(),'Title Text','Electrical Chemistry Datas'],
            ["TitleSize",SpinBox(suffix='pt',lower=1),"Title Size",12],
            ["TitleColor",ColorBar(),"Title Color",'#000000'],
            ["BottumText",QLineEdit(),"Bottum Text",'Capacity (mAh)'],
            ["BottumSize",SpinBox(suffix='pt',lower=1),"Bottum Size",8],
            ["BottumColor",ColorBar(),"Bottum Color",'#000000'],
            ["GridX",SwitchButton(),"GridX",1],
            ["GridY",SwitchButton(),"GridY",1],
            ["GridAlpha",SpinBox(upper=1,step=0.05,dec=2),"Grid Alpha",0.25],
            ["BackgroundColor",ColorBar('#ffffff'),"Background Color",'#ffffff'],
            ["AxisWidth",SpinBox(lower=0.1,step=0.1,dec=1),"Axis Width",1.5],
            ["AxisColor",ColorBar(),"Axis Color",'#000000'],
        ]

        for i in range(len(items)):
            (k,v,label,default) = tuple(items[i])
            layout.addWidget(QLabel(self.translate(label)),i,0,1,1)
            layout.addWidget(v,i,1,1,1)

            if isinstance(default,int):
                v.setValue(int(self.defaultSetting('Graph/'+k,default)))
                v.valueChanged.connect(hotfix(k))
            elif isinstance(default,float):
                v.setValue(float(self.defaultSetting('Graph/'+k,default)))
                v.valueChanged.connect(hotfix(k))
            elif default[0] == '#':
                v.setPalette(QPalette(QColor(self.defaultSetting('Graph/'+k,default))))
                v.doubleClicked.connect(changeColor(v,k))
            else:
                v.setText(self.defaultSetting('Graph/'+k,default))
                v.textChanged.connect(hotfix(k))

        applyBtn = QPushButton(self.translate('Apply'))
        layout.addWidget(applyBtn,12,0,1,4)
        applyBtn.clicked.connect(self.setGraphViewStyle)
        self.stack3.setLayout(layout)

    def tab4UI(self):
        #表单布局
        layout = QFormLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        #绑定事件
        def hotfix(key):
            def func(value):
                self.setSetting('Core/'+key,value)
                self.initCoreFunction()
            return func

        cb = QComboBox()
        cb.addItems(['Manhattan','Euclidean','Minkowski','Cosine'])
        layout.addRow(QLabel(self.translate("Fitting Algorithm")),cb)
        cb.setCurrentText(self.defaultSetting('Core/Fitting',"Manhattan"))
        cb.currentTextChanged.connect(hotfix("Fitting"))
        #创建组件
        items = [
            ["AutoSelect",SwitchButton(),'Auto Select',1],
            ["AutoGuess",SwitchButton(),'Auto Guess',0],
            ["AutoScale",SwitchButton(),'Auto Scale',0],
            ["AutoCalParam",SwitchButton(),'Auto Calculate Parameters',0],
            ["UseMaxCapacity",SwitchButton(),'Generation in Capacity Range',0],
            ["OperationRecord",SwitchButton(),'Operation Record',0],
            ["DecimalsX",SpinBox(lower=1,upper=15),'X Axis Data Decimals',6],
            ["DecimalsY",SpinBox(lower=1,upper=15),'Y Axis Data Decimals',12],
            ["MaxCapacity",SpinBox(suffix='mAh',lower=0,upper=1E7,dec=2),'Maximum Capacity',0.00],
            ["MaxPoints",SpinBox(upper=1E6,step=100),'Generation Points Count',500],

            #["SuffixCut",QLineEdit(),'Cut Subfix','_C'],
            #["SuffixDiff",QLineEdit(),'Diff Suffix','_D'],
            #["SuffixSmooth",QLineEdit(),'Smooth Suffix','_M'],
            #["SuffixInvert",QLineEdit(),'Invert Suffix','_I'],
            #["SuffixSkip",QLineEdit(),'Skip Suffix','_S'],
            ["SuffixScale1",QLineEdit(),'dVdQ Scale Suffix','_F'],
            ["SuffixScale2",QLineEdit(),'VQ Scale Suffix','_N'],
            ["SuffixGen",QLineEdit(),'Gen Suffix','_G'],
        ]

        #创建UI
        for item in items:
            (k,v,label,default) = tuple(item)
            layout.addRow(QLabel(self.translate(label)),v)
            if isinstance(default,int):
                v.setValue(int(self.defaultSetting('Core/'+k,default)))
                v.valueChanged.connect(hotfix(k))
            elif isinstance(default,float):
                v.setValue(float(self.defaultSetting('Core/'+k,default)))
                v.valueChanged.connect(hotfix(k))
            else:
                v.setText(self.defaultSetting('Core/'+k,default))
                v.textChanged.connect(hotfix(k))
        self.stack4.setLayout(layout)

    def tab5UI(self):
        #表单布局
        layout = QFormLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        #创建组件
        AlertBeforeDelete = SwitchButton()
        OpenMultiFiles = SwitchButton()
        SelectRegion = SwitchButton()
        #
        tempbox = QHBoxLayout()
        TempDirectory = QLineEdit()
        selectBtn = QPushButton(self.translate('Browse'))
        selectBtn.setFixedWidth(50)
        tempbox.addWidget(TempDirectory)
        tempbox.addWidget(selectBtn)
        def selectLocation():
            filepath = QFileDialog.getExistingDirectory(None,self.translate('Select Cache Directory'), os.getcwd())
            if not filepath:
                return
            TempDirectory.setText(filepath)

        selectBtn.clicked.connect(selectLocation)

        def updateRegionSelector(value):
            self.setSetting('UI/SelectRegion',value)
            if self.parent:
                self.parent.updateRegionSelector()

        #创建UI
        layout.addRow(QLabel(self.translate('Alert Before Delete')),AlertBeforeDelete)
        layout.addRow(QLabel(self.translate('Enable Open MultiDatas')),OpenMultiFiles)
        layout.addRow(QLabel(self.translate('Select Region')),SelectRegion)
        layout.addRow(QLabel(self.translate('Cache Directory')),tempbox)
        
        self.stack5.setLayout(layout)
        #初始化
        AlertBeforeDelete.setValue(int(self.defaultSetting('UI/AlertBeforeDelete',0)))
        OpenMultiFiles.setValue(int(self.defaultSetting('UI/OpenMultiFiles',0)))
        SelectRegion.setValue(int(self.defaultSetting('UI/SelectRegion',0)))
        TempDirectory.setText(self.defaultSetting('UI/TempDirectory',''))
        #绑定事件
        def hotfix(key):
            def func(value):
                self.setSetting('UI/'+key,value)
            return func

        AlertBeforeDelete.valueChanged.connect(hotfix('AlertBeforeDelete'))
        OpenMultiFiles.valueChanged.connect(hotfix('OpenMultiFiles'))
        SelectRegion.valueChanged.connect(updateRegionSelector)
        TempDirectory.textChanged.connect(hotfix('TempDirectory'))

    def display(self,index):
        self.stack.setCurrentIndex(index)

    def closeEvent(self, QCloseEvent):
        if self.parent:
            self.parent.setEnabled(True)
        QCloseEvent.accept()

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

    def drawCurves(self):
        if self.parent:
            self.parent.drawCurves()

    def setGraphViewStyle(self):
        if self.parent:
            self.parent.setGraphViewStyle()
    
    def initCoreFunction(self):
        if self.parent:
            self.parent.initCoreFunction()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     demo = Preference()
#     demo.show()
#     sys.exit(app.exec_())
