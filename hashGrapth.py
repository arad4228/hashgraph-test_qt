import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from matplotlib import animation    # 에니메이션을 위해서
import matplotlib.pyplot as plt     # 그래프를 그리기 위해서
import networkx as nx               # 그래프를 그리기 위해서 불러온다.
from functools import partial
import plotly.graph_objects as go

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas    # pyQt에 그리기 위해서 사용
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# Graph_form_class = uic.loadUiType("./uis/hash_Graph_GUI.ui")[0]

class Graph_windowClass(QDialog, QWidget):
    graph_nodeCount = 0
    N = 7

    colorList = ["blue", "red", "green", "yellow"]

    def __init__(self):
        super().__init__()
        self.setupUi()
        self.show()

    def setupUi(self):
        self.setGeometry(600, 200, 1200, 600)
        self.setWindowTitle("PET HashGraph alpha Test")

        self.BtnDrawGraph = QPushButton("Hash Graph 그리기")
        self.BtnDrawGraph.setObjectName(u'BtnDrawGraph')
        self.BtnDrawGraph.setGeometry(800, 300, 100, 100)
        self.BtnDrawGraph.clicked.connect(self.clicked_btn)

        self.fig = plt.Figure()
        # self.canvas = FigureCanvas(self.fig)
        # self.toolbar = NavigationToolbar(self.canvas, self)
        self.webEngineview = QWebEngineView()

        leftLayout = QVBoxLayout()
        # leftLayout.addWidget(self.toolbar)
        leftLayout.addWidget(self.webEngineview)

        # Right Layout
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.BtnDrawGraph)
        rightLayout.addStretch(1)

        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        layout.setStretchFactor(leftLayout, 1)
        layout.setStretchFactor(rightLayout, 0)

        self.setLayout(layout)

    def setup_nodeCount(self, nodeCount:int):
        self.graph_nodeCount = nodeCount
        print(self.graph_nodeCount)
    
    def make_networkx(self):
        # networkx 그래프 변수 생성
        g = nx.DiGraph()

        # 전달 받은 노드 만큼 노드를 생성.
        for i in range(self.graph_nodeCount):
            g.add_node((i, 0))
        return g
    
    def make_position(self):
        pos = {}
        for i in range(self.graph_nodeCount):
            for j in range(self.N):
                pos[(i, j)] = [i*5, j*5]
        return pos

    def select_color(self):
        color = {}
        for i in range(self.graph_nodeCount):
            for j in range(self.N):
                color[(i, j)] = self.colorList[i%4]
        return color
    
    def make_nodes(self):
        nodes = []
        for i in range(self.graph_nodeCount):
            for j in range(1, self.N):
                nodes.append((i,j))
        return nodes

    def animate(self, idx, nodes, G, pos, color, ax):
        if idx >= len(nodes) :
            os.system("pause")
        i = nodes[idx][0]
        j = nodes[idx][1]
        G.add_node((i, j))
        G.add_edge((i, j - 1), (i, j))
        nx.draw(G, pos=pos, nodelist=[(i, j)], node_color=color[(i, j)], with_labels=True, ax=ax)

    def clicked_btn(self):
        self.fig.clf()
        fig = plt.figure()
        ax = self.fig.add_subplot(1,1,1)
        G = self.make_networkx()
        pos = self.make_position()
        color = self.select_color()

        nx.draw(G, pos=pos, with_labels=True, ax=ax)
        for i in range(self.graph_nodeCount):
            nx.draw_networkx_nodes(G, pos=pos, nodelist=[(i,0)], node_color=color[(i, 0)], ax=ax)

        nodes = self.make_nodes()

        ani = animation.FuncAnimation(self.fig, partial(self.animate, nodes=nodes, G=G, pos=pos, color=color, ax=ax), frames=len(nodes), interval=500, repeat=False)
        self.canvas.draw()
