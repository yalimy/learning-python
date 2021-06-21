# _*_ coding: utf-8 _*_
import os
import sys
 
#添加环境变量
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #找到路径
sys.path.append(BASE_DIR)          #添加路径
 
 
from core import manage_main
'''管理程序的执行文件'''
 
if __name__ == '__main__':
    manage_main.run_manage()