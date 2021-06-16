from base import Base

class ProductPage(Base):

	def __init__(self, url = "", product = None, page = None):

		self.url = url
		self.product = product
		self.page = page