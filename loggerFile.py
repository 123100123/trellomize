import logging

# Create a logger
logger = logging.getLogger(__name__)

# Set the level of this logger. This level will be used to filter out logs
logger.setLevel(logging.DEBUG)

# Create a file handler for outputting log messages to a file
handler = logging.FileHandler('user.log')

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)
