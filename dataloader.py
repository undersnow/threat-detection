# encoding:utf-8 


# 需要注意的是，再提取记录时不包括ID与内容数据，即
# Logon: date,user,pc,activity
# File: date,user,pc,filename,activity,to_removable_media,from_removable_media
# HTTP: date,user,pc,url
# Email:  date,user,pc,to,cc,bcc,from,activity,size,attachments
# Device: date,user,pc,file_tree,activity
# 实际编写时需要重新确认原始数据格式与要提取的数据格式

import os # 用于创建目录等应用
import sys # 用于返回当前目录，以及关闭程序等
import pandas as pd
import numpy as np
import User_Month_Day_Extract
import tqdm
# 开始上述程序编写
dataset_path = r'E:\eclipse-workspace\my_project\r4.2'
CERT_LDAP__path = r'E:\eclipse-workspace\my_project\r4.2\LDAP'
#all the user name 1000
'''
user_name=pd.read_csv(dataset_path+"\\psychometric.csv",usecols=["user_id"])
print(len(user_name))
print("Loading Devices", flush=True)
devices = pd.read_csv(dataset_path + "\\device.csv", index_col=2)
print("Loading Emails", flush=True)
emails = pd.read_csv(dataset_path + "\\email.csv", index_col=2)
print("Loading Files", flush=True)
files = pd.read_csv(dataset_path + "\\file.csv", index_col=2)
print("Loading Logons", flush=True)
logons = pd.read_csv(dataset_path + "\\logon.csv", index_col=2)
print("Loading Http", flush=True)
#fields = ["date", "user", "url"]
https = pd.read_csv(dataset_path + "\\http.csv",  index_col=2)
print("Finished Loading", flush=True)
'''
logon_path = dataset_path + '\\' + 'logon.csv'
file_path = dataset_path + '\\' + 'file.csv'
http_path = dataset_path + '\\' + 'http.csv'
email_path = dataset_path + '\\' + 'email.csv'
device_path = dataset_path + '\\' + 'device.csv'


result_path = r'E:\eclipse-workspace\my_project\CERT4.2_resulthhhhhhh'  # CERT5.2数据的存放位置，不更新到GitHub
if os.path.exists(result_path) == False:
    os.makedirs(result_path)
'''
for i in range(2):#range(len(user_name)):
    # 第一件工作是获得用户的两个时间列表
    #user=user_name.iloc[i][0]
    user=userd[i]
    print(user)
    user_path = result_path + '\\' + user
    if os.path.exists(user_path) == False:
        os.makedirs(user_path)
    for origin_dataset in [devices, files,emails,https,logons]:
        data_to_write=pd.DataFrame()
        print(user in origin_dataset.index)
        if user in origin_dataset.index:
            data_to_write=data_to_write.append(devices.loc[user])
            print(data_to_write)
            data_to_write.to_csv(user_path+'\\origin_sequence.csv', mode='a', header=True)
    '''
with open(logon_path, 'r') as f:
    for line in f:
        line_lst = line.strip('\n').strip(',').split(',')
        # Logon原始数据格式：id,date,user,pc,activity
        # Logon目标数据格式：Logon: date,user,pc,activity
        if line_lst[2] == 'user':
            continue
        
        y, m, d = User_Month_Day_Extract.Extract_Date(line_lst[1])
        data0=y+"-"+m+"-"+d
        if os.path.exists(result_path + '\\' + line_lst[2] + '\\' + data0) == False:
                os.makedirs(result_path + '\\' + line_lst[2] + '\\' + data0)
        f_day_path = result_path + '\\' + line_lst[2] + '\\' + data0+ '\\Logon.csv'
        f_day = open(f_day_path, 'a')
        for ele in line_lst[1:]:
            f_day.write(ele)
            f_day.write(',')
        f_day.write('\n')
        f_day.close()
print('......<<<<<<Logon数据写入完毕>>>>>>......')

