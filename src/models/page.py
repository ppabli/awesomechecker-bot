from base import Base

class Page(Base):

	def __init__(self, name = "", reviewTag = "", reviewInside = False, reviewInsideTag = "", reviewAttributes = []):

		self.name = name
		self.reviewTag = reviewTag
		self.reviewInside = reviewInside
		self.reviewInsideTag = reviewInsideTag
		self.reviewAttributes = reviewAttributes