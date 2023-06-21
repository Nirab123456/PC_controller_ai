from Data_collection_pandas import pandas_data_collection
import pandas as pd
import time 

# Instantiate the pandas_data_collection class
pdc = pandas_data_collection()

# Instantiate the pandas_data_collection class
pdc = pandas_data_collection()

inner_dfs = []  # Create an empty list to store the dataframes for each inner loop
outer_dfs = []  # Create an empty list to store the merged dataframes for each outer loop

for outer_loop in range(10000):
    for inner_loop in range(1):
        df = pdc.base_df()
        selected_columns = ['Name', 'cpu_uses', 'memory_uses','Wi_fi_uses','disc_uses','Type']

        # Create a new DataFrame with the selected columns
        new_df = df[selected_columns].copy()

        # Shuffle the rows
        new_df = new_df.sample(frac=1).reset_index(drop=True)

        # Reset the index
        new_df = new_df.reset_index()
        new_df = new_df.dropna()
        df = new_df
        inner_dfs.append(df)

    # Concatenate the dataframes from the inner loop
    merged_df = pd.concat(inner_dfs, ignore_index=True)
    outer_dfs.append(merged_df)

    inner_dfs = []  # Clear the list of inner dataframes

# Merge the dataframes from the outer loop
result_df = pd.concat(outer_dfs, ignore_index=True)
result_df = result_df.reset_index(drop=True)
result_df = result_df.drop('index', axis=1)
result_df.to_csv('your_df.csv', index=False)
