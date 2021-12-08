import unittest

from vocabularise import Vocabularise

class TestVocabularise( unittest.TestCase ):

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

		regex = r'[A-Za-z]+'

		actual = self.V.tokenCleanup( dirtyToken, regex )

		self.assertEqual( actual, expected )


	def testTokensCleanup( self ):

		dirty = [ 'football22', '33ironman', 'help,', '  venom ' ]

		expected = [ 'football', 'ironman', 'help', 'venom' ]
	
		regex = r'[A-Za-z]+'

		actual = self.V.tokensCleanup( dirty, regex )

		self.assertListEqual( actual, expected )


	def testStem( self ):

		vocab = [ 'football', 'footballs', 'reducted', 'reduction', 'shining', 'cat', 'cat', 'cats' ]

		expectedStems = [ 'footbal', 'reduct', 'shine', 'cat' ]

		expectedMap = {

			'footbal': [ 'football', 'footballs' ], 
			'reduct': [ 'reducted', 'reduction' ], 
			'shine': [ 'shining' ], 
			'cat': [ 'cat', 'cats' ]

		}
		
		actualStems, stem2word = self.V.stem( vocab )

		self.assertListEqual( actualStems, expectedStems )

		self.assertDictEqual( stem2word, expectedMap )

	def testVocabularise( self ):

		# in the default scenario the assumption is that
		# stem=false, tokeniser=None, cleanup=None

		corpus = [
	
			"Every time I thought I was being rejected from something good, I was actually being re-directed to something better.", 
			"It is not so much the major events as the small day-to-day decisions that map the course of our living. . . Our lives are, in reality, the sum total of our seemingly unimportant decisions and of our capacity to live by those decisions.",
			"Maybe 'Okay' will be our 'always'...", 
			"When the world pushes you to your knees, you're in the perfect position to pray","Criticism , however valid or intellectually engaging , tends to get in the way of a writer who has anything personal to say. A tightrope walker may require practice, but if he starts a theory of equilibrium he will lose grace (and probably fall off)." 

		]
		
		expectedVocabulary = ["Every", "time", "I", "thought", "was", "being", "rejected", "from", "something", "good", "actually", "re-directed", "to", "better", "it", "is", "not", "so", "much", "the", "major", "events", "as", "small", "day-to-day", "decisions", "that", "map", "course", "of", "our", "living", "lives", "are", "in", "reality", "sum", "total", "seemingly", "unimportant", "and", "capacity", "live", "by", "those", "Maybe", "'Okay'", "will", "be", "always", "When", "world", "pushes", "you", "your", "knees", "you're", "perfect", "position", "pray", "Criticism", "however", "valid", "or", "intellectually", "engaging", "tends", "get", "way", "a", "writer", "who", "has", "anything", "personal", "say", "A", "tightrope", "walker", "may", "require", "practice", "but", "he", "starts", "theory", "equilibrium", "lose", "grace", "probably", "fall", "off" ] 	
		
		actualVocabulary = self.V.vocabularise( corpus )

		self.assertListEqual( actualVocabulary, expectedVocabulary )











