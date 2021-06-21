# _*_ coding: utf-8 _*_ #

import os
import sys

# 添加父路径到系统变量
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 将 main.py 里面的所有代码封装成 main 变量
from core import atm_main

if __name__ == '__main__':
    atm_main.run_atm()
    
