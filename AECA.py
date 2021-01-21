# coding=utf-8
import sys,os
sys.path = ['','libs','libs/python.zip','libs/env']
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication,QSplashScreen
from PyQt5.QtGui import QPixmap
from UI.App import Application


if __name__ == '__main__':
    QApplication.setOrganizationName("ATL")
    QApplication.setOrganizationDomain("http://www.atlinfo.com")
    QApplication.setApplicationName("Electrical Chemistry Analysor")
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap("resource/init.png"))
    splash.show()
    mainWin = Application(os.path.dirname(os.path.abspath(__file__)))
    if sys.argv.__len__() > 1:
        mainWin.loadProjectFile(sys.argv[-1])
    splash.finish(mainWin)
    app.exit(app.exec_())

