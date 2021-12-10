import re 

from nltk.stem.porter import PorterStemmer

from nltk.tokenize import word_tokenize, RegexpTokenizer

class Vocabularise( object ):
    
    # This regex removes all punctuation not surrounded by letters.
    PUNCTUATION_MID_WORD_ONLY = r"([\w]+(?:(?!\s)\W?[\w]+)*)"
    
    def __init__( self ):

        self._stemmer = PorterStemmer()

    def tokenise( self, text, regex=None ):
        
        if regex:
            tokeniser = RegexpTokenizer( regex )

            return tokeniser.tokenize( text )
        
        return word_tokenize( text )


    def tokenCleanup( self, dirty, regex ):
        
        if not regex:
        
            return dirty
        
        result = re.findall( regex, dirty )

        if result:

            return result[ 0 ]

        return ''


    def tokensCleanup( self, dirty, regex ):

        result = [ self.tokenCleanup( token, regex ) for token in dirty ]

        return [ token for token in result if token ]


    def stem( self, vocab ):

        stem2word = {}

        for word in vocab:

            stem = self._stemmer.stem( word )

            if stem not in stem2word:

                stem2word[ stem ] = []

            if word not in stem2word[ stem ]:
                
                stem2word[ stem ].append( word )

        return list( stem2word.keys() ), stem2word



    def vocabularise( self, corpus, tokeniser=None, cleanup=None, stem=False ):
        
        vocab = []
        
        for doc in corpus:
            
            doc = doc.lower()
            
            tokenedVocab = self.tokenise( doc, regex=tokeniser )
            
            cleanedVocab = self.tokensCleanup( tokenedVocab, cleanup )
            
            vocab += cleanedVocab
        
        vocabList = list( set( vocab ) )

        if stem:
  
            vocabList, _  = self.stem( vocabList )

        return vocabList





