from Utils import infoLogger, debugLogger, warningLogger
import time

class ThreadTask:

	def __init__(self, trackers):

		self.__trackers = trackers

	def startTask(self):

		for tracker in self.__trackers:

			tracker.trackPrice()
