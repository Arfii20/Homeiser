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

        self.blank_graph = FlowGraph(vertices=self.vertices)

        self.test_graph = FlowGraph(vertices=self.vertices)

        # add edges to the graph only between a, b, c; leave d unconnected
        self.test_graph.add_edge(edge=Edge(self.b, 0, 10), src=self.a)
        self.test_graph.add_edge(edge=Edge(self.c, 0, 5), src=self.b)
        self.test_graph.add_edge(edge=Edge(self.c, 0, 15), src=self.a)

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
            self.assertEqual([v for v in self.blank_graph.graph.keys()], self.vertices)

    def test_add_edge(self):
        """Checks that adding an edge works"""

        # add edge:  A -[0/10]-> B
        edge = Edge(self.b, 0, 10)
        res_edge = Edge(self.a, 0, 0)
        self.blank_graph.add_edge(edge=edge, src=self.a)

        # check to see if the edge has been added properly
        with self.subTest("Edge added"):
            self.assertEqual(self.blank_graph.graph[self.a], [edge])

        # Check residual edge
        with self.subTest("Residual edge added"):
            self.assertEqual(self.blank_graph.graph[self.b], [res_edge])

    def test_unused_capacity(self):
        """Checks that edge detection works, and that we return the correct unused capacities where they do exist"""

        labels = [
            "A -[0/10]-> B",
            "B -[0/0]-> A (res=True)",
            "B -[0/0]-> A (res=False)",
            "A --X--> D",
        ]
        cases = [
            (self.a, self.b),
            (self.b, self.a, True),
            (self.b, self.a, False),
            (self.a, self.d),
        ]
        expected = [10, 0, -1, -1]

        for label, case, exp in zip(labels, cases, expected):
            with self.subTest(label):
                self.assertEqual(self.test_graph.unused_capacity(*case), exp)

        # test that we throw an error when we have two-way edges, and when we have two edges from u -> t

        # set up test table
        labels = [
            "A -[0/10]-> B, A -[0/5]-> B",
            "B <-[0/10]-> C (b, a)",
            "B <-[0/10]-> C (a, b)",
        ]

        cases = [(self.a, self.b), (self.b, self.c, True), (self.c, self.b, True)]

        A, B, C, D = self.vertices

        # set up blank graph fit test case structure
        self.blank_graph.add_edge(edge=Edge(B, 0, 10), src=A)
        self.blank_graph.add_edge(edge=Edge(B, 0, 5), src=A)

        self.blank_graph.add_edge(edge=Edge(C, 0, 10), src=B)
        self.blank_graph.add_edge(edge=Edge(B, 0, 10), src=C)

        for label, case in zip(labels, cases):
            with self.subTest(case), self.assertRaises(FlowGraphError):
                self.blank_graph.unused_capacity(*case)

    def test_remove_vertex(self):

        self.test_graph.remove_vertex(self.b)
        self.test_graph.remove_vertex(self.d)

        self.assertEqual({self.a: [Edge(self.c, 0, 15)],
                          self.c: [Edge(self.a, 0, 0)]},
                         self.test_graph.graph)

    def test_remove_edge(self):
        A, B, C, D = self.vertices
        self.blank_graph.add_edge(edge=Edge(B, 0, 10), src=A)

        with self.subTest("Edge exists"):
            self.assertEqual(10, self.blank_graph.unused_capacity(A, B))

        self.blank_graph.remove_edge(src=A, target=B)

        with self.subTest("Edge exists"):
            self.assertEqual(-1, self.blank_graph.unused_capacity(A, B))
            self.assertEqual(-1, self.blank_graph.unused_capacity(B, A, residual=True))
