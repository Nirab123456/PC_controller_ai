from torch import optim
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from PySimpleGUI.PySimpleGUI import Window
import sys
import os
import PySimpleGUI as sg
import tkinter as tk
from Data_collection_train import TrainingDataFrameApp
from torch.utils.tensorboard import SummaryWriter


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # Create the tkinter window
# window = tk.Tk()
# window.geometry("400x400")
# window.configure(bg="#f0f0f0")

# # Create an instance of the TrainingDataFrameApp class
# app = TrainingDataFrameApp(window)

# # Start the tkinter event loop
# window.mainloop()


def main():
    window = sg.Window("Training DataFrame App")  # Set the window title here
    app = TrainingDataFrameApp(window)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Continue':
            app.collect_data()
        elif event == 'Save':
            app.save_data()

    window.close()


if __name__ == '__main__':
    main()



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
                y_value = .1
            # sleep
            elif cpu_variance > 0.5 and memory_variance > 0.5 and disc_variance > 0.5 and wifi_variance > 0.5 and \
                    cpu_variance < 0.7 and memory_variance < 0.7 and disc_variance < 0.7 and wifi_variance < 0.7:
                y_value = .2
            # shutoff display
            elif cpu_variance < 0.3 and memory_variance < 0.3 and disc_variance > 0.5 and wifi_variance < 0.5:
                y_value = .3
            # shutoff display
            elif cpu_variance < 0.3 and memory_variance < 0.3 and disc_variance < 0.5 and wifi_variance > 0.5:
                y_value = .3
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
        x= x.reshape(1,250)

        if y is not None:
            y = torch.tensor(y)
        else:
            y = torch.tensor(-1)  # Default value when logic doesn't assign a specific value
        return x, y.unsqueeze(-1)



layout = [
    [sg.Text("Enter the name of the file you want to train((.csv)extensin not needed):", font=("Arial", 12))],
    [sg.Input(key='-FILENAME-', size=(40, 1))],
    [sg.Text("Enter the number of epochs:", font=("Arial", 12))],
    [sg.Input(key='-NUM_EPOCHS-', size=(40, 1))],
    [sg.Text("Please Enter the Name of your pre trained model if you have one ((.pt)extensin not needed):", font=("Arial", 12))],
    [sg.Input(key='-PRE_TRAINED-', size=(40, 1))],
    [sg.Button("Run", size=(10, 1), button_color=('white', '#4CAF50'), font=("Arial", 12))],
    [sg.Button("Exit", size=(10, 1), button_color=('white', '#D32F2F'), font=("Arial", 12))],
    [sg.Output(size=(80, 20), font=("Arial", 12), key='-OUTPUT-')]
]

# Create the PySimpleGUI window
window = sg.Window("Program Runner", layout)

if __name__ == '__main__':
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Run':
            file_name = values['-FILENAME-']
            file_path = file_name + '.csv'
            df = pd.read_csv(file_path)
            df = df.astype('float32')
            Dataset = CustomDataset(df, 50)
            dataloader = DataLoader(Dataset, batch_size=32,shuffle=False)

            model = nn.Sequential(
                nn.Flatten(), 
                nn.Linear(250,50),  # here 5 is the number of dataframe columns or input features
                nn.ReLU(),
                nn.Linear(50, 1),  
                nn.Sigmoid()
                
            ).to(device)
            model_state_name = values['-PRE_TRAINED-']
            model_state_name = model_state_name + '.pt'
            if os.path.isfile(model_state_name):
                try:
                    model.load_state_dict(torch.load(model_state_name))
                except:
                    continue

            optimizer = optim.Adam(model.parameters(), lr=0.001)
            loss_fn = nn.MSELoss()

            total_loss = 0
            num_batches = len(dataloader)
            NUM_EPOCHS = int(values['-NUM_EPOCHS-'])  # Retrieve NUM_EPOCHS from the input field
            print_interval = 1
            loop_counter = 0
            losses = [] 
            writer = SummaryWriter()
            for epoch in range(NUM_EPOCHS):
                for batch_idx, (x, y) in enumerate(dataloader):
                    x = x.to(device)
                    y = y.float()
                    y = y.to(device)
                    model.train()
                    # Forward pass
                    y_pred = model(x)

                    # Compute the loss
                    loss = loss_fn(y_pred, y)
                    total_loss += loss.item()

                    # Backward pass and optimization
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                    # Print training progress
                    if (batch_idx + 1) % print_interval == 0:
                        avg_loss = total_loss / print_interval
                        total_loss = 0
                        variance = torch.var(torch.tensor(losses))
                        std_dev = torch.sqrt(variance)
                        losses.append(loss.item())
                        writer.add_scalar('Loss', avg_loss, epoch * num_batches + batch_idx)
                        writer.add_scalar('Variance', variance, epoch * num_batches + batch_idx)
                        # Save the model
                        save_path = f'your_model{loop_counter}.pt'
                        torch.save(model.state_dict(), save_path)
                    
                    loop_counter += 1
            writer.close()
            print("Thank you for your patience Training has been compleated !")
        window['Run'].update(disabled=False)
        window.refresh()


window.close()
