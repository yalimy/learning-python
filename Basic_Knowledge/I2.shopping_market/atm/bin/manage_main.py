# _*_ coding: utf-8 _*_
'''管理端，提供管理接口，包括添加账户，用户额度，冻结账户，解冻账户'''
import os
import sys
import json
 
from core import auth
from core import accounts
from core import transaction
from core import db_handler
from conf import settings
 
 
# 解冻账户
def unlock_account():
    '''解冻账户的初步思路是读取用户文件，把status的状态一更改就ok '''
    account = input("\033[34;1mPlease input the account that you want to unlock:\033[0m")
    read_data = unlock_accountcore(account)
    return read_data
 
 
def unlock_accountcore(account):
    '''
    解冻账户，读取用户文件，读到status，把状态更改为0
    #0 = naormal,1 = locked ,
    :param account:
    :return:
    '''
    # 调用db_handle下的handle方法，返回路径/db/accounts
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = '%s/%s.json' % (db_path, account)
    account_new = '%s/%s.json' % (db_path, account)
    if os.path.isfile(account_file):
        with open(account_file, 'r', encoding='utf-8') as f:
            account_data = json.load(f)
            account_data['status'] = 0
        with open(account_new, 'w', encoding='utf-8') as fnew:
            new_data = json.dump(account_data, fnew)
 
 
# 冻结账户
def lock_account():
    '''
    冻结账户，思路与解冻刚好相反
    :param acc_data:
    :return:
    '''
    account = input("\033[34;1mPlease input the account that you want to lock:\033[0m")
    read_data = lock_accountcore(account)
    return read_data
def lock_accountcore(account):
    '''
    冻结账户，读取用户文件，读到status，把状态更改为1
    #0 = naormal,1 = locked ,
    :param account:
    :return:
    '''
    # 调用db_handle下的handle方法，返回路径/db/accounts
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = '%s/%s.json' % (db_path, account)
    account_new = '%s/%s.json' % (db_path, account)
    if os.path.isfile(account_file):
        with open(account_file, 'r', encoding='utf-8') as f:
            account_data = json.load(f)
            account_data['status'] = 1
        with open(account_new, 'w', encoding='utf-8') as fnew:
            new_data = json.dump(account_data, fnew)
 
# 添加账户
def add_account():
    '''
    添加账户，是admin添加的用户，下次就可以登陆添加的账户了
    :return:
    '''
    acc_dic = {
        'id':None,
        'balance':None,
        'password': None,
        'credit': None,
        'enroll_date': None,
        'expire_date': None,
        'status': None  # 0 = naormal,1 = locked , 2 = disabled
    }
    menu = {
        0:"请输入要添加的账户：",
        1:"请输入要添加的余额：",
        2:"请输入要添加的密码：",
        3:"请输入要添加的信用额度(only more than 0)",
        4:"请输入要添加的办卡日期(such as 2018-8-8)",
        5:"请输入要添加的卡到期时间(such as 2018-8-8)",
        6:"请输入是否锁定添加账号的状态(only input 0 or 1)",
    }
    menu_user = {
        0: "id",
        1: "balance",
        2: "password",
        3: "credit",
        4: "enroll_date",
        5: "expire_date",
        6: "status",
    }
    print("\033[31;1m\t\twelcome to add account\033[0m")
    print('*'.center(40,'*'))
    for i in range(7):
        data = input('%s'%menu[i]).strip()
        acc_dic["%s" % menu_user[i]] = data
    accounts.dump_account(acc_dic)
    print("\033[32;1mcongratulations  you account was created successfully\033[0m")
    return True
# 退出程序
def logout():
    '''
    退出登陆
    :return:
    '''
    print("\033[32;1m-------Looking forward to your next visit-------\033[0m")
    exit()
 
def auth_login():
    '''
    登陆管理员密码账号
    :return:
    '''
    print("\033[34;1m-------Welcome into the management interface--------\033[0m")
    managename = input("\033[34;1mplease input Username：\033[0m")
    password = input("\033[34;1mplease input Password：\033[0m")
    account = account_auth(managename,password)
    return account
 
def account_auth(managename,password):
    '''
    管理员认证信息
    {"id": admin,"password": "root" }
    :return:
    '''
    db_path = db_handler.db_handler(settings.DATABASE)  # 调用db_handle下的handle方法，返回路径/db/accounts
    managename_file = '%s/%s.json'%(db_path,managename)
    if os.path.isfile(managename_file):
        with open(managename_file,'r',encoding='utf-8') as f:
            manage_data = json.load(f)
            # print(manage_data)
            if manage_data['password'] == password:
                print("\033[31;1m-------Welcome to the administrator--------\033[0m")
                return manage_interactive(managename)
            else:
                print("\033[31;1mAccount or Passwordoes not correct!\033[0m")
 
# 管理界面主程序
def manage_interactive(managename):
    menu = '''
    \033[31;1m-----------management console-----------
            1，add_account        
            2，lock_account
            3，unblock_account
            4, exit\033[0m'''
    menu_dic = {
    '1':add_account,
    '2':lock_account,
    '3':unlock_account,
    '4': logout
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input('please input your choice>>>').strip()
        if user_option in menu_dic:
            print(menu_dic[user_option]())
 
        else:
            print("\033[31;1mYou choice doesn't exist!\033[0m")
 
def run_manage():
    '''
    当程序启动的时候调用，主要用于实现主要交互逻辑，客户认证登陆
    :return:
    '''
    auth_login()