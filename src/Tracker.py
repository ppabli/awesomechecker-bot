import re
import smtplib
import ssl
import time

import requests
from bs4 import BeautifulSoup as beautifulSoup

import config
from Utils import debugLogger, infoLogger, warningLogger, errorLogger


class Tracker:

	POST_URL = config.API_PROTOCOL + config.API_HOST + config.API_PREFIX + config.API_VERSION + 'reviews'

	def __init__ (self, product, page, productPage, reviewAttributes):

		self.__product = product
		self.__page = page
		self.__productPage = productPage
		self.__reviewAttributes = reviewAttributes

	def trackPrice(self):

		try:

			infoLogger.info(f"Tracking: {self.__product.name} - {self.__productPage.url}")

			page = requests.get(self.__productPage.url, headers = config.HEADERS)
			soup1 = beautifulSoup(page.content, "html.parser")
			soup2 = beautifulSoup(soup1.prettify(), "html.parser")

			pageAttributes = {}

			for reviewAttribute in self.__reviewAttributes:

				pageAttributes[reviewAttribute.key] = reviewAttribute.value

			element = soup2.find(self.__page.reviewTag, pageAttributes)

			if (element):

				if self.__page.reviewInside == False:

					text = element.getText()

				else:

					text = element[self.__page.reviewInsideTag]

				re.sub('\D', '', text)
				text2 = text.strip().replace(",", ".")
				price = text2.replace('.', '', text2.count('.') - 1)

				review = {
					'value': price,
					'currency': 'eur',
					'productPage': self.__page.id
				}

				try:

					x = requests.post(Tracker.POST_URL, json = review)

					infoLogger.info(f"Track done - {self.__product.name} - {self.__productPage.url}")

				except e:

					errorLogger.error(f"Error posting - {self.__product.name} - {self.__productPage.url}")

			else:

				warningLogger.warning(f"No element detected - {self.__product.name} - {self.__productPage.url}")

		except e:

			errorLogger.error(f"Error scrapping - {self.__product.name} - {self.__productPage.url}")