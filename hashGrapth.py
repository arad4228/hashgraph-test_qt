from PyQt5 import uic
from PyQt5.QtWidgets import *

Graph_form_class = uic.loadUiType("./uis/hash_Graph_GUI.ui")[0]

class Grapth_windowClass(QDialog, QWidget, Graph_form_class):
    graph_nodeCount = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
    
    def setup_nodeCount(self, nodeCount:int):
        self.graph_nodeCount = nodeCount
        print(self.graph_nodeCount)