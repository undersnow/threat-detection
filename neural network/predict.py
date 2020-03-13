# encoding=utf-8 
import torch
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
    

while True:
    list_to_predict=eval(input("list_to_predict:"))#[1,2,1,1,11,11,11]
    if list_to_predict[0] == 0:
        break
    print(predict(sequence_to_tensor(list_to_predict)))

