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

debugLogger = setupLogger('debug', './logs/debugs.log', logging.DEBUG)
infoLogger = setupLogger('info', './logs/infos.log', logging.INFO)
warningLogger = setupLogger('warning', './logs/warnings.log', logging.WARNING)
errorLogger = setupLogger('error', './logs/errors.log', logging.ERROR)