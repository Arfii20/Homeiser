"""Defines the flow graph structure"""
from __future__ import annotations

import copy
from dataclasses import dataclass
from os import getcwd
from typing import Callable

import graphviz  # type: ignore


class FlowGraphError(Exception):
    ...


class EdgeNotFoundError(Exception):
    ...


class OverFlowError(Exception):
    ...


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
        return not bool(self.capacity)

    @property
    def saturated(self) -> bool:
        """Edges are saturated where the unused capacity of an edge is 0"""
        return not self.unused_capacity

    def push_flow(self, flow: int):
        """Pushes flow down an edge"""

        if flow > self.unused_capacity:
            raise OverFlowError(
                f"Tried to push {flow} units down an edge with an unused capacity of "
                f"{self.unused_capacity}"
            )

        else:
            self.flow += flow


class FlowGraph:
    """Graph with edges and residual edges. Stored as an adjacency list.

    ASSUMPTION: Flow graph shouldn't have a two-way edge between two nodes. e.g. a <--> b is not allowed
    """

    def __init__(self, vertices: list[Vertex] = None, graph: dict[Vertex, list[Edge]] = None):  # type: ignore
        """If a list of nodes is passed in, mapping from nodes to empty lists are created.
        If nodes and edges are passed in, builds the graph"""

        # Change type of vertices to an empty list if not provided
        if vertices is None:
            vertices: list[Vertex] = []  # type: ignore

        # If we have been provided with a graph use the graph. If not, generate an empty dict from our list of vertices
        self.graph = graph if graph is not None else {v: [] for v in vertices}

    def __eq__(self, other: FlowGraph) -> bool:
        return self.graph == other.graph

    def add_vertex(self, v: Vertex):
        """Adds a vertex with no edges to the graph"""
        self.graph[v] = []

    def augment_flow(self, path: list[Vertex], flow: int):
        for u, v in zip(path, path[1:]):
            for edge in self.graph[u]:
                if edge.target == v:
                    edge.push_flow(flow)

            for edge in self.graph[v]:
                if edge.target == u:
                    edge.push_flow(-1 * flow)

    def remove_vertex(self, v: Vertex):
        """Removes a vertex, and all of its incoming / outgoing edges from a graph"""

        # delete all edges which have v listed as the target
        for src in self.graph.keys():
            # skip the vertex we are deleting as we cannot have edges from v -> v
            if src == v:
                continue

            # if an edge exists between vertex and v, delete it
            if self.unused_capacity(src, v) != -1:
                self.remove_edge(src=src, target=v)

        # delete all outgoing edges via the remove_edge method s.th. residual edges are removed
        edges_from_v = self.graph[v].copy()
        for edge in edges_from_v:
            self.remove_edge(src=v, target=edge.target)

        # pop node from graph
        self.graph.pop(v)

    def add_edge(self, *, edge: Edge, src: Vertex, add_residual=True):
        """Adds an edge to the flow graph from a given vertex. Will also add the residual edge by default"""

        # append edge to the list if the edge doesn't exist
        if self.unused_capacity(src, edge.target) == -1:
            self.graph[src].append(edge)
        else:
            present_edge = self.get_edge(src, edge.target)
            self.remove_edge(src=src, target=present_edge.target)
            self.add_edge(
                src=src,
                edge=Edge(
                    edge.target,
                    edge.flow + present_edge.flow,
                    edge.capacity + present_edge.capacity,
                ),
            )

        # if we add an edge going opposite the edge that already exists throw an error
        # this should be cleaned **before**
        if len(
            [
                edge_
                for edge_ in self.graph[edge.target]
                if (edge_.target == src) and not edge_.residual
            ]
        ):
            raise FlowGraphError("Edge going in two directions")

        if add_residual:
            # create the residual edge going to from_vertex from e.target
            # flow and capacity set to 0 by def. of residual edge
            res = Edge(src, 0, 0)

            self.graph[edge.target].append(res)

    def remove_edge(self, *, src: Vertex, target: Vertex):
        """Removes an edge given it exists. Can only remove edges that exist. Residual edges removed automatically"""
        # make sure edge exists
        if self.unused_capacity(src, target) == -1:
            raise FlowGraphError(
                "Tried to delete edge which doesn't exist - maybe you are trying to delete a "
                "residual edge?"
            )

        # delete edge
        self.graph[src].remove(self.get_edge(src, target))

        # delete residual edge
        self.graph[target].remove(self.get_edge(target, src, True))

    def neighbours(self, current: Vertex) -> list[Vertex]:
        """Returns the neighbours of the current node
        All nodes which can be accessed by an edge (residual or not) will be
        """

        return [
            neighbouring_edge.target
            for neighbouring_edge in self.graph[current]
            if neighbouring_edge.unused_capacity != -1
            and not neighbouring_edge.saturated
        ]

    def unused_capacity(self, u: Vertex, v: Vertex, residual: bool = False) -> int:
        """Returns the unused capacity of an edge between two nodes. If there is no edge between the nodes return -1.
        Should also be used as test to see if edge exists.

        When residual flag is set to false only non-residual edges will be returned. e.g. if a --[-1/0]-> exists,
        but residual = false then -1 will be returned
        """

        try:
            unused_cap = self.get_edge(u, v, residual).unused_capacity
        except EdgeNotFoundError:
            unused_cap = -1

        return unused_cap

    def get_edge(self, u: Vertex, v: Vertex, residual=False) -> Edge:
        """Returns the edge object given a src and a target node. Will return residual edges by default.
        Will raise an EdgeNotFound error if there is no edge between u and v"""

        # use list comprehensions to pick out edges where target == v

        # results in either a list of length 0 (where no edge exists)
        # or a list of length 1 (in which one edge exists)

        if residual:
            uv_edge: list[Edge] = [edge for edge in self.graph[u] if edge.target == v]
        else:
            uv_edge: list[Edge] = [  # type: ignore
                edge for edge in self.graph[u] if edge.target == v and not edge.residual
            ]

        if len(uv_edge) == 0:
            raise EdgeNotFoundError
        else:
            return uv_edge[0]

    def operate_on_edge(self, u: Vertex, v: Vertex, fn: Callable, *args, **kwargs):
        [fn(edge, *args, **kwargs) for edge in self.graph[u] if edge.target == v]

    def prune_edges(self):
        """Replace edges in graph with an edge of flow 0, capacity of unused capacity"""

        # create deep copy of original graph structure so we can change graph while pruning
        items = copy.deepcopy([(k, v) for k, v in self.graph.items()])

        # for every edge in the graph
        for node, edges in items:
            for edge in edges:
                # self.draw("intra-settle", subdir='test_settle')

                # skip residual edges
                if edge.residual:
                    continue

                # remove the edge
                self.remove_edge(src=node, target=edge.target)

                # if the edge isn't saturated add an edge back to the graph with flow=0,
                # and capacity=old_edge.unused_capacity
                if edge.saturated:
                    continue
                else:
                    self.add_edge(
                        edge=Edge(edge.target, 0, edge.unused_capacity), src=node
                    )

    def draw(self, filename="out", *, subdir="", res=True):
        dot = graphviz.Digraph(comment="Flow Graph")

        # create nodes
        [dot.node(f"{v.v_id}", v.label) for v in self.graph.keys()]

        # add normal edges in black, residual edges in red
        for src, target_edges in self.graph.items():
            for target_edge in target_edges:
                if not target_edge.residual:
                    dot.edge(
                        str(src.v_id),
                        str(target_edge.target.v_id),
                        label=f"{f'{target_edge.flow} / {target_edge.capacity}' if res else f'{target_edge.capacity}'}",
                    )
                elif res:
                    dot.edge(
                        str(src.v_id),
                        str(target_edge.target.v_id),
                        label=f"{target_edge.flow} / {target_edge.capacity}",
                        color="red",
                        fontcolor="red",
                    )

        print(dot.source)
        dot.render(
            filename=f"{filename}",
            directory=f"{getcwd()}/renders{'/' + subdir if subdir else ''}",
            format="svg",
        )
