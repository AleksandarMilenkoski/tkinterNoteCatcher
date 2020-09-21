class Comment:
	'''Domain Comment Object'''
	def __init__(self, id=None, comment='', date_created=None, date_modified=None):
		self._id = id
		self._comment = comment
		self._date_created = date_created
		self._date_modified = date_modified

	def get_id(self):
		return self._id

	def set_id(self, id):
		self._id = id

	def get_comment(self):
		return self._comment

	def set_comment(self, comment):
		self._comment = comment

	def get_date_created(self):
		return self._date_created

	def set_date_created(self, date):
		self._date_created = date

	def get_date_modified(self):
		return self._date_modified

	def set_date_modified(self, date):
		self._date_modified = date


# newComment = Comment(1, 'comment')
# newComment.setId(2)
# newComment.setComment('tamen')
# print(newComment.getId())
# print(newComment.getComment())