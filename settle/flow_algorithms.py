import settle.flow as flow


class MaxFlow:

    @staticmethod
    def edmunds_karp(graph: flow.FlowGraph, src: flow.Vertex, sink: flow.Vertex) -> int:
        """Returns the max flow between src and sink nodes"""


    @staticmethod
    def augmenting_path(graph: flow.FlowGraph, src: flow.Vertex, sink: flow.Vertex) -> list[flow.Vertex]:
        """Returns the shortest path from src -> sink"""

    @staticmethod
    def bottleneck(graph: flow.FlowGraph, path: list[flow.Vertex]) -> int:
        """Returns the bottleneck value from a path specified by a list of vertices"""

    @staticmethod
    def augment_flow(graph: flow.FlowGraph, path: list[flow.Vertex]) -> None:
        """Augments the flow down a path"""

    @staticmethod
    def bfs(graph: flow.FlowGraph, src: flow.Vertex, sink: flow.Vertex) -> list[flow.Vertex]:
        """performs a bfs starting from a src node to a sink node; reconstructs the shortest path
        (in terms of edges traversed) from src to sink and returns it."""


class Settle:
    @staticmethod
    def simplify_debt(debt_network: flow.FlowGraph) -> flow.FlowGraph:
        """Returns the debt network, simplified, in graph form"""
