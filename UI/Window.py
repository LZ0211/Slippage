from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, Signal
from json import load

class DataListWidget(QtWidgets.QListWidget):
    changed = Signal()
    def __init__(self,parent):
        super().__init__(parent)

    def dropEvent(self,event):
        super().dropEvent(event)
        self.changed.emit()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(900, 630)

        icon = QIcon()
        icon.addPixmap(QPixmap("resource/curve.ico"), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)

        MainWindow.setAcceptDrops(True)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)

        self.Process_Box = QtWidgets.QGroupBox(self.centralwidget)
        self.Process_Box.setMinimumSize(QtCore.QSize(290, 610))
        self.Process_Box.setFlat(True)

        self.Data_List_Label = QtWidgets.QLabel(self.Process_Box)
        self.Data_List_Label.setGeometry(QtCore.QRect(10, 13, 90, 16))
        self.Data_List = QtWidgets.QComboBox(self.Process_Box)
        self.Data_List.setGeometry(QtCore.QRect(100, 10, 180, 22))
        self.Data_List.setEditable(False)

        self.Skip_List_Label = QtWidgets.QLabel(self.Process_Box)
        self.Skip_List_Label.setGeometry(QtCore.QRect(10, 43, 90, 16))
        self.Skip_List = QtWidgets.QSpinBox(self.Process_Box)
        self.Skip_List.setGeometry(QtCore.QRect(100, 40, 110, 22))
        self.Skip_List.setMinimum(1)
        self.Skip_Button = QtWidgets.QPushButton(self.Process_Box)
        self.Skip_Button.setGeometry(QtCore.QRect(220, 40, 60, 23))

        self.Diff_List_Label = QtWidgets.QLabel(self.Process_Box)
        self.Diff_List_Label.setGeometry(QtCore.QRect(10, 73, 90, 16))
        self.Diff_List = QtWidgets.QSpinBox(self.Process_Box)
        self.Diff_List.setGeometry(QtCore.QRect(100, 70, 110, 22))
        self.Diff_List.setMinimum(1)
        self.Diff_Button = QtWidgets.QPushButton(self.Process_Box)
        self.Diff_Button.setGeometry(QtCore.QRect(220, 70, 60, 23))

        self.Cut_From_Label = QtWidgets.QLabel(self.Process_Box)
        self.Cut_From_Label.setGeometry(QtCore.QRect(10, 103, 90, 16))
        self.Cut_From = QtWidgets.QDoubleSpinBox(self.Process_Box)
        self.Cut_From.setGeometry(QtCore.QRect(100, 100, 40, 22))
        self.Cut_From.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Cut_From.setDecimals(2)
        self.Cut_From.setSingleStep(0.01)
        self.Cut_From.setProperty("value", 0.0)
        self.Cut_To_Label = QtWidgets.QLabel(self.Process_Box)
        self.Cut_To_Label.setGeometry(QtCore.QRect(145, 103, 20, 16))
        self.Cut_Button = QtWidgets.QPushButton(self.Process_Box)
        self.Cut_Button.setGeometry(QtCore.QRect(220, 100, 60, 23))
        self.Cut_To = QtWidgets.QDoubleSpinBox(self.Process_Box)
        self.Cut_To.setGeometry(QtCore.QRect(170, 100, 40, 22))
        self.Cut_To.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Cut_To.setDecimals(2)
        self.Cut_To.setSingleStep(0.01)
        self.Cut_To.setProperty("value", 0.0)

        self.Methods_List_Label = QtWidgets.QLabel(self.Process_Box)
        self.Methods_List_Label.setGeometry(QtCore.QRect(10, 133, 90, 16))
        self.Methods_List = QtWidgets.QComboBox(self.Process_Box)
        self.Methods_List.setGeometry(QtCore.QRect(100, 130, 180, 22))

        self.Smooth_Label = QtWidgets.QLabel(self.Process_Box)
        self.Smooth_Label.setGeometry(QtCore.QRect(10, 163, 90, 16))
        self.Smooth_Param = QtWidgets.QDoubleSpinBox(self.Process_Box)
        self.Smooth_Param.setGeometry(QtCore.QRect(100, 160,110, 22))
        self.Smooth_Param.setDecimals(6)
        self.Smooth_Param.setSingleStep(0.01)
        self.Smooth_Param.setProperty("value", 0.0)
        self.Smooth_Button = QtWidgets.QPushButton(self.Process_Box)
        self.Smooth_Button.setGeometry(QtCore.QRect(220, 160, 60, 23))

        self.Insert_List_Label = QtWidgets.QLabel(self.Process_Box)
        self.Insert_List_Label.setGeometry(QtCore.QRect(10, 193, 90, 16))
        self.Insert_List = QtWidgets.QSpinBox(self.Process_Box)
        self.Insert_List.setGeometry(QtCore.QRect(100, 190, 110, 22))
        self.Insert_List.setMinimum(0)
        self.Insert_List.setValue(3)
        self.Insert_Button = QtWidgets.QPushButton(self.Process_Box)
        self.Insert_Button.setGeometry(QtCore.QRect(220, 190, 60, 23))

        self.line_2 = QtWidgets.QFrame(self.Process_Box)
        self.line_2.setGeometry(QtCore.QRect(0, 215, 280, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.Param_Name_2 = QtWidgets.QLabel(self.Process_Box)
        self.Param_Name_2.setGeometry(QtCore.QRect(10, 230, 80, 16))
        self.VQ_Radio = QtWidgets.QRadioButton(self.Process_Box)
        self.VQ_Radio.setGeometry(QtCore.QRect(100, 230, 60, 16))
        self.VQ_Radio.setChecked(True)
        self.VQ_Radio.setAutoExclusive(True)
        self.dVdQ_Radio = QtWidgets.QRadioButton(self.Process_Box)
        self.dVdQ_Radio.setGeometry(QtCore.QRect(180, 230, 60, 16))

        self.Pos_List_Label = QtWidgets.QLabel(self.Process_Box)
        self.Pos_List_Label.setGeometry(QtCore.QRect(10, 260, 90, 16))
        self.Pos_List = QtWidgets.QComboBox(self.Process_Box)
        self.Pos_List.setGeometry(QtCore.QRect(100, 257, 180, 22))

        self.Neg_List_Label = QtWidgets.QLabel(self.Process_Box)
        self.Neg_List_Label.setGeometry(QtCore.QRect(10, 290, 90, 16))
        self.Neg_List = QtWidgets.QComboBox(self.Process_Box)
        self.Neg_List.setGeometry(QtCore.QRect(100, 287, 180, 22))

        self.Full_List_Label = QtWidgets.QLabel(self.Process_Box)
        self.Full_List_Label.setGeometry(QtCore.QRect(10, 320, 90, 16))
        self.Full_List = QtWidgets.QComboBox(self.Process_Box)
        self.Full_List.setGeometry(QtCore.QRect(100, 320, 180, 22))
        self.Full_List.addItem('')
        
        self.Positive_Box = QtWidgets.QGroupBox(self.Process_Box)
        self.Positive_Box.setGeometry(QtCore.QRect(5, 345, 275, 110))

        self.Pos_Scale_Label = QtWidgets.QLabel(self.Positive_Box)
        self.Pos_Scale_Label.setGeometry(QtCore.QRect(10, 20, 40, 16))
        self.Pos_Scale_Slider = QtWidgets.QSlider(self.Positive_Box)
        self.Pos_Scale_Slider.setGeometry(QtCore.QRect(55, 20, 90, 20))
        self.Pos_Scale_Slider.setMaximum(4)
        self.Pos_Scale_Slider.setPageStep(1)
        self.Pos_Scale_Slider.setProperty("value", 2)
        self.Pos_Scale_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Pos_Scale_SpinBox = QtWidgets.QDoubleSpinBox(self.Positive_Box)
        self.Pos_Scale_SpinBox.setGeometry(QtCore.QRect(160, 18, 80, 22))
        self.Pos_Scale_SpinBox.setDecimals(4)
        self.Pos_Scale_SpinBox.setSingleStep(1E-2)
        self.Pos_Scale_SpinBox.setProperty("value", 1.0)
        self.Pos_Scale_SpinBox.setMaximum(1E3)
        self.Pos_Scale_SpinBox.setKeyboardTracking(False)
        self.Pos_Scale_checkBox = QtWidgets.QCheckBox(self.Positive_Box)
        self.Pos_Scale_checkBox.setGeometry(QtCore.QRect(250, 18, 22, 22))
        self.Pos_Scale_checkBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Pos_Scale_checkBox.setText("")
        
        self.Pos_Shift_Label = QtWidgets.QLabel(self.Positive_Box)
        self.Pos_Shift_Label.setGeometry(QtCore.QRect(10, 50, 40, 16))
        self.Pos_Shift_Slider = QtWidgets.QSlider(self.Positive_Box)
        self.Pos_Shift_Slider.setGeometry(QtCore.QRect(55, 50, 90, 20))
        self.Pos_Shift_Slider.setMaximum(4)
        self.Pos_Shift_Slider.setPageStep(1)
        self.Pos_Shift_Slider.setProperty("value", 2)
        self.Pos_Shift_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Pos_Shift_SpinBox = QtWidgets.QDoubleSpinBox(self.Positive_Box)
        self.Pos_Shift_SpinBox.setGeometry(QtCore.QRect(160, 48, 80, 22))
        self.Pos_Shift_SpinBox.setWrapping(False)
        self.Pos_Shift_SpinBox.setDecimals(4)
        self.Pos_Shift_SpinBox.setMaximum(1E3)
        self.Pos_Shift_SpinBox.setSingleStep(1E-2)
        self.Pos_Shift_SpinBox.setKeyboardTracking(False)
        self.Pos_Shift_checkBox = QtWidgets.QCheckBox(self.Positive_Box)
        self.Pos_Shift_checkBox.setGeometry(QtCore.QRect(250, 48, 22, 22))
        self.Pos_Shift_checkBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Pos_Shift_checkBox.setText("")

        self.Pos_Shift2_Label = QtWidgets.QLabel(self.Positive_Box)
        self.Pos_Shift2_Label.setGeometry(QtCore.QRect(10, 80, 40, 16))
        self.Pos_Shift2_Slider = QtWidgets.QSlider(self.Positive_Box)
        self.Pos_Shift2_Slider.setGeometry(QtCore.QRect(55, 80, 90, 20))
        self.Pos_Shift2_Slider.setMaximum(4)
        self.Pos_Shift2_Slider.setPageStep(1)
        self.Pos_Shift2_Slider.setProperty("value", 2)
        self.Pos_Shift2_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Pos_Shift2_SpinBox = QtWidgets.QDoubleSpinBox(self.Positive_Box)
        self.Pos_Shift2_SpinBox.setGeometry(QtCore.QRect(160, 78, 80, 22))
        self.Pos_Shift2_SpinBox.setWrapping(False)
        self.Pos_Shift2_SpinBox.setDecimals(4)
        self.Pos_Shift2_SpinBox.setMaximum(1E3)
        self.Pos_Shift2_SpinBox.setSingleStep(1E-2)
        self.Pos_Shift2_SpinBox.setKeyboardTracking(False)
        self.Pos_Shift2_checkBox = QtWidgets.QCheckBox(self.Positive_Box)
        self.Pos_Shift2_checkBox.setGeometry(QtCore.QRect(250, 78, 22, 22))
        self.Pos_Shift2_checkBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Pos_Shift2_checkBox.setText("")

        self.Negative_Box = QtWidgets.QGroupBox(self.Process_Box)
        self.Negative_Box.setGeometry(QtCore.QRect(5, 460, 275, 110))

        self.Neg_Scale_Label = QtWidgets.QLabel(self.Negative_Box)
        self.Neg_Scale_Label.setGeometry(QtCore.QRect(10, 20, 40, 16))
        self.Neg_Scale_Slider = QtWidgets.QSlider(self.Negative_Box)
        self.Neg_Scale_Slider.setGeometry(QtCore.QRect(55, 20, 90, 20))
        self.Neg_Scale_Slider.setMaximum(4)
        self.Neg_Scale_Slider.setPageStep(1)
        self.Neg_Scale_Slider.setProperty("value", 2)
        self.Neg_Scale_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Neg_Scale_SpinBox = QtWidgets.QDoubleSpinBox(self.Negative_Box)
        self.Neg_Scale_SpinBox.setGeometry(QtCore.QRect(160, 18, 80, 22))
        self.Neg_Scale_SpinBox.setDecimals(4)
        self.Neg_Scale_SpinBox.setSingleStep(1E-2)
        self.Neg_Scale_SpinBox.setProperty("value", 1.0)
        self.Neg_Scale_SpinBox.setMaximum(1E3)
        self.Neg_Scale_SpinBox.setKeyboardTracking(False)
        self.Neg_Scale_checkBox = QtWidgets.QCheckBox(self.Negative_Box)
        self.Neg_Scale_checkBox.setGeometry(QtCore.QRect(250, 18, 22, 22))
        self.Neg_Scale_checkBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Neg_Scale_checkBox.setText("")
        
        self.Neg_Shift_Label = QtWidgets.QLabel(self.Negative_Box)
        self.Neg_Shift_Label.setGeometry(QtCore.QRect(10, 50, 40, 16))
        self.Neg_Shift_Slider = QtWidgets.QSlider(self.Negative_Box)
        self.Neg_Shift_Slider.setGeometry(QtCore.QRect(55, 50, 90, 20))
        self.Neg_Shift_Slider.setMaximum(4)
        self.Neg_Shift_Slider.setPageStep(1)
        self.Neg_Shift_Slider.setProperty("value", 2)
        self.Neg_Shift_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Neg_Shift_SpinBox = QtWidgets.QDoubleSpinBox(self.Negative_Box)
        self.Neg_Shift_SpinBox.setGeometry(QtCore.QRect(160, 48, 80, 22))
        self.Neg_Shift_SpinBox.setDecimals(4)
        self.Neg_Shift_SpinBox.setMaximum(1E3)
        self.Neg_Shift_SpinBox.setSingleStep(1E-2)
        self.Neg_Shift_SpinBox.setKeyboardTracking(False)
        self.Neg_Shift_checkBox = QtWidgets.QCheckBox(self.Negative_Box)
        self.Neg_Shift_checkBox.setGeometry(QtCore.QRect(250, 48, 22, 22))
        self.Neg_Shift_checkBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Neg_Shift_checkBox.setText("")

        self.Neg_Shift2_Label = QtWidgets.QLabel(self.Negative_Box)
        self.Neg_Shift2_Label.setGeometry(QtCore.QRect(10, 80, 40, 16))
        self.Neg_Shift2_Slider = QtWidgets.QSlider(self.Negative_Box)
        self.Neg_Shift2_Slider.setGeometry(QtCore.QRect(55, 80, 90, 20))
        self.Neg_Shift2_Slider.setMaximum(4)
        self.Neg_Shift2_Slider.setPageStep(1)
        self.Neg_Shift2_Slider.setProperty("value", 2)
        self.Neg_Shift2_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Neg_Shift2_SpinBox = QtWidgets.QDoubleSpinBox(self.Negative_Box)
        self.Neg_Shift2_SpinBox.setGeometry(QtCore.QRect(160, 78, 80, 22))
        self.Neg_Shift2_SpinBox.setDecimals(4)
        self.Neg_Shift2_SpinBox.setMaximum(1E3)
        self.Neg_Shift2_SpinBox.setSingleStep(1E-2)
        self.Neg_Shift2_SpinBox.setKeyboardTracking(False)
        self.Neg_Shift2_checkBox = QtWidgets.QCheckBox(self.Negative_Box)
        self.Neg_Shift2_checkBox.setGeometry(QtCore.QRect(250, 78, 22, 22))
        self.Neg_Shift2_checkBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Neg_Shift2_checkBox.setText("")

        #self.RMSD_Label = QtWidgets.QLabel(self.Process_Box)
        #self.RMSD_Label.setGeometry(QtCore.QRect(10, 560, 40, 16))
        self.RMSD = QtWidgets.QLineEdit(self.Process_Box)
        #self.RMSD.setGeometry(QtCore.QRect(60, 557, 60, 22))
        self.RMSD.setGeometry(QtCore.QRect(10, 577, 70, 22))
        self.RMSD.setReadOnly(True)
        #self.RMSD.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        #self.RMSD.setText('0.1234E-5')
        
        self.Guess_Button = QtWidgets.QPushButton(self.Process_Box)
        self.Guess_Button.setGeometry(QtCore.QRect(88, 577, 60, 23))

        self.Fitting_Button = QtWidgets.QPushButton(self.Process_Box)
        self.Fitting_Button.setGeometry(QtCore.QRect(154, 577, 60, 23))
        self.Scale_Button = QtWidgets.QPushButton(self.Process_Box)
        self.Scale_Button.setGeometry(QtCore.QRect(220, 577, 60, 23))

        self.gridLayout.addWidget(self.Process_Box, 0, 1, 2, 1)

        self.listWidget = DataListWidget(self.centralwidget)
        self.listWidget.setMinimumSize(QtCore.QSize(0, 160))
        self.listWidget.setMaximumSize(QtCore.QSize(16777215, 160))
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setDefaultDropAction(Qt.MoveAction)
        self.listWidget.setDragDropMode(self.listWidget.InternalMove)

        self.listMenu = QtWidgets.QMenu(self.listWidget)
        self.list_action_delete = QtWidgets.QAction(self.listMenu)
        self.list_action_rename = QtWidgets.QAction(self.listMenu)
        self.list_action_view = QtWidgets.QAction(self.listMenu)
        self.list_action_export = QtWidgets.QAction(self.listMenu)
        self.list_action_delall = QtWidgets.QAction(self.listMenu)
        self.list_menu_display = QtWidgets.QMenu(self.listMenu)
        self.list_action_display = QtWidgets.QAction(self.list_menu_display)
        self.list_action_undisplay = QtWidgets.QAction(self.list_menu_display)
        self.list_action_record = QtWidgets.QAction(self.listMenu)
        self.listMenu.addAction(self.list_action_delete)
        self.listMenu.addAction(self.list_action_rename)
        self.listMenu.addAction(self.list_action_view)
        self.listMenu.addAction(self.list_action_export)
        self.listMenu.addAction(self.list_action_delall)
        self.listMenu.addMenu(self.list_menu_display)
        self.listMenu.addAction(self.list_action_record)
        self.list_menu_display.addAction(self.list_action_display)
        self.list_menu_display.addAction(self.list_action_undisplay)

        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 1)
        self.graphicsView = QtWidgets.QGridLayout()
        self.gridLayout.addLayout(self.graphicsView, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 822, 23))
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menu_Open = QtWidgets.QMenu(self.menuFile)
        self.menu_Open.setIcon(QIcon(QPixmap("resource/Open.png")))
        self.menu_Recent_Files = QtWidgets.QMenu(self.menuFile)
        self.menu_Edit = QtWidgets.QMenu(self.menubar)
        self.menu_Data = QtWidgets.QMenu(self.menubar)
        self.menu_Tool = QtWidgets.QMenu(self.menubar)
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Language = QtWidgets.QMenu(self.menubar)
        self.menu_Theme = QtWidgets.QMenu(self.menubar)
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.toolBar = QtWidgets.QToolBar(MainWindow)
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)

        self.action_New = QtWidgets.QAction(MainWindow)
        self.action_New.setIcon(QIcon(QPixmap("resource/New.png")))
        self.action_Project = QtWidgets.QAction(MainWindow)
        self.action_Project.setIcon(QIcon(QPixmap("resource/Project.png")))
        self.action_Save = QtWidgets.QAction(MainWindow)
        self.action_Save.setIcon(QIcon(QPixmap("resource/Save.png")))
        self.action_Save_As = QtWidgets.QAction(MainWindow)
        self.action_Save_As.setIcon(QIcon(QPixmap("resource/SaveAs.png")))
        self.action_Preferences = QtWidgets.QAction(MainWindow)
        self.action_Preferences.setIcon(QIcon(QPixmap("resource/Gear.png")))
        self.action_Exit = QtWidgets.QAction(MainWindow)
        self.action_Exit.setIcon(QIcon(QPixmap("resource/Exit.png")))
        self.action_Positive_Reference = QtWidgets.QAction(MainWindow)
        self.action_Positive_Reference.setIcon(QIcon(QPixmap("resource/Positive.png")))
        self.action_Negative_Reference = QtWidgets.QAction(MainWindow)
        self.action_Negative_Reference.setIcon(QIcon(QPixmap("resource/Negative.png")))
        self.action_Measured_Data = QtWidgets.QAction(MainWindow)
        self.action_Measured_Data.setIcon(QIcon(QPixmap("resource/Battery.png")))
        self.action_Excel2TXT = QtWidgets.QAction(MainWindow)
        self.action_Excel2CSV = QtWidgets.QAction(MainWindow)
        self.action_CSV2TXT = QtWidgets.QAction(MainWindow)
        self.action_CSV2Excel = QtWidgets.QAction(MainWindow)
        self.action_TXT2CSV = QtWidgets.QAction(MainWindow)
        self.action_TXT2Excel = QtWidgets.QAction(MainWindow)
        self.action_Delete = QtWidgets.QAction(MainWindow)
        self.action_Delete.setIcon(QIcon(QPixmap("resource/Delete.png")))
        self.action_Delete_All = QtWidgets.QAction(MainWindow)
        self.action_Delete_All.setIcon(QIcon(QPixmap("resource/DeleteAll.png")))
        self.action_View = QtWidgets.QAction(MainWindow)
        self.action_View.setIcon(QIcon(QPixmap("resource/View.png")))
        self.action_Swap = QtWidgets.QAction(MainWindow)
        self.action_Swap.setIcon(QIcon(QPixmap("resource/Transform.png")))
        self.action_Rename = QtWidgets.QAction(MainWindow)
        self.action_Rename.setIcon(QIcon(QPixmap("resource/Rename.png")))
        self.action_Export = QtWidgets.QAction(MainWindow)
        self.action_Export.setIcon(QIcon(QPixmap("resource/Export.png")))
        self.action_English = QtWidgets.QAction(MainWindow)
        self.action_Data_Write = QtWidgets.QAction(MainWindow)
        self.action_Data_Write.setIcon(QIcon(QPixmap("resource/Write.png")))
        self.action_Data_View = QtWidgets.QAction(MainWindow)
        self.action_Data_View.setIcon(QIcon(QPixmap("resource/Preview.png")))
        self.action_Data_Export = QtWidgets.QAction(MainWindow)
        self.action_Data_Export.setIcon(QIcon(QPixmap("resource/ExportExcel.png")))
        self.action_Electrode_Export = QtWidgets.QAction(MainWindow)
        self.action_Electrode_Export.setIcon(QIcon(QPixmap("resource/Electrodes.png")))
        self.action_Sheet_Export = QtWidgets.QAction(MainWindow)
        self.action_Sheet_Export.setIcon(QIcon(QPixmap("resource/Sheet.png")))
        self.action_Data_FindPeak = QtWidgets.QAction(MainWindow)
        self.action_Data_FindPeak.setIcon(QIcon(QPixmap("resource/Peak.png")))
        self.action_Chinese_Simplified = QtWidgets.QAction(MainWindow)
        self.action_Chinese_Traditional = QtWidgets.QAction(MainWindow)
        self.action_Author_Email = QtWidgets.QAction(MainWindow)
        self.action_Author_Email.setIcon(QIcon(QPixmap("resource/Email.png")))
        self.action_UserGuide = QtWidgets.QAction(MainWindow)
        self.action_UserGuide.setIcon(QIcon(QPixmap("resource/Help.png")))
        self.menu_Open.addAction(self.action_Positive_Reference)
        self.menu_Open.addAction(self.action_Negative_Reference)
        self.menu_Open.addAction(self.action_Measured_Data)
        self.menuFile.addAction(self.menu_Open.menuAction())
        self.menuFile.addAction(self.action_New)
        self.menuFile.addAction(self.action_Project)
        self.menuFile.addAction(self.action_Save)
        self.menuFile.addAction(self.action_Save_As)
        self.menuFile.addAction(self.action_Exit)
        self.menuFile.addAction(self.action_Preferences)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menu_Recent_Files.menuAction())
        self.menu_Edit.addAction(self.action_View)
        self.menu_Edit.addAction(self.action_Swap)
        self.menu_Edit.addAction(self.action_Rename)
        self.menu_Edit.addAction(self.action_Delete)
        self.menu_Edit.addAction(self.action_Export)
        self.menu_Edit.addAction(self.action_Delete_All)
        self.menu_Data.addAction(self.action_Data_Write)
        self.menu_Data.addAction(self.action_Data_View)
        self.menu_Data.addAction(self.action_Data_Export)
        self.menu_Data.addAction(self.action_Electrode_Export)
        self.menu_Data.addAction(self.action_Sheet_Export)
        self.menu_Data.addAction(self.action_Data_FindPeak)
        self.menu_Tool.addAction(self.action_Excel2TXT)
        self.menu_Tool.addAction(self.action_Excel2CSV)
        self.menu_Tool.addAction(self.action_CSV2TXT)
        self.menu_Tool.addAction(self.action_CSV2Excel)
        self.menu_Tool.addAction(self.action_TXT2CSV)
        self.menu_Tool.addAction(self.action_TXT2Excel)
        self.menu_Language.addAction(self.action_English)
        self.menu_Language.addAction(self.action_Chinese_Simplified)
        self.menu_Language.addAction(self.action_Chinese_Traditional)
        self.menu_Help.addAction(self.action_UserGuide)
        self.menu_Help.addAction(self.action_Author_Email)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_Data.menuAction())
        self.menubar.addAction(self.menu_Tool.menuAction())
        self.menubar.addAction(self.menu_Language.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.menubar.addAction(self.menu_Theme.menuAction())
        self.toolBar.addAction(self.action_Positive_Reference)
        self.toolBar.addAction(self.action_Negative_Reference)
        self.toolBar.addAction(self.action_Measured_Data)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_View)
        self.toolBar.addAction(self.action_Swap)
        self.toolBar.addAction(self.action_Rename)
        self.toolBar.addAction(self.action_Export)
        self.toolBar.addAction(self.action_Delete)
        self.toolBar.addAction(self.action_Delete_All)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Data_Write)
        self.toolBar.addAction(self.action_Data_View)
        self.toolBar.addAction(self.action_Data_Export)
        self.toolBar.addAction(self.action_Data_FindPeak)
        self.langText = {}
        self._translate = lambda k,v:QtCore.QCoreApplication.translate(k,self.translateText(v))
        MainWindow.setWindowTitle(self._translate("MainWindow", "ATL-Electrical Chemistry Analysor"))
        self.retranslateUI()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUI(self):
        _translate = self._translate
        self.Data_List_Label.setText(_translate("MainWindow", "Data List"))
        self.Methods_List_Label.setText(_translate("MainWindow", "Smooth Methods"))
        self.Skip_List_Label.setText(_translate("MainWindow", "Skip Interval"))
        self.Skip_Button.setText(_translate("MainWindow", "Skip"))
        self.Diff_List_Label.setText(_translate("MainWindow", "Diff Interval"))
        self.Diff_Button.setText(_translate("MainWindow", "Diff"))
        self.Smooth_Label.setText(_translate("MainWindow", "Smooth Parameter"))
        self.Smooth_Button.setText(_translate("MainWindow", "Smooth"))
        self.Insert_List_Label.setText(_translate("MainWindow", "Interpolate Order"))
        self.Insert_Button.setText(_translate("MainWindow", "Insert"))
        self.Param_Name_2.setText(_translate("MainWindow", "Date Type"))
        self.VQ_Radio.setText(_translate("MainWindow", "V-Q"))
        self.dVdQ_Radio.setText(_translate("MainWindow", "dVdQ-Q"))
        self.Pos_List_Label.setText(_translate("MainWindow", "Positive"))
        self.Neg_List_Label.setText(_translate("MainWindow", "Negative"))
        self.Full_List_Label.setText(_translate("MainWindow", "FullCell"))
        self.Positive_Box.setTitle(_translate("MainWindow", "Positive"))
        self.Pos_Scale_Label.setText(_translate("MainWindow", "Scale"))
        self.Pos_Shift_Label.setText(_translate("MainWindow", "L-Shift"))
        self.Pos_Shift2_Label.setText(_translate("MainWindow", "R-Shift"))
        self.Negative_Box.setTitle(_translate("MainWindow", "Negative"))
        self.Neg_Scale_Label.setText(_translate("MainWindow", "Scale"))
        self.Neg_Shift_Label.setText(_translate("MainWindow", "L-Shift"))
        self.Neg_Shift2_Label.setText(_translate("MainWindow", "R-Shift"))
        self.Fitting_Button.setText(_translate("MainWindow", "Fitting"))
        self.Cut_From_Label.setText(_translate("MainWindow", "Cut From"))
        self.Cut_To_Label.setText(_translate("MainWindow", "To"))
        self.Cut_Button.setText(_translate("MainWindow", "Cut"))
        #self.RMSD_Label.setText(_translate("MainWindow", "RMSD"))
        self.Scale_Button.setText(_translate("MainWindow", "Scale"))
        self.Guess_Button.setText(_translate("MainWindow", "Guess"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menu_Open.setTitle(_translate("MainWindow", "&Open"))
        self.menu_Recent_Files.setTitle(_translate("MainWindow", "&Recent Files"))
        self.menu_Data.setTitle(_translate("MainWindow", "&Data"))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit"))
        self.menu_Tool.setTitle(_translate("MainWindow", "&Tool"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menu_Language.setTitle(_translate("MainWindow", "&Language"))
        self.menu_Theme.setTitle(_translate("MainWindow", "&Theme"))
        self.action_New.setText(_translate("MainWindow", "&New"))
        self.action_New.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.action_Project.setText(_translate("MainWindow", "&Project"))
        self.action_Project.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_Save.setText(_translate("MainWindow", "&Save"))
        self.action_Save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action_Save_As.setText(_translate("MainWindow", "&Save As"))
        self.action_Save_As.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
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
        self.action_Delete.setShortcut(_translate("MainWindow", "Delete"))
        self.action_View.setText(_translate("MainWindow", "&View"))
        self.action_Swap.setText(_translate("MainWindow", "&Swap Axes"))
        self.action_Rename.setText(_translate("MainWindow", "&Rename"))
        self.action_Rename.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.action_Export.setText(_translate("MainWindow", "&Export"))
        self.action_Export.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.action_Delete_All.setText(_translate("MainWindow", "&Delete All"))
        self.action_Delete_All.setShortcut(_translate("MainWindow", "Shift+Delete"))
        self.action_Data_Export.setText(_translate("MainWindow", "&Export Results"))
        self.action_Electrode_Export.setText(_translate("MainWindow", "Electrodes Potential"))
        self.action_Sheet_Export.setText(_translate("MainWindow", "Electrodes Sheet"))
        self.action_Data_FindPeak.setText(_translate("MainWindow", "&Find Peak"))
        self.action_Data_View.setText(_translate("MainWindow", "&View Results"))
        self.action_Data_Write.setText(_translate("MainWindow", "&Import Results"))
        self.action_English.setText(_translate("MainWindow", "&English"))
        self.action_Chinese_Simplified.setText(_translate("MainWindow", "&Chinese Simplified"))
        self.action_Chinese_Traditional.setText(_translate("MainWindow", "&Chinese Traditional"))
        self.action_UserGuide.setText(_translate("MainWindow", "&User Guide"))
        self.action_Author_Email.setText(_translate("MainWindow", "&Email"))
        self.list_menu_display.setTitle(_translate("MainWindow", "&Display"))
        self.list_action_delete.setText(_translate("MainWindow", "&Delete"))
        self.list_action_rename.setText(_translate("MainWindow", "&Rename"))
        self.list_action_view.setText(_translate("MainWindow", "&View"))
        self.list_action_export.setText(_translate("MainWindow", "&Export"))
        self.list_action_delall.setText(_translate("MainWindow", "&Delete Selected"))
        self.list_action_display.setText(_translate("MainWindow", "All"))
        self.list_action_undisplay.setText(_translate("MainWindow", "None"))
        self.list_action_record.setText(_translate("MainWindow", "Operation records"))

    def translateText(self,text):
        if text in self.langText:
            return self.langText[text]
        return text

    def transEnglish(self):
        self.langText = {}
        self.retranslateUI()

    def transChineseSimplified(self):
        self.langText = load(open('resource/SCN.translation',encoding='utf-8'))
        self.retranslateUI()

    def transChineseTraditional(self):
        self.langText = load(open('resource/TCN.translation',encoding='utf-8'))
        self.retranslateUI()