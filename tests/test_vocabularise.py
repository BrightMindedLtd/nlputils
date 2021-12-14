from vocabularise import Vocabularise

from nltk.tokenize import word_tokenize

from tests.base_test_case import BaseTestCase

class TestVocabularise( BaseTestCase ):

    def setUp( self ):

        self.V = Vocabularise()
   
    def testTokenise( self ):

        # when the input is a string of text a default tokenisation is used
        text = "Good muffins cost $3.88\nin New-York.  Please buy me two of them.\n\nThanks."

        expectedDefault = [ 'Good', 'muffins', 'cost', '$', '3.88', 'in', 'New-York', '.', 'Please', 'buy', 'me', 'two', 'of', 'them', '.', 'Thanks', '.' ]

        actual = self.V.tokenise( text )

        self.assertListEqual( actual, expectedDefault )

        # when the input is a string text and a regex the resulting tokenisation 
        # will honour the regular expression
        regex = r'[\d\w]+'
        
        expectedWRegex = [ 'Good', 'muffins', 'cost', '3', '88', 'in', 'New', 'York', 'Please', 'buy', 'me', 'two', 'of', 'them', 'Thanks' ]

        actual = self.V.tokenise( text, regex )

        self.assertListEqual( actual, expectedWRegex )


    def testTokenCleanup( self ):

        dirtyToken = 'football22'

        expected = 'football'

        regex = r'\d+'

        actual = self.V.tokenCleanup( dirtyToken, regex )

        self.assertEqual( actual, expected )


    def testTokensCleanup( self ):

        dirty = [ 'football22', '33ironman', 'help,', '  venom ' ]

        expected = [ 'football', 'ironman', 'help', 'venom' ]
    
        regex = r'[^A-Za-z]+'
        
        actual = self.V.tokensCleanup( dirty, regex )

        self.assertListEqual( actual, expected )


    def testStem( self ):

        vocab = [ 'football', 'footballs', 'reducted', 'reduction', 'shining', 'cat', 'cat', 'cats' ]

        expectedStems = [ 'footbal', 'footbal', 'reduct', 'reduct', 'shine', 'cat', 'cat', 'cat' ]

        expectedMap = {

            'footbal': [ 'football', 'footballs' ], 
            'reduct': [ 'reducted', 'reduction' ], 
            'shine': [ 'shining' ], 
            'cat': [ 'cat', 'cats' ]

        }
        
        actualStems, stem2word = self.V.stem( vocab )

        self.assertListEqual( actualStems, expectedStems )

        self.assertDictEqual( stem2word, expectedMap )

    
    def testMergeVocabularies( self ):
        
        vocab1 = [ 'apple', 'dog', 'caterpillar', 'hello' ]
        
        vocab2 = [ 'dog', 'wolf', 'beach', 'apple' ]
        
        expectedResult = [ 'apple', 'dog', 'caterpillar', 'hello', 'wolf', 'beach' ]
        
        actualResult = self.V.mergeVocabularies( vocab1, vocab2 )
        
        self.assertUnsortedListEqual( actualResult , expectedResult )

    def testMergeStemMaps( self ):
        
        stemMap1 = {

            'footbal': [ 'football', 'footballs' ], 
            'reduct': [ 'reducted', 'reduction' ], 
            'shine': [ 'shines' ]
            
        }
        
        stemMap2 = {    
            
            'shine': [ 'shining' ], 
            'reduct': [ 'reducted', 'reduction' ], 
            'cat': [ 'cat', 'cats' ]
            
        }
    
        expectedMap = {
            
            'footbal': [ 'football', 'footballs' ], 
            'reduct': [ 'reducted', 'reduction' ], 
            'shine': [ 'shines', 'shining' ],
            'cat': [ 'cat', 'cats' ]
            
        }
        
        actualMap = self.V.mergeStemMaps( stemMap1, stemMap2 )
        
        self.assertListEqual( list( actualMap.keys() ), list( expectedMap.keys() ) )
        
        for key in actualMap.keys():

            self.assertUnsortedListEqual( actualMap[ key ] , expectedMap[ key ] )

    def testFilter( self ):
        
        # If no function is supplied to filter, we
        # take stop_words as default.
        
        vocab = [ "if", "every", "time", "i", "thought", "was", "being", "rejected", "from", "something", "good", "actually", "re-directed", "to" ]

        expectedVocab = [ "every", "time", "thought", "rejected", "something", "good", "actually", "re-directed" ]

        actualVocab = self.V.filter( vocab )
        
        self.assertUnsortedListEqual( actualVocab, expectedVocab )

        with self.assertRaises( ValueError ):
            self.V.filter( vocab, vocab )

        # If multiple filters are supplied,
        #   we filter by all of them
        
        def newFilter( word ):
            return not word[0:2] == 're'

        expectedVocab = [ "every", "time", "thought", "something", "good", "actually" ]

        actualVocab = self.V.filter( vocab, Vocabularise.stopWordsFilter, newFilter )
        
        self.assertUnsortedListEqual( actualVocab, expectedVocab )

    def testVocabularise( self ):

        # in the default scenario the assumption is that
        # tokeniser=None, cleanup=None, stem=False.  The default
        # tokeniser is nltk.word_tokenize.
        
        corpus = [
     
             "Every time I thought I was being rejected from something good, I was actually being re-directed to something better.", 
             "It is not so much the major events as the small day-to-day decisions that map the course of our living. . . Our lives are, in reality, the sum total of our seemingly unimportant decisions and of our capacity to live by those decisions.",
             "Maybe 'Okay' will be our 'always'...", 
             "When the world pushes you to your knees, you're in the perfect position to pray",
             "Criticism , however valid or intellectually engaging , tends to get in the way of a writer who has anything personal to say. A tightrope walker may require practice, but if he starts a theory of equilibrium he will lose grace (and probably fall off)." 

        ]
        
        actualVocabulary, _ = self.V.vocabularise( corpus )
        
        actualVocabularySet = set( actualVocabulary )
        
        for doc in corpus:
            
            expectedVocabulary = set( word_tokenize( doc.lower() ) )
            
            intersection = actualVocabularySet.intersection( expectedVocabulary )
            
            # Testing all created tokens are in the expected vocabulary.
            # All return words should be in lower case.
            
            self.assertSetEqual(  intersection, expectedVocabulary )
            
        # Testing that a vocabulary contains no duplicates.
        
        self.assertEqual( len( actualVocabulary ), len ( actualVocabularySet ) )

        # When a regular expression is supplied to
        # the tokeniser, we expect the text to be 
        # tokenise correctly.

        expectedVocabulary = [ "if", "every", "time", "i", "thought", "was", "being", "rejected", "from", "something", "good", "actually", "re-directed", "to", "better", "it", "is", "not", "so", "much", "the", "major", "events", "as", "small", "day-to-day", "decisions", "that", "map", "course", "of", "our", "living", "lives", "are", "in", "reality", "sum", "total", "seemingly", "unimportant", "and", "capacity", "live", "by", "those", "maybe", "okay", "will", "be", "always", "when", "world", "pushes", "you", "your", "knees", "you're", "perfect", "position", "pray", "criticism", "however", "valid", "or", "intellectually", "engaging", "tends", "get", "way", "a", "writer", "who", "has", "anything", "personal", "say", "tightrope", "walker", "may", "require", "practice", "but", "he", "starts", "theory", "equilibrium", "lose", "grace", "probably", "fall", "off" ] 

        regex = Vocabularise.PUNCTUATION_MID_WORD_ONLY

        actualVocabulary, _ = self.V.vocabularise( corpus, tokeniser=regex )

        self.assertUnsortedListEqual( actualVocabulary, expectedVocabulary )
             
        # When a regular expression is supplied to
        # the cleanup, we expect the text to be 
        # cleaned up correctly.
        
        cleanupRegex = r'[^a-zø]+'

        dirtyCorpus = [ "Sven Magnus Øen Carlsen[a] (born 30 November 1990)[1][2] is a Norwegian[5] chess grandmaster" ]

        expectedVocabulary = [ 'sven', 'magnus', 'øen', 'carlsen', 'born', 'november', 'is', 'a', 'norwegian', 'chess', 'grandmaster' ] 

        actualVocabulary, _ = self.V.vocabularise( dirtyCorpus, cleanup=cleanupRegex )

        self.assertUnsortedListEqual(  actualVocabulary, expectedVocabulary )    

        # When stem == True, the vocabuliser should
        # return correctly stemmed vocabulary.

        unstemmedDoc = [ ( ' ' ).join( [ 'caresses', 'flies', 'dies', 'mules', 'denied',
           'died', 'agreed', 'owned', 'humbled', 'sized',
            'meeting', 'stating', 'siezing', 'itemization',
            'sensational', 'traditional', 'reference', 'colonizer',
            'plotted' ] ) ]

        expectedVocabulary = "caress fli die mule deni agre own humbl size meet state siez item sensat tradit refer colon plot".split( " " )
        
        expectedDoc = [ 'caress', 'fli', 'die', 'mule', 'deni',
           'die', 'agre', 'own', 'humbl', 'size',
            'meet', 'state', 'siez', 'item',
            'sensat', 'tradit', 'refer', 'colon',
            'plot' ]
        
        actualVocabulary, actualNewCorpus = self.V.vocabularise( unstemmedDoc, stem=True )

        self.assertUnsortedListEqual( actualVocabulary, expectedVocabulary )
        
        for doc in actualNewCorpus:
            self.assertListEqual( doc, expectedDoc )
