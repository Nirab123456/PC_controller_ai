from AI_Env_Data_2 import Env_data_process
import pandas as pd
class pandas_data_collection():
    """Convert cpu, memory, wifi, disk used data to a pandas DataFrame."""
    def __init__(self):
        self.Env_data_process = Env_data_process()
        self.intarected_unique_name= self.Env_data_process.get_unique_process_names(self.Env_data_process.interacting_processes)
        self.un_intarected_unique_name = self.Env_data_process.get_unique_process_names(self.Env_data_process.non_interacting_processes)

    def base_intarected_df(self):
        """Convert currently interacting data to a Pandas DataFrame."""
        max_columns = 30
        dict_list = [
            self.Env_data_process.get_cpu_uses_percent(self.Env_data_process.get_current_interaction_results()),
            self.Env_data_process.get_memory_uses_percent(self.Env_data_process.get_current_interaction_results()),
            self.Env_data_process.get_disc_uses_percent(self.Env_data_process.get_current_interaction_results()),
            self.Env_data_process.get_Wi_fi_uses_percent(self.Env_data_process.get_current_interaction_results()),
        ]
        data_dict = {}
        max_length = max_columns  # Find the maximum length among the arrays
        for i in range(max_length):
            for dictionary in dict_list:
                if i < len(dictionary):
                    name, value = list(dictionary.items())[i]
                    if name in data_dict:
                        data_dict[name].append(value)
                    else:
                        data_dict[name] = [value]
                else:
                    # Populate with None if a value is missing
                    for name, values in data_dict.items():
                        if len(values) < i + 1:
                            values.append(None)

        df = pd.DataFrame.from_dict(data_dict)
        df = df.transpose()
        df = df.reset_index()
        df.columns = ['Name', 'cpu_uses', 'memory_uses', 'Wi_fi_uses', 'disc_uses'] + ['Column_' + str(i) for i in range(5, len(df.columns))]
        df['Type'] = 'interacting_processes'
        df = df.sort_values('Name').reset_index(drop=True)
        return df

    def base_un_intarected_df(self):
        """Convert currently non-interacting data to a Pandas DataFrame."""
        max_columns = 30

        dict_list = [
            self.Env_data_process.get_cpu_uses_percent(self.Env_data_process.get_current_non_interaction_results()),
            self.Env_data_process.get_memory_uses_percent(self.Env_data_process.get_current_non_interaction_results()),
            self.Env_data_process.get_disc_uses_percent(self.Env_data_process.get_current_non_interaction_results()),
            self.Env_data_process.get_Wi_fi_uses_percent(self.Env_data_process.get_current_non_interaction_results()),
        ]
        data_dict = {}
        max_length = max_columns  # Find the maximum length among the arrays
        for i in range(max_length):
            for dictionary in dict_list:
                if i < len(dictionary):
                    name, value = list(dictionary.items())[i]
                    if name in data_dict:
                        data_dict[name].append(value)
                    else:
                        data_dict[name] = [value]
                else:
                    # Populate with None if a value is missing
                    for name, values in data_dict.items():
                        if len(values) < i + 1:
                            values.append(None)

        df = pd.DataFrame.from_dict(data_dict)
        df = df.transpose()
        df = df.reset_index()
        df.columns = ['Name', 'cpu_uses', 'memory_uses', 'Wi_fi_uses', 'disc_uses'] + ['Column_' + str(i) for i in range(5, len(df.columns))]
        df['Type'] = 'non_interacting_processes'
        df = df.sort_values('Name').reset_index(drop=True)
        return df

    def base_df(self):
        """Generate the base dataframe by concratng a single base_intarected_df and a base_un_intarected_df."""
        intarected_df = self.base_intarected_df()  # Generate the interacting processes dataframe
        un_intarected_df = self.base_un_intarected_df()  # Generate the non-interacting processes dataframe

        # Ensure all arrays have the same length
        max_length = max(len(intarected_df), len(un_intarected_df))
        intarected_df = self.pad_df(intarected_df, max_length)
        un_intarected_df = self.pad_df(un_intarected_df, max_length)

        # Concatenate the interacting and non-interacting dataframes
        df = pd.concat([intarected_df, un_intarected_df], ignore_index=True)

        df = df.reset_index(drop=True)  # Reset the index
        df = df.sample(frac=1).reset_index(drop=True)  # Shuffle the rows

        return df

    def pad_df(self, df, length):
        """Pad a dataframe with None values to ensure it has a certain length."""
        if len(df) < length:
            num_rows = length - len(df)
            padding = pd.DataFrame([[None] * df.shape[1]] * num_rows, columns=df.columns)
            df = pd.concat([df, padding], ignore_index=True)
        return df
