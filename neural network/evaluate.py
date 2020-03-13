# encoding=utf-8 
import torch
import numpy as np
import tqdm
from lstm_one_layer import LSTM,sequence_to_tensor


num_dropout=0.3
input_size = 60
num_layers = 1

lstm = LSTM(input_size, num_layers,num_dropout)
lstm.load_state_dict(torch.load('lstm_one_layer_test_epoch30.pth'))
lstm.eval()#do not use dropout


def evaluate(sequence):
    h_state_1,c_state_1 =lstm.init_hc()
    for k in range(len(sequence)):
        daily_action=sequence[k:k+1,:,:]
        #print(daily_action)
        output,h_state_1,c_state_1 = lstm(daily_action,h_state_1,c_state_1)

    return output

def predict(sequence):
    output = evaluate(sequence)

    # Get top N categories
    v, i = torch.topk(output,1)
    if i.item() == 1:
        return True
    else:
        return False

if __name__ == '__main__':
    test_num=800
    test_threat_data=np.load('test_threat_data3.npy').tolist()[:test_num]
    test_normal_data=np.load('test_normal_data3.npy').tolist()[:test_num]

    TP=0
    TN=0
    FP=0
    FN=0
    print("----------------evaluating threat data---------------------------")
    for i in range(len(test_threat_data)):
        if predict(sequence_to_tensor(test_threat_data[i])):
            TP+=1#!!!
        else:
            FN+=1
    print("----------------evaluating normal data---------------------------")
    for i in range(len(test_normal_data)):
        if predict(sequence_to_tensor(test_normal_data[i])):
            FP+=1
        else:
            TN+=1#!!!
    precision=TP/(TP+FP)
    recall=TP/(TP+FN)
    print("TP,FN,FP,TN:",TP,FN,FP,TN)

    print("precison:",precision)
    print("recall:",recall)
    
    
    
    
    
    
    
    
    
    
    