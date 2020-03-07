# -*- coding: UTF-8 -*-
# Author  : Liushuai
# Time    : 2020/2/23 19:16
# File    : auth.py

from .db_handler import load_account_data


def authenticate(accont, password):
    """对用户信息进行验证"""
    account_data = load_account_data(accont)
    if account_data['status'] == 0:  # 代表账户文件加载成功
        account_data = account_data['data']  # 真正的用户数据
        if password == account_data['password']:  # 代表认证成功
            return account_data  # 为什么在这里返回账户数据？为了方便后续对账户的操作，直接在内存中进行，以免再次读取
        else:
            return None
    else:
        # print_error(account_data['error'])
        return None
