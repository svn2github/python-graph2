# Copyright (c) 2007-2008 Pedro Matiello <pmatiello@gmail.com>
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
Set of heuristics to be used with A*.
"""


# Imports
import math
import warnings


# Edmond Chow's heuristic
class chow(object):
	"""
	An implementation of the graph searching heuristic proposed by Edmond Chow.

	For details, check: http://www.edmondchow.com/pubs/levdiff-aaai.pdf 
	"""
	
	def __init__(self, *centers):
		"""
		Initialize a Chow heuristic object.
		"""
		self.centers = centers
		self.nodes = {}
		
	def optimize(self, graph):
		"""
		Build a dictionary mapping any node to a chow sequence for that node.
		"""		
		for center in self.centers:
			shortest_routes = graph.shortest_path(center)[1]
			for node, weight in shortest_routes.items():
				self.nodes.setdefault(node, []).append(weight)
		
	def __call__(self, start, end):
		"""
		Estimate how far start is from end.
		"""
		assert len( self.nodes.keys() ) > 0, "You need to optimize this heuristic for your graph before it can be used to estimate."
				
		cmp_sequence = zip( self.nodes[start], self.nodes[end] )
		chow_number = max( abs( a-b ) for a,b in cmp_sequence )
		return chow_number


# Heuristic for Euclidean graphs
class euclidean(object):
	"""
	A heuristic for Euclidean graphs.
	"""
	
	def __init__(self, *centers):
		"""
		Initialize the heuristic object.
		"""
		self.distances = {}
		
	def optimize(self, graph):
		"""
		Build a dictionary mapping each pair of nodes to a number (the distance between them).
		"""
		for start in graph.nodes():
			for end in graph.nodes():
				start_attr = graph.get_node_attributes(start)
				for each in start_attr:
					if (each[0] == 'position'):
						start_attr = each[1]
						break
				end_attr = graph.get_node_attributes(end)
				for each in end_attr:
					if (each[0] == 'position'):
						end_attr = each[1]
						break
				dist = 0
				for i in xrange(len(start_attr)):
					dist = dist + (float(start_attr[i]) - float(end_attr[i]))**2
				self.distances[(start,end)] = dist
		
	def __call__(self, start, end):
		"""
		Estimate how far start is from end.
		"""
		assert len(self.distances.keys()) > 0, "You need to optimize this heuristic for your graph before it can be used to estimate."
				
		return self.distances[(start,end)]