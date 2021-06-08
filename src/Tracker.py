import hashlib
import time
import re
import requests
import smtplib
from bs4 import BeautifulSoup as beautifulSoup
import ssl

import config

class Tracker:

	POST_URL = config.API_PROTOCOL + config.API_HOST + config.API_PREFIX + config.API_VERSION + 'reviews'

	def __init__ (self, product, page, reviewAttributes):

		self.__product = product
		self.__page = page
		self.__reviewAttributes = reviewAttributes

	def trackPrice(self):

		print(f"Tracking: {self.__product['name']} - {self.__page['url']}")

		page = requests.get(self.__page['url'], headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
		soup1 = beautifulSoup(page.content, "html.parser")
		soup2 = beautifulSoup(soup1.prettify(), "html.parser")

		pageAttibutes = {}

		for reviewAttibute in self.__reviewAttributes:

			pageAttibutes[reviewAttibute['key']] = reviewAttibute['value']

		element = soup2.find(self.__page["reviewTag"], attrs = pageAttibutes)

		if (element):

			if self.__page["reviewInside"] == False:

				text = element.getText()

			else:

				text = element[self.__page["reviewInsideTag"]]

			text2 = text.strip().replace(",", ".")
			price = float(re.sub("$|€", '', text2))

			review = {
				'value': price,
				'currency': 'eur',
				'productPage': self.__page['id']
			}

			print(review)

			x = requests.post(Tracker.POST_URL, json = review)

			print(x.text)

			print(f"Done: {price}")

		else:

			print("No element detected")

		print("Track done")