import numpy as np

from vocabularise import Vocabularise

class Frequentise( object ):

    def frequentise( self, corpus, tokeniser=None, cleanup=None, stem=False ):
        
        V = Vocabularise()
        
        vocabList, adjustedCorpus = V.vocabularise( corpus, tokeniser, cleanup, stem )
        
        wordNumber = len( vocabList )
        
        docNumber = len( adjustedCorpus )
        
        frequencyMatrix = np.zeros( [ wordNumber, docNumber ], dtype=np.int16 )
        
        for i in range( wordNumber ):
            
            word = vocabList[ i ]
            
            for j in range( docNumber ):
                
                doc = adjustedCorpus[ j ]
                
                frequencyMatrix[ i, j ] = sum( [ a == word for a in doc ] )
        
        return vocabList, adjustedCorpus, frequencyMatrix


    def merge( self, vx, vy, mx, my ):

        assert isinstance( mx, np.ndarray )
        assert isinstance( my, np.ndarray )

        if len( vx ) != mx.shape[ 0 ]:
            raise ValueError( 'The number of rows in mx must match the size of vx' )

        if len( vy ) != my.shape[ 0 ]:
            raise ValueError( 'The number of rows in my must match the size of vy' )

        return [], np.zeros( 10 )