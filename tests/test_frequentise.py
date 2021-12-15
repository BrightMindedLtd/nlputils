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
            
            

        regex = Vocabularise.PUNCTUATION_MID_WORD_ONLY
        
       
        # expectedVocab = [ 
        #     "maybe", "okay", "will", "be", "our", "always", "when", "the", "world", "pushes",
        #     "you", "to", "your-knees", "you're", "in", "perfect", "position", "pray"
        # ]    

            
            