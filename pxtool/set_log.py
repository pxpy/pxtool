"""
pycharm termcolor不起作用
需要打开 Run/Debug Configurations，然后勾选 Emulate terminal in output console
"""
import logging
import time
import os
from termcolor import colored


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'magenta'
    }

    def format(self, record):
        log_message = super().format(record)
        color = self.COLORS.get(record.levelname, 'white')  # 默认白色
        return colored(log_message, color)


def setup_logger(log_filename_prefix='log', level=logging.INFO, log_folder='logs'):
    current_date = time.strftime('%Y-%m-%d')
    # 获取当前Python文件名（不包含路径和扩展名）
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    log_filename = f'{log_filename_prefix}_{current_date}_{script_name}.log'

    # 配置日志
    logger = logging.getLogger()
    logger.setLevel(level)

    # 确保日志文件夹存在
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # 拼接完整的日志文件路径
    log_filepath = os.path.join(log_folder, log_filename)
    # 创建文件处理器
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # 创建控制台处理器
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s'))
    # 移除默认的handler
    for handler in logger.handlers:
        logger.removeHandler(handler)
    # 将handler添加到logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # 如果需要支持 TRACE 级别日志，可以通过添加自定义级别来实现
    logging.TRACE = logging.DEBUG - 5  # TRACE 级别在 DEBUG 之前
    logging.addLevelName(logging.TRACE, "TRACE")

    def trace(self, message, *args, **kwargs):
        if self.isEnabledFor(logging.TRACE):
            self._log(logging.TRACE, message, args, **kwargs)

    logging.Logger.trace = trace

if  __name__ == '__main__':
    # 使用示例
    setup_logger()

    # 示例日志
    logging.debug("This is a debug message")
    logging.info("This is an info message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")
