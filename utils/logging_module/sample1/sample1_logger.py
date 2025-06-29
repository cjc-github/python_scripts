import os
import logging
from datetime import datetime


# 一个空的Looger, 但是对常见的log函数进行了封装
class EmptyLogger:
    def __init__(self):
        pass
    
    # info函数
    def info(self, message):
        print(f"[+] {message}")
        
    # warning函数
    def warning(self, message):
        """Log a warning message."""
        print(f"[*] {message}")

    # error函数
    def error(self, message):
        print(f"[!] {message}")

    # debug函数
    def debug(self, message):
        print(f"[-] {message}")

    # critical函数
    def critical(self, message):
        print(f"[x] {message}")



# 设置logging函数，适用于开发人员内部测试
# 如果不保存文件和不显示终端都启动的话，也会在终端上出现，但是没有具体的样式
def setup_logging(save_log=True, save_terminal=True, log_prefix="logfile", log_level=logging.INFO, custom_format=None):
    # 创建日志器
    logger = logging.getLogger()
    
    # 创建与模块名称相关的日志器
    
    # 使用这个可以定位到basic_logger, 不推荐使用
    # logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    
    # 检查至少一个处理器是否被启用
    if not save_log and not save_terminal:
        # logging.info("Logging is disabled: no output will be generated.")
        print("[!] Logging is disabled: no output will be generated.")
        return EmptyLogger()  # 直接返回，不创建处理器
    
    # 使用自定义格式或者默认格式
    if custom_format is None:
        # custom_format = '%(asctime)s - %(pathname)s - %(funcName)s - %(levelname)s - %(message)s'
        # custom_format = '%(asctime)s - %(filename)s - %(funcName)s - %(message)s'
        # custom_format = '%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s'
        custom_format = f'%(asctime)s - %(filename)s - %(funcName)s():%(lineno)d - %(message)s'
    
    # 创建格式器
    formatter = logging.Formatter(custom_format)
        
    # 如果需要保存到文件            
    if save_log:
        # 创建带毫秒时间戳的log文件
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        log_file = f"{log_prefix}_{timestamp}.log"
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.info("Logger initialized.")
    
    # 如果需要显示到终端
    if save_terminal:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.info("Logger initialized.")
        
    return logger

