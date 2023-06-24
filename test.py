import pandas as pd
import PySimpleGUI as sg
from Data_collection_pandas import pandas_data_collection
from sklearn.preprocessing import MinMaxScaler







class pandas_dataframe:
    
    def __init__(self):
        pass

    def dataframe(self):
        inner_dfs = []
        outer_dfs = []
        pdc = pandas_data_collection()

        for outer_loop in range(5):
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
        result_df.dropna(inplace=True)
        result_df['Type'] = result_df['Type'].replace({'non_interacting_processes': '0', 'interacting_processes': '1'})
        result_df.drop(['Name'], axis=1, inplace=True)
        result_df = result_df.astype('float32')

        columns_to_normalize = ['cpu_uses', 'memory_uses', 'Wi_fi_uses', 'disc_uses']

        scaler = MinMaxScaler(feature_range=(0, 1))
        result_df[columns_to_normalize] = scaler.fit_transform(result_df[columns_to_normalize])
        return result_df
    










