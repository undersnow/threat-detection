# encoding:utf-8 

import os # 用于创建目录等应用
import sys # 用于返回当前目录，以及关闭程序等
import pandas as pd
import numpy as np
import User_Month_Day_Extract
import tqdm
import glob
import re
import time
# 该模块将每个用户的文件转换成序列
# 保存csv文件
#  用户ID，日期，序列
# AAE0190，2011-05-16，1 2 3，
import sys
import math
LOGON=1
LOGOFF=2
EXE=3
DOC=4
PDF=5
TXT=6
JPG=7
ZIP=8
NEUTRAL=9
HACKTIVIST=10
JOBHUNTING=11
INTERNAL_EMAIL=12
EXTERNAL_EMAIL=13
CONNECT=14
DISCONNECT=15
BASIC_EVENT_COUNT=15
dataset_path = r'E:\eclipse-workspace\my_project\r4.2'
CERT_LDAP__path = r'E:\eclipse-workspace\my_project\r4.2\LDAP'
result_path = r'E:\eclipse-workspace\my_project\CERT4.2_resulthhhhhhh'

#print(insider_dictionary)
threat_data=[]
non_threat_data=[]
result_threat={1:threat_data,0:non_threat_data}


assigned_pc_dictionary={}
pc_csv=pd.read_csv(r'E:\eclipse-workspace\my_project\assigned_pc\device_dictionary.csv',names=['user','pc'],index_col=False)
#print(pc_csv['user'])
#assigned_pc_dictionary=dict(zip(list(pc_csv['user']), list(pc_csv['pc'])))
#print(assigned_pc_dictionary)         
#input("ddd")

#print(pc_csv['user'])
assigned_pc_dictionary=dict(zip(list(pc_csv['user']), list(pc_csv['pc'])))

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


    
    


users_all=os.listdir(result_path)
each_user_path={}#each user
date_path={}#each user and the date
count=0
insider_dictionary = np.load('insider_dictionary.npy').item()


def threat_judge(date,user): 
    if user in insider_dictionary.keys():
        y, m, d = User_Month_Day_Extract.Extract_Date(date)
        regular_date=y+"-"+m+"-"+d
        for i in insider_dictionary[user]:
            if i==regular_date:
                return True    
    return False
    
    
