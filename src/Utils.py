import logging

def setupLogger(name, file: str, level=logging.INFO):

	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
	handler = logging.FileHandler(file)
	handler.setLevel(level)
	handler.setFormatter(formatter)

	logger = logging.getLogger(name)
	logger.setLevel(level)
	logger.addHandler(handler)

	return logger


debugLogger = setupLogger('debug', './logs/debug.log', logging.DEBUG)
infoLogger = setupLogger('info', './logs/info.log', logging.INFO)
warningLogger = setupLogger('warning', './logs/warning.log', logging.WARNING)