import re
import pickle
from datetime import datetime

from stop_words import get_stop_words

from nltk.stem.porter import PorterStemmer

from nltk.tokenize import word_tokenize, RegexpTokenizer

from tqdm import tqdm

class Vocabularise( object ):
    """
    A class used to turn a collection of documents into
    an appropriately cleaned up vocabulary list.  Can also
    be used to save and load vocabularies, as well as
    merging multiple vocabularies.

     Attributes
     ----------
    PUNCTUATION_MID_WORD_ONLY : str
        A regular expression that can be passed to the 
        tokeniser. This regular expression removes all 
        punctiation that isn't surronded by letters
    _stemmer : nltk.stem.porter.PorterStemmer
        The default Porter stemmer
    
    Methods
    -------
    stopWordsFilter( word )
        Static method that returns True unless word is in the 
        stop words list get_stop_words( 'en' )
    
    tokenise( text, regex=None )
        Tokenises a piece of text using the passed regular
        expression
        
    tokenCleanup( dirtyWord, regex )
        Takes a single word and cleans it up based on the 
        passed regular expression

    tokensCleanup( dirtyDoc, regex )
        Cleans up a list of words, applying 
        tokenCleanup( dirtyWord, regex ) to each one
        
    stem( doc )
        Takes a list of words and returns them stemmed, in
        the same order.  Also returns a map with stems as
        keys, and the list of words that stemmed to the key
        as values
    
    mergeVocabularies( vocab1, vocab2 )
        Takes two lists of words and merges them into a single
        list with no repetitions
        
    mergeStemMaps( stemMap1, stemMap2 )
        Takes two stem maps and merges them into a single stem
        map
    
    filter( vocab, *args )
        Takes a vocabulary list and a number of supplied filters,
        and filters the vocabulary of any words in any of the
        filters
    
    vocabularise( corpus, tokeniser=None, cleanup=None, stem=False )
        Takes a corpus of documents and returns the cleaned up
        vocabulary list, as well as the new corpus with all words 
        from the new voabulary
        
    saveVocabulary( vocab, filename=None )
        Saves the vocab list to the local directory
        
    loadVocabulary( filename )
        Loads a pickled vocabulary list from the local directory
    """
    
    # This regex removes all punctuation not surrounded by letters.
    PUNCTUATION_MID_WORD_ONLY = r"([\w]+(?:(?!\s)\W?[\w]+)*)"
    
    @staticmethod
    def stopWordsFilter( word ):
        """Returns True unless word is in the stop words list 
        get_stop_words( 'en' ), in which case it returns False
            
        Parameters
        ----------
        word : str
            The word which may need to be filtered
        
        Returns
        -------
        bool
            A boolean that is True unless word is in the list
            get_stop_words( 'en' ), in which case it is False                
    
        """
        
        return not word in get_stop_words( 'en' )
    
    def __init__( self ):

        self._stemmer = PorterStemmer()

    def tokenise( self, text, regex=None ):
        """Tokenises a piece of text using the passed regular
        expression
        
        If the argument 'regex' isn't passed in, the nltk.tokenize
        tokenizer word_tokenize is used to tokenise instead.
        
        Parameters
        ----------
        text : str
            The text to be tokenised
        regex : str, optional
            The regular expression to tokenise with
            
        Returns
        -------
        list
            a list of strings that are the tokenised words
        """
        
        if regex:
            tokeniser = RegexpTokenizer( regex )

            return tokeniser.tokenize( text )
        
        return word_tokenize( text )

    def tokenCleanup( self, dirtyWord, regex ):
        """Cleans up a single word based on the passed regular
        expression.  Removes the first instance of the matched
        pattern found.
            
        If the argument 'regex' isn't passed in, the word is
        returned unchanged.
        
        Parameters
        ----------
        dirtyWord : str
            The word to be cleaned up
        regex : str
            The regular expression to clean up with
            
        Returns
        -------
        str
            the cleaned up word
        """
        
        if not regex:
        
            return dirtyWord
        
        return re.sub( regex, "", dirtyWord )


    def tokensCleanup( self, dirtyList, regex ):
        """Cleans up a list of words, applying 
        tokenCleanup( dirtyWord, regex ) to each one
        
        Parameters
        ----------
        dirtyList : lst
            A list of strings to be cleaned up
        regex : str
            The regular expression to clean up with
            
        Returns
        -------
        lst
            the list of cleaned up words        
        """
        
        result = [ self.tokenCleanup( token, regex ) for token in dirtyList ]

        return [ token for token in result if token ]

    def stem( self, docList ):
        """Takes a list of words and returns them stemmed, in
        the same order.  Also returns a map with stems as
        keys, and the list of words that stemmed to the key
        as values.  The stemmer used is self._stemmer.
        
        Parameters
        ----------
        docList : lst
            A tokenised document.

        Returns
        -------
        lst
            the document where all words have been stemmed
        dict
            a map with stemmed words as keys, and a list of
            words that stemmed to that key as values
        """

        stem2word = {}

        stemmedDoc = []

        for word in docList:

            stem = self._stemmer.stem( word )

            stemmedDoc.append( stem )

            if stem not in stem2word:

                stem2word[ stem ] = []

            if word not in stem2word[ stem ]:
                
                stem2word[ stem ].append( word )

        return stemmedDoc, stem2word

    def mergeVocabularies( self, vocab1, vocab2 ):
        """Takes two lists of words and merges them into a single
        list with no repetitions

        Parameters
        ----------
        vocab1 : lst
            The first list of words
        vocab2 : lst
            The second list of words

        Returns
        -------
        lst
            a list of all words in vocab1 and vocab2 with no
            repetitions
        """
        
        return list( set ( vocab1 + vocab2 ) )
    
    def mergeStemMaps( self, stemMap1, stemMap2 ):
        """Takes two stem maps and merges them into a single stem
        map       

        Parameters
        ----------
        stemMap1 : dict
            The first stem map
        stemMap2 : dict
            The second stem map

        Returns
        -------
        dict
            the combined stem map
        """
        
        combinedMap = { **stemMap1, **stemMap2 }
        
        for key, value in stemMap1.items():
            
            combinedMap[ key ] = list( set( combinedMap[ key ] + value ) )
             
        return combinedMap

    def filter( self, vocab, *args ):
        """Takes a vocabulary list and a number of supplied filters,
        and filters the vocabulary of any words in any of the
        filters

        If no filters are supplied, it filters using the method
        stopWordsFilter().   

        Parameters
        ----------
        vocab : lst
            A list of words to be filtered
        *args : function
            A variable number of functions, each of which is a
            word filter

        Raises
        ------
        ValueError
            If any of the passed filters are not callable functions

        Returns
        -------
        lst
            the vocab lst with all filtered words removed
        """
        
        if not args:
            
            return list( filter( Vocabularise.stopWordsFilter, vocab ) )
        
        for filterFunction in args:
          
            if not callable( filterFunction ):
                
                raise ValueError( "All filters must be functions" )
                
            vocab = list( filter( filterFunction, vocab ) )
            
            if not vocab:
                
                break
            
        return vocab

    def vocabularise( self, corpus, tokeniser=None, cleanup=None, stem=False ):
        """Takes a corpus of documents and returns the cleaned up
        vocabulary list, as well as the new corpus with all words 
        from the new voabulary.  The tokenising and cleaning is 
        all based on the tokeniser and cleanup regular expression
        passed.
        
        If tokeniser is not passed, the nltk.tokenize tokenizer
        word_tokenize is used to tokenise instead.
        
        If cleanup is not passed, no cleanup is performed.
        
        If stem is not passed, no stemming is performed.
        
        Parameters
        ----------
        corpus : lst
            A list of documents, each of which is a string.
        tokeniser : str
            The regular expression to tokenise with
        cleanup : str
            The regular expression to cleanup with
        stem : bool
            Stemming is performed if and only if this boolean
            is True

        Returns
        -------
        vocabList : lst
            a list of cleaned up words with no repetitions.
        newCorpus : lst
            a list of documents, each of which is a list of
            words found in vocabList
        """
        
        vocab = []
        
        newCorpus = []
        
        for doc in tqdm( corpus ):
            
            doc = doc.lower()
            
            tokenedDoc = self.tokenise( doc, regex=tokeniser )
            
            cleanedDoc = self.tokensCleanup( tokenedDoc, cleanup )
            
            if stem:
                
                cleanedDoc, _ = self.stem( cleanedDoc )
            
            vocab += cleanedDoc
            
            newCorpus += [ cleanedDoc ]
        
        vocabList = list( set( vocab ) )

        return vocabList, newCorpus

    def saveVocabulary( self, vocab, filename=None ):
        """Saves the vocab list to the local directory
        
        Parameters
        ----------
        vocab : lst
            A list of words to be saved
        filename : str, optional
            The name and location of where to save the
            file.  If no filename is passed, the file
            is saved to a default name based on the
            current date.
        """
           
        if not filename:
            
            dateTimeObj = datetime.now()
            
            filename = str( 'vocabulary_list_' + dateTimeObj.strftime( "%d-%b-%Y-%H-%M" ) + '.PKL' ) 
        
        with open( filename, 'wb' ) as outfile:
            pickle.dump( vocab, outfile )

    def loadVocabulary( self, filename ):
        """Loads a pickled vocabulary list from the
        passed local directory location.
        
        Parameters
        ----------
        filename : str
            The vocabulary list of the file to be loaded

        Returns
        -------
        lst
            the loaded vocabulary list
        """
        
        with ( open( filename, "rb" ) ) as infile:
            return pickle.load( infile )
            
            