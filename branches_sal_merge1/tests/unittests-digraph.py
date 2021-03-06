# Copyright (c) Pedro Matiello <pmatiello@gmail.com>
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
Unittests for graph.classes.Digraph
"""


import unittest
import pygraph
from pygraph.algorithms.generators import generate
from pygraph.classes.exceptions import AdditionError
from pygraph.classes.digraph import digraph
import testlib
from copy import copy

class test_digraph(unittest.TestCase):

    # Add/Remove nodes and edges
    
    def test_raise_exception_on_duplicate_node_addition(self):
        gr = digraph()
        gr.add_node('a_node')
        try:
            gr.add_node('a_node')
        except AdditionError:
            pass
        else:
            fail()

    def test_raise_exception_on_duplicate_edge_addition(self):
        gr = digraph()
        gr.add_node('a_node')
        gr.add_node('other_node')
        gr.add_edge("a_node","other_node")
        try:
            gr.add_edge("a_node","other_node")
        except AdditionError:
            pass
        else:
            fail()
    
    def test_raise_exception_when_edge_added_from_non_existing_node(self):
        gr = digraph()
        gr.add_nodes([0,1])
        try:
            gr.add_edge(3,0)
        except KeyError:
            pass
        else:
            fail()
        assert gr.node_neighbors == {0: [], 1: []}
        assert gr.node_incidence == {0: [], 1: []}
    
    def test_raise_exception_when_edge_added_to_non_existing_node(self):
        gr = digraph()
        gr.add_nodes([0,1])
        try:
            gr.add_edge(0,3)
        except KeyError:
            pass
        else:
            fail()
        assert gr.node_neighbors == {0: [], 1: []}
        assert gr.node_incidence == {0: [], 1: []}
    
    def test_remove_node(self):
        gr = testlib.new_digraph()
        gr.del_node(0)
        self.assertTrue(0 not in gr)
        for each, other in gr.edges():
            self.assertTrue(each in gr)
            self.assertTrue(other in gr)
    
    def test_remove_edge_from_node_to_same_node(self):
        gr = digraph()
        gr.add_node(0)
        gr.add_edge(0, 0)
        gr.del_edge(0, 0)
    
    def test_remove_node_with_edge_to_itself(self):
        gr = digraph()
        gr.add_node(0)
        gr.add_edge(0, 0)
        gr.del_node(0)

    
    # Invert graph
    
    def test_invert_digraph(self):
        gr = testlib.new_digraph()
        inv = gr.inverse()
        for each in gr.edges():
            self.assertTrue(each not in inv.edges())
        for each in inv.edges():
            self.assertTrue(each not in gr.edges())
    
    def test_invert_empty_digraph(self):
        gr = digraph()
        inv = gr.inverse()
        self.assertTrue(gr.nodes() == [])
        self.assertTrue(gr.edges() == [])
    
    
    # Reverse graph
    def test_reverse_digraph(self):
        gr = testlib.new_digraph()
        rev = gr.reverse()
        for (u, v) in gr.edges():
            self.assertTrue((v, u) in rev.edges())
        for (u, v) in rev.edges():
            self.assertTrue((v, u) in gr.edges())
    
    def test_invert_empty_digraph(self):
        gr = digraph()
        rev = gr.reverse()
        self.assertTrue(rev.nodes() == [])
        self.assertTrue(rev.edges() == [])
    
    # Complete graph
    
    def test_complete_digraph(self):
        gr = digraph()
        gr.add_nodes(range(10))
        gr.complete()
        for i in range(10):
            for j in range(10):
                self.assertTrue((i, j) in gr.edges() or i == j)
    
    def test_complete_empty_digraph(self):
        gr = digraph()
        gr.complete()
        self.assertTrue(gr.nodes() == [])
        self.assertTrue(gr.edges() == [])
    
    def test_complete_digraph_with_one_node(self):
        gr = digraph()
        gr.add_node(0)
        gr.complete()
        self.assertTrue(gr.nodes() == [0])
        self.assertTrue(gr.edges() == [])
    
    
    # Add graph
    
    def test_add_digraph(self):
        gr1 = testlib.new_digraph()
        gr2 = testlib.new_digraph()
        gr1.add_graph(gr2)
        for each in gr2.nodes():
            self.assertTrue(each in gr1)
        for each in gr2.edges():
            self.assertTrue(each in gr1.edges())
    
    def test_add_empty_digraph(self):
        gr1 = testlib.new_digraph()
        gr1c = copy(gr1)
        gr2 = digraph()
        gr1.add_graph(gr2)
        self.assertTrue(gr1.nodes() == gr1c.nodes())
        self.assertTrue(gr1.edges() == gr1c.edges())
    
    
    # Add spanning tree
    
    def test_add_spanning_tree(self):
        gr = digraph()
        st = {0: None, 1: 0, 2:0, 3: 1, 4: 2, 5: 3}
        gr.add_spanning_tree(st)
        for each in st:
            self.assertTrue((st[each], each) in gr.edges() or (each, st[each]) == (0, None))

    def test_add_empty_spanning_tree(self):
        gr = digraph()
        st = {}
        gr.add_spanning_tree(st)
        self.assertTrue(gr.nodes() == [])
        self.assertTrue(gr.edges() == [])

if __name__ == "__main__":
    unittest.main()