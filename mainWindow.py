from PyQt5 import uic
from PyQt5.QtWidgets import *
from hashGrapth import *

main_form_class = uic.loadUiType("./uis/main_GUI.ui")[0]

class Main_WindowClass(QMainWindow, main_form_class):
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


    # 다음의 화면으로 넘어간다.
    def click_Start(self):
        self.nodeCount = self.nodeNumber.value()
        if self.nodeCount >= 3:
            self.hide()
            self.graph = Grapth_windowClass()
            self.graph.setup_nodeCount(self.nodeCount)
            self.graph.exec_()
            self.show()

    def clicked_BtnSinkType(self, id):
        if self.checkBox_auto.isChecked():
            self.sink_status = 0
        else:
            self.sink_status = 1