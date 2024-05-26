import logging

logger = logging.getLogger('loggerFile')

logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('loggerFile.log')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
