from base import Base

class ReviewAttribute(Base):

	def __init__(self, key = "", value = "", page = None):

		self.key = key
		self.value = value
		self.page = page