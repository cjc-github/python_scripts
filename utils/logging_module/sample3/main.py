import logging

# 自定义日志格式化器，支持颜色输出
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m',    # 青色
        'INFO': '\033[32m',     # 绿色
        'WARNING': '\033[33m',   # 黄色
        'ERROR': '\033[31m',     # 红色
        'CRITICAL': '\033[41m',  # 背景红色
        'TIME': '\033[35m',      # 紫色, 时间戳
        'RESET': '\033[0m'       # 重置颜色
    }

    def format(self, record):
        # 设置 asctime
        record.asctime = self.formatTime(record)
        # 为日志级别添加颜色
        end_color = self.COLORS['RESET']
        start_color = self.COLORS.get(record.levelname, end_color)
        
        # return f"{start_color} {record.asctime} - {record.levelname} - {record.msg} {end_color}"
        # 创建一个字典来存储字段及其对应的颜色化信息
        colored_fields = {
            '%(asctime)s': f"{record.asctime}",
            '%(levelname)s': f"{record.levelname}",
            '%(message)s': f"{record.msg}"
        }

        # 使用字典中的信息进行替换
        log_message = self._fmt
        for field, colored_value in colored_fields.items():
            log_message = log_message.replace(field, colored_value)

        return f"{start_color} {log_message} {end_color}"
    
# 自定义日志格式化器，支持颜色输出
class ColoredMsgFormatter(logging.Formatter):
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
        
        # 为 asctime 添加颜色
        record.asctime = f"{start_color}{record.asctime}{end_color}"
        # 为 levelname 添加颜色
        record.levelname = f"{start_color}{record.levelname}{end_color}"
        # 为 msg 添加颜色
        record.msg = f"{start_color}{record.msg}{end_color}"
        
        
        # 返回格式化后的日志
        return super().format(record)


if __name__ == "__main__":
    # 设置 logging
    logger = logging.getLogger("ColoredLogger")
    handler = logging.StreamHandler()
    custom_formatter = "%(asctime)s - %(levelname)s - %(message)s"
    # custom_formatter = "%(levelname)s - %(message)s"
    formatter = ColoredFormatter(custom_formatter)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)  # 设置日志级别为 DEBUG, 这样所有级别的日志都会被处理

    # 测试不同级别的日志
    logger.debug("这是一条调试信息")
    logger.info("这是一条普通信息")
    logger.warning("这是一条警告信息")
    logger.error("这是一条错误信息")
    logger.critical("这是一条严重错误信息")