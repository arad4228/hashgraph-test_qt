import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation
from functools import partial
import PyQt5
import os

dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'Qt5','plugins','platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

G = nx.DiGraph()
N = 7 # 각 라인 별 노드 수
M = 4 # 라인 수

fig = plt.figure()

for i in range(M) :
    G.add_node((i, 0))

pos = {}
for i in range(M) :
    for j in range(N) :
        pos[(i, j)] = [i * 5, j * 5]

colorList = ["blue", "red", "green", "yellow"]
color = {}
for i in range(M) :
    for j in range(N) :
        color[(i, j)] = colorList[i]

nx.draw(G, pos=pos, with_labels=True)
for i in range(M) :
    nx.draw_networkx_nodes(G, pos=pos, nodelist = [(i, 0)], node_color=colorList[i])

# animate
nodes = []
for i in range(M) :
    for j in range(1, N) :
        nodes.append((i, j))

def animate(idx, nodes) :
    if idx >= len(nodes) :
        os.system("pause")
    i = nodes[idx][0]
    j = nodes[idx][1]
    G.add_node((i, j))
    G.add_edge((i, j - 1), (i, j))
    nx.draw(G, pos=pos, nodelist = [(i, j)], node_color=colorList[i], with_labels=True)

ani = animation.FuncAnimation(fig, partial(animate, nodes=nodes))
plt.show()