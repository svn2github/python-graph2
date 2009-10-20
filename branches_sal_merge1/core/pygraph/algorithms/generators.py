# Copyright (c) 2008-2009 Pedro Matiello <pmatiello@gmail.com>
#                         Zsolt Haraszti <zsolt@drawwell.net>
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
Random graph generators.

@sort: generate
"""


# Imports
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from random import randint, random


# Generator

def generate(num_nodes, num_edges, directed=False, weight_range=(1, 1)):
    """
    Create a random graph.
    
    @type  num_nodes: number
    @param num_nodes: Number of nodes.
    
    @type  num_edges: number
    @param num_edges: Number of edges.
    
    @type  directed: bool
    @param directed: Whether the generated graph should be directed or not.  

    @type  weight_range: tuple
    @param weight_range: tuple of two integers as lower and upper limits on randomly generated
    weights (uniform distribution).
    """
    # Graph creation
    if directed:
        random_graph = digraph()
    else:
        random_graph = graph()
    
    # Nodes
    nodes = range(num_nodes)
    random_graph.add_nodes(nodes)
    
    # Build a list of all possible edges
    edges = generate_possible_edges(nodes, directed, False)
    
    # Randomize the list
    for i in range(len(edges)):
        r = randint(0, len(edges)-1)
        edges[i], edges[r] = edges[r], edges[i]
    
        # Add edges to the graph
        min_wt = min(weight_range)
        max_wt = max(weight_range)
    for i in range(num_edges):
        each = edges[i]
        random_graph.add_edge(each[0], each[1], wt = randint(min_wt, max_wt))

    return random_graph

def generate_independent_edges(graph, num_nodes, prob_edges, allow_loops=False):
    """
    Generate an Erdos-Renyi random graph. Possible edges are added with 
    a fixed probability.

    @type:  graph: graph
    @param: graph: Graph.

    @type:  num_nodes: number
    @param: num_nodes: Number of nodes.

    @type:  prob_edges: number
    @param: prob_edges: Probability for adding a possible edge.

    @type:  allow_loops: bool
    @param: allow_loops: If set to True, loops can be added. Defaults to False.
    """
    # Discover if graph is directed or not
    directed = isinstance( graph, digraph )

    # Nodes first
    nodes = xrange(num_nodes)
    graph.add_nodes(nodes)
    
    # Build a list of all possible edges
    edges = generate_possible_edges(nodes, directed, allow_loops)

    # Now do a random experiment for every edge and add it in case of success
    for each in edges:
        if random() < prob_edges:
            graph.add_edge(each[0], each[1])
 

def generate_possible_edges(nodes, directed, add_loops=False):
    """
    Generates a list of all possible edges for num_nodes vertices.

    @type:  nodes: list
    @param: nodes: List of nodes.

    @type:  directed: bool
    @param: directed: Flag that specifies if the edges are directed or undirected.

    @type:  add_loops: bool
    @param: add_loops: If set to True, all loops are generated, too. Defaults to False.

    @rtype:  list
    @return: List of all possible edges.
    """
    edges = []
    edges_append = edges.append
    for x in nodes:
        for y in nodes:
            if ((directed and x != y) or (x > y) or (add_loops and x == y)):
                edges_append((x, y))
    return edges 