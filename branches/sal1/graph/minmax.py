# Copyright (c) 2007-2008 Pedro Matiello <pmatiello@gmail.com>
#                         Rhys Ulerich <rhys.ulerich@gmail.com>
#                         Roy Smith <roy@panix.com>
#                         Salim Fadhley <sal@stodge.org>
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

@sort: heuristic_search, minimal_spanning_tree, shortest_path, _first_unvisited, _lightest_edge,
_reconstruct_path
"""


# Imports
from utils import priority_queue


# Minimal spanning tree

def minimal_spanning_tree(graph, root=None):
	"""
	Minimal spanning tree.

	@attention: Minimal spanning tree meaningful only for weighted graphs.

	@type  graph: graph
	@param graph: Graph.
	
	@type  root: node
	@param root: Optional root node (will explore only root's connected component)

	@rtype:  dictionary
	@return: Generated spanning tree.
	"""
	visited = []			# List for marking visited and non-visited nodes
	spanning_tree = {}		# MInimal Spanning tree

	# Initialization
	if (root is not None):
		visited.append(root)
		nroot = root
		spanning_tree[root] = None
	else:
		nroot = 1
	
	# Algorithm loop
	while (nroot is not None):
		ledge = _lightest_edge(graph, visited)
		if (ledge == (-1, -1)):
			if (root is not None):
				break
			nroot = _first_unvisited(graph, visited)
			if (nroot is not None):
				spanning_tree[nroot] = None
			visited.append(nroot)
		else:
			spanning_tree[ledge[1]] = ledge[0]
			visited.append(ledge[1])

	return spanning_tree


def _first_unvisited(graph, visited):
	"""
	Return first unvisited node.
	
	@type  graph: graph
	@param graph: Graph.

	@type  visited: list
	@param visited: List of nodes.
	
	@rtype:  node
	@return: First unvisited node.
	"""
	for each in graph:
		if (each not in visited):
			return each
	return None


def _lightest_edge(graph, visited):
	"""
	Return the lightest edge in graph going from a visited node to an unvisited one.
	
	@type  graph: graph
	@param graph: Graph.

	@type  visited: list
	@param visited: List of nodes.

	@rtype:  tuple
	@return: Lightest edge in graph going from a visited node to an unvisited one.
	"""
	lightest_edge = (-1, -1)
	weight = -1
	for each in visited:
		for other in graph[each]:
			if (other not in visited):
				w = graph.get_edge_weight(each, other)
				if (w < weight or weight < 0):
					lightest_edge = (each, other)
					weight = w
	return lightest_edge


# Shortest Path
# Code donated by Rhys Ulerich

def shortest_path(graph, source):
	"""
	Return the shortest path distance between source and all other nodes using Dijkstra's algorithm.
	
	@attention: All weights must be nonnegative.

	@type  graph: graph
	@param graph: Graph.

	@type  source: node
	@param source: Node from which to start the search.

	@rtype:  tuple
	@return: A tuple containing two dictionaries, each keyed by target nodes.
		1. Shortest path spanning tree
		2. Shortest distance from given source to each target node
	Inaccessible target nodes do not appear in either dictionary.
	"""
	# Initialization
	dist	 = { source: 0 }
	previous = { source: None}
	q = graph.nodes()

	# Algorithm loop
	while q:
		# examine_min process performed using O(nodes) pass here.
		# May be improved using another examine_min data structure.
		u = q[0]
		for node in q[1:]:
			if ((not dist.has_key(u)) 
				or (dist.has_key(node) and dist[node] < dist[u])):
				u = node
		q.remove(u)

		# Process reachable, remaining nodes from u
		if (dist.has_key(u)):
			for v in graph[u]:
				if v in q:
					alt = dist[u] + graph.get_edge_weight(u, v)
					if (not dist.has_key(v)) or (alt < dist[v]):
						dist[v] = alt
						previous[v] = u

	return previous, dist


def heuristic_search(G, start, goal, heuristic):
	"""
	A* search algorithm.
	
	@type G: graph
	@param G: Graph
	
	@type start: node
	@param start: Start node
	
	@type goal: node
	@param goal: Goal node
	
	@type heuristic: function
	@param heuristic: Heuristic function
	
	@rtype: list
	@return: Optimized path from start to goal node 
	"""
	# Nodes (fixes) already evaluated
	closed_set = set()
	
	# Nodes (fixes) which still (tentatively) need to be evaluated
	open_set = priority_queue([start])

	# Actual shortest path from start to any given fix
	g = {start: 0}
	
	# A log of nodes and their parents
	p = {start:None}

	while not open_set.empty():
		current = open_set.pop()
		if current == goal:
			path =  [a for a in _reconstruct_path( goal, p )]
			path.reverse()
			return path
			
		# We have not found the goal
		closed_set.add(current)
		for neighbor in G.neighbors(current):

			# The cost of getting to neighbor is the cost of geting to current
			# plust the cost of getting from current to neighbor.
			
			cost = g[current] + G.get_edge_weight(current, neighbor)
			
			if (neighbor in open_set) and (cost < g[neighbor]):
				# Throw away this node because we already have a faster way to get there.
				open_set.discard(neighbor)
				
			if (neighbor in closed_set) and (cost < g[neighbor]):
				# Throw away this node because we already rejected it.
				closed_set.discard(neighbor)
				
			if neighbor not in open_set and neighbor not in closed_set:
				# Store the cost of getting here.
				g[neighbor] = cost
				
				# Estimate the usefulness of this node - the cost of getting to it
				# plus an esitmate of the cost of getting from it to the goal.				
				priority = cost + heuristic(neighbor, goal)
				
				# Schedule it to be investigated later.
				open_set.insert(neighbor, priority)
				
				# Log how we got to this node so that we can re-construct the journey later.
				p[neighbor] = current


def _reconstruct_path( node , parents ):
	yield node
	while True:
		node = parents[ node ]
		if node == None:
			break
		yield node