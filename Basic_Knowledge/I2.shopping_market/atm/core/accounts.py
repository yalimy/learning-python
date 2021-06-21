# _*_ coding: utf-8 _*_
import os
import sys
import json
import logging
import time
import datetime
 
 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  #添加环境变量
 
from core import auth
from core import db_handler
from conf import settings
 
 
def load_current_balance(account_id):
    '''
     # 把数据load下，返回账户余额和其他基础信息
    :param account_id: 用户账户的名字
    :return: 返回最新读到的数据文件中的最新数据
    '''
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json"%(db_path,account_id)
    with open(account_file,'r',encoding='utf-8') as f:
        acc_data = json.load(f)
        return acc_data
 
def  dump_account(account_dic):
    '''
    在更新完后，把数据dump到文件中,文件地址为\atm-learn/db/accounts
    :param account_data:
    :return:
    '''
    db_path =db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" %(db_path,account_dic['id'])
    with open(account_file,'w',encoding='utf-8') as f:
        acc_data = json.dump(account_dic,f)