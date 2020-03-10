# encoding:utf-8 
import os # 用于创建目录等应用
import sys # 用于返回当前目录，以及关闭程序等
import pandas as pd
import numpy as np
import User_Month_Day_Extract
import tqdm
import glob
import re
# 该模块将每个用户的文件转换成序列
# 保存csv文件
#  用户ID，日期，序列
# AAE0190，2011-05-16，1 2 3，
import sys
import math


assigned_pc_dictionary={}

def progress_bar(portion, total):
    """
    total 总数据大小，portion 已经传送的数据大小
    :param portion: 已经接收的数据量
    :param total: 总数据量
    :return: 接收数据完成，返回True
    """
    part = total / 50  # 1%数据的大小
    count = math.ceil(portion / part)
    
    print(('[%-50s]%.2f%%' % (('>' * count), portion / total * 100)))#,end="")
    
    
    if portion >= total:
        print('all done !!! \n')
        return True


dataset_path = r'E:\eclipse-workspace\my_project\r4.2'
CERT_LDAP__path = r'E:\eclipse-workspace\my_project\r4.2\LDAP'
result_path = r'E:\eclipse-workspace\my_project\CERT4.2_resulthhhhhhh'
users_all=os.listdir(result_path)
each_user_path={}#each user
date_path={}#each user and the date
count=0
for each_user in users_all:#each_user 用户ID
    each_user_path[each_user]=os.path.join(result_path,each_user)
    date_path[each_user]=os.listdir(each_user_path[each_user])
    count+=1
    progress_bar(count,1000)

    #print(date_path[each_user][i])  2011-05-16
    daily_actions_path=os.path.join(each_user_path[each_user],date_path[each_user][0])#E:\eclipse-workspace\my_project\CERT4.2_resulthhhhhhh\ZKS0899\2011-05-16
    daily_actions_file=os.listdir(daily_actions_path)
    #print(daily_actions_file)
    #input("d")
    for i in daily_actions_file:     
        if i=='http.csv':
            current_csv=pd.read_csv(daily_actions_path+"\\"+i,names=['date','user','pc','url'],index_col=False)
            assigned_pc_dictionary[current_csv.iloc[0]['user']]=current_csv.iloc[0]['pc']
            break
        elif i=='Logon.csv':
            current_csv=pd.read_csv(daily_actions_path+"\\"+i,names=['date','user','pc','url'],index_col=False)
            assigned_pc_dictionary[current_csv.iloc[0]['user']]=current_csv.iloc[0]['pc']    
            break       
        

result_assigned_pc=pd.DataFrame(pd.Series(assigned_pc_dictionary),columns=['pc'])
result_assigned_pc=result_assigned_pc.reset_index().rename(columns={'user':'pc'})

#print(result_assigned_pc)
result_assigned_pc.to_csv(r'E:\eclipse-workspace\my_project\assigned_pc\device_dictionary.csv',header=0,index=0)
print("finished!!!")