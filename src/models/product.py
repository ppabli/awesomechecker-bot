from base import Base

class Product(Base):

	def __init__(self, name = "", productPages = []):

		self.name = name
		self.productPages = []