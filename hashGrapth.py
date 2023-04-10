import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QUrl

import networkx as nx               # 그래프를 그리기 위해서 불러온다.
import plotly.graph_objects as go
import plotly

# Graph_form_class = uic.loadUiType("./uis/hash_Graph_GUI.ui")[0]

updatemenus = [
    {
        'buttons': [
            {
                'label': 'Play',
                'method': 'animate',
                'args': [None, {'frame': {'duration': 100, 'redraw': False},
                                 'fromcurrent': True, 'transition': {'duration':0}}],
            },
            {
                'label': 'Pause',
                'method': 'animate',
                'args': [[None], {'frame': {'duration': 0, 'redraw': False},
                                 'mode': 'immediate', 'transition': {'duration': 0}}],
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }
]

class Graph_windowClass(QDialog, QWidget):
    graph_nodeCount = 0
    N = 7

    colorList = ["blue", "red", "green", "yellow"]

    node_x = []
    node_y = []
    node_color_list = []
    edge_x = []
    edge_y = []

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

        self.webEngineview = QWebEngineView()

        leftLayout = QVBoxLayout()
        # plotly를 위한 공간 할당
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

    def clear_old_data(self):
        self.node_x.clear()
        self.node_y.clear()
        self.node_color_list.clear()
        self.edge_x.clear()
        self.edge_y.clear()
    
    def init_graph(self):
        # networkx 그래프 변수 생성
        g = nx.DiGraph()

        # 전달 받은 노드 만큼 노드를 생성.
        for i in range(self.graph_nodeCount):
            g.add_node((i, 0), value = str((i,0)) +"!!!", pos =(5*i, 0), color = self.colorList[i%4])
        
        for i in range(self.graph_nodeCount):
            for j in range(1,self.N):
                g.add_node((i, j), value = str((i,j)) +"!!!", pos =(5*i, 5*j), color = self.colorList[i%4])
                g.add_edge((i, j-1), (i, j))
        return g

    def make_nodes(self, g):
        for node in g.nodes():
            x, y = g.nodes[node]['pos']
            self.node_x.append(x)
            self.node_y.append(y)
            self.node_color_list.append(g.nodes[node]["color"])

    def make_edge(self, g):
        for edge in g.edges():
            startPoint = edge[0]
            endPoint = edge[1]
            x0, y0 = g.nodes[startPoint]['pos']
            x1, y1 = g.nodes[endPoint]['pos']

            self.edge_x.append(x0)
            self.edge_x.append(x1)
            self.edge_x.append(None)
            self.edge_y.append(y0)
            self.edge_y.append(y1)
            self.edge_y.append(None)
            # None : 그냥 구분용
    
    def clicked_btn(self):
        # 리스트에 데이터가 축적되는 것을 막기위해서
        self.clear_old_data()

        # 그래프에 들어갈 데이터 준비
        G = self.init_graph()

        # Edge 정보 만들기
        self.make_edge(G)
        # edge에 대한 줄 만들기
        edge_trace = edge_trace = go.Scatter(x=self.edge_x, y=self.edge_y, line=dict(width=0.5), hoverinfo='none', 
                                         mode='lines')
        
        # Node의 정보 만들기
        self.make_nodes(G)
        # Node의 정보 붙이기
        node_trace = go.Scatter(x=self.node_x, y=self.node_y, mode='markers', hoverinfo='text', 
                            marker=dict(color=self.node_color_list, size=20))
    
        node_text = []
        for node in G.nodes():
            node_text.append(G.nodes[node]["value"])
    
        node_trace.text = node_text

        fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(showlegend=False, hovermode='closest', margin=dict(b=20,l=5,r=5,t=40),
                                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    
        frames = [go.Frame(
            data=[
                go.Scatter(x=self.edge_x[:3 * (i+1)], y=self.edge_y[:3 * (i+1)]), 
                go.Scatter(x=self.node_x[:i+1], y=self.node_y[:i+1])])
        for i in range(self.graph_nodeCount*self.N)]

        fig.update(frames=frames)
        fig.update_layout(updatemenus=updatemenus)
        
        # HTML 파일 생성 및 로드
        html = plotly.io.to_html(fig, include_plotlyjs=True, full_html=True)
        with open('graph.html', 'w', encoding='utf-8') as f:
            f.write(html)
        self.webEngineview.setUrl(QUrl.fromLocalFile(os.path.abspath('graph.html')))