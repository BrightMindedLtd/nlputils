import unittest

class TestAnnoytise( unittest.TestCase ):

	def setUp( self ):

		self.A = Annoytise()

	def testAnnoytise( self ):

		vocabulary = [ 'ironman', 'thor', 'black widow', 'spiderman', 'captain america', 'doctor strange' ]

		annoy = self.A.annoytise( vocabulary )

		self.assertIsNotNone( annoy )

		for idx in range( len( Vocabulary ) ):

			