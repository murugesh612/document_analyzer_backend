import logging
from flask_app import app


class Logger:
    def __init__(self):
        self.logger = app.logger
        self.setup_logger()

    def setup_logger(self):
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler('app.log')
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
