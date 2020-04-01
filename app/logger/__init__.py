from flask import current_app, has_request_context, request
from logging import Formatter, StreamHandler
import logging

error_logger = logging.Logger('app.error.logger')
error_handler = StreamHandler()
error_handler.setFormatter(Formatter(
        '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s '
        '[in %(pathname)s:%(lineno)d]', "%Y-%m-%d %H:%M:%S %z"))
error_handler.setLevel(logging.ERROR)
error_logger.addHandler(error_handler)


class Logger:

    @staticmethod
    def request():
        current_app.logger.info("{:5} {:15} {:12} {:30}".format(request.method,
                                                                request.path,
                                                                request.remote_addr,
                                                                request.user_agent.string))

    @staticmethod
    def info(msg: str):
        if has_request_context():
            current_app.logger.info("{:5} {:15} {:30}".format(request.method,
                                                              request.path,
                                                              msg))
        else:
            current_app.logger.info("{:30}".format(msg))

    @staticmethod
    def error(msg: str, ex: Exception):
        error_logger.error("{:50} {}".format(msg, str(ex)))


logger = Logger()