with open(device_path, 'r') as f:
    for line in f:
        line_lst = line.strip('\n').strip(',').split(',')
        # Logon原始数据格式：id,date,user,pc,activity
        # Logon目标数据格式：Logon: date,user,pc,activity
        if line_lst[2] == 'user':
            continue
        
        y, m, d = User_Month_Day_Extract.Extract_Date(line_lst[1])
        data0=y+"-"+m+"-"+d
        if os.path.exists(result_path + '\\' + line_lst[2] + '\\' + data0) == False:
                os.makedirs(result_path + '\\' + line_lst[2] + '\\' + data0)
        f_day_path = result_path + '\\' + line_lst[2] + '\\' + data0+ '\\device.csv'
        f_day = open(f_day_path, 'a')
        for ele in line_lst[1:]:
            f_day.write(ele)
            f_day.write(',')
        f_day.write('\n')
        f_day.close()
print('......<<<<<<device数据写入完毕>>>>>>......')

with open(http_path, 'r') as f:
    for line in f:
        line_lst = line.strip('\n').strip(',').split(',')
        # Logon原始数据格式：id,date,user,pc,activity
        # Logon目标数据格式：Logon: date,user,pc,activity
        if line_lst[2] == 'user':
            continue
        
        y, m, d = User_Month_Day_Extract.Extract_Date(line_lst[1])
        data0=y+"-"+m+"-"+d
        if os.path.exists(result_path + '\\' + line_lst[2] + '\\' + data0) == False:
                os.makedirs(result_path + '\\' + line_lst[2] + '\\' + data0)
        f_day_path = result_path + '\\' + line_lst[2] + '\\' + data0+ '\\http.csv'
        f_day = open(f_day_path, 'a')
        for ele in line_lst[1:-1]:
            f_day.write(ele)
            f_day.write(',')
        f_day.write('\n')
        f_day.close()
print('......<<<<<<http数据写入完毕>>>>>>......')

with open(email_path, 'r') as f:
    for line in f:
        line_lst = line.strip('\n').strip(',').split(',')
        # Logon原始数据格式：id,date,user,pc,activity
        # Logon目标数据格式：Logon: date,user,pc,activity
        if line_lst[2] == 'user':
            continue
        
        y, m, d = User_Month_Day_Extract.Extract_Date(line_lst[1])
        data0=y+"-"+m+"-"+d
        if os.path.exists(result_path + '\\' + line_lst[2] + '\\' + data0) == False:
                os.makedirs(result_path + '\\' + line_lst[2] + '\\' + data0)
        f_day_path = result_path + '\\' + line_lst[2] + '\\' + data0+ '\\email.csv'
        f_day = open(f_day_path, 'a')
        for ele in line_lst[1:-1]:
            f_day.write(ele)
            f_day.write(',')
        f_day.write('\n')
        f_day.close()
print('......<<<<<<email数据写入完毕>>>>>>......')

with open(file_path, 'r') as f:
    for line in f:
        line_lst = line.strip('\n').strip(',').split(',')
        # Logon原始数据格式：id,date,user,pc,activity
        # Logon目标数据格式：Logon: date,user,pc,activity
        if line_lst[2] == 'user':
            continue
        
        y, m, d = User_Month_Day_Extract.Extract_Date(line_lst[1])
        data0=y+"-"+m+"-"+d
        if os.path.exists(result_path + '\\' + line_lst[2] + '\\' + data0) == False:
                os.makedirs(result_path + '\\' + line_lst[2] + '\\' + data0)
        f_day_path = result_path + '\\' + line_lst[2] + '\\' + data0+ '\\file.csv'
        f_day = open(f_day_path, 'a')
        for ele in line_lst[1:-1]:
            f_day.write(ele)
            f_day.write(',')
        f_day.write('\n')
        f_day.close()
print('......<<<<<<file数据写入完毕>>>>>>......')