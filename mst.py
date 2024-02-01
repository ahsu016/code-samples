# Algorithm I: MST (with priority queue implementation)
# edges is adjacency list representation of a weighted, undirected graph with a minimum of one node

def mst(edges):
        
    # initial vertex
        
    init_vertex = 0

    # number of vertices in the graph
    total = len(edges)

    # a list to keep track of the vertices that have been traversed. Boolean TRUE/FALSE for whether the vertex has been traversed
    traversed = [False] * total

    # a list to store output
    output_list  = [[] for i in range(total)] 

    # set initial vertex to traversed
    traversed[init_vertex] = True

    # priority queue
    prio_q = []

    # # # weight list
    # # weights = []
    # # dead code, tried to make an edge a pair with source / destination vertices and
    # # a separate list of weights, but it was too much and too inefficient

    # for containing edges of the vertex, which checks adjacent vertices
    for adjacent_vertex, weight in edges[init_vertex]:
        prio_q.append((weight, init_vertex, adjacent_vertex))

    def min_adj_edge(queue):
        # set minimum weight to largest value
        min_weight = float('inf')
        # set minimum edge to none
        min_edge = None
        # for each edge, find the minimum weight adjacent edge
        for edge in queue:
            # source is for current vertex, dest is for destination vertex; together with weight
            # the two vertices represent an edge
            weight, source, dest = edge
            # if weight of current edge is less than the minimum you have checked for
            if weight < min_weight:
                # set the minimum to the current edge's weight
                min_weight = weight
                min_edge = edge
        # return edge with minimum weight of current vertex
        return min_edge
        
    # execute above functions; find current vertex's edge with minimum weight
    # for every vertex in the graph (as represented by a priority queue)
    while prio_q:
        minimum_edge = min_adj_edge(prio_q)
        prio_q.remove(minimum_edge)
        weight, source, dest = minimum_edge

        # set the destination vertex to TRUE in the Boolean traversal checker list
        if not(traversed[dest]):
            traversed[dest] = True
            # add to output list
            output_list[source].append([dest, weight])
            output_list[dest].append([source, weight])
            # for the new vertex, add all untraversed edges to priority queue
            for adj_v, weight in edges[dest]:
                if not traversed[adj_v]:
                    prio_q.append((weight, dest, adj_v))
        
    # check if the graph is connected; the minimum spanning tree contains every vertex
    if all(traversed):
        return output_list
    # else return minimum spanning forest, will automatically be 'None' because graph is unconnected
    else:
        return None

# initialize sample input graph

edges = [

[[1, 3], [2, 5]],
[[0, 3], [2, 10], [3, 12]],
[[0, 5], [1, 10]],
[[1, 12]]
    
]

mst_print = mst(edges)
print(mst_print)