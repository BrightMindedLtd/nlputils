import numpy as np

from frequentise import Frequentise

from vocabularise import Vocabularise

#from nltk.tokenize import word_tokenize

from tests.base_test_case import BaseTestCase

class TestFrequentise( BaseTestCase ):
    
    def setUp( self ):
        
        self.F = Frequentise()

    def testFrequentise( self ):
        
        corpus = [
            "Maybe 'Okay' will be our- 'always'...", 
            "When the world pushes you to your-knees, you're in the perfect position to pray",
        ]
        
        actualVocab, actualAdjustedCorpus, actualMatrix = self.F.frequentise( corpus, tokeniser=None, cleanup=None, stem=False )
                
        expectedVocab = [ 
            "maybe", "'okay", "'", "will", "be", "our-", "'always", "...", "when", "the", "world", "pushes",
            "you", "to", "your-knees", "'re", "in", "perfect", "position", "pray", ","
        ]
        
        self.assertUnsortedListEqual( actualVocab, expectedVocab )
        
        expectedAdjustedCorpus= [
            [ "maybe", "'okay", "'", "will", "be", "our-", "'always", "'", "..."], 
            [ "when", "the", "world", "pushes", "you", "to", "your-knees", ",", "you", "'re", "in", "the",
              "perfect", "position", "to", "pray" ],
        ]
        
        expectedMatrix = np.array( [
            [ 1, 1, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1 ]
            ] ).T
        
        for i in range( 2 ):
            self.assertListEqual( actualAdjustedCorpus[ i ], expectedAdjustedCorpus[ i ] )
        
        actualword2idx = { word: actualVocab.index( word ) for word in actualVocab }
        
        for i, word in enumerate( expectedVocab ):
            
            for j in range(2):
                
                actualidx = actualword2idx[ word ]

            self.assertEqual( actualMatrix[ actualidx, j ], expectedMatrix[ i, j ] )

        tokeniser = Vocabularise.PUNCTUATION_MID_WORD_ONLY
        
        expectedVocab = [ 
            "maybe", "okay", "will", "be", "our", "always", "when", "the", "world", "pushes",
            "you", "to", "your-knees", "you're", "in", "perfect", "position", "pray"
        ]    

        actualVocab, actualAdjustedCorpus, actualMatrix = self.F.frequentise( corpus, tokeniser=tokeniser, cleanup=None, stem=False )

        self.assertUnsortedListEqual( actualVocab, expectedVocab )

        expectedAdjustedCorpus= [
            [ "maybe", "okay", "will", "be", "our", "always" ], 
            [ "when", "the", "world", "pushes", "you", "to", "your-knees", "you're", "in", "the",
              "perfect", "position", "to", "pray" ],
        ]
        
        expectedMatrix = np.array( [
            [ 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1 ]
            ] ).T    

        for i in range( 2 ):
            self.assertListEqual( actualAdjustedCorpus[ i ], expectedAdjustedCorpus[ i ] )
        
        actualword2idx = { word: actualVocab.index( word ) for word in actualVocab }
        
        for i, word in enumerate( expectedVocab ):
            
            for j in range(2):
                
                actualidx = actualword2idx[ word ]

            self.assertEqual( actualMatrix[ actualidx, j ], expectedMatrix[ i, j ] )


    def testMerge( self ):

        # it should raise an exception if the number of rows in M_(xy)
        # differs from the V_(xy) length
        with self.assertRaises( ValueError ):
            self.F.merge( [ 'tony', 'stark', 'is', 'ironman' ], [ 'nat', 'romanoff', 'is', 'blackwidow' ], np.zeros( ( 5, 3 ) ), np.zeros( ( 4, 2 ) ) )

        with self.assertRaises( ValueError ):
            self.F.merge( [ 'tony', 'stark', 'is', 'ironman' ], [ 'nat', 'romanoff', 'is', 'blackwidow' ], np.zeros( ( 4, 3 ) ), np.zeros( ( 5, 2 ) ) )

        # given two vocabularies V_x and V_y and corresponding frequency matrices
        # M_x and M_y, it should return one merged vocabulary V and merged matrix M
        # where V = V_x \cup V_y
        V_x = [ 'quicksilver', 'ironman', 'thor', 'captainamerica', 'spiderman', 'hawkeye', 'scarlet' ]
        V_y = [ 'wolverine', 'quicksilver', 'beast', 'cyclops', 'phoenix' ]

        M_x = np.array( [ [ 8, 10, 20 ], [ 1, 2, 11 ], [ 5, 0, 10 ], [ 0, 2, 1 ], [ 1, 1, 0 ], [ 20, 10, 8 ], [ 1, 1, 1 ] ] ) 
        M_y = np.array( [ [ 5, 3 ], [ 0, 2 ], [ 10, 1 ], [ 21, 23 ], [ 1, 0 ] ] )

        expectedV = [ 'quicksilver', 'ironman', 'thor', 'captainamerica', 'spiderman', 'hawkeye', 'scarlet', 'wolverine', 'beast', 'cyclops', 'phoenix' ]
        expectedM = np.array( [ [ 8, 10, 20, 0, 2 ], [ 1, 2, 11, 0, 0 ], [ 5, 0, 10, 0, 0 ], [ 0, 2, 1, 0, 0 ], [ 1, 1, 0, 0, 0 ], [ 20, 10, 8, 0, 0 ], [ 1, 1, 1, 0, 0 ], [ 0, 0, 0, 5, 3 ], [ 0, 0, 0, 10, 1 ], [ 0, 0, 0, 21, 23 ], [ 0, 0, 0, 1, 0 ] ] )

        V, M = self.F.merge( V_x, V_y, M_x, M_y )

        self.assertUnsortedListEqual( V, expectedV )

        # the rows in M should match the vocabulary indices
        # matrix M should match matrix expectedV 
        
        vidxmap = { word: M[ i ] for i, word in enumerate( V ) }
        
        for idx, word in enumerate( expectedV ):
        
            try:
    		
                np.testing.assert_array_equal( vidxmap[ word ], expectedM[ idx ] )
    		
            except AssertionError as e:
    		
                self.fail( e )
        
        
        
        


