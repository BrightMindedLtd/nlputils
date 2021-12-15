import unittest

class BaseTestCase( unittest.TestCase ):
    
    def assertUnsortedListEqual( self, list1, list2 ):
        
        return self.assertListEqual( sorted( list1 ), sorted( list2 ) )
