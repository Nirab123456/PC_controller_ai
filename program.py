import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import MinMaxScaler
from test import pandas_dataframe
from torch import optim
import subprocess
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Window
import sys
import os
from try_act_1 import new_folder

layout = [
    [sg.Text("Please Enter the Name of your pre-trained model (without the '.pt' extension):", font=("Arial", 12))],
    [sg.Input(key='-PRE_TRAINED-', size=(40, 1))],
    [sg.Text("Click 'Run' to start the program")],
    [sg.Button("Run")],
    [sg.Button("Exit")],
    [sg.Output(size=(80, 20))]
]

# Create the PySimpleGUI window
window = sg.Window("Program Runner", layout)

if __name__ == '__main__':
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Run':
            window['Run'].update(disabled=True)

            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

            pandas_dataframe_1 = pandas_dataframe()

            df = pandas_dataframe_1.dataframe()

            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

            if not df.empty:
                class CustomDataset(Dataset):
                    """Custom Dataset for loading data from the dataframe"""

                    def __init__(self, df, num_columns):
                        self.df = df
                        self.num_columns = num_columns

                    def _custom_logic(self, subset):
                        cpu_variance = subset['cpu_uses'].var()
                        memory_variance = subset['memory_uses'].var()
                        disc_variance = subset['disc_uses'].var()
                        wifi_variance = subset['Wi_fi_uses'].var()

                        y_value = 0
                        if 1 in subset['Type'].values:
                            y_value = 0
                        else:
                            # hibernate
                            if (
                                cpu_variance > 0.7
                                and memory_variance > 0.7
                                and disc_variance > 0.7
                                and wifi_variance > 0.7
                            ):
                                y_value = 0.1
                            # sleep
                            elif (
                                cpu_variance > 0.5
                                and memory_variance > 0.5
                                and disc_variance > 0.5
                                and wifi_variance > 0.5
                                and cpu_variance < 0.7
                                and memory_variance < 0.7
                                and disc_variance < 0.7
                                and wifi_variance < 0.7
                            ):
                                y_value = 0.2
                            # shutoff display
                            elif (
                                cpu_variance < 0.3
                                and memory_variance < 0.3
                                and disc_variance > 0.5
                                and wifi_variance < 0.5
                            ):
                                y_value = 0.3
                            # shutoff display
                            elif (
                                cpu_variance < 0.3
                                and memory_variance < 0.3
                                and disc_variance < 0.5
                                and wifi_variance > 0.5
                            ):
                                y_value = 0.3
                        return y_value

                    def __len__(self):
                        return len(self.df) // self.num_columns

                    def __getitem__(self, idx):
                        start_row = idx * self.num_columns
                        end_row = (idx + 1) * self.num_columns
                        subset = self.df.iloc[start_row:end_row]
                        y = self._custom_logic(subset)
                        x = subset.values
                        x = torch.tensor(x)
                        if y is not None:
                            y = torch.tensor(y)
                        else:
                            y = torch.tensor(-1)  # Default value when logic doesn't assign a specific value
                        return x, y.unsqueeze(-1)

                Dataset = CustomDataset(df, 50)
                dataloader = DataLoader(Dataset, batch_size=32, shuffle=False)
                model = nn.Sequential(
                    nn.Flatten(),
                    nn.Linear(250, 50),  # here 5 is the number of dataframe columns or input features
                    nn.ReLU(),
                    nn.Linear(50, 1),
                    nn.Sigmoid(),
                ).to(device)

                model_state_name = values['-PRE_TRAINED-']
                model_state_name = model_state_name + '.pt'
                if os.path.isfile(model_state_name):
                    try:
                        model.load_state_dict(torch.load(model_state_name))
                    except:
                        continue


                    # model = model.to(device)
                optimizer = optim.Adam(model.parameters(), lr=0.001)
                loss_fn = nn.MSELoss()

                total_loss = 0
                num_batches = len(dataloader)
                print_interval = 1
                loop_counter = 0
                losses = []

                optimizer = optim.Adam(model.parameters(), lr=0.001)
                loss_fn = nn.MSELoss()

                total_loss = 0
                num_batches = len(dataloader)
                print_interval = 1
                loop_counter = 0
                losses = []

                for batch_idx, (x, y) in enumerate(dataloader):
                    x = x.float()
                    x = x.to(device)
                    y = y.float()
                    y = y.to(device)
                    model.train()
                    # Forward pass
                    y_pred = model(x)
                    # print(f'shape of x: {x.shape}')
                    # print(f'shape of y: {y.shape}')
                    # print(f'shape of y_pred: {y_pred.shape}')
                    # print(f'y_pred: {y_pred}')

                    for item in y_pred:
                        value = item.item()  # Get the value of the item as a Python float
                        print(value)
                        if value >0:
                            new_folder_1 = new_folder.make_new_folder()
                    
                    print('Sir i have exe')
                            

                    # Compute the loss
                    loss = loss_fn(y_pred, y)
                    total_loss += loss.item()

                    # Backward pass and optimization
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                    # Save the model
                    save_path = f'model_test_trained.pt'
                    print('sir please load model_test_trained.pt model from next time')
                    torch.save(model.state_dict(), save_path)
                
                    loop_counter += 1




        window['Run'].update(disabled=False)
        window.refresh()


window.close()











# df.to_csv('data.csv', index=False)

