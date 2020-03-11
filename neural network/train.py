# encoding=utf-8 
import torch
from torch import nn, optim
import numpy as np
from tqdm import tqdm
import random
import torch.nn.functional as F

num_epochs = 30
learning_rate = 0.01
num_dropout=0.5
input_size = 60
hidden_size = 60
num_layers = 1
seq_length = 1

def sequence_to_tensor(line):
    tensor = torch.zeros(len(line), 1, 60)
    for i, number in enumerate(line):
        tensor[i][0][int(number)-1] = 1
    return tensor



class LSTM(nn.Module):
    def __init__(self,  input_size, num_layers,num_dropout):#num_classes
        super(LSTM, self).__init__()
        #self.num_classes = num_classes
        self.num_layers = num_layers
        self.input_size = input_size
        #self.hidden_size = hidden_size
        self.seq_length = seq_length
        self.dp=nn.Dropout(num_dropout)
        self.lstm_1 = nn.LSTM(input_size=input_size, hidden_size=60,#hidden_size,
                            num_layers=num_layers, batch_first=True)
        self.lstm_2 = nn.LSTM(input_size=60, hidden_size=40,#hidden_size,
                            num_layers=num_layers, batch_first=True)
        self.lstm_3 = nn.LSTM(input_size=40, hidden_size=20,#hidden_size,
                            num_layers=num_layers, batch_first=True)        
        #分类问题
        self.fc = nn.Linear(20, 2)  

    def forward(self, x,h0_1,c0_1,h0_2,c0_2,h0_3,c0_3):
        # Propagate input through LSTM
        out_1, (h_1, c_1) = self.lstm_1(x, (h0_1, c0_1))
        out_2, (h_2, c_2) = self.lstm_2(self.dp(out_1), (h0_2, c0_2))
        out_3, (h_3, c_3) = self.lstm_3(self.dp(out_2), (h0_3, c0_3))
        #h_out = h_out.view(-1, self.hidden_size)
        
        
        out = F.log_softmax(self.fc(out_3[:,-1:,:]),dim=2)
        
        return out,h_1,c_1,h_2,c_2,h_3,c_3
    
    def init_hc(self):
        return torch.zeros(self.num_layers, 1, 60),torch.zeros(self.num_layers, 1, 60),torch.zeros(self.num_layers, 1, 40) ,torch.zeros(self.num_layers, 1, 40),torch.zeros(self.num_layers, 1, 20) ,torch.zeros(self.num_layers, 1, 20) 
    

#num_classes = 59

#lstm = LSTM(num_classes, input_size, hidden_size, num_layers)
if __name__ == "__main__":
    train_threat_data=np.load('train_threat_data.npy').tolist()#676
    #test_threat_data=np.load('test_threat_data.npy').tolist()
    train_normal_data=np.load('train_normal_data.npy').tolist()#6760
    #test_normal_data=np.load('test_normal_data.npy').tolist()
    '''
    print(train_normal_data[0])
    train_threat=[]
    for i in tqdm(range(len(train_normal_data))):
        train_threat.append(sequence_to_tensor(train_normal_data[i]))
    print(train_threat)
    '''
    input_list=train_normal_data+train_threat_data#7436
    valve=len(train_normal_data)
    normal_len=len(train_normal_data)
    threat_len=len(train_threat_data)
    index_input_list=list(range(len(input_list)))
    '''
    print(index_input_list[:10])
    print(len(train_normal_data))
    print(train_threat_data[0])
    print(input_list[valve])
    '''
    #print(sequence_to_tensor([1,2,2,3,60,60,60]))
    
    #each epoch
    threat_to_train=index_input_list[valve:]
    normal_to_train=index_input_list[:valve]
    

    '''
    print(data_to_train[:100])
    print(len(data_to_train))
    '''
    
    lstm = LSTM(input_size, num_layers,num_dropout)
    #lstm=lstm
    #criterion = torch.nn.MSELoss()  # mean-squared error for regression
    #criterion = torch.nn.CrossEntropyLoss()
    criterion = torch.nn.NLLLoss()
    optimizer = torch.optim.Adam(lstm.parameters(), lr=learning_rate)
    threat_category=torch.tensor([0], dtype=torch.long)
    #each epoch
    for epoch in tqdm(range(num_epochs)):
        # random choose normal data
        random.shuffle(normal_to_train)
        data_to_train=normal_to_train[:threat_len]+threat_to_train
        
        #random shuffle input data
        random.shuffle(data_to_train)
        for i in range(len(data_to_train)):#  i stands for each sequence in one epoch(current_train_data)
            threat_category=torch.tensor([0], dtype=torch.long)
            input_list[data_to_train[i]] 
            #print(input_list[data_to_train[i]])
            current_train_data=input_list[data_to_train[i]]
            if data_to_train[i]>=valve:
                threat_category=torch.tensor([1], dtype=torch.long)
            #print()
            #print(threat_category)
            #print(sequence_to_tensor(current_train_data))
            #input("eee")   
            h_state_1,c_state_1,h_state_2,c_state_2,h_state_3,c_state_3 =lstm.init_hc()
            origin_daily_sequence=current_train_data
            encoded_daily_sequence=sequence_to_tensor(origin_daily_sequence)
            sizechanged_daily_sequence=encoded_daily_sequence.view(1,-1,60)
            sequence_length=sizechanged_daily_sequence.shape[1]
            #print(sequence_length)
            #input("d")
            #print(sizechanged_daily_sequence)
            #print("------------------------------------")
            #print(sizechanged_daily_sequence)
            for k in range(sequence_length):
                daily_action=sizechanged_daily_sequence[:,k:k+1,:]
                #print(daily_action.size())#torch.Size([1, 1, 60])
                #input("d")
                outputs,h_state_1,c_state_1,h_state_2,c_state_2,h_state_3,c_state_3 = lstm(daily_action,h_state_1,c_state_1,h_state_2,c_state_2,h_state_3,c_state_3)
                '''
                h_state_1=h_state_1.detach()
                c_state_1=c_state_1.detach()
                h_state_2=h_state_2.detach()
                c_state_2=c_state_2.detach()
                h_state_3=h_state_3.detach()
                c_state_3=c_state_3.detach()
                '''
                '''if k!=0:
                    feature=torch.cat([feature,h_state_3],dim=1)
                else:
                    feature=h_state_3
                print(feature.size())
                input("kkk")            '''
            #print(c_state_3.size())
            #print(outputs)   
            #print("++++++++++++++++++loss++++++++++++++++++++++=")
            changed_output=outputs.view(1,-1)
            #print(changed_output.size())
            #print(threat_category)
            loss = criterion(changed_output, threat_category)     
            loss.backward()#retain_graph=True
            optimizer.step()
            #input("eee")
            '''
            if k <=sequence_length-2:
                next_action=sizechanged_daily_sequence[:,k+1:k+2,:]
                optimizer.zero_grad()              
                #print(next_action)
                #print(outputs.view(1,64).size())
                # obtain the loss function
                #print(next_action.argmax(dim=2).view(-1))
              
                loss = criterion(outputs.view(1,64), next_action.argmax(dim=2).view(-1))     
                loss.backward()#retain_graph=True
                optimizer.step()
                '''
        print("Epoch: %d, loss: %1.5f" % (epoch, loss.item())) 
    #print(outputs)
    torch.save(lstm.state_dict(),"lstm_test0.pth")
    print("successfully saved file!")