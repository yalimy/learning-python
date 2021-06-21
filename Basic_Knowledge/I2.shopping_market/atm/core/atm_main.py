# _*_ coding: utf-8 _*_ #
''' 主逻辑交换模块 '''
import logging
import sys
from core import auth
from core import logger
from core import accounts
from core import transaction
from core import db_handler

# 用户信息
user_data = {
    'account_id' : None,
    'is_authenticated' : False,
    'account_data' : None
}

# 日志记录
access_logger = logger.logger('access')
trans_logger = logger.logger('transaction')

def account_info(func):
    # 检查账户有效性，并确认是否被锁
    def wrapper(acc_data):
        account_id = acc_data["account_id"]
        account_data = acc_data["account_data"]
        status = acc_data["account_data"]["status"]
        if int(status) == 0:
            func(acc_data)
            return True
        else:
            print('\033[32;1msorry your account was locked\033[0m')
            exit()
     
    return wrapper


@account_info
def disp_account_info(acc_data):
    # 展示 user info
    print('---------- user info -------------')
    for i in acc_data['account_data']:
        print("{:^20}:\033[32;1m{:^20}\033[0m".format(i, acc_data['account_data'][i]))

        
@account_info
def repay(acc_data):
    # 退款
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = '''------------BALANCE INFO ------------
     Credit :     %s
     Balance:     %s''' %(account_data['credit'],account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        repay_amount = input("\033[32;1mInput repay amout('b' is back):\033[0m").strip()
        if len(repay_amount) > 0 and repay_amout.isdigit():
            new_balance = transaction.make_transaction(trans_logger,account_data,'repay',repay_amout)
            if new_balance:
                print("\033[31;1mNew Balance:%s\033[0m" % (new_balance['balance']))
         elif repay_amount == 'b':
            back_flag = True
         else:
            print("\033[31;1m%s is not valid amount, only accept integer\033[0m" % repay_amount)

            
@account_info
def withdraw(acc_data):
    # 取钱
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = '''------------BALANCE INFO ------------
     Credit :     %s
     Balance:     %s''' %(account_data['credit'],account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        withdraw_amount = input("\033[32;1mInput withdraw amout('b' is back):\033[0m").strip()
        if len(withdraw_amount) > 0 and withdraw_amout.isdigit():
            new_balance = transaction.make_transaction(trans_logger,account_data,'repay',withdraw_amout)
            if new_balance:
                print("\033[31;1mNew Balance:%s\033[0m" % (new_balance['balance']))
         elif withdraw_amount == 'b':
            back_flag = True
         else:
            print("\033[31;1m%s is not valid amount, only accept integer\033[0m" % withdraw_amount)
            
            
@account_info
def transfer(acc_data):
    # 转账
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = '''---------------------BALANCE INFO-----------------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        transfer_amount = input("\033[33;1mInput transfer amount(input 'b' is back):\033[0m").strip()
        if len( transfer_amount) > 0 and  transfer_amount.isdigit():
            new_balance = transaction.make_transaction(
                trans_logger, account_data, 'transfer',  transfer_amount)
            if new_balance:
                print('''\033[32;1mNEW Balance:%s\033[0m''' % (new_balance['balance']))
        elif transfer_amount == 'b':
            back_flag = True
        else:
            print('\033[31;1m[%s] is not a valid amount , only accept integer\033[0m' % transfer_amount)
 
@account_info
def paycheck(acc_data):
    '''账单检查,记录每月日常消费流水'''
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = '''---------------------BALANCE INFO-----------------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
 
 
@account_info
def logout(acc_data):
    '''退出登陆'''
    print("\033[32;1m-------Looking forward to your next visit-------\033[0m")
    exit()
    
    
def interactive(acc_data):
    '''用户交互'''
    msg = (
        '''
        ------------------CHINA BANK --------------
                        \033[31;1m1.账户信息
                        2.存款
                        3.取款
                        4.转账
                        5.账单
                        6.退出
        \033[0m'''
    )
    menu_dic = {
        "1":disp_account_info,
        "2":repay,
        "3":withdraw,
        "4":transfer,
        "5":paycheck,
        "6":logout,
    }
    exit_flag = False
    while not exit_flag:
        print(msg)
        user_choice = input(">>>>").strip()
        if user_choice in menu_dic:
            menu_dic[user_choice](acc_data)
        else:
            print("\033[31;1mYou choice doesn't exist!\033[0m")
            
            
def run_atm():
    '''当程序启动时候，调用，主要用于实现主要交互逻辑'''
    # 调用认证模块，返回用户文件json.load后的字典，传入access_logger日志对象
    access_data = auth.access_login(user_data,access_logger)
 
    if user_data['is_authenticated']:       #如果用户认证成功
        user_data["account_data"] = access_data
        interactive(user_data)      #用户交互开始