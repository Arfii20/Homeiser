from unittest import TestCase

from settle.flow_algorithms import *


class TestMaxFlow(TestCase):
    def setUp(self) -> None:
        """Build the graph used in my notebook (helpful documentation)"""

        self.vertices = [flow.Vertex(0, "S")]
        self.vertices += [
            flow.Vertex(i + 1, label) for i, label in enumerate(["A", "B", "C", "D"])
        ]
        self.vertices.append(flow.Vertex(5, "T"))

        self.test_graph = flow.FlowGraph(vertices=self.vertices)

        s, a, b, c, d, t = self.vertices

        edges = [
            (b, 0, 10),
            (a, 0, 10),
            (c, 0, 25),
            (d, 0, 15),
            (t, 0, 10),
            (a, 0, 6),
            (t, 0, 10),
        ]
        srcs = [s, s, a, b, c, d, d]

        for edge, src in zip(edges, srcs):
            self.test_graph.add_edge(edge=flow.Edge(*edge), src=src)

        # self.test_graph.draw("max_flow_test")

    def test_edmunds_karp(self):
        s, a, b, c, d, t = self.vertices

        karp = MaxFlow.edmunds_karp(self.test_graph, s, t)
        self.assertEqual(20, karp)

    def test_bottleneck(self):
        s, a, b, c, d, t = self.vertices

        self.assertEqual(MaxFlow.bottleneck(self.test_graph, [s, a, c, t]), 10)

    def test_augment_flow(self):
        """This test is very much in the wrong place but that's okay"""
        s, a, b, c, d, t = self.vertices

        path = [s, a, c, t]
        self.test_graph.augment_flow(
            [s, a, c, t], MaxFlow.bottleneck(self.test_graph, path)
        )

        # test that flow through relevant edges is 10
        flows = [self.test_graph.get_edge(u, v).flow for u, v in zip(path, path[1:])]

        # check that every item in the list is 10 (the bottleneck for the path)
        self.assertEqual(flows.count(10), len(flows))

    def test__bfs(self):
        s, a, b, c, d, t = self.vertices

        exp = [s, a, c, t]
        actual = MaxFlow._bfs(self.test_graph, s, t)

        self.assertEqual(exp, actual)

    def test__path_from_map(self):
        s, a, b, c, d, t = self.vertices

        test_map: dict[flow.Vertex, flow.Vertex | None] = {
            s: None,
            a: d,
            b: s,
            c: None,
            d: b,
            t: None,
        }

        # check that an empty path is returned when nothing points to the sink node
        with self.subTest("Invalid map - nothing pointing to sink node"):
            got = MaxFlow._path_from_map(test_map, src=s, sink=t)
            self.assertFalse(got)

        # fix the map
        test_map[t] = d

        with self.subTest("Build map"):
            self.assertEqual(
                MaxFlow._path_from_map(test_map, src=s, sink=t), [s, b, d, t]
            )

        # break the path and make sure an error is raised
        test_map[b] = None

        with self.subTest("Path broken midway through"), self.assertRaises(PathError):
            MaxFlow._path_from_map(test_map, src=s, sink=t)


class TestSettle(TestCase):
    def test_simplify_debt(self):
        """Test debt simplification on simple test graph

        Alice owes Bob $5
        Bob owes Charlie $5
        Alice owes Charlie $10

        Thus, Bob can be 'settled out' of transaction leaving Alice owes Charlie $15

        """

        # generate vertices for each person in example
        vertices = [
            flow.Vertex(0, "Alice"),
            flow.Vertex(1, "Bob"),
            flow.Vertex(2, "Charlie"),
        ]
        a, b, c = vertices

        # build graph
        debt = flow.FlowGraph(vertices=vertices)

        # add edges
        debt.add_edge(edge=flow.Edge(b, 0, 10), src=a)
        debt.add_edge(edge=flow.Edge(b, 0, 5), src=c)
        debt.add_edge(edge=flow.Edge(c, 0, 5), src=a)
        debt.draw("pre-settle", subdir="test_settle")
        settled = Settle.simplify_debt(debt)
        settled.draw("post-settled", subdir="test_settle")

        exp = {
            flow.Vertex(v_id=0, label="Alice"): [
                flow.Edge(target=flow.Vertex(v_id=1, label="Bob"), flow=0, capacity=15)
            ],
            flow.Vertex(v_id=1, label="Bob"): [
                flow.Edge(target=flow.Vertex(v_id=0, label="Alice"), flow=0, capacity=0)
            ],
            flow.Vertex(v_id=2, label="Charlie"): [],
        }

        self.assertEqual(exp, settled.graph)

    def test_simplify_debt_no_simplifications(self):
        """Raise an error when no simplifications take place"""

        vertices = [flow.Vertex(0, "Alice"), flow.Vertex(1, "Bob")]
        debt = flow.FlowGraph(vertices=vertices)
        debt.add_edge(edge=flow.Edge(vertices[1], 0, 5), src=vertices[0])

        with self.assertRaises(NoSimplification):
            Settle.simplify_debt(debt)
