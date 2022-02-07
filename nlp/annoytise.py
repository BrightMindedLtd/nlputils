from annoy import AnnoyIndex

import torch
import torchtext

DEFAULT_GLOVE_DIM = 100 
NUM_TREES = 100

class Annoytise( object ):

	@staticmethod
	def glove( dim=DEFAULT_GLOVE_DIM ):

		return torchtext.vocab.GloVe( name="6B", dim=dim )


	def __init__( self, embedding=None, dim=DEFAULT_GLOVE_DIM, trees=NUM_TREES ):

		# we assume embedding to be a dictionary-like object
		# that accepts tokens as keys and returns dim-dimensional
		# torch tensor as values

		self._embedding = embedding
		self._dim = dim 
		self._trees = trees

		if self._embedding is None:
			self._embedding = Annoytise.glove( self._dim )

		self._index = AnnoyIndex( self._dim, 'angular' )

	
	def annoytise( self, vocabulary ):

		try:

			for idx, word in enumerate( vocabulary ):
				# we may have vocabulary entries made
				# out of several tokens ...
				tokens = word.lower().split()
				
				# ... in which case we vectorise each token...
				vectors = [ self._embedding[ token ] for token in tokens ]

				# ... and we index their mean
				v = torch.stack( vectors ).mean( dim=0 ).tolist()
				self._index.add_item( idx, v)

			self._index.build( self._trees )

			return self._index

		except Exception as e: 

			print ( e )
		

	def saveAnnoy( self, filename=None ):

		if not filename:
			
			dateTimeObj = datetime.now()    
			filename = str( 'vocabulary_index_' + dateTimeObj.strftime( "%d-%b-%Y-%H-%M" ) + '.ANN' ) 
		
		if self._index:
		
			self._index.save( filename )

	def loadAnnoy( self, filename ):

		self._index.load( filename )


	def getNNsByIdx( self, idx, n ):

		return self._index.get_nns_by_item( idx, n )

