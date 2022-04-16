import re
from decimal import Decimal

import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import config
from Utils import debugLogger, infoLogger, warningLogger, errorLogger


class Tracker:

	POST_URL = f'{config.API_PROTOCOL}://{config.API_HOST}:{config.API_PORT}/{config.API_PREFIX}/{config.API_VERSION}/reviews'

	def __init__ (self, product, page, productPage, reviewAttributes):

		self.__product = product
		self.__page = page
		self.__productPage = productPage
		self.__reviewAttributes = reviewAttributes

	def trackPrice(self):

		try:

			driver = webdriver.Remote(command_executor=f'http://{config.GRID_HOST}:{config.GRID_PORT}/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)

			infoLogger.info(f"Tracking: {self.__product.name} - {self.__productPage.url}")

			driver.get(self.__productPage.url)

			requestAttributes = "and".join(map(lambda reviewAttribute: f'@{reviewAttribute.key}="{reviewAttribute.value}"', self.__reviewAttributes))

			priceElements = driver.find_elements_by_xpath(f'.//{self.__page.reviewTag}[{requestAttributes}]')

			if len(priceElements) != 0:

				priceElement = priceElements[0]
				priceText = priceElement.get_attribute('innerHTML')

				priceFormatted = priceText.replace(',', '.')
				priceFormatted = re.sub('[^\d\.]', '', priceFormatted)

				dotsNumber = priceFormatted.split('.')

				if len(dotsNumber) > 1:

					decimalPart = int(dotsNumber[-1])

					intPart = int(''.join(dotsNumber[0:-1]))

				elif len(dotsNumber) == 1:

					decimalPart = 0

					intPart = int(dotsNumber[0])

				price = intPart + (decimalPart / 100)

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

				warningLogger.warning(f"No price found - {self.__product.name} - {self.__productPage.url}")

			driver.quit()

		except e:

			errorLogger.error(f"Error scrapping - {self.__product.name} - {self.__productPage.url}")