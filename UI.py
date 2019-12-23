# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(822, 578)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resource/curve.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.Process_Box = QtWidgets.QGroupBox(self.centralwidget)
        self.Process_Box.setMinimumSize(QtCore.QSize(280, 515))
        self.Process_Box.setFlat(True)
        self.Data_List = QtWidgets.QComboBox(self.Process_Box)
        self.Data_List.setGeometry(QtCore.QRect(80, 10, 199, 22))
        self.Data_List.setEditable(False)
        self.label = QtWidgets.QLabel(self.Process_Box)
        self.label.setGeometry(QtCore.QRect(10, 13, 54, 16))
        self.Methods_List = QtWidgets.QComboBox(self.Process_Box)
        self.Methods_List.setGeometry(QtCore.QRect(110, 130, 161, 22))
        self.label_2 = QtWidgets.QLabel(self.Process_Box)
        self.label_2.setGeometry(QtCore.QRect(10, 133, 91, 16))
        self.label_3 = QtWidgets.QLabel(self.Process_Box)
        self.label_3.setGeometry(QtCore.QRect(10, 43, 80, 16))
        self.Skip_List = QtWidgets.QSpinBox(self.Process_Box)
        self.Skip_List.setGeometry(QtCore.QRect(110, 40, 91, 22))
        self.Skip_List.setMinimum(1)
        self.Skip_Button = QtWidgets.QPushButton(self.Process_Box)
        self.Skip_Button.setGeometry(QtCore.QRect(220, 40, 60, 23))
        self.label_4 = QtWidgets.QLabel(self.Process_Box)
        self.label_4.setGeometry(QtCore.QRect(10, 73, 80, 16))
        self.Diff_List = QtWidgets.QSpinBox(self.Process_Box)
        self.Diff_List.setGeometry(QtCore.QRect(110, 70, 91, 22))
        self.Diff_List.setMinimum(1)
        self.Diff_Button = QtWidgets.QPushButton(self.Process_Box)
        self.Diff_Button.setGeometry(QtCore.QRect(220, 70, 60, 23))
        self.Param_Name = QtWidgets.QLabel(self.Process_Box)
        self.Param_Name.setGeometry(QtCore.QRect(11, 163, 101, 16))
        self.Smooth_Param = QtWidgets.QDoubleSpinBox(self.Process_Box)
        self.Smooth_Param.setGeometry(QtCore.QRect(130, 160, 81, 22))
        self.Smooth_Param.setDecimals(6)
        self.Smooth_Param.setSingleStep(0.01)
        self.Smooth_Param.setProperty("value", 0.0)
        self.Smooth_Button = QtWidgets.QPushButton(self.Process_Box)
        self.Smooth_Button.setGeometry(QtCore.QRect(220, 160, 60, 23))
        self.line_2 = QtWidgets.QFrame(self.Process_Box)
        self.line_2.setGeometry(QtCore.QRect(0, 190, 281, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Param_Name_2 = QtWidgets.QLabel(self.Process_Box)
        self.Param_Name_2.setGeometry(QtCore.QRect(10, 210, 61, 16))
        self.VQ_Radio = QtWidgets.QRadioButton(self.Process_Box)
        self.VQ_Radio.setGeometry(QtCore.QRect(90, 210, 61, 16))
        self.VQ_Radio.setChecked(True)
        self.VQ_Radio.setAutoExclusive(True)
        self.dVdQ_Radio = QtWidgets.QRadioButton(self.Process_Box)
        self.dVdQ_Radio.setGeometry(QtCore.QRect(180, 210, 61, 16))
        self.Pos_List = QtWidgets.QComboBox(self.Process_Box)
        self.Pos_List.setGeometry(QtCore.QRect(70, 237, 201, 22))
        self.Neg_List = QtWidgets.QComboBox(self.Process_Box)
        self.Neg_List.setGeometry(QtCore.QRect(70, 267, 201, 22))
        self.Full_List = QtWidgets.QComboBox(self.Process_Box)
        self.Full_List.setGeometry(QtCore.QRect(70, 300, 201, 22))
        self.Param_Name_5 = QtWidgets.QLabel(self.Process_Box)
        self.Param_Name_5.setGeometry(QtCore.QRect(10, 240, 51, 16))
        self.Param_Name_6 = QtWidgets.QLabel(self.Process_Box)
        self.Param_Name_6.setGeometry(QtCore.QRect(10, 270, 61, 16))
        self.Param_Name_7 = QtWidgets.QLabel(self.Process_Box)
        self.Param_Name_7.setGeometry(QtCore.QRect(10, 300, 51, 16))
        self.Positive_Box = QtWidgets.QGroupBox(self.Process_Box)
        self.Positive_Box.setGeometry(QtCore.QRect(5, 330, 271, 72))
        self.Pos_Scale_Slider = QtWidgets.QSlider(self.Positive_Box)
        self.Pos_Scale_Slider.setGeometry(QtCore.QRect(45, 18, 111, 20))
        self.Pos_Scale_Slider.setMaximum(4)
        self.Pos_Scale_Slider.setPageStep(1)
        self.Pos_Scale_Slider.setProperty("value", 2)
        self.Pos_Scale_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Param_Name_3 = QtWidgets.QLabel(self.Positive_Box)
        self.Param_Name_3.setGeometry(QtCore.QRect(8, 18, 41, 16))
        self.Param_Name_4 = QtWidgets.QLabel(self.Positive_Box)
        self.Param_Name_4.setGeometry(QtCore.QRect(8, 45, 51, 16))
        self.Pos_Shift_Slider = QtWidgets.QSlider(self.Positive_Box)
        self.Pos_Shift_Slider.setGeometry(QtCore.QRect(45, 45, 111, 20))
        self.Pos_Shift_Slider.setMaximum(4)
        self.Pos_Shift_Slider.setPageStep(1)
        self.Pos_Shift_Slider.setProperty("value", 2)
        self.Pos_Shift_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Pos_Scale_SpinBox = QtWidgets.QDoubleSpinBox(self.Positive_Box)
        self.Pos_Scale_SpinBox.setGeometry(QtCore.QRect(170, 15, 61, 22))
        self.Pos_Scale_SpinBox.setDecimals(4)
        self.Pos_Scale_SpinBox.setSingleStep(1.0)
        self.Pos_Scale_SpinBox.setProperty("value", 1.0)
        self.Pos_Shift_SpinBox = QtWidgets.QDoubleSpinBox(self.Positive_Box)
        self.Pos_Shift_SpinBox.setGeometry(QtCore.QRect(170, 43, 61, 22))
        self.Pos_Shift_SpinBox.setWrapping(False)
        self.Pos_Shift_SpinBox.setDecimals(4)
        self.Pos_Scale_checkBox = QtWidgets.QCheckBox(self.Positive_Box)
        self.Pos_Scale_checkBox.setGeometry(QtCore.QRect(240, 16, 22, 22))
        self.Pos_Scale_checkBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Pos_Scale_checkBox.setText("")
        self.Pos_Shift_checkBox = QtWidgets.QCheckBox(self.Positive_Box)
        self.Pos_Shift_checkBox.setGeometry(QtCore.QRect(240, 43, 22, 22))
        self.Pos_Shift_checkBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Pos_Shift_checkBox.setText("")
        self.Negative_Box = QtWidgets.QGroupBox(self.Process_Box)
        self.Negative_Box.setGeometry(QtCore.QRect(5, 406, 271, 72))
        self.Neg_Scale_Slider = QtWidgets.QSlider(self.Negative_Box)
        self.Neg_Scale_Slider.setGeometry(QtCore.QRect(45, 18, 111, 20))
        self.Neg_Scale_Slider.setMaximum(4)
        self.Neg_Scale_Slider.setPageStep(1)
        self.Neg_Scale_Slider.setProperty("value", 2)
        self.Neg_Scale_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Param_Name_8 = QtWidgets.QLabel(self.Negative_Box)
        self.Param_Name_8.setGeometry(QtCore.QRect(8, 18, 41, 16))
        self.Param_Name_9 = QtWidgets.QLabel(self.Negative_Box)
        self.Param_Name_9.setGeometry(QtCore.QRect(8, 45, 51, 16))
        self.Neg_Shift_Slider = QtWidgets.QSlider(self.Negative_Box)
        self.Neg_Shift_Slider.setGeometry(QtCore.QRect(45, 45, 111, 20))
        self.Neg_Shift_Slider.setMaximum(4)
        self.Neg_Shift_Slider.setPageStep(1)
        self.Neg_Shift_Slider.setProperty("value", 2)
        self.Neg_Shift_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Neg_Scale_SpinBox = QtWidgets.QDoubleSpinBox(self.Negative_Box)
        self.Neg_Scale_SpinBox.setGeometry(QtCore.QRect(170, 15, 61, 22))
        self.Neg_Scale_SpinBox.setDecimals(4)
        self.Neg_Scale_SpinBox.setProperty("value", 1.0)
        self.Neg_Shift_SpinBox = QtWidgets.QDoubleSpinBox(self.Negative_Box)
        self.Neg_Shift_SpinBox.setGeometry(QtCore.QRect(170, 43, 61, 22))
        self.Neg_Shift_SpinBox.setDecimals(4)
        self.Neg_Scale_checkBox = QtWidgets.QCheckBox(self.Negative_Box)
        self.Neg_Scale_checkBox.setGeometry(QtCore.QRect(240, 16, 22, 22))
        self.Neg_Scale_checkBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Neg_Scale_checkBox.setText("")
        self.Neg_Shift_checkBox = QtWidgets.QCheckBox(self.Negative_Box)
        self.Neg_Shift_checkBox.setGeometry(QtCore.QRect(240, 43, 22, 22))
        self.Neg_Shift_checkBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Neg_Shift_checkBox.setText("")
        self.Fitting_Button = QtWidgets.QPushButton(self.Process_Box)
        self.Fitting_Button.setGeometry(QtCore.QRect(130, 487, 75, 23))
        self.label_6 = QtWidgets.QLabel(self.Process_Box)
        self.label_6.setGeometry(QtCore.QRect(10, 103, 51, 16))
        self.Cut_From = QtWidgets.QDoubleSpinBox(self.Process_Box)
        self.Cut_From.setGeometry(QtCore.QRect(80, 100, 41, 22))
        self.Cut_From.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Cut_From.setDecimals(2)
        self.Cut_From.setSingleStep(0.01)
        self.Cut_From.setProperty("value", 0.0)
        self.Cut_To = QtWidgets.QDoubleSpinBox(self.Process_Box)
        self.Cut_To.setGeometry(QtCore.QRect(160, 100, 41, 22))
        self.Cut_To.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Cut_To.setDecimals(2)
        self.Cut_To.setSingleStep(0.01)
        self.Cut_To.setProperty("value", 0.0)
        self.label_7 = QtWidgets.QLabel(self.Process_Box)
        self.label_7.setGeometry(QtCore.QRect(130, 103, 21, 16))
        self.Cut_Button = QtWidgets.QPushButton(self.Process_Box)
        self.Cut_Button.setGeometry(QtCore.QRect(220, 100, 60, 23))
        self.label_26 = QtWidgets.QLabel(self.Process_Box)
        self.label_26.setGeometry(QtCore.QRect(10, 490, 41, 16))
        self.RMSD = QtWidgets.QDoubleSpinBox(self.Process_Box)
        self.RMSD.setGeometry(QtCore.QRect(60, 487, 60, 22))
        self.RMSD.setReadOnly(True)
        self.RMSD.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.RMSD.setDecimals(5)
        self.Scale_Button = QtWidgets.QPushButton(self.Process_Box)
        self.Scale_Button.setGeometry(QtCore.QRect(215, 487, 60, 23))
        self.gridLayout.addWidget(self.Process_Box, 0, 1, 2, 1)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setMinimumSize(QtCore.QSize(0, 50))
        self.listWidget.setMaximumSize(QtCore.QSize(16777215, 120))
        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 1)
        self.graphicsView = QtWidgets.QGridLayout()
        self.gridLayout.addLayout(self.graphicsView, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 822, 23))
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menu_Open = QtWidgets.QMenu(self.menuFile)
        self.menu_Recent_Files = QtWidgets.QMenu(self.menuFile)
        self.menu_Edit = QtWidgets.QMenu(self.menubar)
        self.menu_Tool = QtWidgets.QMenu(self.menubar)
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Language = QtWidgets.QMenu(self.menubar)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.action_Save = QtWidgets.QAction(MainWindow)
        self.action_Preferences = QtWidgets.QAction(MainWindow)
        self.action_Exit = QtWidgets.QAction(MainWindow)
        self.action_Positive_Reference = QtWidgets.QAction(MainWindow)
        self.action_Negative_Reference = QtWidgets.QAction(MainWindow)
        self.action_Measured_Data = QtWidgets.QAction(MainWindow)
        self.action_Excel2TXT = QtWidgets.QAction(MainWindow)
        self.action_Excel2CSV = QtWidgets.QAction(MainWindow)
        self.action_CSV2TXT = QtWidgets.QAction(MainWindow)
        self.action_CSV2Excel = QtWidgets.QAction(MainWindow)
        self.action_TXT2CSV = QtWidgets.QAction(MainWindow)
        self.action_TXT2Excel = QtWidgets.QAction(MainWindow)
        self.action_Delete = QtWidgets.QAction(MainWindow)
        self.action_Delete_All = QtWidgets.QAction(MainWindow)
        self.action_View = QtWidgets.QAction(MainWindow)
        self.action_Rename = QtWidgets.QAction(MainWindow)
        self.action_Export = QtWidgets.QAction(MainWindow)
        self.action_English = QtWidgets.QAction(MainWindow)
        self.action_Chinese_Simplified = QtWidgets.QAction(MainWindow)
        self.action_Chinese_Traditional = QtWidgets.QAction(MainWindow)
        self.action_Author_Email = QtWidgets.QAction(MainWindow)
        self.menu_Open.addAction(self.action_Positive_Reference)
        self.menu_Open.addAction(self.action_Negative_Reference)
        self.menu_Open.addAction(self.action_Measured_Data)
        self.menuFile.addAction(self.menu_Open.menuAction())
        self.menuFile.addAction(self.action_Save)
        self.menuFile.addAction(self.action_Exit)
        self.menuFile.addAction(self.action_Preferences)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menu_Recent_Files.menuAction())
        self.menu_Edit.addAction(self.action_View)
        self.menu_Edit.addAction(self.action_Rename)
        self.menu_Edit.addAction(self.action_Delete)
        self.menu_Edit.addAction(self.action_Export)
        self.menu_Edit.addAction(self.action_Delete_All)
        self.menu_Tool.addAction(self.action_Excel2TXT)
        self.menu_Tool.addAction(self.action_Excel2CSV)
        self.menu_Tool.addAction(self.action_CSV2TXT)
        self.menu_Tool.addAction(self.action_CSV2Excel)
        self.menu_Tool.addAction(self.action_TXT2CSV)
        self.menu_Tool.addAction(self.action_TXT2Excel)
        self.menu_Language.addAction(self.action_English)
        self.menu_Language.addAction(self.action_Chinese_Simplified)
        self.menu_Language.addAction(self.action_Chinese_Traditional)
        self.menu_Help.addAction(self.action_Author_Email)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_Tool.menuAction())
        self.menubar.addAction(self.menu_Language.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.langText = {}
        self._translate = lambda k,v:QtCore.QCoreApplication.translate(k,self.translateText(v))
        MainWindow.setWindowTitle(self._translate("MainWindow", "ATL-Electrical Chemistry Analysor"))
        self.retranslateUI()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUI(self):
        _translate = self._translate
        self.label.setText(_translate("MainWindow", "Data List"))
        self.label_2.setText(_translate("MainWindow", "Smooth Methods"))
        self.label_3.setText(_translate("MainWindow", "Skip Interval"))
        self.Skip_Button.setText(_translate("MainWindow", "Skip"))
        self.label_4.setText(_translate("MainWindow", "Diff Interval"))
        self.Diff_Button.setText(_translate("MainWindow", "Diff"))
        self.Param_Name.setText(_translate("MainWindow", "Smooth Parameter"))
        self.Smooth_Button.setText(_translate("MainWindow", "Smooth"))
        self.Param_Name_2.setText(_translate("MainWindow", "Date Type"))
        self.VQ_Radio.setText(_translate("MainWindow", "V-Q"))
        self.dVdQ_Radio.setText(_translate("MainWindow", "dVdQ-Q"))
        self.Param_Name_5.setText(_translate("MainWindow", "Positive"))
        self.Param_Name_6.setText(_translate("MainWindow", "Negative"))
        self.Param_Name_7.setText(_translate("MainWindow", "FullCell"))
        self.Positive_Box.setTitle(_translate("MainWindow", "Positive"))
        self.Param_Name_3.setText(_translate("MainWindow", "Scale"))
        self.Param_Name_4.setText(_translate("MainWindow", "Shift"))
        self.Negative_Box.setTitle(_translate("MainWindow", "Negative"))
        self.Param_Name_8.setText(_translate("MainWindow", "Scale"))
        self.Param_Name_9.setText(_translate("MainWindow", "Shift"))
        self.Fitting_Button.setText(_translate("MainWindow", "Fitting"))
        self.label_6.setText(_translate("MainWindow", "Cut From"))
        self.label_7.setText(_translate("MainWindow", "To"))
        self.Cut_Button.setText(_translate("MainWindow", "Cut"))
        self.label_26.setText(_translate("MainWindow", "RMSD"))
        self.Scale_Button.setText(_translate("MainWindow", "Scale"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menu_Open.setTitle(_translate("MainWindow", "&Open"))
        self.menu_Recent_Files.setTitle(_translate("MainWindow", "&Recent Files"))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit"))
        self.menu_Tool.setTitle(_translate("MainWindow", "&Tool"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menu_Language.setTitle(_translate("MainWindow", "&Language"))
        self.action_Save.setText(_translate("MainWindow", "&Save"))
        self.action_Save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action_Preferences.setText(_translate("MainWindow", "&Preferences"))
        self.action_Preferences.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.action_Exit.setText(_translate("MainWindow", "&Exit"))
        self.action_Exit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.action_Positive_Reference.setText(_translate("MainWindow", "Positive Reference"))
        self.action_Positive_Reference.setShortcut(_translate("MainWindow", "Alt+P"))
        self.action_Negative_Reference.setText(_translate("MainWindow", "Negative Reference"))
        self.action_Negative_Reference.setShortcut(_translate("MainWindow", "Alt+N"))
        self.action_Measured_Data.setText(_translate("MainWindow", "Measured Data"))
        self.action_Measured_Data.setShortcut(_translate("MainWindow", "Alt+M"))
        self.action_Excel2TXT.setText(_translate("MainWindow", "Excel2TXT"))
        self.action_Excel2CSV.setText(_translate("MainWindow", "Excel2CSV"))
        self.action_CSV2TXT.setText(_translate("MainWindow", "CSV2TXT"))
        self.action_CSV2Excel.setText(_translate("MainWindow", "CSV2Excel"))
        self.action_TXT2CSV.setText(_translate("MainWindow", "TXT2CSV"))
        self.action_TXT2Excel.setText(_translate("MainWindow", "TXT2Excel"))
        self.action_Delete.setText(_translate("MainWindow", "&Delete"))
        self.action_View.setText(_translate("MainWindow", "&View"))
        self.action_Rename.setText(_translate("MainWindow", "&Rename"))
        self.action_Export.setText(_translate("MainWindow", "&Export"))
        self.action_Delete_All.setText(_translate("MainWindow", "&Delete All"))
        self.action_English.setText(_translate("MainWindow", "&English"))
        self.action_Chinese_Simplified.setText(_translate("MainWindow", "&Chinese Simplified"))
        self.action_Chinese_Traditional.setText(_translate("MainWindow", "&Chinese Traditional"))
        self.action_Author_Email.setText(_translate("MainWindow", "&Email"))

    def translateText(self,text):
        if text in self.langText:
            return self.langText[text]
        return text

    def transEnglish(self):
        self.langText = {}
        self.retranslateUI()

    def transChineseSimplified(self):
        self.langText = {"Data List":"数据列表","Smooth Methods":"滤波方法","Skip Interval":"采点间隔","Skip":"采点","Diff Interval":"微分间隔","Diff":"微分","Smooth Parameter":"滤波参数","Smooth":"滤波","Date Type":"数据类型","Positive":"正极","Negative":"负极","FullCell":"全电池","Scale":"缩放","Shift":"平移","Fitting":"拟合","Cut From":"切割 从","To":"到","Cut":"切割","&File":"文件","&Open":"打开","&Recent Files":"最近打开","&Edit":"编辑","&Tool":"工具","&Help":"帮助","&Language":"语言","&Save":"保存","&Preferences":"首选项","&Exit":"退出","Positive Reference":"正极参考数据","Negative Reference":"负极参考数据","Measured Data":"测试数据","Excel2TXT":"Excel转TXT","Excel2CSV":"Excel转CSV","CSV2TXT":"CSV转TXT","CSV2Excel":"CSV转Excel","TXT2CSV":"TXT转CSV","TXT2Excel":"TXT转Excel","&Delete":"删除","&View":"查看","&Rename":"重命名","&Export":"导出","&Delete All":"删除全部","&English":"英语","&Chinese Simplified":"简体中文","&Chinese Traditional":"繁体中文","&Email":"电子邮箱"
        ,"Smooth Window":"滤波窗口","Noise Factor":"噪声因子","Sigma":"标准差","Data Rename":"数据重命名","Please input new data name:":"请输入新的数据名：","Information":"消息","Critical":"警告","No data selcted!":"没有选中的数据！","Save File":"保存文件","Please select a data file":"请选择一个数据文件","Invalid Data File!":"不是合法的数据文件！","A error occur, please contact author for help!":"未知错误，请联系作者！"}
        self.retranslateUI()

    def transChineseTraditional(self):
        self.langText = {"Data List":"數據列表","Smooth Methods":"濾波方法","Skip Interval":"采點間隔","Skip":"采點","Diff Interval":"微分間隔","Diff":"微分","Smooth Parameter":"濾波參數","Smooth":"濾波","Date Type":"數據類型","Positive":"正極","Negative":"負極","FullCell":"全電池","Scale":"縮放","Shift":"平移","Fitting":"擬合","Cut From":"切割 從","To":"到","Cut":"切割","&File":"文件","&Open":"打開","&Recent Files":"最近打開","&Edit":"編輯","&Tool":"工具","&Help":"幫助","&Language":"語言","&Save":"保存","&Preferences":"首選項","&Exit":"退出","Positive Reference":"正極參考數據","Negative Reference":"負極參考數據","Measured Data":"測試數據","Excel2TXT":"Excel轉TXT","Excel2CSV":"Excel轉CSV","CSV2TXT":"CSV轉TXT","CSV2Excel":"CSV轉Excel","TXT2CSV":"TXT轉CSV","TXT2Excel":"TXT轉Excel","&Delete":"刪除","&View":"查看","&Rename":"重命名","&Export":"導出","&Delete All":"刪除全部","&English":"英語","&Chinese Simplified":"簡體中文","&Chinese Traditional":"繁體中文","&Email":"電子郵箱"
        ,"Smooth Window":"濾波窗口","Noise Factor":"噪聲因子","Sigma":"標準差","Data Rename":"數據重命名","Please input new data name:":"請輸入新的數據名：","Information":"消息","Critical":"警告","No data selcted!":"沒有選中的數據！","Save File":"保存文件","Please select a data file":"請選擇壹個數據文件","Invalid Data File!":"不是合法的數據文件！","A error occur, please contact author for help!":"未知錯誤，請聯系作者！"}
        self.retranslateUI()
