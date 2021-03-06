import unittest

import graph

from test_data import nations_of_the_world

class testAStar( unittest.TestCase ):
    """
    Test some very basic graph functions
    """
    
    def setUp(self):
        self.G = graph.graph()
        nations_of_the_world(self.G)
        
    def testBasic1(self):
        """
        Test some very basic functionality
        """
        englands_neighbors = self.G.neighbors("England")
        assert set(['Wales', 'Scotland', 'France', 'Ireland']) == set( englands_neighbors )
        
    def testAStar1(self):
        heuristic = graph.heuristics.chow( "Wales", "North Korea", "Russia" )
        heuristic.optimize( self.G )
        result = graph.minmax.heuristic_search( self.G, "England", "India", heuristic )
        
        
                