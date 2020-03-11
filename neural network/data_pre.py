import numpy as np
import random


random.seed(3)
dataset="E:\eclipse-workspace\my_project\CERT5.2-UserDataExtract-UserMonthActivity-master\PythonCode\\result_threat0_fully.npy"

threat_dict = np.load(dataset).item()

random.shuffle(threat_dict[0])
train_normal_data=threat_dict[0][:6760]
test_normal_data=threat_dict[0][-290:]

random.shuffle(threat_dict[1])
train_threat_data=threat_dict[1][:676]
test_threat_data=threat_dict[1][676:]

print(len(train_threat_data))
print(len(test_threat_data))
print(len(train_normal_data))
print(len(test_normal_data))

np.save('train_threat_data.npy', train_threat_data) 
np.save('test_threat_data.npy', test_threat_data) 

np.save('train_normal_data.npy', train_normal_data) 
np.save('test_normal_data.npy', test_normal_data) 
