import logging
import os

# 声明一个全局 logger 变量
logger = None

def setup_logging(file_path):
    global logger  # 声明使用全局变量
    logger_name = os.path.basename(file_path)
    logger = logging.getLogger(logger_name)

    # 设置日志格式
    custom_format = '%(asctime)s - %(filename)s - %(funcName)s():%(lineno)d - %(message)s'
    logging.basicConfig(level=logging.INFO, format=custom_format)

    # 设置 logger 的级别
    logger.setLevel(logging.INFO)

    # 添加文件处理器
    file_handler = logging.FileHandler('xfuzz.log')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(custom_format)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

def error(message, *args):
    logger.error(message % args)

def info(message, *args):
    logger.info(message % args)

def warn(message, *args):
    logger.warning(message % args)