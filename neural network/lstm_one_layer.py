# encoding=utf-8 
import torch
from torch import nn, optim
import numpy as np
from tqdm import tqdm
import random
import torch.nn.functional as F
random.seed(3)



num_epochs = 100
learning_rate = 0.01
num_dropout=0.3
input_size = 60
hidden_size = 128
num_layers = 1
seq_length = 1

def sequence_to_tensor(line):
    tensor = torch.zeros(len(line), 1, 60)
    for i, number in enumerate(line):
        tensor[i][0][int(number)-1] = 1
    return tensor

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

class LSTM(nn.Module):
    def __init__(self,  input_size, num_layers,num_dropout):#num_classes
        super(LSTM, self).__init__()
        #self.num_classes = num_classes
        self.num_layers = num_layers
        self.input_size = input_size
        #self.hidden_size = hidden_size
        self.seq_length = seq_length
        self.dp=nn.Dropout(num_dropout)
        self.lstm_1 = nn.LSTM(input_size=input_size, hidden_size=hidden_size,#hidden_size,
                            num_layers=num_layers, batch_first=True)
     
        #分类问题
        self.fc = nn.Linear(hidden_size, 2)  

    def forward(self, x,h0_1,c0_1):
        # Propagate input through LSTM
        out_1, (h_1, c_1) = self.lstm_1(self.dp(x), (h0_1, c0_1))

        #h_out = h_out.view(-1, self.hidden_size)
        
        
        out = F.log_softmax(self.fc(out_1[:,-1:,:]),dim=2)
        
        return out,h_1,c_1
    
    def init_hc(self):
        return torch.zeros(self.num_layers, 1, hidden_size),torch.zeros(self.num_layers, 1, hidden_size)
    

#num_classes = 59

#lstm = LSTM(num_classes, input_size, hidden_size, num_layers)
if __name__ == "__main__":
    
    train_threat_data=np.load('train_threat_data3.npy').tolist()[:2000]#676[:100]#
    train_normal_data=np.load('train_normal_data3.npy').tolist()[:2000]#6760[:100]#
    test_threat_data=np.load('test_threat_data3.npy').tolist()[:500]#20]#
    test_normal_data=np.load('test_normal_data3.npy').tolist()[:500]#20]#
    
    '''
    train_threat_data=np.load('train_threat_origin_data3.npy').tolist()[:2000]#676
    train_normal_data=np.load('train_normal_origin_data3.npy').tolist()[:2000]#6760
    test_threat_data=np.load('test_threat_origin_data3.npy').tolist()[:500]
    test_normal_data=np.load('test_normal_origin_data3.npy').tolist()[:500]
    '''
    
    input_list=train_normal_data+train_threat_data#7436
    valve=len(train_normal_data)
    normal_len=len(train_normal_data)
    threat_len=len(train_threat_data)
    index_input_list=list(range(len(input_list)))


    threat_to_train=index_input_list[valve:]
    normal_to_train=index_input_list[:valve]

    lstm = LSTM(input_size, num_layers,num_dropout)

    criterion = torch.nn.NLLLoss()
    optimizer = torch.optim.Adam(lstm.parameters(), lr=learning_rate)
    threat_category=torch.tensor([0], dtype=torch.long)
    #each epoch
    for epoch in tqdm(range(num_epochs)):
        # random choose normal data
        lstm.train()
        random.shuffle(normal_to_train)
        data_to_train=normal_to_train[:threat_len]+threat_to_train
        
        #random shuffle input data
        random.shuffle(data_to_train)
        #print(input_list[data_to_train[0]])
        #input("d")
        for i in range(len(data_to_train)):#  i stands for each sequence in one epoch(current_train_data)
            threat_category=torch.tensor([0], dtype=torch.long)
            input_list[data_to_train[i]] 
            #print(input_list[data_to_train[i]])
            current_train_data=input_list[data_to_train[i]]
            if data_to_train[i]>=valve:
                threat_category=torch.tensor([1], dtype=torch.long)
            h_state_1,c_state_1 =lstm.init_hc()
            lstm.zero_grad()
            origin_daily_sequence=current_train_data
            encoded_daily_sequence=sequence_to_tensor(origin_daily_sequence)
            sizechanged_daily_sequence=encoded_daily_sequence.view(1,-1,60)
            sequence_length=sizechanged_daily_sequence.shape[1]

            for k in range(sequence_length):
                daily_action=sizechanged_daily_sequence[:,k:k+1,:]

                outputs,h_state_1,c_state_1 = lstm(daily_action,h_state_1,c_state_1)
               
                h_state_1=h_state_1.detach()
                c_state_1=c_state_1.detach()

            loss = criterion(outputs.view(1,-1), threat_category)     
            loss.backward(retain_graph=True)#
            #optimizer.step()
            with torch.no_grad():
                for p in lstm.parameters():
                    p.data.add_(-learning_rate, p.grad.data)
        print("Epoch: %d, loss: %1.5f" % (epoch, loss.item())) 

        lstm.eval()#do not use dropout
        TP=0
        TN=0
        FP=0
        FN=0
        
        for i in range(len(test_threat_data)):
            if predict(sequence_to_tensor(test_threat_data[i])):
                TP+=1#!!!
            else:
                FN+=1
        print("-----------------hhh----------------------------")
        for i in range(len(test_normal_data)):
            if predict(sequence_to_tensor(test_normal_data[i])):
                FP+=1
            else:
                TN+=1#!!!
        
        print(TP,FN)
        print(FP,TN)
    #print(outputs)
        torch.save(lstm.state_dict(),"(origin)lstm_one_layer_test_epoch"+str(epoch)+".pth")
    print("successfully saved file!")
    
