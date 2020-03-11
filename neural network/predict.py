# encoding=utf-8 
from train import LSTM
import torch

lstm = torch.load('char-rnn-classification.pt')
lstm.eval()#do not use dropout
def evaluate(sequence):
    h_state_1,c_state_1,h_state_2,c_state_2,h_state_3,c_state_3 =lstm.init_hc()
    for k in range(len(sequence)):
        daily_action=sequence[:,k:k+1,:]
        output,h_state_1,c_state_1,h_state_2,c_state_2,h_state_3,c_state_3 = lstm(daily_action,h_state_1,c_state_1,h_state_2,c_state_2,h_state_3,c_state_3)
       
    
    return output

def predict(line):
    output = evaluate(Variable(lineToTensor(line)))

    # Get top N categories
    v, i = torch.topk(output,1)
    if i.item() == 1:
        return True
    else:
        return False


if __name__ == '__main__':

    test_threat_data=np.load('test_threat_data.npy').tolist()
    test_normal_data=np.load('test_normal_data.npy').tolist()
    
    TP=0
    TN=0
    FP=0
    FN=0


    for i in range(len(test_threat_data)):
        if predict(test_threat_data[i]):
            TP+=1#!!!
        else:
            FN+=1
    
    for i in range(len(test_normal_data)):
        if predict(test_normal_data[i]):
            FP+=1
        else:
            TN+=1#!!!

    print(TP,FN)
    print(FP,TN)
    
    
    
    
    
    
    
    
    
    