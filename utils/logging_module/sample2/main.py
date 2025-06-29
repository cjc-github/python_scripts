import logging
from sample2_logger import Logger

logging = Logger(save_log=False, save_terminal=True, log_level=logging.DEBUG)

# 级别: critical > error > warning > info > debug
    
"""
save_log=False, save_terminal=false的话, logging.info实际调用的是print
save_log=True, save_terminal=True的话, 终端和文件均保存
save_log=False, save_terminal=True的话, 终端显示, 但文件不保存
save_log=True, save_terminal=False的话, 文件保存, 但终端不显示

使用方法: 导入import, 并全局调用setup_logging即可
"""
    

def test():
    logging.info("info")
    logging.warning("warning")
    logging.error("error")
    logging.debug("debug")
    logging.critical("critical")
    
    
if __name__ == "__main__":
    test()
    
    