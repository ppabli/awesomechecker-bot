import requests
import json
import config
import logging
from Tracker import Tracker

class App:

	def __init__(self):

		logging.basicConfig(level = logging.INFO, filename = 'logs/log', format = '%(asctime)s %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p')
		self.__API_URL = config.API_PROTOCOL + config.API_HOST + config.API_PREFIX + config.API_VERSION
		self.__data = {}
		self.__trackers = []

	def run(self):

		while True:

			self.loadData()
			self.startTracking()
			break

	def loadData(self):

		data = {}

		tmpProducts = json.loads(requests.get(self.__API_URL + 'products').text)
		tmpProductPages = json.loads(requests.get(self.__API_URL + 'productPages').text)
		tmpReviewAttributes = json.loads(requests.get(self.__API_URL + 'reviewAttributes').text)

		for product in tmpProducts:

			productPages = list(filter(lambda productPage: productPage['product']['id'] ==  product['id'], tmpProductPages))
			productPagesData = list(map((lambda productPage: {'id': productPage['id'], 'pageId': productPage['page']['id'], 'reviewTag': productPage['page']['reviewTag'], 'reviewInside': productPage['page']['reviewInside'], 'reviewInsideTag': productPage['page']['reviewInsideTag'], 'url': productPage['url']}), productPages))

			for index, productPage in enumerate(productPages):

				reviewAttributes = list(filter(lambda reviewAttribute: reviewAttribute['page']['id'] == productPage['page']['id'], tmpReviewAttributes))
				reviewAttributesData = list(map((lambda reviewAttribute: {'id': reviewAttribute['id'], 'pageId': reviewAttribute['page']['id'], 'key': reviewAttribute['key'], 'value': reviewAttribute['value']}), reviewAttributes))
				productPagesData[index]['reviewAttributes'] = reviewAttributesData;

			data[product['id']] = {
				'name': product['name'],
				'productPages': productPagesData
			}

		self.__data = data

		with open('data.json', 'w') as outfile:
			json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))

	def startTracking(self):

		for index in self.__data:

			for page in self.__data[index]['productPages']:

				newTracker = Tracker(self.__data[index], page, page['reviewAttributes'])

				self.__trackers.append(newTracker)

				newTracker.trackPrice()
