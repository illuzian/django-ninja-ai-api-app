import logging
import os
import sys

import langchain
from icecream import ic

ic.configureOutput(includeContext=True)


def setup_logging(loguru_logger):
    log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'TRACE']
    # noinspection PyPep8

    log_format = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <c>{module}</c>:<c>{"
                  "function}</c>:<c>{line}</c> <level>{message}</level> ((<level>ELAPSED={elapsed};FILE='{"
                  "file}';</level>)) |END LINE|")
    log_format_file = ("{time:YYYY-MM-DD HH:mm:ss} | {level}| {module} {function}:{line} {message} ((ELAPSED={"
                       "elapsed};FILE='{file}';)) |END LINE|")

    log_retention = '2 days'
    log_rotate_size = '1 MB'
    if os.getenv('LOG_RETENTION'):
        log_retention = os.getenv('LOG_RETENTION')
        ic(f'Set Loguru log retention to: {log_retention} from env variables')
    if os.getenv('LOG_ROTATE_SIZE'):
        log_rotate_size = os.getenv('LOG_ROTATE_SIZE')
        ic(f'Set Loguru log rotate size to: {log_rotate_size} from env variables')

    # print(os.getenv('APP_LOG_LEVEL'))
    if os.getenv('APP_LOG_LEVEL') is not None and os.getenv('APP_LOG_LEVEL').upper() in log_levels:
        log_level = os.getenv('APP_LOG_LEVEL').upper()
    else:
        log_level = 'DEBUG'

    if log_level == 'DEBUG':
        langchain.verbose = True
        langchain.debug = True

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            logger_opt = loguru_logger.opt(depth=6, exception=record.exc_info)
            logger_opt.log(record.levelname, record.getMessage())

    # default_logger.setLevel(log_level)

    loguru_logger.remove()

    log_console_target = sys.stderr

    loguru_logger.add(
        log_console_target, level=log_level, colorize=True,
        format=log_format)
    if os.getenv('APP_LOG_TO_FILE') != 'False':
        loguru_logger.add(
            "app.log", rotation=log_rotate_size, compression='tar.gz',
            retention=log_retention, enqueue=True, level=log_level,
            encoding="utf8", format=log_format_file)

    return InterceptHandler
