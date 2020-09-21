class Comment:
	'''Domain Comment Object'''
	def __init__(self, id=None, comment=''):
		self._id = id
		self._comment = comment

	def getId(self):
		return self._id

	def setId(self, id):
		self._id = id

	def getComment(self):
		return self._comment

	def setComment(self, comment):
		self._comment = comment


# newComment = Comment(1, 'comment')
# newComment.setId(2)
# newComment.setComment('tamen')
# print(newComment.getId())
# print(newComment.getComment())