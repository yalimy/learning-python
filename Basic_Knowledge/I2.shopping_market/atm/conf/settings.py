# _*_ coding: utf-8 _*_
'''初始化的配置'''
 
import logging
import os
import sys
 
#到ATM目录，方便后面创建账户文件
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
 
DATABASE = {
    'engine':'file_storage',       #文件存储，这里可扩展成数据库形式的
    'name':'accounts',              #db下的文件名
    'path':'%s/db' %BASE_DIR
}
 
LOGIN_LEVEL = logging.INFO     #初始化日志记录级别为INFO，INFO以下的可以直接打印
#日志类型
LOGIN_TYPE = {
    'access':'access.log',
    'transaction':'transaction.log'
}
 
TRANSACTION_TYPE = {
    'repay':{'action':'plus','interest':0},
    'withdraw':{'action':'minus','interest':0.05},
    'transfer':{'action':'minus','interest':0.05},
    'consume':{'action':'minus','interest':0},
}