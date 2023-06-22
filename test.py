import pandas as pd
from Data_collection_pandas import pandas_data_collection

class pandas_dataframe:
    
    def __init__(self):
        pass

    def dataframe(self):
        inner_dfs = []
        outer_dfs = []
        pdc = pandas_data_collection()

        for outer_loop in range(1):
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
        return result_df







