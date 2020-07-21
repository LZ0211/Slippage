import os,sys,re
from json import load
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QBrush, QColor, QCursor, QPalette, QPainter, QFont, QPen
from PyQt5.QtCore import Qt, Signal, QRect
from PyQt5.QtWidgets import QWidget, QFileDialog, QListWidget, QListWidgetItem, QApplication, QStackedWidget, QRadioButton, QAbstractItemView, QHBoxLayout, QFormLayout, QGridLayout, QLineEdit, QCheckBox, QLabel,QComboBox,QDesktopWidget, QPushButton, QSpinBox, QColorDialog, QMenu, QAction, QTextEdit, QDoubleSpinBox, QSlider

class ColorLabel(QLabel):
    clicked = Signal()
    doubleClicked = Signal()
    def __int__(self):
        super().__init__()

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

class Preference(QWidget):
    def __init__(self,parent=None):
        super(Preference, self).__init__()
        self.langText = {}
        self.parent = parent
        self.setupUI()
        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        posX = (screen.width() - size.width()) / 2
        posY = (screen.height() - size.height()) / 2
        if self.parent:
            geometry = self.parent.geometry()
            posX = self.parent.pos().x() + (geometry.width() - size.width())/2
            posY = self.parent.pos().y() + (geometry.height() - size.height())/2
        self.move(posX,posY)

    def setupUI(self):
        self.setGeometry(500, 400, 10, 10)
        self.setFixedSize(500, 400)
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

        defaultExtension=extensions()
        defaultDataStructure=structures()
        posDataStructure=structures()
        negDataStructure=structures()
        fullDataStructure=structures()

        layout.addRow(QLabel(self.translate('Default File Extension')),defaultExtension)
        layout.addRow(QLabel(self.translate('Default Data Structure')),defaultDataStructure)
        layout.addRow(QLabel(self.translate('Positive Data Structure')),posDataStructure)
        layout.addRow(QLabel(self.translate('Negative Data Structure')),negDataStructure)
        layout.addRow(QLabel(self.translate('Full Cell Data Structure')),fullDataStructure)

        self.stack1.setLayout(layout)

        def hotfix(key):
            def func(value):
                self.setSetting('FileStructure/'+key,value)
            return func

        defaultExtension.setCurrentText(self.defaultSetting('FileStructure/defaultExtension','Text File (*.txt)'))
        defaultExtension.currentTextChanged.connect(hotfix('defaultExtension'))

        defaultDataStructure.setCurrentText(self.defaultSetting('FileStructure/dataStructure','Voltage:Capacity'))
        defaultDataStructure.currentTextChanged.connect(hotfix('dataStructure'))

        posDataStructure.setCurrentText(self.defaultSetting('FileStructure/posDataStructure','Voltage:Capacity'))
        posDataStructure.currentTextChanged.connect(hotfix('posDataStructure'))

        negDataStructure.setCurrentText(self.defaultSetting('FileStructure/negDataStructure','Voltage:Capacity'))
        negDataStructure.currentTextChanged.connect(hotfix('negDataStructure'))

        fullDataStructure.setCurrentText(self.defaultSetting('FileStructure/fullDataStructure','Voltage:Capacity'))
        fullDataStructure.currentTextChanged.connect(hotfix('fullDataStructure'))

    def tab2UI(self):
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        radio_line = QRadioButton('line')
        radio_scatter = QRadioButton('scatter')
        layout.addWidget(QLabel(self.translate('Curve Type')),0,0,1,1)
        layout.addWidget(radio_line,0,1,1,1)
        layout.addWidget(radio_scatter,0,2,1,1)

        lineWidth = QSpinBox(self)
        lineWidth.setMinimum(1)
        layout.addWidget(QLabel(self.translate('Curve Width')),1,0,1,1)
        layout.addWidget(lineWidth,1,1,1,1)

        symbolSize = QSpinBox(self)
        symbolSize.setMinimum(1)
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

        titleText = QLineEdit()
        layout.addWidget(QLabel(self.translate('Title Text')),0,0,1,1)
        layout.addWidget(titleText,0,1,1,3)

        TitleSize = QSpinBox()
        TitleSize.setSuffix('pt')
        TitleSize.setMinimum(1)
        TitleSize.setFixedWidth(80)
        layout.addWidget(QLabel(self.translate('Title Size')),1,0,1,1)
        layout.addWidget(TitleSize,1,1,1,1)

        TitleColor = ColorLabel()
        TitleColor.setAutoFillBackground(True)
        TitleColor.setPalette(QPalette(Qt.black))
        TitleColor.setFixedSize(80,20)
        layout.addWidget(QLabel(self.translate('Title Color')),2,0,1,1)
        layout.addWidget(TitleColor,2,1,1,1)

        BottumText = QLineEdit()
        layout.addWidget(QLabel(self.translate('Bottum Text')),3,0,1,1)
        layout.addWidget(BottumText,3,1,1,3)

        BottumSize = QSpinBox()
        BottumSize.setSuffix('pt')
        BottumSize.setMinimum(1)
        BottumSize.setFixedWidth(80)
        layout.addWidget(QLabel(self.translate('Bottum Size')),4,0,1,1)
        layout.addWidget(BottumSize,4,1,1,1)

        BottumColor = ColorLabel()
        BottumColor.setAutoFillBackground(True)
        BottumColor.setPalette(QPalette(Qt.black))
        BottumColor.setFixedSize(80,20)
        layout.addWidget(QLabel(self.translate('Bottum Color')),5,0,1,1)
        layout.addWidget(BottumColor,5,1,1,1)

        GridX = QDoubleSpinBox()
        GridX.setMinimum(0.1)
        GridX.setSingleStep(0.1)
        GridX.setFixedWidth(80)
        layout.addWidget(QLabel(self.translate('GridX Width')),6,0,1,1)
        layout.addWidget(GridX,6,1,1,1)

        GridY = QDoubleSpinBox()
        GridY.setMinimum(0.1)
        GridY.setSingleStep(0.1)
        GridY.setFixedWidth(80)
        layout.addWidget(QLabel(self.translate('GridY Width')),7,0,1,1)
        layout.addWidget(GridY,7,1,1,1)

        GridAlpha = QDoubleSpinBox()
        GridAlpha.setMaximum(1)
        GridAlpha.setMinimum(0)
        GridAlpha.setSingleStep(0.05)
        GridAlpha.setFixedWidth(80)
        layout.addWidget(QLabel(self.translate('Grid Alpha')),8,0,1,1)
        layout.addWidget(GridAlpha,8,1,1,1)

        bgColor = ColorLabel()
        bgColor.setAutoFillBackground(True)
        bgColor.setPalette(QPalette(Qt.white))
        bgColor.setFixedSize(80,20)
        layout.addWidget(QLabel(self.translate('Background Color')),9,0,1,1)
        layout.addWidget(bgColor,9,1,1,1)

        AxisWidth = QDoubleSpinBox()
        AxisWidth.setMinimum(0.1)
        AxisWidth.setSingleStep(0.1)
        AxisWidth.setFixedWidth(80)
        layout.addWidget(QLabel(self.translate('Axis Width')),10,0,1,1)
        layout.addWidget(AxisWidth,10,1,1,1)

        AxisColor = ColorLabel()
        AxisColor.setAutoFillBackground(True)
        AxisColor.setPalette(QPalette(Qt.white))
        AxisColor.setFixedSize(80,20)
        layout.addWidget(QLabel(self.translate('Axis Color')),11,0,1,1)
        layout.addWidget(AxisColor,11,1,1,1)      

        applyBtn = QPushButton(self.translate('Apply'))
        layout.addWidget(applyBtn,12,0,1,4)

        def changeColor(obj,key):
            bg = QColor(self.defaultSetting(key,'#000000'))
            color = QColorDialog.getColor(bg)
            if not QColor.isValid(color):
                return
            obj.setPalette(QPalette(color))
            self.setSetting('Graph/'+key,color.name())

        def hotfix(key):
            def func(value):
                self.setSetting('Graph/'+key,value)
            return func

        titleText.setText(self.defaultSetting('Graph/TitleText','Electrical Chemistry Datas'))
        TitleSize.setValue(int(self.defaultSetting('Graph/TitleSize',12)))
        TitleColor.setPalette(QPalette(QColor(self.defaultSetting('Graph/TitleColor','#000000'))))
        BottumText.setText(self.defaultSetting('Graph/BottumText','Capacity (mAh)'))
        BottumSize.setValue(int(self.defaultSetting('Graph/BottumSize',8)))
        BottumColor.setPalette(QPalette(QColor(self.defaultSetting('Graph/BottumColor','#000000'))))
        GridX.setValue(float(self.defaultSetting('Graph/GridX',1)))
        GridY.setValue(float(self.defaultSetting('Graph/GridY',1)))
        GridAlpha.setValue(float(self.defaultSetting('Graph/GridAlpha',0.25)))
        bgColor.setPalette(QPalette(QColor(self.defaultSetting('Graph/BackgroundColor','#ffffff'))))
        AxisWidth.setValue(float(self.defaultSetting('Graph/AxisWidth',1.5)))
        AxisColor.setPalette(QPalette(QColor(self.defaultSetting('Graph/AxisColor','#000000'))))

        titleText.textChanged.connect(hotfix('TitleText'))
        TitleSize.valueChanged.connect(hotfix('TitleSize'))
        TitleColor.doubleClicked.connect(lambda:changeColor(TitleColor,'TitleColor'))
        BottumText.textChanged.connect(hotfix('BottumText'))
        BottumSize.valueChanged.connect(hotfix('BottumSize'))
        BottumColor.doubleClicked.connect(lambda:changeColor(BottumColor,'BottumColor'))
        GridX.valueChanged.connect(hotfix('GridX'))
        GridY.valueChanged.connect(hotfix('GridY'))
        GridAlpha.valueChanged.connect(hotfix('GridAlpha'))
        bgColor.doubleClicked.connect(lambda:changeColor(bgColor,'BackgroundColor'))
        AxisWidth.valueChanged.connect(hotfix('AxisWidth'))
        AxisColor.doubleClicked.connect(lambda:changeColor(AxisColor,'AxisColor'))

        applyBtn.clicked.connect(self.setGraphViewStyle)

        self.stack3.setLayout(layout)

    def tab4UI(self):
        #表单布局
        layout = QFormLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        #创建组件
        AutoGuess = SwitchButton()
        AutoScale = SwitchButton()
        AutoCalParam = SwitchButton()
        MaxCapacity = QDoubleSpinBox()
        MaxCapacity.setSuffix('mAh')
        MaxCapacity.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        MaxCapacity.setMaximum(1E7)
        SuffixCut = QLineEdit()
        SuffixDiff = QLineEdit()
        SuffixSmooth = QLineEdit()
        SuffixInvert = QLineEdit()
        SuffixSkip = QLineEdit()
        SuffixScale1 = QLineEdit()
        SuffixScale2 = QLineEdit()
        SuffixGen = QLineEdit()
        #创建UI
        layout.addRow(QLabel(self.translate('Auto Guess')),AutoGuess)
        layout.addRow(QLabel(self.translate('Auto Scale')),AutoScale)
        layout.addRow(QLabel(self.translate('Auto Calculate Parameters')),AutoCalParam)
        layout.addRow(QLabel(self.translate('Maximum Capacity')),MaxCapacity)
        layout.addRow(QLabel(self.translate('Cut Subfix')),SuffixCut)
        layout.addRow(QLabel(self.translate('Diff Suffix')),SuffixDiff)
        layout.addRow(QLabel(self.translate('Smooth Suffix')),SuffixSmooth)
        layout.addRow(QLabel(self.translate('Invert Suffix')),SuffixInvert)
        layout.addRow(QLabel(self.translate('Skip Suffix')),SuffixSkip)
        layout.addRow(QLabel(self.translate('dVdQ Scale Suffix')),SuffixScale1)
        layout.addRow(QLabel(self.translate('VQ Scale Suffix')),SuffixScale2)
        layout.addRow(QLabel(self.translate('Gen Suffix')),SuffixGen)
        self.stack4.setLayout(layout)
        #初始化
        AutoScale.setValue(int(self.defaultSetting('Core/AutoScale',0)))
        AutoCalParam.setValue(int(self.defaultSetting('Core/AutoCalParam',0)))
        MaxCapacity.setValue(float(self.defaultSetting('Core/MaxCapacity',0)))
        SuffixCut.setText(self.defaultSetting('Core/SuffixCut','_C'))
        SuffixDiff.setText(self.defaultSetting('Core/SuffixDiff','_D'))
        SuffixSmooth.setText(self.defaultSetting('Core/SuffixSmooth','_M'))
        SuffixInvert.setText(self.defaultSetting('Core/SuffixInvert','_I'))
        SuffixSkip.setText(self.defaultSetting('Core/SuffixSkip','_S'))
        SuffixScale1.setText(self.defaultSetting('Core/SuffixScale1','_F'))
        SuffixScale2.setText(self.defaultSetting('Core/SuffixScale2','_N'))
        SuffixGen.setText(self.defaultSetting('Core/SuffixGen','_G'))
        #绑定事件
        def hotfix(key):
            def func(value):
                self.setSetting('Core/'+key,value)
                self.initCoreFunction()
            return func

        def lockMaxCapacity(*argv):
            if AutoCalParam.value == 0:
                MaxCapacity.setDisabled(True)
            else:
                MaxCapacity.setEnabled(True)

        AutoGuess.valueChanged.connect(hotfix('AutoGuess'))
        AutoScale.valueChanged.connect(hotfix('AutoScale'))
        AutoCalParam.valueChanged.connect(hotfix('AutoCalParam'))
        AutoCalParam.valueChanged.connect(lockMaxCapacity)
        MaxCapacity.valueChanged.connect(hotfix('MaxCapacity'))
        SuffixCut.textChanged.connect(hotfix('SuffixCut'))
        SuffixDiff.textChanged.connect(hotfix('SuffixDiff'))
        SuffixSmooth.textChanged.connect(hotfix('SuffixSmooth'))
        SuffixInvert.textChanged.connect(hotfix('SuffixInvert'))
        SuffixSkip.textChanged.connect(hotfix('SuffixSkip'))
        SuffixScale1.textChanged.connect(hotfix('SuffixScale1'))
        SuffixScale2.textChanged.connect(hotfix('SuffixScale2'))
        SuffixGen.textChanged.connect(hotfix('SuffixGen'))

    def tab5UI(self):
        #表单布局
        layout = QFormLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        #创建组件
        AlertBeforeDelete = SwitchButton()
        OpenMultiFiles = SwitchButton()
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

        #创建UI
        layout.addRow(QLabel(self.translate('Alert Before Delete')),AlertBeforeDelete)
        layout.addRow(QLabel(self.translate('Enable Open MultiDatas')),OpenMultiFiles)
        layout.addRow(QLabel(self.translate('Cache Directory')),tempbox)
        self.stack5.setLayout(layout)
        #初始化
        AlertBeforeDelete.setValue(int(self.defaultSetting('UI/AlertBeforeDelete',0)))
        OpenMultiFiles.setValue(int(self.defaultSetting('UI/OpenMultiFiles',0)))
        TempDirectory.setText(self.defaultSetting('UI/TempDirectory',''))
        #绑定事件
        def hotfix(key):
            def func(value):
                self.setSetting('UI/'+key,value)
            return func

        AlertBeforeDelete.valueChanged.connect(hotfix('AlertBeforeDelete'))
        OpenMultiFiles.valueChanged.connect(hotfix('OpenMultiFiles'))
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Preference()
    demo.show()
    sys.exit(app.exec_())
