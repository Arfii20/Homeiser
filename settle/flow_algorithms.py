import settle.flow as flow

class MaxFlow:
    @staticmethod
    def edmunds_karp(graph: flow.FlowGraph, src: flow.Vertex, sink: flow.Vertex) -> int:
        """Returns the max flow between src and sink nodes"""

    @staticmethod
    def augmenting_path(
        graph: flow.FlowGraph, src: flow.Vertex, sink: flow.Vertex
    ) -> list[flow.Vertex]:
        """Returns the shortest path from src -> sink"""

    @staticmethod
    def bottleneck(graph: flow.FlowGraph, path: list[flow.Vertex]) -> int:
        """Returns the bottleneck value from a path specified by a list of vertices"""

    @staticmethod
    def augment_flow(graph: flow.FlowGraph, path: list[flow.Vertex]) -> None:
        """Augments the flow down a path"""

    @staticmethod
    def _bfs(
        graph: flow.FlowGraph, src: flow.Vertex, sink: flow.Vertex
    ) -> list[flow.Vertex]:
        """performs a bfs starting from a src node to a sink node; reconstructs the shortest path
        (in terms of edges traversed) from src to sink and returns it."""

        # store vertices of the graph
        vertices = graph.graph.keys()

        # initialise the visited map with all nodes set to false
        visited: dict[flow.Vertex, bool] = {v: False for v in vertices}

        # initialise the came_from map with all nodes set to None
        came_from: dict[flow.Vertex, flow.Vertex | None] = {v: None for v in vertices}

        # initialise the queue; enqueue src node
        queue: list[flow.Vertex] = [src]

        while queue:
            # dequeue into current; mark current as visited
            current = queue.pop(0)
            visited[current] = True

            # if neighbours haven't been visited, enqueue them and mark them as coming from current
            for neighbour in graph.neighbours(current):
                # move on if we have already visited the neighbour
                if visited[neighbour]:
                    continue

                # otherwise enqueue
                queue.append(neighbour)

                # and mark as coming from current node
                came_from[neighbour] = current

                # can exit early if we have just processed the sink node
                if neighbour == sink:
                    break

        return MaxFlow._path_from_map(came_from)


    @staticmethod
    def _path_from_map(came_from: dict[flow.Vertex, flow.Vertex | None]) -> list[flow.Vertex]:
        ...



class Settle:
    @staticmethod
    def simplify_debt(debt_network: flow.FlowGraph) -> flow.FlowGraph:
        """Returns the debt network, simplified, in graph form"""
