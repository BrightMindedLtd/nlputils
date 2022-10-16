import numpy as np
import pickle
from datetime import datetime
import time 

from nlp.vocabularise import Vocabularise

class Frequentise( object ):
    """
    A class used to simultaneously turn a corpus of documents into a
    cleaned up vocabulary list, an appropriately adjusted corpus, and a
    frequency matrix.  It can also be used to merge two frequency matrices
    (and their appropriate vocabulary lists) into a single frequency matrix
    (and its appropriate vocabulary list).

    Methods
    -------
    frequentise( corpus, tokeniser=None, cleanup=None, stem=False )
        Turn a corpus of documents into a cleaned up vocabulary list, an
        appropriately adjusted corpus, and a frequency matrix
    
    merge( vx, vy, mx, my )
        Merges two frequency matrices (and their appropriate vocabulary
        lists) into a single frequency matrix (and its appropriate vocabulary
        list)
    
    saveMergedFiles( vocabList, adjustedCorpus, frequencyMatrix, filename=None )
        Saves the passed files to the local directory
        
    loadFile( filename )
        Loads a pickled file from the local directory
    """
    
    def frequentise( self, corpus, V=None, tokeniser=None, cleanup=None, stem=False ):
        """Turn a corpus of documents into a cleaned up vocabulary list, an
        appropriately adjusted corpus, and a frequency matrix.

        This method creates the vocabulary from the corpus unless V is specified.
        
        If V is specified, it is assumed that every token in the corpus exists in V.

        If tokeniser is not passed, the nltk.tokenize tokenizer
        word_tokenize is used to tokenise instead.
        
        If cleanup is not passed, no cleanup is performed.
        
        If stem is not passed, no stemming is performed.        

        Parameters
        ----------
        corpus : lst
            A list of documents, each of which is a string.
        V: lst
            A list of words constituting a pre-specifed vocabulary
        tokeniser : str
            The regular expression to tokenise with
        cleanup : str
            The regular expression to cleanup with
        stem : bool
            Stemming is performed if and only if this boolean
            is True

        Returns
        -------
        lst
            a list of cleaned up words with no repetitions. If V was specified
            then V is returned here
        lst
            A list of documents, each of which is a list of words found
            in vocabList
        numpy.ndarray
            A V x D matrix, where V is the number of words in the new 
            vocabulary list and D is the number of documents in the corpus.
            The [ i, j ] entry of this matrix is the number of times the i'th
            word of the new vocabulary list appears in the j'th document of the
            new corpus.
        """
        vize = Vocabularise()
        vocabList = V

        if not vocabList:
            vocabList, adjustedCorpus = vize.vocabularise( corpus, tokeniser, cleanup, stem )
        else:
            adjustedCorpus = [ vize.tokensCleanup( vize.tokenise( doc ), regex=None ) for doc in corpus ]

        wordNumber = len( vocabList )
        docNumber = len( adjustedCorpus )
        frequencyMatrix = np.zeros( [ wordNumber, docNumber ], dtype=np.int16 )

        vidx = { w:idx for idx, w in enumerate( vocabList) }

        for j in range( docNumber ):
            x = np.zeros( wordNumber, dtype=np.int16 )

            for w in adjustedCorpus[ j ]:
                try:
                    idx = vidx[ w ]
                    x[ idx ] += 1
                except:
                    continue

            frequencyMatrix[ :,j ] += x

        return vocabList, adjustedCorpus, frequencyMatrix


    def merge( self, vx, vy, mx, my ):
        """Merges two frequency matrices (and their appropriate vocabulary
        lists) into a single frequency matrix (and its appropriate vocabulary
        list)
        
        Parameters
        ----------
        vx : lst
            The first list of words
        vy : lst
            The second list of words
        mx : numpy.ndarray
            A frequency matrix, whose rows are indexed by vx
        my : numpy.ndarray
            A frequency matrix, whose rows are indexed by vy

        Raises
        ------
        ValueError
            If either the number of rows in mx doesn't match the length of
            vx or the number of rows in my doesn't match the length of
            vy

        Returns
        -------
        lst
            a list of all words in vx and vy with no
            repetitions
        numpy.ndarray
            A V x D matrix, where V is the number of words in the new 
            vocabulary list and D is the number of documents in the new
            combined corpus. The [ i, j ] entry of this matrix is the number
            of times the i'th word of the new vocabulary list appears in the
            j'th document of the new corpus.
        """
        
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
                        
        return combinedV, mergedMatrix
    
    def saveMergedFiles( self, vocabList, adjustedCorpus, frequencyMatrix ):
        """Saves the vocab list, adjusted corpus, and frequency matrix
        to the local directory
        
        Parameters
        ----------
        vocabList : lst
            A list of words to be saved
        adjustedCorpus : lst
            A list of documents to be saved
        frequencyMatrix : numpy.ndarray
            The frequency matrix to be saved
        """

        files = [ vocabList, adjustedCorpus, frequencyMatrix ]
        
        default_names = [ 'vocabulary_list_', 'adjusted_corpus', 'frequencyMatrix' ]
        
        dateTimeObj = datetime.now()
        
        for file, default_name in zip( files, default_names ):
            
            filename = str( default_name + dateTimeObj.strftime( "%d-%b-%Y-%H-%M" ) + '.PKL' ) 
   
        with open( filename, 'wb' ) as outfile:
            pickle.dump( file, outfile )
        
    def loadFile( self, filename ):
        """Loads a pickled file from the passed local directory location.
        
        Parameters
        ----------
        filename : str
            The locationf of the file to be loaded

        Returns
        -------
        lst
            the loaded file
        """
        
        with ( open( filename, "rb" ) ) as infile:
            return pickle.load( infile )
