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
    
    
    
            
        # docNumx = M_x.shape[ 0 ]
        
        # docNumy = M_y.shape[ 0 ]
        
        # for i, word in enumerate( V ):
            
        #     if word in V_x:
                
        #         rowV_x = M_x[ V_x.index( word ) ]
                
        #     else:
                
        #         rowV_x = np.zeros( [ 1, docNumx ] )
            
        #     if word in V_y:
                
        #         rowV_y = M_y[ V_y.index( word ) ]
                
        #     else:
                
        #         rowV_y = np.zeros( [ 1, docNumy ] )
        
        #     expectedRow = np.hstack( ( rowV_x, rowV_y ) )
        
        #     try:
    		
        #         np.testing.assert_array_equal( M[ i ], expectedRow )
    		
        #     except AssertionError as e:
    		
        #         self.fail( e )