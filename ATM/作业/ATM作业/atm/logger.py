# -*- coding: UTF-8 -*-
# Author  : Liushuai
# Time    : 2020/2/23 19:16
# File    : logger.py

import logging
import os

from 作业.ATM作业.conf import settings


def logger(log_type):
    # creat logger
    logger = logging.getLogger(log_type)
    logger.setLevel(settings.LOG_LEVEL)

    log_file = os.path.join(settings.LOG_PATH, settings.LOG_TYPES[log_type])
    fh = logging.FileHandler(log_file)
    fh.setLevel(settings.LOG_LEVEL)
    formatter = settings.LOG_FORMAT

    # add formatter to ch and fh
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

    # 'application' code
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warn('warn message')
    # logger.error('error message')
    # logger.critical('critical message')
