import logging
from basic_logger import Logger


logger = Logger(log_level=logging.INFO)


if __name__ == "__main__":
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")