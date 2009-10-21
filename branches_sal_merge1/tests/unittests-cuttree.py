import unittest
import pygraph
from pygraph.classes.graph import graph
from test_data import nations_of_the_world
from pygraph.algorithms.minmax import cut_tree

class test_cuttree(unittest.TestCase):
    
    def test_cuttree0(self):
        G = graph()
        nations_of_the_world(G)
        
        ct = cut_tree( G )
        
        import pdb
        pdb.set_trace()