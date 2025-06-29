import logging

# 自定义日志格式化器，支持颜色输出
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m',    # 青色
        'INFO': '\033[32m',     # 绿色
        'WARNING': '\033[33m',   # 黄色
        'ERROR': '\033[31m',     # 红色
        'CRITICAL': '\033[41m',  # 背景红色
        'TIME': '\033[35m',      # 紫色
        'RESET': '\033[0m'       # 重置颜色
    }

    def format(self, record):
        # 设置 asctime
        record.asctime = self.formatTime(record)
        # 为日志级别添加颜色
        end_color = self.COLORS['RESET']
        start_color = self.COLORS.get(record.levelname, end_color)
        
        # # 为 asctime 添加颜色
        # record.asctime = f"{start_color}{record.asctime}{end_color}"
        # # 为 levelname 添加颜色
        # record.levelname = f"{start_color}{record.levelname}{end_color}"
        # # 为 msg 添加颜色
        # record.msg = f"{start_color}{record.msg}{end_color}"
        
        
        # 返回格式化后的日志
        # return super().format(record)
        return f"{start_color} {record.asctime} - {record.levelname} - {record.msg} {end_color}"

# 设置 logging
logger = logging.getLogger("ColoredLogger")
handler = logging.StreamHandler()
formatter = ColoredFormatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# 测试不同级别的日志
logger.debug("这是一条调试信息")
logger.info("这是一条普通信息")
logger.warning("这是一条警告信息")
logger.error("这是一条错误信息")
logger.critical("这是一条严重错误信息")