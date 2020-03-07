# -*- coding: UTF-8 -*-
# Author  : Liushuai
# Time    : 2020/2/23 19:35
# File    : settings.py

import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = "%s/db/account" % BASE_DIR

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'transaction': 'transaction.log',
    'access': 'access.log',
}
LOG_PATH = os.path.join(BASE_DIR, 'logs')
LOG_FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TRANSACTION_TYPE = {
    'repay': {'action': 'plus', 'interest': 0},
    'withdraw': {'action': 'minus', 'interest': 0.05},
    'transfer': {'action': 'minus', 'interest': 0.05},
    'consume': {'action': 'minus', 'interest': 0},
}