for each_user in users_all:#each_user 用户ID
    each_user_path[each_user]=os.path.join(result_path,each_user)
    date_path[each_user]=os.listdir(each_user_path[each_user])
    count+=1
    if each_user not in list(insider_dictionary.keys()):
        continue
    
    progress_bar(count,1000)
    print("当前时间： ",time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time())))
    for i in range(len(date_path[each_user])):
        final_list=[]
        #print(date_path[each_user][i])  2011-05-16
        daily_actions_path=os.path.join(each_user_path[each_user],date_path[each_user][i])#E:\eclipse-workspace\my_project\CERT4.2_resulthhhhhhh\ZKS0899\2011-05-16
        daily_actions_file=os.listdir(daily_actions_path)
        dataframe_list=[]
        for i in daily_actions_file:     
            if i=='email.csv':
                #print("email")
                current_csv=pd.read_csv(daily_actions_path+"\\"+i,names=['date','user','pc','to','cc','bcc','from','size','attachments'],index_col=False)#date,user,pc,to,cc,bcc,from,activity,size,attachments
                changed_data=current_csv[['date','user','pc','to','cc','bcc','from']]
                result_data=current_csv[['date','user','pc']]
                event_list = np.zeros(changed_data.shape[0],int)
                for i in range(len(event_list)):
                    event_list[i]=INTERNAL_EMAIL
                for j in range(changed_data.shape[0]):
                    for k in ['to','cc','bcc','from']:
                        #print(changed_data.iloc[j][k])
                        if pd.isnull(changed_data.iloc[j][k]):
                            continue
                        elif re.match(r"^[a-zA-Z0-9_.-]+@dtaa.com(;[a-zA-Z0-9_.-]+@dtaa.com)*$",changed_data.iloc[j][k]):
                            continue
                        else:
                            event_list[j]=EXTERNAL_EMAIL
                            break
                #print("--------------")
                result_data.insert(2,'event', event_list)
                #print(result_data)  
                #input("email finished")  
            elif i=='http.csv':
                #print("http")
                current_csv=pd.read_csv(daily_actions_path+"\\"+i,names=['date','user','pc','url'],index_col=False)#date,user,pc,to,cc,bcc,from,activity,size,attachments
                changed_data=current_csv[['date','user','pc','url']]
                result_data=current_csv[['date','user','pc']]
                event_list = np.zeros(changed_data.shape[0],int)
                for i in range(len(event_list)):
                    event_list[i]=NEUTRAL
                #print(changed_data)
                for j in range(changed_data.shape[0]):
                    #print(changed_data.iloc[j]['url'])
                    if pd.isnull(changed_data.iloc[j]['url']):
                        continue
                    elif re.search(r"(wikileaks|spectorsoft|keylog|softactivity|webwatchernow|wellresearchedreviews|moniter|surveillance|www.relytec.com|www.best-spy-soft|www.refog.com)",changed_data.iloc[j]['url']):
                        event_list[j]=HACKTIVIST
                        #input("true")
                        continue
                    elif re.search(r"(jobhunter|craigslist|monster.com|linkedin|indeed.com|boeing.com|raytheon|aol.com|northropgrumman|hp.com|harris.com|simplyhired|lockheedmartin|hotjob|job-hunt|beyond.com|idealist.org|careerbuilder)",changed_data.iloc[j]['url']):
                        event_list[j]=JOBHUNTING
                        
                #print("--------------")
                result_data.insert(2,'event', event_list)
                #print(result_data)  
                #input("http finished") 
            elif i=='Logon.csv':
                #print("logon begin")
                current_csv=pd.read_csv(daily_actions_path+"\\"+i,names=['date','user','pc','event'],index_col=False)
                changed_data=current_csv[['date','user','pc','event']]
                result_data=current_csv[['date','user','pc']]
                #print(changed_data)
                event_list = np.zeros(changed_data.shape[0],int)
                for i in range(len(event_list)):
                    event_list[i]=LOGON
                for j in range(changed_data.shape[0]):
                    if( changed_data.iloc[j]['event']=="Logon"):
                        event_list[j]=LOGON
                    elif (changed_data.iloc[j]['event']=="Logoff"):
                        event_list[j]=LOGOFF
                result_data.insert(2,'event', event_list)
                #print(result_data)  
                #input("logon finished")     
            elif i=='file.csv':
                #print("file")
                '''             
                EXE=3
                DOC=4
                PDF=5
                TXT=6
                JPG=7
                ZIP=8
                '''
                current_csv=pd.read_csv(daily_actions_path+"\\"+i,names=['date','user','pc','file'],index_col=False)#date,user,pc,to,cc,bcc,from,activity,size,attachments
                changed_data=current_csv[['date','user','pc','file']]
                result_data=current_csv[['date','user','pc']]
                event_list = np.zeros(changed_data.shape[0],int)
                for i in range(len(event_list)):
                    event_list[i]=NEUTRAL
                #print(changed_data)
                for j in range(changed_data.shape[0]):
                    #print(changed_data.iloc[j]['file'])
                    if pd.isnull(changed_data.iloc[j]['file']):
                        continue
                    elif re.search(r".exe$",changed_data.iloc[j]['file']):
                        event_list[j]=EXE
                        #input("true")
                    elif re.search(r".doc$",changed_data.iloc[j]['file']):
                        event_list[j]=DOC
                    elif re.search(r".pdf$",changed_data.iloc[j]['file']):
                        event_list[j]=PDF
                        #input("true")
                    elif re.search(r".txt$",changed_data.iloc[j]['file']):
                        event_list[j]=TXT                        
                    elif re.search(r".jpg$",changed_data.iloc[j]['file']):
                        event_list[j]=JPG
                        #input("true")
                    #elif re.search(r".zip$",changed_data.iloc[j]['file']):
                    else:
                        event_list[j]=ZIP
                
                #print("--------------")
                result_data.insert(2,'event', event_list)
                #print(result_data)  
                #input("file finished") 
            elif i=='device.csv':
                #print("device begin")
                current_csv=pd.read_csv(daily_actions_path+"\\"+i,names=['date','user','pc','event'],index_col=False)
                changed_data=current_csv[['date','user','pc','event']]
                result_data=current_csv[['date','user','pc']]
                #print(changed_data)
                event_list = np.zeros(changed_data.shape[0],int)
                for i in range(len(event_list)):
                    event_list[i]=CONNECT
                for j in range(changed_data.shape[0]):
                    if( changed_data.iloc[j]['event']=="Connect"):
                        event_list[j]=CONNECT
                    elif (changed_data.iloc[j]['event']=="Disconnect"):
                        event_list[j]=DISCONNECT
                result_data.insert(2,'event', event_list)
                #print(result_data)  
                #input("device finished") 
            else:
                #print("wrong")
                #input("d")
                continue
            final_list.append(result_data)   
        df=pd.concat(final_list)
        #print(df)
        df.sort_values("date",inplace=True)
        df = df.reset_index(drop=True)
        #print(df)
        #date_column=df.loc[:,'date']
        final_event_list = np.zeros(df.shape[0],int)
        #time judge
        for i in range(df.shape[0]):
            hours=df.iloc[i]['date'][11:13]
            final_event_list[i]=df.iloc[i]['event']
            if int(hours)<7 or int(hours)>=18:
                final_event_list[i]=df.iloc[i]['event']+BASIC_EVENT_COUNT
                #print(final_event_list[i])
            if  assigned_pc_dictionary[df.iloc[i]['user']]!=df.iloc[i]['pc']:
                final_event_list[i]=df.iloc[i]['event']+BASIC_EVENT_COUNT*2                    
        #device judge    
         

        #print(final_event_list)        #action sequence :each user each day
        df.insert(3,'final_event', final_event_list)     
        #print(df.iloc[0]['date'],df.iloc[0]['user'])  
        
        if threat_judge(df.iloc[0]['date'],df.iloc[0]['user']):
            threat_data.append(final_event_list.tolist())
        else:
            non_threat_data.append(final_event_list.tolist())     
        #print(result_threat)
    if count%200==0:
        np.save('result_threat0_'+str(count)+'.npy', result_threat) 
        print("save one file ")

np.save('result_threat0_fully.npy', result_threat) 
print("save result_threat.npy successfully !!!")
        
