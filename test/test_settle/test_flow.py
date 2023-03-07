from unittest import TestCase
from settle.flow import *


class TestFlowGraph(TestCase):

    def setUp(self) -> None:
        """create a blank test graph with three nodes: {A, B, C}

        A --> B --> C
        |           ^
        |           |
        -------------

        """

        self.a = Vertex(0, 'A')
        self.b = Vertex(1, 'B')
        self.c = Vertex(2, 'C')

        self.vertices = [self.a, self.b, self.c]

        self.graph = FlowGraph(vertices=self.vertices)



    def test_add_vertex(self):
        g = FlowGraph()

        with self.subTest("Blank creation"):
            self.assertEqual(g.graph, {})

        vertex = Vertex(0, "Alice")
        g.add_vertex(vertex)

        with self.subTest("Check vertex added as expected"):
            self.assertEqual(g.graph, {vertex: []})

        # also test that the test graph had its vertices added correctly
        with self.subTest("Check test graph"):
            self.assertEqual(self.graph.graph, {v: [] for v in self.vertices})

    def test_add_edge(self):
        """Checks that adding an edge works"""

        # add edge:  A -[0/10]-> B
        edge = Edge(self.b, 0, 10)
        res_edge = Edge(self.a, 0, 0)
        self.graph.add_edge(edge=edge, from_vertex=self.a)

        # check to see if the edge has been added properly
        with self.subTest("Edge added"):
            self.assertEqual(self.graph.graph[self.a], [edge])

        # Check residual edge
        with self.subTest("Residual edge added"):
            self.assertEqual(self.graph.graph[self.b], [res_edge])

    def test_remove_vertex(self): ...

