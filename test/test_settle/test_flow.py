from unittest import TestCase
from settle.flow import *


class TestEdge(TestCase):
    def test_push_flow(self):
        edge = Edge(Vertex(0, "A"), 0, 5)

        edge.push_flow(2)

        with self.subTest("push flow"):
            self.assertEqual(edge.unused_capacity, 3)

        with self.subTest("Trigger Overflow"), self.assertRaises(OverFlowError):
            edge.push_flow(4)


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

        # Check that adding another edge with the same src/dest adds to flow and capacity
        self.blank_graph.add_edge(edge=Edge(self.b, 5, 5), src=self.a)

        modified_edge = self.blank_graph.get_edge(self.a, self.b)

        labels = ["Flow", "Capacity"]
        cases = [modified_edge.flow, modified_edge.capacity]
        expected = [5, 15]

        for label, case, exp in zip(labels, cases, expected):
            with self.subTest(label):
                self.assertEqual(case, exp)

        # try and add an edge going in the opposite direction
        with self.subTest("Block 2 way edge"), self.assertRaises(FlowGraphError):
            self.blank_graph.add_edge(edge=Edge(self.a, 5, 5), src=self.b)

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

    def test_remove_vertex(self):
        self.test_graph.remove_vertex(self.b)
        self.test_graph.remove_vertex(self.d)

        self.assertEqual(
            {self.a: [Edge(self.c, 0, 15)], self.c: [Edge(self.a, 0, 0)]},
            self.test_graph.graph,
        )

    def test_remove_edge(self):
        A, B, C, D = self.vertices
        self.blank_graph.add_edge(edge=Edge(B, 0, 10), src=A)

        with self.subTest("Edge exists"):
            self.assertEqual(10, self.blank_graph.unused_capacity(A, B))

        self.blank_graph.remove_edge(src=A, target=B)

        with self.subTest("Edge exists"):
            self.assertEqual(-1, self.blank_graph.unused_capacity(A, B))
            self.assertEqual(-1, self.blank_graph.unused_capacity(B, A, residual=True))

    def test_prune_edges(self):
        """Push 15 units of flow along the edge a --[0/15]--> c and prune
        Make sure A->B and B-> C still exist, and that a --> c (or its residual edge)
         no longer exists"""

        a, b, c, d = self.vertices

        # push flow and prune graph
        self.test_graph.augment_flow([a, c], 15)
        self.test_graph.draw('a-15_15_c', dir_ext='test_prune_edges')
        self.test_graph.prune_edges()
        self.test_graph.draw('pruned', dir_ext='test_prune_edges')

        # configure test table to run 4 tests above
        tests = ["A->C removed", "C->A (residual) removed", "A->B exists", "B->C exists"]
        cases = [(a, c), (c, a, True), (a, b), (b, c)]
        expected = [-1, -1, 10, 5]

        # run tests

        for test, case, exp in zip(tests, cases, expected):
            with self.subTest(test):
                self.assertEqual(self.test_graph.unused_capacity(*case), exp)


    def test_draw(self):
        self.test_graph.draw(filename="test")
