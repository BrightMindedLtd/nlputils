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
        
        wordNumx, docNumx = mx.shape
        wordNumy, docNumy = my.shape
        
        vxdict = { word:idx for idx, word in enumerate( vx ) }
        vydict = { word:idx for idx, word in enumerate( vy ) }
        
        assert isinstance( mx, np.ndarray )
        assert isinstance( my, np.ndarray )

        if len( vx ) != wordNumx:
            raise ValueError( 'The number of rows in mx must match the size of vx' )

        if len( vy ) != wordNumy:
            raise ValueError( 'The number of rows in my must match the size of vy' )

        combinedV = list( set( vx + vy ) )

        mergedMatrix = np.zeros( [ len( combinedV ), docNumx + docNumy ] )
        
        for idx, word in enumerate( combinedV ):
            
            if word in vxdict:
                
                mergedMatrix[ idx, :docNumx ] += mx[ vxdict[ word ] ]

            if word in vydict:
                
                mergedMatrix[ idx, docNumx: ] += my[ vydict[ word ] ]
                
                
                
        print("vx:", vx)
        print("vy:", vy)  
        print( "combined:", combinedV )
        
        print("mx:", mx)
        print("my:", my)
        print( "Merged:", mergedMatrix )
        
        return combinedV, mergedMatrix
    
    
    