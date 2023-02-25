"""Defines the flow graph structure"""
from dataclasses import dataclass


class Vertex: ...


@dataclass
class Edge: ...


class FlowGraph:
    """Graph with edges and residual edges. Stored as an adjacency list"""

    def __init__(self, vertices: list[Vertex] = None, edges: list[Edge] = None):  # type: ignore
        """If a list of nodes is passed in, mapping from nodes to empty lists are created.
        If nodes and edges are passed in, builds the graph"""

        # Change type of vertices to an empty list if not provided
        if vertices is None:
            vertices: list[Vertex] = []  # type: ignore

        # Change type of vertices to an empty list if not provided
        if edges is None:
            edges: list[Edge] = []  # type: ignore

        # build empty adjacency graph
        self.graph: dict[Vertex, list[Edge]] = {v: [] for v in vertices}

        # add edges
        for e in edges:
            self.add_edge(e)

    def add_vertex(self, v: Vertex): ...

    def remove_vertex(self, v: Vertex): ...

    def add_edge(self, e: Edge): ...

    def remove_edge(self, e: Edge): ...

    def neighbours(self, v: Vertex) -> list[Edge]: ...

    def edge_between(self, u: Vertex, v: Vertex, residual: bool = False) -> bool: ...
