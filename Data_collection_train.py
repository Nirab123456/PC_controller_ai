import PySimpleGUI as sg
from Data_collection_pandas import pandas_data_collection
import pandas as pd
import time
from sklearn.preprocessing import MinMaxScaler


class TrainingDataFrameApp:
    """Collect data from the environment and convert it to a Pandas DataFrame for training."""

    def __init__(self, window):
        self.window = window

        # Create the skip text
        self.skip_text = sg.Text("Skip this step if you have already collected data", font=("Arial", 12), pad=((10, 10), (10, 0)))

        # Create the input label
        self.input_label = sg.Text("Enter the number of iterations:", font=("Arial", 12))
        self.input_entry = sg.Input(key='-ITERATIONS-', font=("Arial", 12), size=(15, 1))
        self.continue_button = sg.Button("Continue", button_color=('white', '#4CAF50'), font=("Arial", 12), size=(10, 1))
        self.output_label = sg.Text("Collected Data:", font=("Arial", 12), pad=((10, 10), (10, 0)))
        self.output_text = sg.Output(size=(50, 10), font=("Arial", 12), pad=((10, 10), (0, 10)))
        self.save_button = sg.Button("Save", button_color=('white', '#4CAF50'), font=("Arial", 12), size=(10, 1))

        # Define the layout
        layout = [
            [self.skip_text],
            [self.input_label, self.input_entry, self.continue_button],
            [self.output_label],
            [self.output_text],
            [self.save_button]
        ]

        # Create the window layout
        self.window.layout(layout)

    def collect_data(self):
        """Collect data from the environment and convert it to a Pandas DataFrame for training."""
        iterations = int(self.window['-ITERATIONS-'].get())
        total_iterations = iterations * 5  # takes 5 times more dataframes to match approximately 50 df
        estimated_time = total_iterations * 1.3
        print(f"This program will take approximately {estimated_time} minutes to run and the program may be unresponsive for a while... :(\n\n Done to save computing power\n\n")

        user_input = sg.popup_yes_no("Continue?", "Do you want to continue?", 
                                    relative_location=(300, -50), background_color='#FE3E15')
        if not user_input:
            return

        inner_dfs = []
        outer_dfs = []
        pdc = pandas_data_collection()

        for outer_loop in range(total_iterations):
            for inner_loop in range(1):
                df = pdc.base_df()
                selected_columns = ['Name', 'cpu_uses', 'memory_uses', 'Wi_fi_uses', 'disc_uses', 'Type']
                new_df = df[selected_columns].copy()
                new_df = new_df.sample(frac=1).reset_index(drop=True)
                new_df = new_df.reset_index()
                new_df = new_df.dropna()
                inner_dfs.append(new_df)

            merged_df = pd.concat(inner_dfs, ignore_index=True)
            outer_dfs.append(merged_df)
            inner_dfs = []

        result_df = pd.concat(outer_dfs, ignore_index=True)
        result_df = result_df.drop('index', axis=1)
        # post-processing start
        result_df.dropna(inplace=True)
        result_df['Type'] = result_df['Type'].replace({'non_interacting_processes': '0', 'interacting_processes': '1'})
        result_df.drop(['Name'], axis=1, inplace=True)
        result_df = result_df.astype('float32')

        columns_to_normalize = ['cpu_uses', 'memory_uses', 'Wi_fi_uses', 'disc_uses']

        scaler = MinMaxScaler(feature_range=(0, 1))
        result_df[columns_to_normalize] = scaler.fit_transform(result_df[columns_to_normalize])
        # post-processing end
        print("Data collection complete.\n\n")
        print('please double click to the save button\nprovide desigred extension(.csv to train the model)\n')
        result_df = result_df.astype('float32')
        self.result_df = result_df

    def save_data(self):
        save_clicked = False  # Flag to track save button click

        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Save':
                save_clicked = True
                break

        if save_clicked:
            save_path = sg.popup_get_file(
                "Save As",
                save_as=True,
                initial_folder="./",
                default_extension=".csv",
                button_color=('white', '#4CAF50')
            )
            if save_path:
                self.result_df.to_csv(save_path, index=False)
                print(f"Data saved to {save_path}\n")
                print("close the programe .....\nNext training phase\n")
            else:
                print("Save canceled\n")
        else:
            print("Save canceled\n")





