# encoding:utf-8 
import pandas as pd
import numpy as np
import User_Month_Day_Extract

# 该模块将每个用户的文件转换成序列
# 保存csv文件
#  用户ID，日期，序列
# AAE0190，2011-05-16，1 2 3，


answer_path = r'E:\eclipse-workspace\my_project\answers\answers'
insider_path = r'E:\eclipse-workspace\my_project\r4.2\insiders.csv'

insider_dictionary={}
insider_file_dict={}
insider_origindata=pd.read_csv(insider_path,names=['dataset','scenario','details','user','start','end'],index_col=False)
insider_filename=insider_origindata['details'] #r4.2-1-BLS0678.csv
for i in range(insider_origindata.shape[0]):
    insider_file_dict[insider_origindata.iloc[i]['user']]=answer_path+"\\"+insider_origindata.iloc[i]['details'][:6]+"\\"+insider_origindata.iloc[i]['details']
#print(insider_file_dict)  {'AAM0658': 'E:\\eclipse-workspace\\my_project\\answers\\answers\\r4.2-1\\r4.2-1-AAM0658.csv', 'EDB0714': 'E:\\ecl
for i in insider_file_dict.keys():
    #print(insider_file_dict[i][53:54])
    if(insider_file_dict[i][53:54]!='3'):
        each_insider_file=pd.read_csv(insider_file_dict[i],names=['dataset','scenario','date','user','start','end','d'],index_col=False)
    else:
        each_insider_file=pd.read_csv(insider_file_dict[i],names=['dataset','scenario','date','user','start','end','d','usr','stt','ed','dio'],index_col=False)
    
    temp_list=[]
    for j in range(each_insider_file.shape[0]):
        y, m, d = User_Month_Day_Extract.Extract_Date(each_insider_file.iloc[j]['date'])
        regular_date=y+"-"+m+"-"+d
        temp_list.append(regular_date)
    temp_list1=list(set(temp_list)) 
    temp_list1.sort(key=temp_list.index)
    insider_dictionary[i]=temp_list1
#print(insider_dictionary)


np.save('insider_dictionary.npy', insider_dictionary) 
print("-------finished!!!---------")
