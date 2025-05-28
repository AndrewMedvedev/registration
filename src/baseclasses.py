import logging
from logging import Logger, getLogger


class LoggerMixin:
    logger: Logger = getLogger()

    def config_logging(logger: Logger):
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                fmt="%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s",  # noqa: E501
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)
        return logger

    def __new__(cls, *_, **__):
        obj = super().__new__(cls)
        obj.logger = cls.logger.getChild(f"{cls.__name__}")
        cls.config_logging(obj.logger)
        return obj


class BaseControl(LoggerMixin):
    logger = getLogger("control")


class BaseAPI(LoggerMixin):
    logger = getLogger("rest")
