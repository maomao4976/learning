# -*- coding: UTF-8 -*-
# Author  : Liushuai
# Time    : 2020/2/23 17:30
# File    : main.py

from . import logics
from .auth import authenticate
from .logger import logger
from .utils import print_error

transaction_logger = logger("transaction")
access_logger = logger("access")

features = [
    ('账户信息', logics.view_account_info),
    ('取现', logics.with_draw),
    ('还款', logics.pay_back),
]


def controller(user_obj):
    """功能分配"""
    while True:
        for index, feature in enumerate(features):
            print(index, feature[0])
        choice = input("ATM>>: ").strip()
        if not choice: continue
        if choice.isdigit():
            choice = int(choice)
            if len(features) > choice >= 0:
            #  if choice < len(features) and choice >= 0:
                features[choice][1](user_obj, transaction_logger=transaction_logger, access_logger=access_logger)
        if choice == 'exit':
            exit("Bye.")


def entrance():
    """ATM程序交互入口"""
    user_obj = {  # 用户对象字典
        'is_authenticated': False,  # 用户是否已认证
        'data': None
    }
    retry_count = 0
    while user_obj['is_authenticated'] is not True:  # 代表没认证
        account = input("\033[32;1maccount:\033[0m").strip()
        password = input("\033[32;1mpassword:\033[0m").strip()
        auth_data = authenticate(account, password)  # 验证
        if auth_data:  # not None means passed the authentication  说明此时已经拿到了账户数据 auth_data 就是账户数据
            user_obj['is_authenticated'] = True  # 意味着其他函数直接可以通过uesr_obj就能知道用户是否登录
            user_obj['data'] = auth_data
            print("Welcome")
            access_logger.info("user %s just logged in" % user_obj['data']['id'])

            controller(user_obj)

        else:  # None
            print_error("Wrong username or password!")
        retry_count += 1

        if retry_count == 3:
            msg = "user %s tried wrong password reached 3 times" % account
            print_error(msg)
            access_logger.info(msg)
            break
