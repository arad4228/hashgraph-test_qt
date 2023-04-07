import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
N = 7 # 라인 별 노드 수
M = 4 # 라인 수

colorList = ["blue", "red", "green", "yellow"]

for i in range(M) :
    G.add_node((i, 0), 
               value = str((i, 0)) + "!!!",
               pos = (5 * i, 0), 
               color = colorList[i])

for i in range(M) :
    for j in range(1, N) :
        G.add_node((i, j), 
                   value = str((i, j)) + "!!!", 
                   pos = (5 * i, 5 * j), 
                   color = colorList[i])
        G.add_edge((i, j - 1), (i, j))

edge_x = []
edge_y = []

for edge in G.edges() :
    startPoint = edge[0]
    endPoint = edge[1]
    x0, y0 = G.nodes[startPoint]['pos']
    x1, y1 = G.nodes[endPoint]['pos']

    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)
    # None : 그냥 구분용

# hoverinfo : 마우스 위에 올리면 나오는 거
edge_trace = go.Scatter(
    x=edge_x, y=edge_y, line=dict(width=0.5),
    hoverinfo='none', mode='lines'
)

node_x = []
node_y = []
node_color = []
for node in G.nodes() :
    print(G.nodes[node])
    x, y = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)
    node_color.append(G.nodes[node]["color"])

node_trace = go.Scatter(
    x=node_x, y=node_y, mode='markers',
    hoverinfo='text',
    marker=dict(
        color=node_color,
        size=20,
    )
)

node_text = []
for node in G.nodes() :
    node_text.append(G.nodes[node]["value"])

node_trace.text = node_text

fig = go.Figure(data=[edge_trace, node_trace])
fig.show()