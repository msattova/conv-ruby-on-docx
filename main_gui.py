import sys
from PySide2.QtWidgets import QApplication

from gui.mainwindow import MainWindow

if __name__ == '__main__':

    qAp = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    qAp.exec_()
