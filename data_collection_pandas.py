from AI_Env_Data_2 import Env_data_process
import numpy as np
import pandas as pd


class pandas_data_collection():
    """Convert cpu, memory, wifi, disk used data to a pandas DataFrame."""
    def __init__(self):
        self.Env_data_process = Env_data_process()
        self.intarected_unique_name= self.Env_data_process.get_unique_process_names(self.Env_data_process.interacting_processes)
        # print(f'interacting_unique_name: {self.intarected_unique_name}')
        self.un_intarected_unique_name = self.Env_data_process.get_unique_process_names(self.Env_data_process.non_interacting_processes)
        # print(f'un_interacting_unique_name: {self.un_intarected_unique_name}')


    def base_intarected_df(self):
        """Convert currently interacting data to a Pandas DataFrame."""
        dict_list = [
            self.Env_data_process.get_cpu_uses_percent(self.Env_data_process.get_current_interaction_results()),
            self.Env_data_process.get_memory_uses_percent(self.Env_data_process.get_current_interaction_results()),
            self.Env_data_process.get_disc_uses_percent(self.Env_data_process.get_current_interaction_results()),
            self.Env_data_process.get_Wi_fi_uses_percent(self.Env_data_process.get_current_interaction_results()),
        ]
        data_dict = {}
        for i, dictionary in enumerate(dict_list):
            for name, value in dictionary.items():
                if name in data_dict:
                    data_dict[name].append(value)
                else:
                    data_dict[name] = [value]

        df = pd.DataFrame.from_dict(data_dict)
        df = df.transpose()
        df = df.reset_index()
        df.columns = ['Name'] + ['cpu_uses'] + ['memory_uses'] + ['Wi_fi_uses'] + ['disc_uses']
        df['Type'] = 'interacting_processes'
        df = df.sort_values('Name').reset_index(drop=True)
        return df



    def base_un_intarected_df(self):
        """Convert currently non-interacting data to a Pandas DataFrame."""
        dict_list = [
            self.Env_data_process.get_cpu_uses_percent(self.Env_data_process.get_current_non_interaction_results()),
            self.Env_data_process.get_memory_uses_percent(self.Env_data_process.get_current_non_interaction_results()),
            self.Env_data_process.get_disc_uses_percent(self.Env_data_process.get_current_non_interaction_results()),
            self.Env_data_process.get_Wi_fi_uses_percent(self.Env_data_process.get_current_non_interaction_results()),
        ]
        data_dict = {}
        for i, dictionary in enumerate(dict_list):
            for name, value in dictionary.items():
                if name in data_dict:
                    data_dict[name].append(value)
                else:
                    data_dict[name] = [value]

        df = pd.DataFrame.from_dict(data_dict)
        df = df.transpose()
        df = df.reset_index()
        df.columns = ['Name'] + ['cpu_uses'] + ['memory_uses'] + ['Wi_fi_uses'] + ['disc_uses']
        df['Type'] = 'non_interacting_processes'
        df = df.sort_values('Name').reset_index(drop=True)
        return df


    def base_df(self):
        intarected_df = self.base_intarected_df()  # Generate the interacting processes dataframe
        un_intarected_df = self.base_un_intarected_df()  # Generate the non-interacting processes dataframe

        # Concatenate the interacting and non-interacting dataframes
        df = pd.concat([intarected_df, un_intarected_df], ignore_index=True)

        df = df.reset_index(drop=True)  # Reset the index
        df = df.sample(frac=1).reset_index(drop=True)  # Shuffle the rows

        return df








































# class pandas_data_collection(Env_data_process):
#     """Convert cpu, memory, wifi, disk used data to a pandas DataFrame."""

#     def __init__(self):
#         super().__init__()
#         self.data = pd.DataFrame()
#         self.intarected_unique_name = None
#         self.un_intarected_unique_name = None
#         self.inerected_cpu_uses_percent = None
#         self.un_inerected_cpu_uses_percent = None
#         self.inerected_memory_uses_percent = None
#         self.un_inerected_memory_uses_percent = None
#         self.inerected_Wi_fi_uses_percent = None
#         self.un_inerected_Wi_fi_uses_percent = None
#         self.inerected_disc_uses_percent = None
#         self.un_inerected_disc_uses_percent = None
#         self.update_data()
#         # Initialize interacting_processes and non_interacting_processes with the necessary data
#         self.interacting_processes = self.interacting_processes
#         self.non_interacting_processes = self.non_interacting_processes
#         self.update_data()


