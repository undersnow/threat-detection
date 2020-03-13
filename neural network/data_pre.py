import numpy as np
import random


random.seed(3)
dataset="E:\eclipse-workspace\my_project\CERT5.2-UserDataExtract-UserMonthActivity-master\PythonCode\\result_threat_all_fully0.npy"

threat_dict = np.load(dataset).item()
print(len(threat_dict[0]))
print(len([]))
input("e")
random.shuffle(threat_dict[0])
train_normal_data=threat_dict[0][:10000]
test_normal_data=threat_dict[0][-1010:]

random.shuffle(threat_dict[1])
train_threat_data=threat_dict[1][:2020]
test_threat_data=threat_dict[1][2020:]
print(train_threat_data[:100])
print(train_normal_data[:100])
input("e")

print(len(train_threat_data))
print(len(test_threat_data))
print(len(train_normal_data))
print(len(test_normal_data))

def change_list(list):
    out=[]
    for i in range(len(list)-1):
        if list[i]==9 and list[i+1]==9:
            continue
        elif list[i]==24 and list[i+1]==24:
            continue
        elif list[i]==39 and list[i+1]==39:
            continue
        elif list[i]==54 and list[i+1]==54:
            continue
        else:
            out.append(list[i])
    return out
'''
np.save('train_threat_origin_data3.npy', train_threat_data) 
np.save('test_threat_origin_data3.npy', test_threat_data) 
np.save('train_normal_origin_data3.npy', train_normal_data) 
np.save('test_normal_origin_data3.npy', test_normal_data) 
'''
for i in range(len(train_threat_data)):
    train_threat_data[i]=change_list(train_threat_data[i])
for i in range(len(test_threat_data)):
    test_threat_data[i]=change_list(test_threat_data[i])
for i in range(len(train_normal_data)):
    train_normal_data[i]=change_list(train_normal_data[i])
for i in range(len(test_normal_data)):
    test_normal_data[i]=change_list(test_normal_data[i])    

def abc(train_threat_data):  
    out=[]
    for i in range(len(train_threat_data)):    
        if len(train_threat_data[i])<=3:
            continue
        else:
            out.append(train_threat_data[i])
    return out

input("eee")
np.save('train_threat_data3.npy', abc(train_threat_data)) 
np.save('test_threat_data3.npy', abc(test_threat_data))
np.save('train_normal_data3.npy', abc(train_normal_data)) 
np.save('test_normal_data3.npy', abc(test_normal_data)) 


#print(train_normal_data[:100])
#print(change_list(train_normal_data[0]))
#print(train_threat_data[100:250])
#print(change_list(train_threat_data[0]))

print("--------------finished-----------")