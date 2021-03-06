# Copyright (c) 2008-2009 Pedro Matiello <pmatiello@gmail.com>
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


"""
Cycle detection algorithms.

@sort: find_cycle
"""


# Imports
import pygraph
from pygraph.classes.Exceptions import InvalidGraphType
from pygraph.classes.Digraph import digraph
from pygraph.classes.Graph import graph

def find_cycle(G):
    """
    Find a cycle in the given graph.
    
    This function will return a list of nodes which form a cycle in the graph or an empty list if
    no cycle exists.
    
    @type graph: graph, digraph
    @param graph: Graph.
    
    @rtype: list
    @return: List of nodes. 
    """
    
    if (type(G) == graph):
        directed = False
    elif (type(G) == digraph):
        directed = True
    else:
        raise InvalidGraphType

    def find_cycle_to_ancestor(node, ancestor):
        """
        Find a cycle containing both node and ancestor.
        """
        path = []
        orignode = node
        while (node != ancestor):
            if (node is None):
                return []
            path.append(node)
            node = spanning_tree[node]
        path.append(node)
        path.reverse()
        return path
    
    def dfs(node):
        """
        Depht-first search subfunction.
        """
        visited[node] = 1
        # Explore recursively the connected component
        for each in G[node]:
            if (cycle):
                return
            if (each not in visited):
                spanning_tree[each] = node
                dfs(each)
            else:
                if (directed or spanning_tree[node] is not each):
                    cycle.extend(find_cycle_to_ancestor(node, each))

    visited = {}              # List for marking visited and non-visited nodes
    spanning_tree = {}        # Spanning tree
    cycle = []

    # Algorithm outer-loop
    for each in G:
        # Select a non-visited node
        if (each not in visited):
            spanning_tree[each] = None
            root = each
            # Explore node's connected component
            dfs(each)
            if (cycle):
                return cycle

    return []
