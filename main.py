from copy import deepcopy
import time
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class Node:
    def __init__(self, name, degree):
        self.name = name
        self.degree = degree


class GraphSeries:

    def __init__(self, series):
        self.series = sorted([Node(f"v{i}", series[i]) for i in range(len(series))], reverse=True,
                             key=lambda x: x.degree)
        self.degree_series = None
        self.graph_series = None
        self.edges = None
        self.graph = None
        self.is_degree_series()
        self.is_graph_series()
        self.set_graph()

    @staticmethod
    def all_positive(series):
        return bool((np.array([x.degree for x in series]) >= 0).all())

    @staticmethod
    def all_zeros(series):
        return bool((np.array([x.degree for x in series]) == 0).all())

    def is_degree_series(self):
        if not self.degree_series:
            self.degree_series = not bool(sum([i.degree for i in self.series]) % 2)

    def is_graph_series(self):
        if (not self.graph_series) and self.degree_series and max([x.degree for x in self.series]) < len(self.series):
            self.edges = []
            process = [self.series]
            while self.all_positive(process[-1]) and (not self.all_zeros(process[-1])):
                tmp = deepcopy(process[-1])
                for i in range(1, min(tmp[0].degree + 1, len(tmp))):
                    tmp[i].degree -= 1
                    self.edges.append((tmp[0].name, tmp[i].name))
                tmp.pop(0)
                tmp.sort(reverse=True, key=lambda x: x.degree)
                process.append(tmp)
            self.graph_series = self.all_zeros(process[-1])
        else:
            self.graph_series = False

    def set_graph(self):
        if self.graph_series:
            self.graph = nx.Graph()
            self.graph.add_edges_from(self.edges)

    def show(self):
        options = {
            "font_size": 10,
            "node_size": 1600,
            "node_color": 'orange',
            "edgecolors": "black",
            "linewidths": 3,
            "width": 3,
            "with_labels": True
        }
        nx.draw(self.graph, **options)
        plt.show(figsize=(10, 10), dpi=500)

if __name__ == '__main__':
    

    


    print("姓名：展天翔 (ztxtech)")
    print("学号：202321210214")
    print("日期：2024.03.04")
    print("开源代码地址: https://github.com/ztxtech/graph_series_verification")
    print("______________________________________________________________")
    series = input("o(〃^▽^〃)o 请输入一个整数序列: ").split(',')
        
    for i in range(len(series)):
        series[i] = int(series[i])

    print("检测中......................")
    time.sleep(1)
    graph_series = GraphSeries(series)
    print("检测完毕，结果如下：")
    degree = "是" if graph_series.degree_series else "不是"
    print(f"刚刚输入的序列  {degree}  度序列")
    graph = "是" if graph_series.graph_series else "不是"
    print(f"刚刚输入的序列  {graph}  图序列")
    for node in graph_series.series:
        print(f"D({node.name})={node.degree}")
    if graph_series.graph_series:
        print("o(〃^▽^〃)o 我画给你看看吧")
        time.sleep(1)
        graph_series.show()
    input("按任意键退出")
