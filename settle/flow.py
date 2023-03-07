"""Defines the flow graph structure"""
from dataclasses import dataclass


@dataclass
class Vertex:
    v_id: int
    label: str

    def __hash__(self):
        return hash(f"{self.v_id}{self.label}")


@dataclass
class Edge:
    target: Vertex
    flow: int
    capacity: int

    @property
    def unused_capacity(self) -> int:
        return self.capacity - self.flow

    @property
    def residual(self) -> bool:
        """(Capacity = 0) <=> edge is residual. Thus use capacity to determine if edge residual"""
        return bool(self.capacity)


class FlowGraph:
    """Graph with edges and residual edges. Stored as an adjacency list"""

    def __init__(self, vertices: list[Vertex] = None, graph: dict[Vertex, list[Edge]] = None):  # type: ignore
        """If a list of nodes is passed in, mapping from nodes to empty lists are created.
        If nodes and edges are passed in, builds the graph"""

        # Change type of vertices to an empty list if not provided
        if vertices is None:
            vertices: list[Vertex] = []  # type: ignore

        # If we have been provided with a graph use the graph. If not, generate an empty dict from our list of vertices
        self.graph = graph if graph is not None else {v: [] for v in vertices}

    def add_vertex(self, v: Vertex):
        """Adds a vertex with no edges to the graph"""
        self.graph[v] = []

    def remove_vertex(self, v: Vertex):
        """Removes a vertex, and all of its incoming / outgoing edges from a graph"""

        # remove outgoing by removing

    def add_edge(self, *,  edge: Edge, from_vertex: Vertex, add_residual=True):
        """Adds an edge to the flow graph from a given vertex. Will also add the residual edge by default"""
        self.graph[from_vertex].append(edge)

        if add_residual:

            # create the residual edge going to from_vertex from e.target
            # flow and capacity set to 0 by def. of residual edge
            res = Edge(from_vertex, 0, 0)

            self.graph[edge.target].append(res)


    def remove_edge(self, e: Edge):
        ...

    def neighbours(self, v: Vertex, residual: bool = False) -> list[Edge]:
        ...

    def unused_capacity(self, u: Vertex, v: Vertex, residual: bool = False) -> int:
        """Returns the unused capacity of an edge between two nodes. If there is no edge between the nodes return -1.
        Should also be used as test to see if edge exists"""
