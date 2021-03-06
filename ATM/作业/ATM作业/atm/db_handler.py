# -*- coding: UTF-8 -*-
# Author  : Liushuai
# Time    : 2020/2/23 19:16
# File    : db_handler.py

import json
import os

from 作业.ATM作业.conf import settings


def load_account_data(account):
    """根据account id 找到对应的账户文件，并加载"""
    account_file = os.path.join(settings.DB_PATH, "%s.json" % account)
    if os.path.isfile(account_file):
        f = open(account_file)
        data = json.load(f)
        f.close()
        return {'status': 0, 'data': data}
    else:
        return {'status': -1, 'error': "account file does not exist."}


def save_db(account_data):
    """根据account_data找到对应的账户文件，把内存里的用户数据保存到硬盘"""

    account_file = os.path.join(settings.DB_PATH, "%s.json" % account_data['id'])
    if os.path.isfile(account_file):
        f = open("%s.new" % account_file, 'w')
        data = json.dump(account_data, f)
        f.close()
        os.remove(account_file)                              # 自己添加的，不然报错
        os.rename("%s.new" % account_file, account_file)
        return {'status': 0, 'data': data}
    else:
        return {'status': -1, 'error': "account file does not exist."}
