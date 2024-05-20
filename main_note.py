from copy import deepcopy
import time

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx

import numpy as np


class Node:
    """
    节点类，用于表示图中的节点。
    
    Attributes:
        name (str): 节点的名称。
        degree (int): 节点的度。
    """
    def __init__(self, name, degree):
        self.name = name
        self.degree = degree


class GraphSeries:
    """
    图序列类，用于处理和分析图序列数据。
    
    Attributes:
        series (list): 排序后的节点列表，节点的度降序排列。
        degree_series (bool): 标记是否为度序列。
        graph_series (bool): 标记是否为图序列。
        edges (list): 图中的边列表。
        graph (nx.Graph): 图对象。
    """
    def __init__(self, series):
        """
        初始化图序列对象。
        
        Args:
            series (list): 输入的图序列数据，每个元素为节点的度。
        """
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
        """
        检查序列中所有节点的度是否都为正数。
        
        Args:
            series (list): 节点列表，每个元素为节点的度。
        
        Returns:
            bool: 如果所有节点的度都为正数，则返回True；否则返回False。
        """
        return bool((np.array([x.degree for x in series]) >= 0).all())

    @staticmethod
    def all_zeros(series):
        """
        检查序列中所有节点的度是否都为零。
        
        Args:
            series (list): 节点列表，每个元素为节点的度。
        
        Returns:
            bool: 如果所有节点的度都为零，则返回True；否则返回False。
        """
        return bool((np.array([x.degree for x in series]) == 0).all())

    def is_degree_series(self):
        """
        判断输入序列是否为度序列。
        
        根据度序列的定义（节点度之和为偶数），判断输入序列是否满足条件。
        """
        if not self.degree_series:
            self.degree_series = not bool(sum([i.degree for i in self.series]) % 2)

    def is_graph_series(self):
        """
        判断输入的度序列是否能构成图序列。
        
        根据图序列的定义，检查是否满足构造图序列的条件：
        1. 所有节点的度都非负；
        2. 最大节点度小于节点总数；
        3. 能通过连线将节点的度减至0，且不形成回路。
        
        Returns:
            bool: 如果满足条件，则返回True；否则返回False。
        """
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
        """
        根据图序列构建图对象。
        
        如果图序列有效，则创建一个无向图，并添加边。
        """
        if self.graph_series:
            self.graph = nx.Graph()
            self.graph.add_edges_from(self.edges)

    def show(self):
        """
        展示构建的图。
        
        使用Matplotlib和NetworkX绘制图，并显示。
        """
        options = {
            "font_size": 10,
            "node_size": 160,
            "node_color": 'orange',
            "edgecolors": "black",
            "with_labels": True,
            "pos": nx.circular_layout(self.graph)
        }
        matplotlib.use('TkAgg')
        nx.draw(self.graph, **options)
        plt.show()

if __name__ == '__main__':


    print("姓名：ztxtech")
    print("学号：XXXXXXXXXXXXXXXX")
    print("日期：2024.03.04")
    print("开源代码地址: https://github.com/ztxtech/graph_series_verification")
    print("______________________________________________________________")
    series = input("o(〃^▽^〃)o 请输入一个整数序列\n !!!!!!以英文逗号 ,  分隔: ").split(',')
        
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