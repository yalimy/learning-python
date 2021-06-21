# _*_ coding: utf-8 _*_
 
import os
import json
import time
 
from core import accounts
from core import db_handler
from conf import settings
from bin import atm_manage
from core import atm_main
 
 
def access_auth(account,password,log_obj):
    '''
    下面access_login调用access_auth方法，用于登陆
    :param account: 用户名
    :param password: 密码
    :return: 如果为超期，返回字典，超期则打印相应提示
    '''
    db_path = db_handler.db_handler(settings.DATABASE)       #调用db_handle下的handle方法，返回路径/db/accounts
    account_file = '%s/%s.json'%(db_path, account)     #用户文件
    #判断文件和i否存在，如果存在的话 则执行下面的
    if os.path.isfile(account_file):        #如果用户文件存在（即用户存在）
        with open(account_file,'r',encoding='utf-8') as f:  #打开文件
            account_data = json.load(f)     #file_data为字典形式
            if account_data['password']  == password:
                expire_time = time.mktime(time.strptime(account_data['expire_date'],'%Y-%m-%d'))
                if time.time() > expire_time:        #如果信用卡已经过期，当前时间戳大于国企的时间戳
                    log_obj.error("Account [%s] had expired,Please contract the bank" % account)
                    print("\033[31;1mAccount %s had expired,Please contract the bank"%account)
                else:       #信用卡未过期，返回用户数据的字典
                    log_obj.info("Account [%s] logging success" % account)
                    return account_data
            else:
                log_obj.error("Account or Password does not correct!")
                print("\033[31;1mAccount or Passwordoes not correct!\033[0m")
    else:       #用户不存在
        log_obj.error("Account [%s] does not exist!" % account)
        print("\033[31;1mAccount [%s] does not exist!\033[0m"%account)
 
def access_login(user_data,log_obj):
    '''
    用户登陆，当登陆失败超过三次
    :param user_date:main.py里面的字典，用户信息数据，只存在内存中
    :return:若用户账号密码正确，且信用卡未过期，则返回用户数据的字典
    '''
    retry_count = 0
    while  user_data['is_authenticated'] is not True and retry_count < 3:
        account = input('\033[32;1mplease input Acount:\033[0m').strip()
        password = input('\033[32;1mplease input Password:\033[0m').strip()
        #用户账号密码正确而且信用卡未过期，返回用户数据的字典
        auth = access_auth(account, password,log_obj)
        if auth:
            user_data['is_authenticated'] = True        #用户认证为True
            user_data['account_id'] = account            #用户账号ID为账号名
            # print("welcome")
            return auth
        retry_count += 1
    else:
        print("Account [%s] try logging too many times..."%account)
        log_obj.error("Account [%s] try logging too many times..." % account)
        exit()