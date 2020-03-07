# -*- coding: UTF-8 -*-
# Author  : Liushuai
# Time    : 2020/2/23 19:17
# File    : transaction.py

from 作业.ATM作业.conf import settings
from .db_handler import save_db

def make_transaction(logger,user_obj,tran_type,amount,**kwargs):
    """
    deal all the user transactions
    :param account_data: user account data
    :param tran_type: transaction type
    :param amount: transaction amount
    :param kwargs: mainly for logging usage
    :return:
    """
    global new_balance
    amount = float(amount)
    if tran_type in settings.TRANSACTION_TYPE:
        interest = amount * settings.TRANSACTION_TYPE[tran_type]['interest']  # 算出利息
        old_balance = user_obj['data']['balance']
        if settings.TRANSACTION_TYPE[tran_type]['action'] == 'plus':
            new_balance =old_balance + amount + interest
        elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'minus':
            new_balance = old_balance -amount - interest
            # check credit
            if new_balance < 0 :
                print('''\033[31,1mYour credit [%s] is not enough for this transaction [-%s],your current balance is
                [%s]''' %(user_obj['data']['credit'],(amount + interest),old_balance))
                return {'status':1,'error':'交易失败，余额不足'}

        user_obj['data']['balance'] = new_balance  # 把新余额存到用户内存账户数据里
        save_db(user_obj['data']) # 数据实时更新到磁盘账户文件中

        logger.info("account:%s   action:%s   amount:%s  interest:%s  balance:%s" %
                    (user_obj['data']['id'],tran_type,amount,interest,new_balance))
        return {'status':0, 'msg':'交易操作成功'}
    else:
        print("\033[31;1mTransaction type [%s] is not exist!\033[0m" % tran_type)
        return {'status':1,'error':'交易失败,Transaction type [%s] is not exist!' % tran_type}