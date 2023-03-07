from unittest import TestCase
from settle.flow import *


class TestFlowGraph(TestCase):
    def setUp(self) -> None:
        """create a blank test graph with three nodes: {A, B, C}

        A -[10]-> B -[5]-> C
        |                  ^
        |                  |
        --------[15]--------

        also create a blank graph to test things like adding nodes, adding edges etc.

        """

        self.a = Vertex(0, "A")
        self.b = Vertex(1, "B")
        self.c = Vertex(2, "C")
        self.d = Vertex(3, "D")

        self.vertices = [self.a, self.b, self.c, self.d]

        self.graph = FlowGraph(vertices=self.vertices)

        self.test_graph = FlowGraph(vertices=self.vertices)

        # add edges to the graph only between a, b, c; leave d unconnected
        self.test_graph.add_edge(edge=Edge(self.b, 0, 10), from_vertex=self.a)
        self.test_graph.add_edge(edge=Edge(self.c, 0, 5), from_vertex=self.b)
        self.test_graph.add_edge(edge=Edge(self.c, 0, 15), from_vertex=self.a)


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
            # compare graph dict keys with list of vertices (ignore edges)
            self.assertEqual([v for v in self.graph.graph.keys()], self.vertices)

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

    def test_unused_capacity(self):
        """Checks that edge detection works, and that we return the correct unused capacities where they do exist"""

        labels = ["A -[0/10]-> B", "B -[0/0]-> A (res=True)", "B -[0/0]-> A (res=False)", "A --X--> D"]
        cases = [(self.a, self.b), (self.b, self.a, True), (self.b, self.a, False), (self.a, self.d)]
        expected = [10, 0, -1, -1]

        for label, case, exp in zip(labels, cases, expected):
            with self.subTest(label):
                self.assertEqual(self.test_graph.unused_capacity(*case), exp)

        # test that we throw an error when we


    def test_remove_vertex(self):
        ...
