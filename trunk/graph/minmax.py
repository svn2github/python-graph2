# Copyright (c) 2007 Pedro Matiello <pmatiello@gmail.com>
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
Minimization and maximization algorithms for python-graph.
"""


# Module metadata
__authors__ = "Pedro Matiello"
__license__ = "MIT"


# Imports
import graph


# Minimal spanning tree

def minimal_spanning_tree(graph):
	"""
	Minimal spanning tree.

	@attention: Minimal spanning tree meaningful only for weighted graphs.

	@type  graph: graph
	@param graph: Graph.

	@rtype:  list
	@return: Generated spanning tree.
	"""
	visited = []			# List for marking visited and non-visited nodes
	spanning_tree = []		# MInimal Spanning tree

	# Initialization
	for each in graph.get_nodes():
		spanning_tree.append(-1)
	
	# Algorithm loop
	while (1):
		larrow = lighter_arrow(graph, visited)
		if (larrow == (-1, -1)):
			root = first_unvisited(graph, visited)
			if (root >= 0):
				visited.append(root)
			else:
				break
		else:
			spanning_tree[larrow[1]] = larrow[0]
			visited.append(larrow[1])

	return spanning_tree


def first_unvisited(graph, visited):
	"""
	Return first unvisited node.
	
	@type  graph: graph
	@param graph: Graph.

	@type  visited: list
	@param visited: List of nodes.
	
	@rtype:  number
	@return: First unvisited node.
	"""
	for each in graph.get_nodes():
		if (not each in visited):
			return each
	return -1


def lighter_arrow(graph, visited):
	"""
	Return the lighter arrow in graph going from a visited node to an unvisited one.
	
	@type  graph: graph
	@param graph: Graph.

	@type  visited: list
	@param visited: List of nodes.

	@rtype:  tuple
	@return: Lighter arrow (u,v) | u visited, v unvisited.
	"""
	lighter_arrow = (-1, -1)
	weight = -1
	for each in visited:
		for other in graph.get_node(each):
			if (not other in visited):
				w = graph.get_arrow_weight(each, other)
				if (w < weight or weight < 0):
					lighter_arrow = (each, other)
					weight = w
	return lighter_arrow
