import json
import math
import sys
import threading
import time

import numpy as np
import requests

import config
from ThreadTask import ThreadTask
from Tracker import Tracker
from Utils import debugLogger, infoLogger, warningLogger, errorLogger

sys.path.insert(0, './models/')

from page import Page
from product import Product
from productPage import ProductPage
from review import Review
from reviewAttribute import ReviewAttribute


class App:

	def __init__(self):

		self.__API_URL = f'{config.API_PROTOCOL}://{config.API_HOST}:{config.API_PORT}/{config.API_PREFIX}/{config.API_VERSION}/'
		self.__data = []
		self.__trackers = []
		self.__iteration = 0

	def run(self):

		while True:

			infoLogger.info("New iteration")

			self.loadData()
			self.startTracking()

			time.sleep(60 * config.ITERATION_TIME)

			self.__iteration += 1

	def loadData(self):

		self.__data = []

		tmpProducts = json.loads(requests.get(self.__API_URL + 'products').text)
		tmpProductPages = json.loads(requests.get(self.__API_URL + 'productPages').text)
		tmpReviewAttributes = json.loads(requests.get(self.__API_URL + 'reviewAttributes').text)

		for product in tmpProducts:

			newProduct = Product()
			newProduct.id = product['id']
			newProduct.name = product['name']

			productPages = list(filter(lambda productPage: productPage['product']['id'] ==  product['id'], tmpProductPages))
			productPagesData = []

			for productPage in productPages:

				newPage = Page()
				newProductPage = ProductPage()

				newPage.id = productPage['page']['id']
				newPage.name = productPage['page']['name']
				newPage.reviewTag = productPage['page']['reviewTag']
				newPage.reviewInside = productPage['page']['reviewInside']
				newPage.reviewInsideTag = productPage['page']['reviewInsideTag']

				newProductPage.id = productPage['id']
				newProductPage.url = productPage['url']
				newProductPage.product = product

				reviewAttributesData = []

				reviewAttributes = list(filter(lambda reviewAttribute: reviewAttribute['page']['id'] == productPage['page']['id'], tmpReviewAttributes))

				for reviewAttribute in reviewAttributes:

					newReviewAttribute = ReviewAttribute()
					newReviewAttribute.id = reviewAttribute['id']
					newReviewAttribute.key = reviewAttribute['key']
					newReviewAttribute.value = reviewAttribute['value']

					reviewAttributesData.append(newReviewAttribute)

				newPage.reviewAttributes = reviewAttributesData
				newProductPage.page = newPage

				productPagesData.append(newProductPage)

			newProduct.productPages = productPagesData

			self.__data.append(newProduct)

	def startTracking(self):

		self.__trackers = []

		for product in self.__data:

			for productPage in product.productPages:

				newTracker = Tracker(product, productPage.page, productPage, productPage.page.reviewAttributes)

				self.__trackers.append(newTracker)

		tasksNumber = math.ceil(len(self.__trackers) / config.PAGES_TASK)

		infoLogger.info(f"Iteration {self.__iteration} - launched threads: {tasksNumber}")

		array = np.array(self.__trackers)
		tempArrays = np.array_split(array, tasksNumber)

		for idx, tempArray in enumerate(tempArrays):

			task = ThreadTask(tempArray)
			threading.Thread(target = task.startTask()).start()

