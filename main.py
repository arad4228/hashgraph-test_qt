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
    nodeCount = 0
    sink_status = 0 # 0 is auto, 1 is min settings

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("PET HashGraph")

        # self.nodeNumber.valueChanged.connect(self.printValue)
        self.pushButton.clicked.connect(self.click_Start)

        self.group_checkBoxes.buttonClicked[int].connect(self.clicked_BtnSinkType)
        # Auto Sink는 항상 켜진 상태이다.
        self.checkBox_auto.toggle()

    # def printValue(self):
    #     print(self.nodeNumber.value())

    # 다음의 화면으로 넘어간다.
    def click_Start(self):
        self.nodeCount = self.nodeNumber.value()

    def clicked_BtnSinkType(self, id):
        if self.checkBox_auto.isChecked():
            print("Auto Clicked")
            self.sink_status = 0
        else:
            print("Min Clicked")
            self.sink_status = 1
        print(self.sink_status)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()