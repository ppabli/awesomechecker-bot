import requests
import json
import config
import time
import math
import numpy as np
import time
import threading

from Tracker import Tracker
from ThreadTask import ThreadTask
from Utils import infoLogger, debugLogger, warningLogger
class App:

	def __init__(self):

		self.__API_URL = config.API_PROTOCOL + config.API_HOST + config.API_PREFIX + config.API_VERSION
		self.__data = {}
		self.__trackers = []
		self.__iteration = 0

	def run(self):

		while True:

			infoLogger.info("New iteration")

			self.loadData()
			self.startTracking()

			time.sleep(30 * 60)

			self.__iteration += 1

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

	def startTracking(self):

		for index in self.__data:

			for page in self.__data[index]['productPages']:

				newTracker = Tracker(self.__data[index], page, page['reviewAttributes'])

				self.__trackers.append(newTracker)

		tasksNumber = math.ceil(len(self.__trackers) / config.PAGES_TASK)

		infoLogger.info(f"Iteration {self.__iteration} - launched threads: {tasksNumber}")

		array = np.array(self.__trackers)
		tempArrays = np.array_split(array, tasksNumber)

		for idx, tempArray in enumerate(tempArrays):

			task = ThreadTask(tempArray)
			threading.Thread(target = task.startTask()).start()

			infoLogger.info(f"Iteration {self.__iteration} - thread: {idx} launched")

