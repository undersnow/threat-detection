# encoding:utf-8 
import os

'''
 Logon: date,user,pc,activity
 File: date,user,pc,filename,activity,to_removable_media,from_removable_media
 HTTP: date,user,pc,url
 Email:  date,user,pc,to,cc,bcc,from,activity,size,attachments
 Device: date,user,pc,file_tree,activity
'''


dataset_path = r'E:\eclipse-workspace\my_project\r4.2'
result_path = r'test000'#'r'E:\eclipse-workspace\my_project\CERT4.2_resulthhhhhhh'  

#all the user name 1000

logon_path = dataset_path + '\\' + 'logon.csv'
file_path = dataset_path + '\\' + 'file.csv'
http_path = dataset_path + '\\' + 'http.csv'
email_path = dataset_path + '\\' + 'email.csv'
device_path = dataset_path + '\\' + 'device.csv'

# 01/01/2010 01:01:01
def extract_date(date):
    year = date[6:10]
    day= date[3:5]
    month = date[:2]
    return year, month, day

if os.path.exists(result_path) == False:
    os.makedirs(result_path)

with open(logon_path, 'r') as f:
    for line in f:
        line_lst = line.strip('\n').strip(',').split(',')
        if line_lst[2] == 'user':
            continue
        
        y, m, d = extract_date(line_lst[1])
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
print("-------logon finished---------")

with open(device_path, 'r') as f:
    for line in f:
        line_lst = line.strip('\n').strip(',').split(',')
        if line_lst[2] == 'user':
            continue
        
        y, m, d = extract_date(line_lst[1])
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
print("-------device finished---------")

with open(http_path, 'r') as f:
    for line in f:
        line_lst = line.strip('\n').strip(',').split(',')
        if line_lst[2] == 'user':
            continue
        
        y, m, d = extract_date(line_lst[1])
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
print("-------http finished---------")

with open(email_path, 'r') as f:
    for line in f:
        line_lst = line.strip('\n').strip(',').split(',')
        if line_lst[2] == 'user':
            continue
        
        y, m, d = extract_date(line_lst[1])
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
print("-------email finished---------")

with open(file_path, 'r') as f:
    for line in f:
        line_lst = line.strip('\n').strip(',').split(',')
        if line_lst[2] == 'user':
            continue
        
        y, m, d = extract_date(line_lst[1])
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
print("-------file finished---------")