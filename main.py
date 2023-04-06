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

        # self.nodeNumber.valueChanged.connect(self.printValue)
        self.pushButton.clicked.connect(self.click_Start)

        # Auto Sink는 항상 켜져있다.
        self.checkBox_auto.toggle()
        # 만약 min 버튼이 눌리거나 auto 버튼이 눌린다면
        self.checkBox_min.clicked.connect(self.clicked_Btn_min)
        self.checkBox_auto.clicked.connect(self.clicked_Btn_auto)

    # def printValue(self):
    #     print(self.nodeNumber.value())

    # 다음의 화면으로 넘어간다.
    def click_Start(self):
        self.nodeCount = self.nodeNumber.value()

    # 만약 min 버튼이 눌렸다면
    def clicked_Btn_min(self):
        print("Min 버튼이 눌림")
        self.checkBox_auto.toggle()
        self.sink_status = 1
    
    # 만약 auto 버튼이 눌렸다면
    def clicked_Btn_auto(self):
        print("auto 버튼이 눌림")
        self.checkBox_min.toggle()
        self.sink_status = 0
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()