import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import MinMaxScaler
from test import pandas_dataframe
from torch import optim 
from torch import optim
import subprocess
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Window

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

pandas_dataframe_1 = pandas_dataframe()

df = pandas_dataframe_1.dataframe()
df.dropna(inplace=True)
df['Type'] = df['Type'].replace({'non_interacting_processes': '0', 'interacting_processes': '1'})
df.drop(['Name'], axis=1, inplace=True)
df = df.astype('float32')

columns_to_normalize = ['cpu_uses', 'memory_uses', 'Wi_fi_uses', 'disc_uses']

scaler = MinMaxScaler(feature_range=(0, 1))
df[columns_to_normalize] = scaler.fit_transform(df[columns_to_normalize])
# Create the PySimpleGUI window layout
# Run the program when the 'Run' button is clicked

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

layout = [
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
            if not df.empty:
                class CustomDataset(Dataset):
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
                            if cpu_variance > 0.7 and memory_variance > 0.7 and disc_variance > 0.7 and wifi_variance > 0.7:
                                y_value = 1
                            # sleep
                            elif cpu_variance > 0.5 and memory_variance > 0.5 and disc_variance > 0.5 and wifi_variance > 0.5 and \
                                    cpu_variance < 0.7 and memory_variance < 0.7 and disc_variance < 0.7 and wifi_variance < 0.7:
                                y_value = 2
                            # shutoff display
                            elif cpu_variance < 0.3 and memory_variance < 0.3 and disc_variance > 0.5 and wifi_variance < 0.5:
                                y_value = 3
                            # shutoff display
                            elif cpu_variance < 0.3 and memory_variance < 0.3 and disc_variance < 0.5 and wifi_variance > 0.5:
                                y_value = 3
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

                model = nn.Sequential(
                    nn.Flatten(),  # Reshape the input tensor to [batch_size, 25]
                    nn.Linear(25, 30),
                    nn.ReLU(),
                    nn.Linear(30, 10),
                    nn.Tanh(),
                    nn.Linear(10, 1),  # Output size is set to 10 instead of 1
                ).to(device)
                model.load_state_dict(torch.load('model.pt'))
                model.to(device)
                custom_dataset = CustomDataset(df, 5)
                dataloader = DataLoader(custom_dataset, batch_size=32)
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
                    x = x.to(device)
                    y = y.float()
                    y = y.to(device)
                    model.train()
                    # Forward pass
                    y_pred = model(x)
                    print(f'shape of x: {x.shape}')
                    print(f'shape of y: {y.shape}')
                    print(f'shape of y_pred: {y_pred.shape}')
                    print(f'y_pred: {y_pred}')

                    for item in y_pred:
                        value = item.item()  # Get the value of the item as a Python float
                        print(value)
                        if value >0:
                            subprocess.run(["python", "try_act_1.py"])

                    # Compute the loss
                    loss = loss_fn(y_pred, y)
                    total_loss += loss.item()

                    # Backward pass and optimization
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                    # Save the model
                    save_path = f'model1.pt'
                    torch.save(model.state_dict(), save_path)
                
                    loop_counter += 1




        window['Run'].update(disabled=False)
        window.refresh()


window.close()











# df.to_csv('data.csv', index=False)

