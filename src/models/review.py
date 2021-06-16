from base import Base

class Review(Base):

	def __init__(self, currency = "", value = -1, productPage = None):

		self.currency = currency
		self.value = value
		self.productPage = productPage