#     def update_data(self):
#         """Update the data for the current state."""
#         self.intarected_unique_name = self.get_unique_process_names(self.interacting_processes)
#         self.un_intarected_unique_name = self.get_unique_process_names(self.non_interacting_processes)
#         self.inerected_cpu_uses_percent = self.get_cpu_uses_percent(self.interacting_processes)
#         self.un_inerected_cpu_uses_percent = self.get_cpu_uses_percent(self.non_interacting_processes)
#         self.inerected_memory_uses_percent = self.get_memory_uses_percent(self.interacting_processes)
#         self.un_inerected_memory_uses_percent = self.get_memory_uses_percent(self.non_interacting_processes)
#         self.inerected_Wi_fi_uses_percent = self.get_Wi_fi_uses_percent(self.interacting_processes)
#         self.un_inerected_Wi_fi_uses_percent = self.get_Wi_fi_uses_percent(self.non_interacting_processes)
#         self.inerected_disc_uses_percent = self.get_disc_uses_percent(self.interacting_processes)
#         self.un_inerected_disc_uses_percent = self.get_disc_uses_percent(self.non_interacting_processes)
        


#     def base_intarected_df(self):
#         """Convert currently interacting data to a Pandas DataFrame."""
#         self.update_data()

#         dict_list = [
#             self.inerected_cpu_uses_percent,
#             self.inerected_memory_uses_percent,
#             self.inerected_Wi_fi_uses_percent,
#             self.inerected_disc_uses_percent
#         ]
#         data_dict = {}
#         for i, dictionary in enumerate(dict_list):
#             for name, value in dictionary.items():
#                 if name in data_dict:
#                     data_dict[name].append(value)
#                 else:
#                     data_dict[name] = [value]

#         # Convert data_dict to a Pandas DataFrame
#         df = pd.DataFrame.from_dict(data_dict)

#         # Transpose the DataFrame to have names as rows and values as columns
#         df = df.transpose()

#         # Reset the index to make the names a column in the DataFrame
#         df = df.reset_index()

#         # Rename the columns
#         df.columns = ['Name'] + ['cpu_uses'] + ['memory_uses'] + ['Wi_fi_uses'] + ['disc_uses']

#         # Add non-interacting process type column with value 'interacting_processes' for all rows
#         df['Type'] = 'interacting_processes'

#         # Sort the DataFrame by the Name column
#         df = df.sort_values('Name').reset_index(drop=True)

#         return df
    

#     def base_un_intarected_df(self):
#         """Converts currently_un_intarected data to a Pandas DataFrame."""
#         self.update_data()

#         dict_list = [
#             self.un_inerected_cpu_uses_percent,
#             self.un_inerected_memory_uses_percent,
#             self.un_inerected_Wi_fi_uses_percent,
#             self.un_inerected_disc_uses_percent
#         ]
#         data_dict = {}
#         for i, dictionary in enumerate(dict_list):
#             for name, value in dictionary.items():
#                 if name in data_dict:
#                     data_dict[name].append(value)
#                 else:
#                     data_dict[name] = [value]

#         data_dict = {}

#         for i, dictionary in enumerate(dict_list):
#             for name, value in dictionary.items():
#                 if name in data_dict:
#                     data_dict[name].append(value)
#                 else:
#                     data_dict[name] = [value]

#         # Convert data_dict to a Pandas DataFrame
#         df = pd.DataFrame.from_dict(data_dict)

#         # Transpose the DataFrame to have names as rows and values as columns
#         df = df.transpose()

#         # Reset the index to make the names a column in the DataFrame
#         df = df.reset_index()

#         # Rename the columns
#         df.columns = ['Name'] + ['cpu_uses'] + ['memory_uses'] + ['Wi_fi_uses'] + ['disc_uses']

#         # Add non-interacting process type column with value 'interacting_processes' for all rows
#         df['Type'] = 'un_interacting_processes'

#         # Sort the DataFrame by the Name column
#         df = df.sort_values('Name').reset_index(drop=True)

#         return df


    
#     def base_df(self):
#         intarected_df = self.base_intarected_df()  # Generate the interacting processes dataframe
#         un_intarected_df = self.base_un_intarected_df()  # Generate the non-interacting processes dataframe

#         # Concatenate the interacting and non-interacting dataframes
#         df = pd.concat([intarected_df, un_intarected_df], ignore_index=True)

#         df = df.reset_index(drop=True)  # Reset the index
#         df = df.sample(frac=1).reset_index(drop=True)  # Shuffle the rows

#         return df
