# _*_ coding: utf-8 _*_
 
import json
 
acc_dic = {
    'id':1234,
    'password':'abc',
    'credit':15000,
    'balance':15000,
    'enroll_date':'2018-01-01',
    'expire_date':'2023-01-01',
    # 'pay_day':22,  #支付日期（但是现在没有要求，可以不考虑）
    'status':0      #0 = naormal,1 = locked , 2 = disabled
}
print(acc_dic,type(acc_dic))
a = json.dumps(acc_dic)
print(a,type(a))