# Copyright (c) 2008-2009 Pedro Matiello <pmatiello@gmail.com>
#                         Christian Muise <christian.muise@gmail.com>
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
Hypergraph class
"""


# Imports
from pygraph.classes.graph import graph
#from pygraph.algorithms import *
from pygraph.algorithms import accessibility
from pygraph.classes.exceptions import AdditionError

class hypergraph (object):
    """
    Hypergraph class.
    
    Hypergraphs are a generalization of graphs where an edge (called hyperedge) can connect more
    than two nodes.
    
    @sort: __init__, __len__, __str__, add_hyperedge, add_hyperedges, add_node, add_nodes,
    has_node, hyperedges, link, links, nodes, unlink, accessibility, connected_components,
    cut_hyperedges, cut_nodes
    """


    def __init__(self):
        """
        Initialize a hypergraph.
        """
        self.node_links = {}    # Pairing: Node -> Hyperedge
        self.edge_links = {}     # Pairing: Hyperedge -> Node
        self.graph = graph()    # Ordinary graph


    def __str__(self):
        """
        Return a string representing the hypergraph when requested by str() (or print).

        @rtype:  string
        @return: String representing the hypergraph.
        """
        return "<hypergraph object " + str(self.nodes()) + " " + str(self.edge_links) + ">"


    def __len__(self):
        """
        Return the size of the hypergraph when requested by len().

        @rtype:  number
        @return: Size of the hypergraph.
        """
        return len(self.node_links)
    
    
    def __iter__(self):
        """
        Return a iterator passing through all nodes in the hypergraph.
        
        @rtype:  iterator
        @return: Iterator passing through all nodes in the hypergraph.
        """
        for each in self.node_links.keys():
            yield each


    def __getitem__(self, node):
        """
        Return a iterator passing through all neighbors of the given node.
        
        @rtype:  iterator
        @return: Iterator passing through all neighbors of the given node.
        """
        for each in self.neighbors(node):
            yield each


    def nodes(self):
        """
        Return node list.
        
        @rtype:  list
        @return: Node list.
        """
        return list(self.node_links.keys())


    def hyperedges(self):
        """
        Return hyperedge list.

        @rtype:  list
        @return: List of hyperedges linked to the given node.
        """
        return list(self.edge_links.keys())


    def links(self, obj):
        """
        Return all nodes connected by the given hyperedge.
        
        @type  obj: hyperedge
        @param obj: Object identifier.
        
        @rtype:  list
        @return: List of node objects linked to the given hyperedge.
        """
        return self.edge_links[obj]
    
    
    def neighbors(self, obj):
        """
        Return all neighbors adjacent to the given node.
        
        @type  obj: node
        @param obj: Object identifier.
        
        @rtype:  list
        @return: List of all node objects adjacent to the given node.
        """
        neighbors = set([])
        
        for e in self.node_links[obj]:
            neighbors.update(set(self.edge_links[e]))
        
        return neighbors - set([obj])


    def has_node(self, node):
        """
        Return whether the requested node exists.

        @type  node: node
        @param node: Node identifier

        @rtype:  boolean
        @return: Truth-value for node existence.
        """
        return node in self.node_links


    def add_node(self, node):
        """
        Add given node to the hypergraph.
        
        @attention: While nodes can be of any type, it's strongly recommended to use only numbers
        and single-line strings as node identifiers if you intend to use write().

        @type  node: node
        @param node: Node identifier.
        """
        if (not node in self.node_links):
            self.node_links[node] = []
            self.graph.add_node((node,'n'))
        else:
            raise AdditionError("Node %s already in graph" % node)
    
    
    def del_node(self, node):
        """
        Delete a given node from the hypergraph.
        
        @type  node: node
        @param node: Node identifier.
        """
        if self.has_node(node):
            for e in self.node_links[node]:
                self.edge_links[e].remove(node)

            self.node_links.pop(node)
            self.graph.del_node((node,'n'))


    def add_nodes(self, nodelist):
        """
        Add given nodes to the hypergraph.
        
        @attention: While nodes can be of any type, it's strongly recommended to use only numbers
        and single-line strings as node identifiers if you intend to use write().

        @type  nodelist: list
        @param nodelist: List of nodes to be added to the graph.
        """
        for each in nodelist:
            self.add_node(each)


    def add_hyperedge(self, hyperedge):
        """
        Add given hyperedge to the hypergraph.

        @attention: While hyperedge-nodes can be of any type, it's strongly recommended to use only
        numbers and single-line strings as node identifiers if you intend to use write().
        
        @type  hyperedge: hyperedge
        @param hyperedge: Hyperedge identifier.
        """
        if (not hyperedge in self.edge_links):
            self.edge_links[hyperedge] = []
            self.graph.add_node((hyperedge,'h'))


    def add_hyperedges(self, edgelist):
        """
        Add given hyperedges to the hypergraph.

        @attention: While hyperedge-nodes can be of any type, it's strongly recommended to use only
        numbers and single-line strings as node identifiers if you intend to use write().
        
        @type  edgelist: list
        @param edgelist: List of hyperedge-nodes to be added to the graph.
        """
        for each in edgelist:
            self.add_hyperedge(each)


    def link(self, node, hyperedge):
        """
        Link given node and hyperedge.

        @type  node: node
        @param node: Node.

        @type  hyperedge: node
        @param hyperedge: Hyperedge.
        """
        if (hyperedge not in self.node_links[node]):
            self.edge_links[hyperedge].append(node)
            self.node_links[node].append(hyperedge)
            self.graph.add_edge((node,'n'), (hyperedge,'h'))
        else:
            raise AdditionError("Link (%s, %s) already in graph" % (node, hyperedge))


    def unlink(self, node, hyperedge):
        """
        Unlink given node and hyperedge.

        @type  node: node
        @param node: Node.

        @type  hyperedge: hyperedge
        @param hyperedge: Hyperedge.
        """
        self.node_links[node].remove(hyperedge)
        self.edge_links[hyperedge].remove(node)


    def accessibility(self):
        """
        Accessibility matrix (transitive closure).

        @rtype:  dictionary
        @return: Accessibility information for each node.
        """
        access_ = accessibility.accessibility(self.graph)
        access = {}
        
        for each in list(access_.keys()):
            if (each[1] == 'n'):
                access[each[0]] = []
                for other in access_[each]:
                    if (other[1] == 'n'):
                        access[each[0]].append(other[0])
        
        return access

    
    def cut_nodes(self):
        """
        Return the cut-nodes of the given hypergraph.
        
        @rtype:  list
        @return: List of cut-nodes.
        """
        cut_nodes_ = accessibility.cut_nodes(self.graph)
        cut_nodes = []
        
        for each in cut_nodes_:
            if (each[1] == 'n'):
                cut_nodes.append(each[0])
        
        return cut_nodes


    def cut_hyperedges(self):
        """
        Return the cut-hyperedges of the given hypergraph.
        
        @rtype:  list
        @return: List of cut-nodes.
        """
        cut_nodes_ = accessibility.cut_nodes(self.graph)
        cut_nodes = []
        
        for each in cut_nodes_:
            if (each[1] == 'h'):
                cut_nodes.append(each[0])
        
        return cut_nodes
        
    def rank(self):
        """
        Return the rank of the given hypergraph.
        
        @rtype:  int
        @return: Rank of graph.
        """
        max_rank = 0
        
        for each in self.hyperedges():
            if len(self.edge_links[each]) > max_rank:
                max_rank = len(self.edge_links[each])
                
        return max_rank
