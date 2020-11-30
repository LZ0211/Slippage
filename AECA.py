# coding=utf-8
import sys,os
sys.path = ['','libs','libs/python.zip','libs/env']
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtNetwork import QLocalSocket, QLocalServer
from UI.App import Application


if __name__ == '__main__':
    QApplication.setOrganizationName("ATL")
    QApplication.setOrganizationDomain("http://www.atlinfo.com")
    QApplication.setApplicationName("Electrical Chemistry Analysor")
    app = QApplication(sys.argv)
    mainWin = Application(os.path.dirname(os.path.abspath(__file__)))
    if sys.argv.__len__() > 1:
        mainWin.loadProjectFile(sys.argv[-1])
    app.exit(app.exec_())
    # try:
    #     QApplication.setOrganizationName("ATL")
    #     QApplication.setOrganizationDomain("http://www.atlinfo.com")
    #     QApplication.setApplicationName("Electrical Chemistry Analysor")
    #     app = QApplication(sys.argv)
    #     serverName = 'ATL'
    #     socket = QLocalSocket()
    #     socket.connectToServer(serverName)
    #     if socket.waitForConnected(500):
    #         app.quit()
    #     else:
    #         localServer = QLocalServer()
    #         localServer.listen(serverName)
    #         mainWin = Application(os.path.dirname(os.path.abspath(__file__)))
    #         #拖拽文件到App上的时候直接打开
    #         if sys.argv.__len__() > 1:
    #             mainWin.loadProjectFile(sys.argv[-1])
    #         #sys.exit(app.exec_())
    #         app.exit(app.exec_())
    # except:
    #     pass
