# Settle

---
## Overview
Part of the application which deals with simplifying chains of debt
Works using the Edmonds-Karp max flow algorithm.

---
## Structures
**Flow Graph**: Weighted digraph with _flow edges_

**Flow Edge**: Has a flow and a capacity. Initialised with `flow`=0, `capacity`=weight of edge. In this context,
the edge weight (and thus capacity of an edge) will be the amount of money owed in a transaction.

**Augmenting path**: A path through the _residual graph_ with unused capacity (`capacity` - `flow` > 0`) from s -> t.
All augmenting paths have a **bottleneck value**. This is the maximum amount of flow that can be pushed through the 
path and is equal to the edge in the path with the smallest unused capacity.

**Residual graph**: The flow graph with _residual edges_. For all edges (s, t) in graph, there exists a _residual edge_
(t, s). Residual edges have a **capacity of 0**. 

---
## Algorithm

Edmonds-Karp is a combination of the Ford-Fulkerson Max Flow algorithm and a Breadth First Search (BFS).

It finds the max flow between a source node, s, and a sink node, t

It works as follows:
* Find an augmenting path through the residual graph
* Augment the flow
* Repeat until no more augmenting paths exist.

### 'Augment the flow'
Augmenting the flow means that we push flow down an augmenting path. For instance, let the graph G = 
A -[0/5]-> B -[0/10]-> C. Of course there exist residual edges for each edge shown. A <-[0/0]- B <-[0/0]- C
There exists and augmenting path A -> B -> C with a bottleneck value of 5. After augmenting
the flow, the graph becomes A -[5/5]-> B -[5/10]-> C. 

When we augment the flow, we also update the flow of all the corresponding edges in the residual graph by augmenting 
with the bottleneck value x -1. Thus, after augmenting the flow the residual edges become A <-[-5/0]- B <-[-5/0]- C.

Notice before augmenting the flow, the unused capacity of all the residual edges were given by 0 - 0 = 0. This means
that they were not valid edges for the algorithm to consider when looking for augmenting paths, as no flow could be 
pushed down the edge. 

After augmenting, the unused capacity becomes 0 - -5 = 5. Hence, the residual edges are now valid paths for the
algorithm to consider when looking for augmenting paths.

### Finding augmenting paths
Edmonds-Karp specifies that paths should be found via a BFS. O(VE^2) - doesn't depend on the max flow of the graph
hence it is considered _strongly polynomial_.

Very standard BFS. Looks for paths between src and sink node.
Only extra constraint is that we only queue the neighbours connected to the current node 
if there is an edge with unused capacity connecting the current node to the neighbour.

e.g. Queue neighbours only if remaining capacity of connecting edge > 0

Residual edges with unused capacity **should** be considered when looking at neighbours to queue.

To reconstruct path need to keep track of where we got to each node from. e.g. if we start at node A and 
next look at node B, then we record {B: A}

### Settling a network of debts
Edmonds-Karp will only find the max flow between two arbitrary nodes on a graph. This is not quite the same as finding
an easy way to settle debts.

A solution which will reduce the edges in a network of debts is as follows:

```python
from dataclasses import dataclass
    

def max_flow(src, sink):
    """Returns max flow from src -> sink. Changes initial graph in place"""


class Vertex: 
    """Class representing vertices in the graph"""


@dataclass
class WeightedDigraph:
    """Class representing the flow graph"""
    graph: dict[Vertex, list[Vertex]]
    def append(self, src, target, flow): ...
    
    def remove_edge(self, src, target): ...
    
    def __iter__(self):
        """returns two nodes at a time e.g. (a, b) on first call then (b, c) on second"""

#     
initial_graph = WeightedDigraph({})
clean_graph = WeightedDigraph({})
for u, v in initial_graph:
    if flow := max_flow(u, v):
        # append an edge to the new graph from u -> v with weight flow if flow > 0
        clean_graph.append(u, v, flow)
        
        # remove edge that has been 'max-flowed'
        initial_graph.remove_edge(u, v)

```