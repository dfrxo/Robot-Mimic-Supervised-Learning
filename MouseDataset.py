import torch
import torchvision
from torch.utils.data import Dataset, DataLoader
import numpy as np
import math
import pandas as pd
from sklearn.preprocessing import OneHotEncoder


class MouseDataset(Dataset):
    def __init__(self, csv_file):
           # Load the data
        self.data = pd.read_csv(csv_file)
        
        # Change from string to list 
        self.data['ship_layout'] = self.data['ship_layout'].apply(eval)
        self.data['probability_map'] = self.data['probability_map'].apply(eval)
        
        self.layout_encoder = OneHotEncoder(sparse_output=False) # Initialize OneHotEncoder
       
        

    def __len__(self):
        return len(self.data)
    
csv_file = r'C:\Users\vsh00\OneDrive - Rutgers University\python\Mimic-SupervisedLearning\training_data\stationary_train_data.csv'
mouse_dataset = MouseDataset(csv_file)
data_loader = DataLoader(mouse_dataset, batch_size=10, shuffle=True)
