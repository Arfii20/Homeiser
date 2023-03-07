from unittest import TestCase
from settle.flow import *

class TestFlowGraph(TestCase):
    def test_add_vertex(self):
        g = FlowGraph()

        with self.subTest("Blank creation"):
            self.assertEqual(g.graph, {})

        vertex = Vertex(0, 'Alice')
        g.add_vertex(vertex)

        with self.subTest("Check vertex added as expected"):
            self.assertEqual(g.graph, {vertex: []})