import sys
import os
import PyQt5
from PyQt5 import uic
from PyQt5.QtWidgets import *

dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'Qt5','plugins','platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

main_form_class = uic.loadUiType("./uis/main_GUI.ui")[0]

class WindowClass(QMainWindow, main_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.nodeNumber.valueChanged.connect(self.printValue)
        self.pushButton.clicked.connect(self.click_Start)

    def printValue(self):
        print(self.nodeNumber.value())

    def click_Start(self):
        self.printValue()
        print("Start가 눌림")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()