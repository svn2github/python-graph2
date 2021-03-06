# Copyright (c) 2007-2008 Pedro Matiello <pmatiello@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
import heapq
import logging

log = logging.getLogger( __name__ )

"""
Search algorithms.

@sort: breadth_first_search, depth_first_search, _bfs, _dfs
"""

# Depth-first search

def depth_first_search(graph, root=None):
    """
    Depth-first search.

    @type  graph: graph
    @param graph: Graph.
    
    @type  root: node
    @param root: Optional root node (will explore only root's connected component)

    @rtype:  tuple
    @return: A tupple containing a dictionary and two lists:
        1. Generated spanning tree
        2. Graph's preordering
        3. Graph's postordering
    """

    def dfs(node):
        """
        Depht-first search subfunction.
        """
        visited[node] = 1
        pre.append(node)
        # Explore recursively the connected component
        for each in graph[node]:
            if (each not in visited):
                spanning_tree[each] = node
                dfs(each)
        post.append(node)

    visited = {}            # List for marking visited and non-visited nodes
    spanning_tree = {}        # Spanning tree
    pre = []                # Graph's preordering
    post = []                # Graph's postordering

    # DFS from one node only
    if (root is not None):
        spanning_tree[root] = None
        dfs(root)
        return spanning_tree, pre, post
    
    # Algorithm loop
    for each in graph:
        # Select a non-visited node
        if (each not in visited):
            spanning_tree[each] = None
            # Explore node's connected component
            dfs(each)

    return spanning_tree, pre, post


# Breadth-first search

def breadth_first_search(graph, root=None):
    """
    Breadth-first search.

    @type  graph: graph
    @param graph: Graph.

    @type  root: node
    @param root: Optional root node (will explore only root's connected component)

    @rtype:  tuple
    @return: A tuple containing a dictionary and a list.
        1. Generated spanning tree
        2. Graph's level-based ordering
    """

    def bfs():
        """
        Breadth-first search subfunction.
        """
        while (queue != []):
            node = queue.pop(0)
    
            for other in graph[node]:
                if (other not in spanning_tree):
                    queue.append(other)
                    ordering.append(other)
                    spanning_tree[other] = node

    queue = []            # Visiting queue
    spanning_tree = {}    # Spanning tree
    ordering = []

    # BFS from one node only
    if (root is not None):
        queue.append(root)
        ordering.append(root)
        spanning_tree[root] = None
        bfs()
        return spanning_tree, ordering

    # Algorithm
    for each in graph:
        if (each not in spanning_tree):
            queue.append(each)
            ordering.append(each)
            spanning_tree[each] = None
            bfs()

    return spanning_tree, ordering


                
def filtered_breadth_first_search(graph, root, filter=None ):
    """
    Breadth-first search with optional filtering implemented as a generator-function. 
    Use Case: Find all the nodes connected to root which meet a filter-criteria in ascending-cost order.

    @type  graph: graph
    @param graph: Graph.
    
    @type  root: node
    @param root: Root node (will explore only root's connected component)
    
    @type filter: function
    @param filter: A function which takes the arguments (cost, node) and must
    return either True or False. If the function returns False then the node is
    excluded from the output and any of it's children (except those which are
    queued because they are connected to another node) are ignored.
    
    @rtype:  iterator
    @return: Each iterator will produce a tuple of (int cost, nodevalue)
    """
    if filter == None:
        filter = lambda *n: True
    
    assert callable( filter ), "Filter should be callable, got %s" % repr( filter )
    visited = set()
    queue = []

    if filter( 0, root ):
        # Even the root of the search must pass the filter test.
        heapq.heappush( queue, ( 0, root ) )

    while queue:
        cost, current = heapq.heappop( queue )
        visited.add( current )
        
        yield cost, current

        new_nodes = set( graph[ current ] ) - visited

        for neighbor in new_nodes:
            new_cost = cost + graph.get_edge_weight( current , neighbor )
            
            if filter( new_cost, neighbor ):    
                if  not neighbor in [ q[1] for q in queue ]:
                    heapq.heappush( queue, (new_cost, neighbor) )
            else:
                # Ensure that we do not bother with that node in future.
                visited.add( neighbor )
        
