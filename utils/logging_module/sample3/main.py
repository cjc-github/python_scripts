import logging
import re

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

    colored_fields = {}  # 定义为类属性

    # 初始化步骤
    def __init__(self, fmt, select_field=None):
        super().__init__(fmt)
        self.fmt = fmt
        self.select_field = select_field or []

    
    # 预处理
    def init_preload(self):
        # 预处理格式化字符
        pattern = r'%\((.*?)\)'
        matches = re.findall(pattern, self.fmt)

        # 使用集合来存储已选字段
        selected_keys = {key.split("%(")[1].split(")")[0] for key in self.colored_fields.keys()}

        for i in matches:
            if i not in selected_keys:
                print(f" [!] Formatter Field `{i}` is not selected.")
                exit(0)

        # 预处理选定字段
        for i in self.select_field:
            if i not in selected_keys:
                print(f" [!] Custom Field `{i}` is not selected.")
                exit(0)

    # 设置
    def format(self, record):
        # 设置 asctime
        record.asctime = self.formatTime(record)
        # 为日志级别添加颜色
        end_color = self.COLORS['RESET']
        start_color = self.COLORS.get(record.levelname, end_color)
        
        # 创建一个字典来存储字段及其对应的颜色化信息
        self.colored_fields = {
            '%(asctime)s': record.asctime,
            '%(levelno)s': str(record.levelno),
            '%(levelname)s': record.levelname,
            '%(pathname)s': record.pathname,
            '%(filename)s': record.filename,
            '%(module)s': record.module,
            '%(lineno)d': str(record.lineno),
            '%(funcName)s': record.funcName,
            '%(created)f': str(f"{record.created:.6f}"),
            '%(msecs)d': str(record.msecs),
            '%(relativeCreated)d': str(record.relativeCreated),
            '%(thread)d': str(record.thread),
            '%(threadName)s': record.threadName,
            '%(process)d': str(record.process),
            '%(message)s': record.msg
        }

        # 提取字典键中的内容
        self.init_preload()
        

        # 使用字典中的信息进行替换
        log_message = self._fmt

        for field, colored_value in self.colored_fields.items():
            key = field.split("%(")[1].split(")")[0]
            if key in self.select_field:
                log_message = log_message.replace(field, f"{start_color} {colored_value} {end_color}")
            else:
                log_message = log_message.replace(field, colored_value)
        
        # 自定义字段是否上颜色
        if len(self.select_field) == 0:
            return f"{start_color} {log_message} {end_color}"
        else:
            return f"{log_message}"


if __name__ == "__main__":
    # 设置 logging
    logger = logging.getLogger("ColoredLogger")
    handler = logging.StreamHandler()
    # custom_formatter = "%(asctime)s - %(levelname)s - %(message)s"
    # custom_formatter = "%(levelname)s - %(message)s"
    custom_formatter = (
        "%(asctime)s - %(levelname)s - %(levelno)s - %(message)s - "
        "%(pathname)s - %(filename)s - %(module)s - %(lineno)d - "
        "%(funcName)s - %(created)f - %(msecs)d - "
        "%(relativeCreated)d - %(thread)d - %(threadName)s - %(process)d"
    )
    select_field = ["asctime", "message"]
    # select_field = []
    formatter = ColoredFormatter(custom_formatter, select_field = select_field)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)  # 设置日志级别为 DEBUG, 这样所有级别的日志都会被处理

    # 测试不同级别的日志
    logger.debug("这是一条调试信息")
    logger.info("这是一条普通信息")
    logger.warning("这是一条警告信息")
    logger.error("这是一条错误信息")
    logger.critical("这是一条严重错误信息")