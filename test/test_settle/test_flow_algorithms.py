from unittest import TestCase
from settle.flow_algorithms import *


class TestMaxFlow(TestCase):

    def setUp(self) -> None:
        """Build the graph used in my notebook (helpful documentation)"""

        self.vertices = [flow.Vertex(0, 'S')]
        self.vertices += [flow.Vertex(i + 1, label) for i, label in enumerate(['A', 'B', 'C', 'D'])]
        self.vertices.append(flow.Vertex(5, 'T'))

        self.test_graph = flow.FlowGraph(vertices=self.vertices)

        s, a, b, c, d, t = self.vertices

        edges = [(a, 0, 10), (b, 0, 10), (c, 0, 25), (d, 0, 15), (t, 0, 10), (a, 0, 6), (t, 0, 10)]
        srcs = [s, s, a, b, c, d, d]

        for edge, src in zip(edges, srcs):
            self.test_graph.add_edge(edge=flow.Edge(*edge), src=src)

        self.test_graph.draw('max_flow_test')

    def test_edmunds_karp(self):
        ...

    def test_augmenting_path(self):
        ...

    def test_bottleneck(self):
        ...

    def test_augment_flow(self):
        ...

    def test__bfs(self):
        ...

    def test__path_from_map(self):
        ...


class TestSettle(TestCase):
    def test_simplify_debt(self):
        ...
