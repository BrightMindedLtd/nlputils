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








